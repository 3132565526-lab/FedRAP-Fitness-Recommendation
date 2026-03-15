"""
FedRAP 模型推理服务
通过命令行接口为Java后端提供模型推荐
"""

import sys
import os
import json
import torch
import numpy as np

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir  # 修改：直接使用当前目录作为项目根
sys.path.insert(0, project_root)

from model.model_fitness import FedRAPFitness
from data.fitness_data_loader import load_fitness_data


def load_model_for_inference(model_path=None):
    """加载训练好的模型用于推理"""
    if model_path is None:
        model_path = os.path.join(project_root, 'results/checkpoints/FedRAP/fitness/[best]Epoch10.model')
    
    datasets_path = os.path.join(project_root, 'datasets')
    
    # 配置
    config = {
        'num_items': 200,
        'latent_dim': 32,
        'use_cuda': False  # Java调用时禁用CUDA简化部署
    }
    
    # 加载数据特征
    _, _, _, user_features_df, exercise_features_df = load_fitness_data(
        datasets_path, 'fitness', 'fitness_ratings.dat'
    )
    
    # 初始化模型
    model = FedRAPFitness(config)
    
    # 加载权重
    if os.path.exists(model_path):
        state_dict = torch.load(model_path, map_location='cpu')
        model.load_state_dict(state_dict)
        model.eval()
    else:
        raise FileNotFoundError(f"模型文件不存在: {model_path}")
    
    return model, config, exercise_features_df


def build_user_feature_vector(user_profile):
    """构建用户特征向量 (13维)"""
    feature_vector = [
        float(user_profile.get('age', 30)),
        float(user_profile.get('weight', 70)),
        float(user_profile.get('height', 170)),
        float(user_profile.get('bmi', 24.0)),
        float(user_profile.get('heartRate', 75)),
        float(user_profile.get('fitnessLevel', 0.5)),
        float(user_profile.get('goalWeightLoss', 0.3)),
        float(user_profile.get('goalMuscleGain', 0.3)),
        float(user_profile.get('goalEndurance', 0.2)),
        float(user_profile.get('goalFlexibility', 0.2)),
        float(user_profile.get('experienceYears', 1)),
        float(user_profile.get('weeklyFrequency', 3)),
        float(user_profile.get('avgSessionDuration', 45))
    ]
    return torch.FloatTensor([feature_vector])


def apply_personalization_boost(ratings, user_profile, exercise_features):
    """基于用户目标对评分进行个性化调整"""
    goal_weight_loss = user_profile.get('goalWeightLoss', 0.3)
    goal_muscle_gain = user_profile.get('goalMuscleGain', 0.3)
    goal_endurance = user_profile.get('goalEndurance', 0.2)
    goal_flexibility = user_profile.get('goalFlexibility', 0.2)
    
    exercise_feature_cols = [
        'intensity', 'duration', 'equipment_required', 'difficulty',
        'cardio_focus', 'strength_focus', 'flexibility_focus',
        'calories_burned', 'muscle_group', 'space_required',
        'skill_level', 'injury_risk', 'popularity'
    ]
    
    # 提取特征
    cardio_focus = exercise_features['cardio_focus'].values
    strength_focus = exercise_features['strength_focus'].values
    flexibility_focus = exercise_features['flexibility_focus'].values
    
    # 计算个性化加权
    personalization_weight = 0.3
    goal_boost = (
        goal_weight_loss * cardio_focus +
        goal_muscle_gain * strength_focus +
        goal_endurance * cardio_focus +
        goal_flexibility * flexibility_focus
    )
    
    adjusted_ratings = ratings * (1 - personalization_weight) + goal_boost * personalization_weight
    return adjusted_ratings


def get_recommendations(user_profile, top_k=10):
    """获取个性化推荐"""
    model, config, exercise_features = load_model_for_inference()
    
    # 构建用户特征向量
    user_features = build_user_feature_vector(user_profile)
    
    # 构建运动特征矩阵
    exercise_feature_cols = [
        'intensity', 'duration', 'equipment_required', 'difficulty',
        'cardio_focus', 'strength_focus', 'flexibility_focus',
        'calories_burned', 'muscle_group', 'space_required',
        'skill_level', 'injury_risk', 'popularity'
    ]
    
    exercise_features_matrix = exercise_features[exercise_feature_cols].values
    exercise_features_tensor = torch.FloatTensor(exercise_features_matrix)
    
    # 使用模型预测
    with torch.no_grad():
        item_ids = torch.LongTensor(list(range(config['num_items'])))
        user_features_expanded = user_features.repeat(config['num_items'], 1)
        
        ratings, _, _ = model(item_ids, user_features_expanded, exercise_features_tensor)
        ratings = ratings.squeeze().cpu().numpy()
    
    # 个性化调整
    ratings = apply_personalization_boost(ratings, user_profile, exercise_features)
    
    # Top-K推荐
    top_indices = np.argsort(ratings)[::-1][:top_k]
    
    # 构建推荐结果
    recommendations = []
    for idx in top_indices:
        idx_int = int(idx)
        exercise = exercise_features[exercise_features['exerciseId'] == idx_int]
        if len(exercise) > 0:
            exercise_row = exercise.iloc[0]
            recommendations.append({
                'exerciseId': idx_int,
                'score': float(ratings[idx]),
                'name': exercise_row.get('name', f'Exercise {idx_int}'),
                'category': exercise_row.get('category', 'GENERAL'),
                'intensity': float(exercise_row.get('intensity', 0.5)),
                'duration': int(exercise_row.get('duration', 30)),
                'difficulty': float(exercise_row.get('difficulty', 0.5))
            })
    
    return recommendations


if __name__ == '__main__':
    """
    命令行接口：接收JSON格式的用户资料，返回推荐结果
    用法: python model_inference.py '{"age": 25, "weight": 70, ...}'
    """
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'Missing user profile JSON argument'}))
        sys.exit(1)
    
    try:
        user_profile_json = sys.argv[1]
        user_profile = json.loads(user_profile_json)
        
        top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        
        recommendations = get_recommendations(user_profile, top_k)
        
        result = {
            'success': True,
            'recommendations': recommendations
        }
        
        print(json.dumps(result, ensure_ascii=False))
        
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e)
        }
        print(json.dumps(error_result, ensure_ascii=False))
        sys.exit(1)
