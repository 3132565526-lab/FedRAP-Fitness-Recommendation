"""
综合个性化测试 - 验证年龄、BMI、健身水平等因素的影响
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def create_and_test_user(username, email, profile_data, description):
    """创建用户并测试推荐"""
    
    # 注册或登录
    user_data = {
        "username": username,
        "password": "test123",
        "email": email
    }
    
    resp = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    if resp.status_code == 201:
        token = resp.json()['token']
    else:
        # 如果已存在，尝试登录
        resp = requests.post(f"{BASE_URL}/api/auth/login", json=user_data)
        token = resp.json()['token']
    
    # 更新资料
    headers = {"Authorization": f"Bearer {token}"}
    requests.put(f"{BASE_URL}/api/user/profile", json={"profile": profile_data}, headers=headers)
    
    # 获取推荐
    rec_resp = requests.post(f"{BASE_URL}/api/recommend", json={"top_k": 5}, headers=headers)
    
    if rec_resp.status_code == 200:
        recs = rec_resp.json()['recommendations']
        
        print(f"\n{'='*80}")
        print(f"【{description}】")
        print(f"{'='*80}")
        print(f"年龄: {profile_data['age']}岁 | BMI: {profile_data.get('bmi', 'N/A')} | "
              f"健身水平: {profile_data['fitness_level']:.1f} | 经验: {profile_data['experience_years']}年")
        print(f"目标: 减脂={profile_data['goal_weight_loss']:.1f}, 增肌={profile_data['goal_muscle_gain']:.1f}")
        print(f"\n推荐运动:")
        
        for i, rec in enumerate(recs, 1):
            print(f"  {i}. {rec['name']:<20} "
                  f"评分:{rec['score']:.3f} | "
                  f"强度:{rec['intensity']:.2f} | "
                  f"难度:{rec['difficulty']:.2f} | "
                  f"卡路里:{rec['calories']:>3}")
        
        return [r['id'] for r in recs]
    else:
        print(f"❌ 获取推荐失败: {rec_resp.status_code}")
        return []

def main():
    print("="*80)
    print("综合个性化推荐测试")
    print("="*80)
    
    test_cases = []
    
    # 测试案例1: 年轻健身爱好者（高强度）
    test_cases.append(create_and_test_user(
        "young_athlete",
        "athlete@test.com",
        {
            "age": 22,
            "weight": 70,
            "height": 178,
            "bmi": 22.1,
            "fitness_level": 0.8,
            "goal_weight_loss": 0.2,
            "goal_muscle_gain": 0.7,
            "goal_endurance": 0.5,
            "goal_flexibility": 0.3,
            "experience_years": 4,
            "weekly_frequency": 5,
            "avg_session_duration": 90
        },
        "22岁年轻运动员 - 高健身水平、增肌目标"
    ))
    
    # 测试案例2: 中年超重减脂者（低冲击）
    test_cases.append(create_and_test_user(
        "middle_age_weightloss",
        "weightloss@test.com",
        {
            "age": 45,
            "weight": 85,
            "height": 170,
            "bmi": 29.4,  # 超重
            "fitness_level": 0.3,
            "goal_weight_loss": 0.9,
            "goal_muscle_gain": 0.1,
            "goal_endurance": 0.4,
            "goal_flexibility": 0.2,
            "experience_years": 0.5,
            "weekly_frequency": 3,
            "avg_session_duration": 45
        },
        "45岁中年人士 - 超重BMI、减脂目标、新手"
    ))
    
    # 测试案例3: 老年人保健（低强度、低风险）
    test_cases.append(create_and_test_user(
        "senior_health",
        "senior@test.com",
        {
            "age": 65,
            "weight": 70,
            "height": 165,
            "bmi": 25.7,
            "fitness_level": 0.4,
            "goal_weight_loss": 0.3,
            "goal_muscle_gain": 0.2,
            "goal_endurance": 0.2,
            "goal_flexibility": 0.8,  # 重视柔韧性
            "experience_years": 2,
            "weekly_frequency": 4,
            "avg_session_duration": 30
        },
        "65岁老年人 - 重视柔韧性、低风险运动"
    ))
    
    # 测试案例4: 偏瘦增重者（力量训练）
    test_cases.append(create_and_test_user(
        "underweight_gain",
        "gain@test.com",
        {
            "age": 28,
            "weight": 55,
            "height": 175,
            "bmi": 17.9,  # 偏瘦
            "fitness_level": 0.5,
            "goal_weight_loss": 0.0,
            "goal_muscle_gain": 0.9,
            "goal_endurance": 0.3,
            "goal_flexibility": 0.2,
            "experience_years": 1.5,
            "weekly_frequency": 4,
            "avg_session_duration": 60
        },
        "28岁偏瘦人士 - 增肌增重目标"
    ))
    
    # 测试案例5: 初学者（低难度）
    test_cases.append(create_and_test_user(
        "beginner",
        "beginner@test.com",
        {
            "age": 30,
            "weight": 68,
            "height": 170,
            "bmi": 23.5,
            "fitness_level": 0.2,  # 低健身水平
            "goal_weight_loss": 0.5,
            "goal_muscle_gain": 0.5,
            "goal_endurance": 0.3,
            "goal_flexibility": 0.3,
            "experience_years": 0.2,  # 新手
            "weekly_frequency": 2,
            "avg_session_duration": 30
        },
        "30岁健身新手 - 低健身水平、刚开始锻炼"
    ))
    
    # 分析差异化
    print("\n" + "="*80)
    print("个性化差异分析")
    print("="*80)
    
    for i in range(len(test_cases)):
        for j in range(i+1, len(test_cases)):
            overlap = len(set(test_cases[i]) & set(test_cases[j]))
            diff = 5 - overlap
            print(f"用户{i+1} vs 用户{j+1}: 重叠{overlap}项, 差异{diff}项 ({diff/5*100:.0f}%不同)")

if __name__ == '__main__':
    main()
