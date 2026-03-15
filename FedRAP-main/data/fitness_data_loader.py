"""
健身数据加载和预处理工具
支持加载用户特征、运动特征，并进行数据过滤和标准化
"""
import os
import pandas as pd
import numpy as np
import torch


def load_fitness_data(path, dataset='fitness', file_name='fitness_ratings.dat'):
    """
    加载健身数据集
    
    Args:
        path: 数据集根目录
        dataset: 数据集名称
        file_name: 交互数据文件名
        
    Returns:
        ratings: DataFrame with columns [userId, itemId, rating, timestamp]
        num_users: 用户数量
        num_items: 运动项目数量
        user_features: 用户特征DataFrame
        exercise_features: 运动特征DataFrame
    """
    dataset_path = os.path.join(path, dataset)
    
    # 加载交互数据
    ratings_file = os.path.join(dataset_path, file_name)
    ratings = pd.read_csv(ratings_file, sep=',', header=None, 
                         names=['userId', 'itemId', 'rating', 'timestamp'],
                         engine='python')
    
    # 过滤交互少于5次的用户
    min_interactions = 5
    user_counts = ratings.groupby('userId').size()
    active_users = user_counts[user_counts >= min_interactions].index
    ratings = ratings[ratings['userId'].isin(active_users)].reset_index(drop=True)
    
    # 重新映射用户和项目ID (确保连续)
    user_id_mapping = {old_id: new_id for new_id, old_id in enumerate(ratings['userId'].unique())}
    item_id_mapping = {old_id: new_id for new_id, old_id in enumerate(ratings['itemId'].unique())}
    
    ratings['userId'] = ratings['userId'].map(user_id_mapping)
    ratings['itemId'] = ratings['itemId'].map(item_id_mapping)
    
    num_users = ratings['userId'].nunique()
    num_items = ratings['itemId'].nunique()
    
    # 加载用户特征
    user_features = None
    user_file = os.path.join(dataset_path, 'users_normalized.csv')
    if os.path.exists(user_file):
        user_features = pd.read_csv(user_file)
        # 根据映射重新索引用户特征
        user_features = user_features[user_features['userId'].isin(user_id_mapping.keys())].copy()
        user_features['userId'] = user_features['userId'].map(user_id_mapping)
        user_features = user_features.sort_values('userId').reset_index(drop=True)
    
    # 加载运动特征
    exercise_features = None
    exercise_file = os.path.join(dataset_path, 'exercises_normalized.csv')
    if os.path.exists(exercise_file):
        exercise_features = pd.read_csv(exercise_file)
        # 根据映射重新索引运动特征
        exercise_features = exercise_features[exercise_features['exerciseId'].isin(item_id_mapping.keys())].copy()
        exercise_features['exerciseId'] = exercise_features['exerciseId'].map(item_id_mapping)
        exercise_features = exercise_features.sort_values('exerciseId').reset_index(drop=True)
    
    print(f"数据加载完成:")
    print(f"  用户数: {num_users}")
    print(f"  运动项目数: {num_items}")
    print(f"  交互记录数: {len(ratings)}")
    print(f"  平均每用户交互数: {len(ratings) / num_users:.2f}")
    
    return ratings, num_users, num_items, user_features, exercise_features


class FitnessFeatureEncoder:
    """健身特征编码器"""
    
    def __init__(self, user_features, exercise_features, latent_dim=32):
        """
        Args:
            user_features: 用户特征DataFrame
            exercise_features: 运动特征DataFrame
            latent_dim: 编码后的嵌入维度
        """
        self.user_features = user_features
        self.exercise_features = exercise_features
        self.latent_dim = latent_dim
        
        # 用户特征维度 (13维)
        self.user_feature_cols = [
            'age', 'weight', 'height', 'bmi', 'heart_rate',
            'fitness_level', 'goal_weight_loss', 'goal_muscle_gain',
            'goal_endurance', 'goal_flexibility', 'experience_years',
            'weekly_frequency', 'avg_session_duration'
        ]
        
        # 运动特征维度 (13维)
        self.exercise_feature_cols = [
            'intensity', 'duration', 'equipment_required', 'difficulty',
            'cardio_focus', 'strength_focus', 'flexibility_focus',
            'calories_burned', 'muscle_group', 'space_required',
            'skill_level', 'injury_risk', 'popularity'
        ]
        
        # 构建特征编码器网络
        self.user_encoder = self._build_encoder(len(self.user_feature_cols))
        self.exercise_encoder = self._build_encoder(len(self.exercise_feature_cols))
    
    def _build_encoder(self, input_dim):
        """构建特征编码器 (全连接网络 + ReLU)"""
        return torch.nn.Sequential(
            torch.nn.Linear(input_dim, 64),
            torch.nn.ReLU(),
            torch.nn.Linear(64, self.latent_dim),
            torch.nn.ReLU()
        )
    
    def get_user_feature_vector(self, user_id):
        """获取用户特征向量"""
        if self.user_features is None:
            return None
        
        user_row = self.user_features[self.user_features['userId'] == user_id]
        if len(user_row) == 0:
            return None
        
        features = user_row[self.user_feature_cols].values[0]
        return torch.FloatTensor(features)
    
    def get_exercise_feature_vector(self, exercise_id):
        """获取运动特征向量"""
        if self.exercise_features is None:
            return None
        
        exercise_row = self.exercise_features[self.exercise_features['exerciseId'] == exercise_id]
        if len(exercise_row) == 0:
            return None
        
        features = exercise_row[self.exercise_feature_cols].values[0]
        return torch.FloatTensor(features)
    
    def encode_user(self, user_id):
        """编码用户特征"""
        feature_vec = self.get_user_feature_vector(user_id)
        if feature_vec is None:
            return torch.zeros(self.latent_dim)
        
        with torch.no_grad():
            encoded = self.user_encoder(feature_vec.unsqueeze(0))
        return encoded.squeeze(0)
    
    def encode_exercise(self, exercise_id):
        """编码运动特征"""
        feature_vec = self.get_exercise_feature_vector(exercise_id)
        if feature_vec is None:
            return torch.zeros(self.latent_dim)
        
        with torch.no_grad():
            encoded = self.exercise_encoder(feature_vec.unsqueeze(0))
        return encoded.squeeze(0)


def create_fitness_plan(user_profile, recommended_exercises, exercise_features):
    """
    根据推荐结果生成个性化健身计划
    
    Args:
        user_profile: 用户档案 (dict)
        recommended_exercises: 推荐的运动ID列表
        exercise_features: 运动特征DataFrame
        
    Returns:
        fitness_plan: 健身计划字典
    """
    plan = {
        'user_id': int(user_profile.get('userId', 0)),
        'goal': determine_primary_goal(user_profile),
        'exercises': [],
        'total_duration': 0,
        'estimated_calories': 0
    }
    
    for exercise_id in recommended_exercises:
        exercise = exercise_features[exercise_features['exerciseId'] == int(exercise_id)].iloc[0]
        
        exercise_info = {
            'id': int(exercise_id),
            'name': str(exercise.get('name', f'运动{exercise_id}')),
            'intensity': float(exercise.get('intensity', 0.5)),
            'duration': int(exercise.get('duration', 30)),
            'difficulty': float(exercise.get('difficulty', 0.5)),
            'equipment': '需要器械' if exercise.get('equipment_required', 0) > 0.5 else '无需器械'
        }
        
        plan['exercises'].append(exercise_info)
        plan['total_duration'] += int(exercise_info['duration'])
        plan['estimated_calories'] += int(exercise.get('calories_burned', 0.5) * 500)
    
    return plan


def determine_primary_goal(user_profile):
    """确定用户的主要健身目标"""
    goals = {
        'goal_weight_loss': '减脂',
        'goal_muscle_gain': '增肌',
        'goal_endurance': '耐力',
        'goal_flexibility': '柔韧性'
    }
    
    max_goal = max(goals.keys(), 
                   key=lambda k: user_profile.get(k, 0))
    
    return goals[max_goal]


if __name__ == '__main__':
    # 测试数据加载
    ratings, num_users, num_items, user_feat, exercise_feat = load_fitness_data(
        '../datasets', 'fitness', 'fitness_ratings.dat'
    )
    
    print("\n=== 用户特征示例 ===")
    if user_feat is not None:
        print(user_feat.head())
    
    print("\n=== 运动特征示例 ===")
    if exercise_feat is not None:
        print(exercise_feat.head())
