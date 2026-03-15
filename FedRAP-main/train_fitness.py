"""
健身推荐系统训练脚本
基于FedRAP联邦学习框架
"""
import argparse
import datetime
import logging
import os
import time

import numpy as np
import torch

from utils.data import SampleGenerator
from utils.utils import setSeed, initLogging, loadData


def loadEngine(configuration):
    """加载训练引擎"""
    if configuration['alias'] == 'FedRAP':
        # 使用增强版健身推荐模型
        from model.model_fitness import FedRAPFitnessEngine as FedRAPEngine
        load_engine = FedRAPEngine(configuration)
    else:
        # 使用原始模型
        from model.model import FedRAPEngine
        load_engine = FedRAPEngine(configuration)

    return load_engine


if __name__ == '__main__':
    # 训练参数
    parser = argparse.ArgumentParser(description='FedRAP健身推荐系统')
    
    # 基础配置
    parser.add_argument('--alias', type=str, default='FedRAP', help='模型名称')
    parser.add_argument('--dataset', type=str, default='fitness', help='数据集名称')
    parser.add_argument('--data_file', type=str, default='fitness_ratings.dat', help='数据文件')
    parser.add_argument('--model_dir', type=str, 
                       default='results/checkpoints/{}/{}/[{}]Epoch{}.model',
                       help='模型保存路径')
    
    # 联邦学习参数
    parser.add_argument('--clients_sample_ratio', type=float, default=1.0, 
                       help='客户端采样率')
    parser.add_argument('--num_round', type=int, default=50, 
                       help='联邦学习轮数')
    parser.add_argument('--local_epoch', type=int, default=5, 
                       help='本地训练轮数')
    
    # 模型参数
    parser.add_argument('--latent_dim', type=int, default=32, 
                       help='嵌入维度')
    parser.add_argument('--batch_size', type=int, default=1024, 
                       help='批次大小')
    parser.add_argument('--num_negative', type=int, default=4, 
                       help='负样本数量')
    
    # 优化器参数
    parser.add_argument('--lr_network', type=float, default=1e-3, 
                       help='网络学习率')
    parser.add_argument('--lr_args', type=float, default=1e2, 
                       help='嵌入学习率')
    parser.add_argument('--l2_regularization', type=float, default=1e-6, 
                       help='L2正则化')
    parser.add_argument('--decay_rate', type=float, default=0.97, 
                       help='学习率衰减')
    
    # FedRAP特定参数
    parser.add_argument('--lambda', type=float, default=0.1, 
                       help='独立性约束权重', dest='lambda_')
    parser.add_argument('--mu', type=float, default=1e-3, 
                       help='稀疏性约束权重')
    parser.add_argument('--regular', type=str, default='l1', 
                       choices=['l1', 'l2', 'nuc', 'inf', 'none'],
                       help='正则化类型')
    
    # 评估参数
    parser.add_argument('--top_k', type=int, default=10, 
                       help='Top-K推荐')
    parser.add_argument('--tol', type=float, default=1e-4, 
                       help='收敛容差')
    
    # 系统参数
    parser.add_argument('--device_id', type=int, default=0, 
                       help='GPU设备ID')
    parser.add_argument('--use_cuda', type=bool, default=True, 
                       help='是否使用CUDA')
    parser.add_argument('--seed', type=int, default=0, 
                       help='随机种子')
    parser.add_argument('--comment', type=str, default='fitness_fedrap', 
                       help='实验备注')
    parser.add_argument('--vary_param', type=str, default='fixed',
                       help='参数变化模式')
    parser.add_argument('--type', type=str, default='seed',
                       help='实验类型')
    parser.add_argument('--on_server', type=bool, default=False,
                       help='是否在服务器运行')

    args = parser.parse_args()
    config = vars(args)
    config['lambda'] = config.pop('lambda_')  # 恢复lambda参数名

    # 设置CUDA设备
    if config['use_cuda'] and torch.cuda.is_available():
        torch.cuda.set_device(config['device_id'])
        os.environ["CUDA_VISIBLE_DEVICES"] = str(config['device_id'])
        print(f"✓ 使用GPU: {torch.cuda.get_device_name(config['device_id'])}")
    else:
        config['use_cuda'] = False
        print("✓ 使用CPU训练")

    # 设置随机种子
    setSeed(config['seed'])

    # 创建日志目录
    os.makedirs('logs', exist_ok=True)
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file_name = os.path.join('logs',
                                 f'[{config["alias"]}]-[{config["dataset"]}]-[{current_time}].txt')
    initLogging(log_file_name)

    logging.info("=" * 80)
    logging.info("🏋️ FedRAP健身推荐系统 - 联邦学习训练")
    logging.info("=" * 80)

    # 加载数据
    logging.info("📂 加载健身数据集...")
    ratings, config['num_users'], config['num_items'] = loadData(
        'datasets', config['dataset'], config['data_file']
    )

    # 创建模型保存目录
    checkpoint_path = f'results/checkpoints/{config["alias"]}/{config["dataset"]}/'
    os.makedirs(checkpoint_path, exist_ok=True)

    # 加载训练引擎
    logging.info("🔧 初始化FedRAP引擎...")
    engine = loadEngine(config)

    logging.info("\n📋 训练配置:")
    for key, value in config.items():
        logging.info(f"  {key}: {value}")
    logging.info("=" * 80)

    # 数据加载器
    sample_generator = SampleGenerator(ratings=ratings)
    validate_data = sample_generator.validate_data
    test_data = sample_generator.test_data

    # 初始化记录
    test_hrs, test_ndcgs = [], []
    val_hrs, val_ndcgs = [], []
    train_losses, sparsity_values = [], []
    best_test_hr, final_test_round = 0, 0

    # 全局共享嵌入
    item_commonality = torch.nn.Embedding(
        num_embeddings=config['num_items'], 
        embedding_dim=config['latent_dim']
    )
    if config['use_cuda']:
        item_commonality = item_commonality.cuda()

    # 开始联邦训练
    logging.info("\n🚀 开始联邦学习训练...\n")
    
    for iteration in range(config['num_round']):
        
        logging.info(f'{"="*80}')
        logging.info(f'📍 联邦学习轮次 {iteration + 1}/{config["num_round"]}')
        logging.info(f'{"="*80}')

        # 生成训练数据
        train_data = sample_generator.store_all_train_data(config['num_negative'])

        # 本地训练
        start_time = time.perf_counter()
        train_loss, sparse_value = engine.federatedTrainOneRound(
            train_data, item_commonality, iteration
        )
        end_time = time.perf_counter()

        training_time = end_time - start_time
        
        # 计算平均损失
        avg_loss = sum(train_loss.values()) / len(train_loss.keys())
        train_losses.append(avg_loss)
        sparsity_values.append(sparse_value)

        logging.info(
            f'⏱️  训练时间: {training_time:.2f}秒 | '
            f'损失: {avg_loss:.4f} | '
            f'稀疏度: {sparse_value:.4f}'
        )

        # 测试集评估
        hr, ndcg = engine.federatedEvaluate(test_data)
        test_hrs.append(hr)
        test_ndcgs.append(ndcg)

        logging.info(
            f'📊 [测试集] HR@{config["top_k"]}: {hr:.4f} | '
            f'NDCG@{config["top_k"]}: {ndcg:.4f}'
        )

        # 更新最佳模型
        if hr >= best_test_hr:
            best_test_hr = hr
            final_test_round = iteration
            
            # 保存最佳模型
            save_path = config['model_dir'].format(
                config['alias'], config['dataset'], 'best', iteration + 1
            )
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            torch.save(engine.model.state_dict(), save_path)
            logging.info(f'💾 保存最佳模型: {save_path}')

        # 验证集评估
        val_hr, val_ndcg = engine.federatedEvaluate(validate_data)
        val_hrs.append(val_hr)
        val_ndcgs.append(val_ndcg)

        logging.info(
            f'📊 [验证集] HR@{config["top_k"]}: {val_hr:.4f} | '
            f'NDCG@{config["top_k"]}: {val_ndcg:.4f}\n'
        )

    # 训练结束
    logging.info("\n" + "=" * 80)
    logging.info("✅ 训练完成！")
    logging.info("=" * 80)
    logging.info(f'\n🏆 最佳性能:')
    logging.info(f'  轮次: {final_test_round + 1}')
    logging.info(f'  HR@{config["top_k"]}: {best_test_hr:.4f}')
    logging.info(f'  NDCG@{config["top_k"]}: {test_ndcgs[final_test_round]:.4f}')
    logging.info("=" * 80)

    # 保存最终结果
    results_dir = f'results/{config["alias"]}/{config["dataset"]}'
    os.makedirs(results_dir, exist_ok=True)
    
    results = {
        'test_hrs': test_hrs,
        'test_ndcgs': test_ndcgs,
        'val_hrs': val_hrs,
        'val_ndcgs': val_ndcgs,
        'train_losses': train_losses,
        'sparsity': sparsity_values,
        'best_hr': best_test_hr,
        'best_round': final_test_round,
        'config': config
    }
    
    import pickle
    result_file = os.path.join(results_dir, f'results_{current_time}.pkl')
    with open(result_file, 'wb') as f:
        pickle.dump(results, f)
    
    logging.info(f'💾 结果已保存至: {result_file}\n')
