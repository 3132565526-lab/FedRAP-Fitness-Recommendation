"""
测试个性化推荐是否生效
验证不同用户特征是否产生不同的推荐结果
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_personalization():
    """测试两个不同用户特征是否产生不同推荐"""
    
    # 注册第一个用户 - 减脂目标
    user1_data = {
        "username": "test_user_fat_loss",
        "password": "test123",
        "email": "fat_loss@test.com"
    }
    
    # 注册第二个用户 - 增肌目标
    user2_data = {
        "username": "test_user_muscle",
        "password": "test123",
        "email": "muscle@test.com"
    }
    
    # 注册并获取token
    print("=" * 80)
    print("1. 注册两个测试用户...")
    print("=" * 80)
    
    # 用户1
    resp1 = requests.post(f"{BASE_URL}/api/auth/register", json=user1_data)
    if resp1.status_code == 201:
        token1 = resp1.json()['token']
        print(f"✓ 用户1注册成功: {user1_data['username']}")
    else:
        # 如果已存在，尝试登录
        resp1 = requests.post(f"{BASE_URL}/api/auth/login", json=user1_data)
        token1 = resp1.json()['token']
        print(f"✓ 用户1登录成功: {user1_data['username']}")
    
    # 用户2
    resp2 = requests.post(f"{BASE_URL}/api/auth/register", json=user2_data)
    if resp2.status_code == 201:
        token2 = resp2.json()['token']
        print(f"✓ 用户2注册成功: {user2_data['username']}")
    else:
        # 如果已存在，尝试登录
        resp2 = requests.post(f"{BASE_URL}/api/auth/login", json=user2_data)
        token2 = resp2.json()['token']
        print(f"✓ 用户2登录成功: {user2_data['username']}")
    
    # 更新用户资料 - 用户1: 减脂为主
    print("\n" + "=" * 80)
    print("2. 设置不同的健身目标...")
    print("=" * 80)
    
    profile1 = {
        "profile": {
            "age": 30,
            "weight": 80,
            "height": 175,
            "fitness_level": 0.5,
            "goal_weight_loss": 0.9,      # 减脂目标高
            "goal_muscle_gain": 0.1,       # 增肌目标低
            "goal_endurance": 0.5,
            "goal_flexibility": 0.3,
            "experience_years": 2,
            "weekly_frequency": 4,
            "avg_session_duration": 60
        }
    }
    
    # 更新用户资料 - 用户2: 增肌为主
    profile2 = {
        "profile": {
            "age": 25,
            "weight": 65,
            "height": 175,
            "fitness_level": 0.6,
            "goal_weight_loss": 0.1,       # 减脂目标低
            "goal_muscle_gain": 0.9,       # 增肌目标高
            "goal_endurance": 0.3,
            "goal_flexibility": 0.2,
            "experience_years": 3,
            "weekly_frequency": 5,
            "avg_session_duration": 90
        }
    }
    
    headers1 = {"Authorization": f"Bearer {token1}"}
    headers2 = {"Authorization": f"Bearer {token2}"}
    
    resp1 = requests.put(f"{BASE_URL}/api/user/profile", json=profile1, headers=headers1)
    print(f"✓ 用户1资料更新: 减脂目标={profile1['profile']['goal_weight_loss']}, 增肌目标={profile1['profile']['goal_muscle_gain']}")
    
    resp2 = requests.put(f"{BASE_URL}/api/user/profile", json=profile2, headers=headers2)
    print(f"✓ 用户2资料更新: 减脂目标={profile2['profile']['goal_weight_loss']}, 增肌目标={profile2['profile']['goal_muscle_gain']}")
    
    # 获取推荐
    print("\n" + "=" * 80)
    print("3. 获取个性化推荐...")
    print("=" * 80)
    
    rec_resp1 = requests.post(
        f"{BASE_URL}/api/recommend", 
        json={"top_k": 5},
        headers=headers1
    )
    
    rec_resp2 = requests.post(
        f"{BASE_URL}/api/recommend",
        json={"top_k": 5},
        headers=headers2
    )
    
    if rec_resp1.status_code == 200 and rec_resp2.status_code == 200:
        recs1 = rec_resp1.json()['recommendations']
        recs2 = rec_resp2.json()['recommendations']
        
        print("\n【用户1 - 减脂为主】的推荐结果:")
        for i, rec in enumerate(recs1, 1):
            print(f"  {i}. {rec['name']} (评分: {rec['score']:.4f}, 强度: {rec['intensity']:.2f}, 卡路里: {rec['calories']})")
        
        print("\n【用户2 - 增肌为主】的推荐结果:")
        for i, rec in enumerate(recs2, 1):
            print(f"  {i}. {rec['name']} (评分: {rec['score']:.4f}, 强度: {rec['intensity']:.2f}, 卡路里: {rec['calories']})")
        
        # 检查推荐是否不同
        ids1 = [r['id'] for r in recs1]
        ids2 = [r['id'] for r in recs2]
        
        print("\n" + "=" * 80)
        print("4. 个性化验证结果:")
        print("=" * 80)
        
        if ids1 == ids2:
            print("❌ 警告: 两个用户的推荐完全相同，个性化可能未生效！")
            print(f"   用户1推荐ID: {ids1}")
            print(f"   用户2推荐ID: {ids2}")
        else:
            overlap = len(set(ids1) & set(ids2))
            print(f"✓ 个性化推荐生效！")
            print(f"   用户1推荐ID: {ids1}")
            print(f"   用户2推荐ID: {ids2}")
            print(f"   重叠项数量: {overlap}/5")
            print(f"   差异化程度: {(5-overlap)/5*100:.1f}%")
    else:
        print(f"❌ 获取推荐失败")
        print(f"   用户1: {rec_resp1.status_code} - {rec_resp1.text}")
        print(f"   用户2: {rec_resp2.status_code} - {rec_resp2.text}")

if __name__ == '__main__':
    test_personalization()
