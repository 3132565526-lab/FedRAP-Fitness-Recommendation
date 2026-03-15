"""
验证模型的作用 - 对比有模型 vs 无模型的推荐差异
"""
import torch
import numpy as np
import pandas as pd
import sys
import os

# 添加项目路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from model.model_fitness import FedRAPFitness
from data.fitness_data_loader import load_fitness_data

def test_model_impact():
    """测试模型对推荐结果的影响"""
    
    print("="*80)
    print("验证FedRAP模型的作用")
    print("="*80)
    
    # 1. 加载数据
    print("\n[1] 加载数据...")
    datasets_path = os.path.join(project_root, 'datasets')
    ratings, num_users, num_items, user_features, exercise_features = load_fitness_data(
        datasets_path, 'fitness', 'fitness_ratings.dat'
    )
    print(f"✓ 数据加载完成: {num_users}用户, {num_items}运动项目")
    
    # 2. 配置
    config = {
        'num_items': num_items,
        'latent_dim': 32,
        'use_cuda': False
    }
    
    # 3. 创建两个模型：训练好的 vs 随机初始化的
    print("\n[2] 加载模型...")
    
    # 训练好的模型
    trained_model = FedRAPFitness(config)
    model_path = os.path.join(project_root, 'results/checkpoints/FedRAP/fitness/[best]Epoch10.model')
    
    if os.path.exists(model_path):
        trained_model.load_state_dict(torch.load(model_path, map_location='cpu'))
        trained_model.eval()
        print(f"✓ 训练好的模型加载成功")
    else:
        print(f"✗ 模型文件不存在: {model_path}")
        return
    
    # 随机初始化的模型（未训练）
    random_model = FedRAPFitness(config)
    random_model.eval()
    print(f"✓ 随机模型创建成功")
    
    # 4. 准备输入
    print("\n[3] 准备测试数据...")
    item_ids = torch.LongTensor(list(range(num_items)))
    
    # 构建运动特征矩阵
    exercise_feature_cols = [
        'intensity', 'duration', 'equipment_required', 'difficulty',
        'cardio_focus', 'strength_focus', 'flexibility_focus',
        'calories_burned', 'muscle_group', 'space_required',
        'skill_level', 'injury_risk', 'popularity'
    ]
    exercise_features_matrix = exercise_features[exercise_feature_cols].values
    exercise_features_tensor = torch.FloatTensor(exercise_features_matrix)
    
    # 模拟一个用户特征
    user_feature_vector = torch.FloatTensor([[
        30,    # age
        70,    # weight
        170,   # height
        24.2,  # bmi
        75,    # heart_rate
        0.5,   # fitness_level
        0.8,   # goal_weight_loss (减脂为主)
        0.2,   # goal_muscle_gain
        0.3,   # goal_endurance
        0.2,   # goal_flexibility
        2,     # experience_years
        3,     # weekly_frequency
        45     # avg_session_duration
    ]])
    user_features_expanded = user_feature_vector.repeat(num_items, 1)
    
    print(f"✓ 输入数据准备完成")
    print(f"  - 运动项目数: {num_items}")
    print(f"  - 用户特征: 30岁, BMI=24.2, 减脂目标=0.8")
    
    # 5. 对比预测结果
    print("\n[4] 模型预测对比...")
    
    with torch.no_grad():
        # 训练好的模型预测
        trained_ratings, _, _ = trained_model(item_ids, user_features_expanded, exercise_features_tensor)
        trained_ratings = trained_ratings.squeeze().numpy()
        
        # 随机模型预测
        random_ratings, _, _ = random_model(item_ids, user_features_expanded, exercise_features_tensor)
        random_ratings = random_ratings.squeeze().numpy()
    
    # 6. 分析差异
    print("\n[5] 评分统计对比:")
    print(f"\n训练好的模型:")
    print(f"  平均评分: {trained_ratings.mean():.4f}")
    print(f"  标准差:   {trained_ratings.std():.4f}")
    print(f"  最小值:   {trained_ratings.min():.4f}")
    print(f"  最大值:   {trained_ratings.max():.4f}")
    
    print(f"\n随机初始化模型:")
    print(f"  平均评分: {random_ratings.mean():.4f}")
    print(f"  标准差:   {random_ratings.std():.4f}")
    print(f"  最小值:   {random_ratings.min():.4f}")
    print(f"  最大值:   {random_ratings.max():.4f}")
    
    # 7. Top-10推荐对比
    print("\n[6] Top-10推荐对比:")
    
    trained_top10 = np.argsort(trained_ratings)[::-1][:10]
    random_top10 = np.argsort(random_ratings)[::-1][:10]
    
    print(f"\n训练好的模型 Top-10:")
    for i, idx in enumerate(trained_top10, 1):
        exercise = exercise_features[exercise_features['exerciseId'] == int(idx)].iloc[0]
        print(f"  {i}. {exercise.get('name', f'运动{idx}'):<20} "
              f"评分:{trained_ratings[idx]:.4f} "
              f"强度:{exercise.get('intensity', 0):.2f} "
              f"卡路里:{int(exercise.get('calories_burned', 0)*500)}")
    
    print(f"\n随机初始化模型 Top-10:")
    for i, idx in enumerate(random_top10, 1):
        exercise = exercise_features[exercise_features['exerciseId'] == int(idx)].iloc[0]
        print(f"  {i}. {exercise.get('name', f'运动{idx}'):<20} "
              f"评分:{random_ratings[idx]:.4f} "
              f"强度:{exercise.get('intensity', 0):.2f} "
              f"卡路里:{int(exercise.get('calories_burned', 0)*500)}")
    
    # 8. 重叠度分析
    overlap = len(set(trained_top10) & set(random_top10))
    print(f"\n[7] 差异分析:")
    print(f"  Top-10重叠数: {overlap}/10")
    print(f"  差异化程度: {(10-overlap)/10*100:.1f}%")
    
    if overlap < 5:
        print(f"\n✅ 结论: 训练好的模型产生了明显不同的推荐结果")
        print(f"         模型学到了有效的用户-运动交互模式")
    else:
        print(f"\n⚠ 警告: 训练模型与随机模型的推荐较为相似")
        print(f"         可能需要进一步训练或调整")
    
    # 9. 评分分布可视化（文本版）
    print(f"\n[8] 评分分布对比:")
    print(f"\n训练模型评分分布:")
    bins = np.linspace(0, 1, 11)
    hist, _ = np.histogram(trained_ratings, bins=bins)
    for i in range(len(hist)):
        bar = '█' * int(hist[i] / hist.max() * 40)
        print(f"  [{bins[i]:.1f}-{bins[i+1]:.1f}]: {bar} ({hist[i]})")
    
    print(f"\n随机模型评分分布:")
    hist, _ = np.histogram(random_ratings, bins=bins)
    for i in range(len(hist)):
        bar = '█' * int(hist[i] / hist.max() * 40)
        print(f"  [{bins[i]:.1f}-{bins[i+1]:.1f}]: {bar} ({hist[i]})")

if __name__ == '__main__':
    test_model_impact()
