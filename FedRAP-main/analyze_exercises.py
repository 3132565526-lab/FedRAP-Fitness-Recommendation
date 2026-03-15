import pandas as pd

# 读取CSV文件
df = pd.read_csv(r'd:\桌面加\FedRAP-main (3)\FedRAP-main\datasets\fitness\exercises.csv')

# 提取基础动作名称（去掉下划线和数字）
df['base_name'] = df['name'].str.split('_').str[0]

print("=" * 60)
print("健身项目分布统计")
print("=" * 60)

# 统计每种基础动作的数量
name_counts = df['base_name'].value_counts()
print("\n各类动作的数量:")
print(name_counts)

print(f"\n总项目数: {len(df)}")
print(f"动作类型数: {len(name_counts)}")

# 展示几个跑步的例子
print("\n" + "=" * 60)
print("以'跑步'为例，展示不同变体的差异:")
print("=" * 60)
running = df[df['base_name'] == '跑步'].head(5)
for idx, row in running.iterrows():
    print(f"\n{row['name']}:")
    print(f"  难度: {row['difficulty']:.2f}, 强度: {row['intensity']:.2f}")
    print(f"  时长: {row['duration']}分钟, 卡路里: {row['calories_burned']:.2f}")
    print(f"  有氧: {row['cardio_focus']:.2f}, 力量: {row['strength_focus']:.2f}, 柔韧: {row['flexibility_focus']:.2f}")
