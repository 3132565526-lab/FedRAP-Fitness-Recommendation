"""
健身数据生成器
用于生成模拟的健身训练数据，包括用户特征、运动项目特征和用户-运动交互数据
"""
import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(0)
np.random.seed(0)


class FitnessDataGenerator:
    """生成健身推荐系统的模拟数据"""
    
    def __init__(self, num_users=500, num_exercises=200):
        self.num_users = num_users
        self.num_exercises = num_exercises
        
        # 用户特征维度 (13维)
        self.user_feature_names = [
            'age', 'weight', 'height', 'bmi', 'heart_rate',
            'fitness_level', 'goal_weight_loss', 'goal_muscle_gain',
            'goal_endurance', 'goal_flexibility', 'experience_years',
            'weekly_frequency', 'avg_session_duration'
        ]
        
        # 运动特征维度 (13维)
        self.exercise_feature_names = [
            'intensity', 'duration', 'equipment_required', 'difficulty',
            'cardio_focus', 'strength_focus', 'flexibility_focus',
            'calories_burned', 'muscle_group', 'space_required',
            'skill_level', 'injury_risk', 'popularity'
        ]
        
        # 健身目标类型
        self.fitness_goals = ['减脂', '增肌', '耐力', '柔韧性']
        
        # 运动类型
        self.exercise_types = [
            '跑步', '深蹲', '卧推', '引体向上', '瑜伽', '平板支撑',
            '波比跳', '俯卧撑', '硬拉', '划船', '单车', '游泳',
            '拉伸', '普拉提', '箭步蹲', '哑铃弯举', '仰卧起坐',
            '登山跑', '开合跳', '战绳'
        ]
        
    def generate_user_features(self):
        """生成用户特征数据"""
        users_data = []
        
        for user_id in range(self.num_users):
            # 基础信息
            age = np.random.randint(18, 65)
            height = np.random.normal(170, 10)  # cm
            weight = np.random.normal(70, 15)   # kg
            bmi = weight / ((height / 100) ** 2)
            heart_rate = np.random.randint(60, 100)
            
            # 健身水平 (0-1标准化)
            fitness_level = np.random.random()
            
            # 健身目标 (0-1, 可以多目标)
            goal_weight_loss = np.random.random()
            goal_muscle_gain = np.random.random()
            goal_endurance = np.random.random()
            goal_flexibility = np.random.random()
            
            # 经验与频率
            experience_years = np.random.randint(0, 10)
            weekly_frequency = np.random.randint(1, 7)
            avg_session_duration = np.random.randint(30, 120)  # 分钟
            
            user_feature = {
                'userId': user_id,
                'age': age,
                'weight': weight,
                'height': height,
                'bmi': bmi,
                'heart_rate': heart_rate,
                'fitness_level': fitness_level,
                'goal_weight_loss': goal_weight_loss,
                'goal_muscle_gain': goal_muscle_gain,
                'goal_endurance': goal_endurance,
                'goal_flexibility': goal_flexibility,
                'experience_years': experience_years,
                'weekly_frequency': weekly_frequency,
                'avg_session_duration': avg_session_duration
            }
            users_data.append(user_feature)
            
        return pd.DataFrame(users_data)
    
    def generate_exercise_features(self):
        """生成运动项目特征数据"""
        exercises_data = []
        
        for exercise_id in range(self.num_exercises):
            # 使用预定义的运动类型，循环使用
            exercise_name = self.exercise_types[exercise_id % len(self.exercise_types)]
            
            # 运动强度 (0-1)
            intensity = np.random.random()
            
            # 持续时间 (分钟)
            duration = np.random.randint(10, 60)
            
            # 设备需求 (0: 无需设备, 1: 需要设备)
            equipment_required = np.random.choice([0, 1], p=[0.4, 0.6])
            
            # 难度等级 (0-1)
            difficulty = np.random.random()
            
            # 训练重点 (0-1)
            cardio_focus = np.random.random()
            strength_focus = np.random.random()
            flexibility_focus = np.random.random()
            
            # 卡路里消耗 (标准化)
            calories_burned = np.random.randint(100, 500) / 500.0
            
            # 肌肉群 (0-10编码)
            muscle_group = np.random.randint(0, 10)
            
            # 空间需求 (0-1)
            space_required = np.random.random()
            
            # 技能要求 (0-1)
            skill_level = np.random.random()
            
            # 受伤风险 (0-1)
            injury_risk = np.random.random()
            
            # 流行度 (0-1)
            popularity = np.random.random()
            
            exercise_feature = {
                'exerciseId': exercise_id,
                'name': f'{exercise_name}_{exercise_id}',
                'intensity': intensity,
                'duration': duration,
                'equipment_required': equipment_required,
                'difficulty': difficulty,
                'cardio_focus': cardio_focus,
                'strength_focus': strength_focus,
                'flexibility_focus': flexibility_focus,
                'calories_burned': calories_burned,
                'muscle_group': muscle_group,
                'space_required': space_required,
                'skill_level': skill_level,
                'injury_risk': injury_risk,
                'popularity': popularity
            }
            exercises_data.append(exercise_feature)
            
        return pd.DataFrame(exercises_data)
    
    def generate_user_exercise_interactions(self, users_df, exercises_df, 
                                           min_interactions=10, max_interactions=50):
        """生成用户-运动交互数据 (隐式反馈)"""
        interactions = []
        base_time = datetime(2024, 1, 1)
        
        for user_id in range(self.num_users):
            # 每个用户的交互次数
            num_interactions = np.random.randint(min_interactions, max_interactions)
            
            # 用户特征
            user_bmi = users_df.loc[user_id, 'bmi']
            user_fitness = users_df.loc[user_id, 'fitness_level']
            
            # 根据用户特征选择适合的运动
            for _ in range(num_interactions):
                # 基于用户水平选择运动
                if user_fitness < 0.3:  # 初学者偏好低难度
                    exercise_id = np.random.choice(
                        exercises_df[exercises_df['difficulty'] < 0.5]['exerciseId'].values
                    )
                elif user_fitness > 0.7:  # 高手偏好高难度
                    exercise_id = np.random.choice(
                        exercises_df[exercises_df['difficulty'] > 0.5]['exerciseId'].values
                    )
                else:  # 中等水平随机选择
                    exercise_id = np.random.randint(0, self.num_exercises)
                
                # 生成评分 (1.0表示完成, 0.0表示未完成/放弃)
                # 难度匹配度影响完成率
                exercise_difficulty = exercises_df.loc[exercise_id, 'difficulty']
                completion_prob = 1.0 - abs(user_fitness - exercise_difficulty)
                rating = 1.0 if np.random.random() < completion_prob else 0.0
                
                # 时间戳
                days_offset = np.random.randint(0, 365)
                timestamp = int((base_time + timedelta(days=days_offset)).timestamp())
                
                interactions.append({
                    'userId': user_id,
                    'exerciseId': exercise_id,
                    'rating': rating,
                    'timestamp': timestamp
                })
        
        return pd.DataFrame(interactions)
    
    def normalize_features(self, df, feature_cols):
        """特征标准化到 [0, 1] 区间"""
        df_normalized = df.copy()
        
        for col in feature_cols:
            if col in df.columns:
                min_val = df[col].min()
                max_val = df[col].max()
                if max_val > min_val:
                    df_normalized[col] = (df[col] - min_val) / (max_val - min_val)
                else:
                    df_normalized[col] = 0.0
        
        return df_normalized
    
    def generate_complete_dataset(self, output_dir='../datasets/fitness'):
        """生成完整的健身数据集并保存"""
        import os
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        print("生成用户特征数据...")
        users_df = self.generate_user_features()
        
        print("生成运动项目特征数据...")
        exercises_df = self.generate_exercise_features()
        
        print("生成用户-运动交互数据...")
        interactions_df = self.generate_user_exercise_interactions(users_df, exercises_df)
        
        # 特征标准化
        print("标准化用户特征...")
        users_normalized = self.normalize_features(users_df, self.user_feature_names)
        
        print("标准化运动特征...")
        exercises_normalized = self.normalize_features(exercises_df, self.exercise_feature_names)
        
        # 保存数据
        users_df.to_csv(f'{output_dir}/users.csv', index=False)
        users_normalized.to_csv(f'{output_dir}/users_normalized.csv', index=False)
        exercises_df.to_csv(f'{output_dir}/exercises.csv', index=False)
        exercises_normalized.to_csv(f'{output_dir}/exercises_normalized.csv', index=False)
        interactions_df.to_csv(f'{output_dir}/interactions.csv', index=False)
        
        # 生成适配原始代码的格式 (userId, itemId, rating, timestamp)
        ratings_df = interactions_df.copy()
        ratings_df.columns = ['userId', 'itemId', 'rating', 'timestamp']
        ratings_df.to_csv(f'{output_dir}/fitness_ratings.dat', index=False, header=False)
        
        print(f"\n数据集生成完成！")
        print(f"用户数: {len(users_df)}")
        print(f"运动项目数: {len(exercises_df)}")
        print(f"交互记录数: {len(interactions_df)}")
        print(f"平均每用户交互数: {len(interactions_df) / len(users_df):.2f}")
        print(f"数据保存在: {output_dir}")
        
        return users_df, exercises_df, interactions_df


if __name__ == '__main__':
    # 生成数据集
    generator = FitnessDataGenerator(num_users=500, num_exercises=200)
    users, exercises, interactions = generator.generate_complete_dataset()
    
    # 显示统计信息
    print("\n=== 用户特征统计 ===")
    print(users.describe())
    
    print("\n=== 运动特征统计 ===")
    print(exercises.describe())
    
    print("\n=== 交互数据统计 ===")
    print(interactions.describe())
