"""
FedRAP模型的健身推荐版本
集成用户特征和运动特征编码
"""
import copy
import torch
import torch.nn as nn

from model.engine import Engine


class FedRAPFitness(nn.Module):
    """
    FedRAP健身推荐模型
    - 支持用户特征和运动特征编码
    - 个性化嵌入 + 全局共享嵌入
    - 加性融合机制
    """
    
    def __init__(self, config, user_feature_dim=13, exercise_feature_dim=13):
        super(FedRAPFitness, self).__init__()
        self.config = config
        self.num_items = config['num_items']
        self.latent_dim = config['latent_dim']
        self.user_feature_dim = user_feature_dim
        self.exercise_feature_dim = exercise_feature_dim
        
        # 运动项目嵌入 - 个性化 (本地)
        self.item_personality = nn.Embedding(
            num_embeddings=self.num_items, 
            embedding_dim=self.latent_dim
        )
        
        # 运动项目嵌入 - 全局共享
        self.item_commonality = nn.Embedding(
            num_embeddings=self.num_items, 
            embedding_dim=self.latent_dim
        )
        
        # 特征编码器
        self.user_feature_encoder = self._build_encoder(
            user_feature_dim, self.latent_dim
        )
        
        self.exercise_feature_encoder = self._build_encoder(
            exercise_feature_dim, self.latent_dim
        )
        
        # 评分预测层
        self.affine_output = nn.Linear(
            in_features=self.latent_dim, 
            out_features=1
        )
        
        self.logistic = nn.Sigmoid()
        
        # 初始化权重
        self._init_weights()
    
    def _build_encoder(self, input_dim, output_dim):
        """构建特征编码器 (全连接 + ReLU)"""
        return nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, output_dim),
            nn.ReLU()
        )
    
    def _init_weights(self):
        """初始化模型权重"""
        nn.init.normal_(self.item_personality.weight, std=0.01)
        nn.init.normal_(self.item_commonality.weight, std=0.01)
    
    def setItemCommonality(self, item_commonality):
        """设置全局共享的运动嵌入"""
        self.item_commonality = copy.deepcopy(item_commonality)
        # 冻结全局嵌入，防止在本地训练中被修改
        for param in self.item_commonality.parameters():
            param.requires_grad = True  # 仍需要梯度用于服务器聚合
    
    def encode_user_features(self, user_features):
        """编码用户特征"""
        if user_features is None:
            return None
        return self.user_feature_encoder(user_features)
    
    def encode_exercise_features(self, exercise_features):
        """编码运动特征"""
        if exercise_features is None:
            return None
        return self.exercise_feature_encoder(exercise_features)
    
    def forward(self, item_indices, user_features=None, exercise_features=None):
        """
        前向传播
        
        Args:
            item_indices: 运动项目索引
            user_features: 用户特征 (可选, [batch_size, 13])
            exercise_features: 运动特征 (可选, [batch_size, 13])
            
        Returns:
            rating: 预测评分
            item_personality: 个性化嵌入
            item_commonality: 全局共享嵌入
        """
        # 获取项目嵌入
        item_personality = self.item_personality(item_indices)
        item_commonality = self.item_commonality(item_indices)
        
        # 加性融合：个性化 + 全局
        combined_embedding = item_personality + item_commonality
        
        # 如果有用户特征，融合到个性化嵌入中
        if user_features is not None:
            user_encoded = self.encode_user_features(user_features)
            # 用户特征强烈影响个性化推荐（权重0.5）
            combined_embedding = combined_embedding + 0.5 * user_encoded
        
        # 如果有运动特征，可以进一步融合
        if exercise_features is not None:
            exercise_encoded = self.encode_exercise_features(exercise_features)
            # 特征增强（权重0.3）
            combined_embedding = combined_embedding + 0.3 * exercise_encoded
        
        # 评分预测
        logits = self.affine_output(combined_embedding)
        rating = self.logistic(logits)
        
        return rating, item_personality, item_commonality
    
    def predict(self, item_indices, user_features=None, exercise_features=None):
        """预测接口（推理模式）"""
        self.eval()
        with torch.no_grad():
            rating, _, _ = self.forward(item_indices, user_features, exercise_features)
        return rating


class FedRAPFitnessEngine(Engine):
    """FedRAP健身推荐引擎"""
    
    def __init__(self, config):
        self.model = FedRAPFitness(config)
        if config['use_cuda'] is True:
            self.model.cuda()
        super(FedRAPFitnessEngine, self).__init__(config)
        print("=" * 60)
        print("FedRAP健身推荐模型初始化完成")
        print("=" * 60)
        print(self.model)
        print("=" * 60)


# 兼容原有接口
class FedRAP(FedRAPFitness):
    """为兼容性保留原有类名"""
    pass


class FedRAPEngine(FedRAPFitnessEngine):
    """为兼容性保留原有类名"""
    pass


if __name__ == '__main__':
    # 测试模型
    config = {
        'num_items': 200,
        'latent_dim': 32,
        'use_cuda': False
    }
    
    model = FedRAPFitness(config)
    print("\n模型结构:")
    print(model)
    
    # 测试前向传播
    item_ids = torch.LongTensor([0, 1, 2, 3, 4])
    user_feat = torch.randn(5, 13)
    exercise_feat = torch.randn(5, 13)
    
    rating, personality, commonality = model(item_ids, user_feat, exercise_feat)
    
    print(f"\n预测评分形状: {rating.shape}")
    print(f"个性化嵌入形状: {personality.shape}")
    print(f"全局嵌入形状: {commonality.shape}")
    print(f"\n预测评分示例: {rating[:3].squeeze()}")
