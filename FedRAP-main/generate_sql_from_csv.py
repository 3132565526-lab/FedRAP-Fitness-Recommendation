import pandas as pd
import numpy as np
import os

# 切换到脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("当前工作目录:", os.getcwd())
print("开始读取CSV文件...")

# 读取CSV文件
csv_path = r'datasets\fitness\exercises.csv'
if not os.path.exists(csv_path):
    print(f"错误: 找不到文件 {csv_path}")
    exit(1)
    
df = pd.read_csv(csv_path)
print(f"成功读取CSV文件，共 {len(df)} 行数据")

# 肌肉群映射
muscle_groups = ['胸肌', '背部', '肩部', '手臂', '腿部', '腹肌', '核心', '全身', '臀部', '小腿']

# 器械映射
equipment_map = {
    0: '无需器械',
    1: '需要器械'
}

# 类别映射（基于运动特征）
def get_category(row):
    if row['cardio_focus'] > 0.6:
        return 'CARDIO'
    elif row['strength_focus'] > 0.6:
        return 'STRENGTH'
    elif row['flexibility_focus'] > 0.6:
        return 'FLEXIBILITY'
    elif row['strength_focus'] > 0.4 and row['cardio_focus'] < 0.3:
        return 'STRENGTH'
    else:
        return 'CARDIO'

# 生成SQL语句
sql_lines = []
sql_lines.append("-- 初始化数据脚本 UTF-8编码")
sql_lines.append("-- 健身动作数据（200个项目）")
sql_lines.append("MERGE INTO exercises (name, description, category, target_muscle, equipment, difficulty, intensity, calories_per_minute, suitability_weight_loss, suitability_muscle_gain, suitability_endurance, suitability_flexibility, recommended_duration, recommended_sets, recommended_reps, is_active) KEY(name) VALUES ")

values_list = []

for idx, row in df.iterrows():
    # 提取基础名称
    base_name = row['name'].split('_')[0]
    variant_num = row['name'].split('_')[1] if '_' in row['name'] else '0'
    
    category = get_category(row)
    muscle_group = muscle_groups[int(row['muscle_group'])]
    equipment = equipment_map[int(row['equipment_required'])]
    difficulty = round(row['difficulty'], 1)
    intensity = round(row['intensity'], 1)
    calories = int(8 + intensity * 10)  # 估算每分钟卡路里
    duration = int(row['duration'])
    
    # 适应性评分（基于运动特征）
    weight_loss = round(row['cardio_focus'] * 0.6 + row['calories_burned'] * 0.4, 1)
    muscle_gain = round(row['strength_focus'], 1)
    endurance = round((row['cardio_focus'] + row['duration'] / 60) / 2, 1)
    flexibility = round(row['flexibility_focus'], 1)
    
    # 推荐组数和次数
    if category == 'CARDIO':
        sets = 1
        reps = 1
    elif category == 'FLEXIBILITY':
        sets = 2
        reps = 1
    else:
        sets = np.random.randint(3, 5)
        reps = np.random.randint(8, 20)
    
    # 生成难度和强度标签
    if difficulty < 0.3:
        diff_label = '入门级'
    elif difficulty < 0.6:
        diff_label = '进阶级'
    else:
        diff_label = '高级'
    
    if intensity < 0.3:
        intensity_label = '低强度'
    elif intensity < 0.7:
        intensity_label = '中强度'
    else:
        intensity_label = '高强度'
    
    # 生成训练风格标签
    cardio_val = row['cardio_focus']
    strength_val = row['strength_focus']
    flexibility_val = row['flexibility_focus']
    
    if cardio_val > 0.6:
        style_label = '燃脂训练'
    elif strength_val > 0.6:
        style_label = '力量增肌'
    elif flexibility_val > 0.6:
        style_label = '柔韧拉伸'
    elif cardio_val > strength_val and cardio_val > flexibility_val:
        style_label = '有氧耐力'
    elif strength_val > cardio_val and strength_val > flexibility_val:
        style_label = '肌肉塑形'
    else:
        style_label = '综合训练'
    
    # 优化后的显示名称
    display_name = f"{base_name} - {style_label}（{diff_label}）"
    
    # 生成详细描述
    description = f"{base_name}训练 | {style_label} | "
    description += f"难度: {diff_label}({difficulty:.1f}) | 强度: {intensity_label}({intensity:.1f}) | "
    description += f"主要锻炼{muscle_group} | {equipment} | "
    description += f"建议时长{duration}分钟 | "
    description += f"每分钟消耗约{calories}卡路里 | "
    
    if weight_loss > 0.7:
        description += "适合减脂 | "
    if muscle_gain > 0.7:
        description += "适合增肌 | "
    if endurance > 0.7:
        description += "提升耐力 | "
    if flexibility > 0.7:
        description += "增强柔韧性 | "
    
    description = description.rstrip(' | ')
    
    value = f"('{display_name}', '{description}', '{category}', '{muscle_group}', '{equipment}', {difficulty}, {intensity}, {calories}, {weight_loss}, {muscle_gain}, {endurance}, {flexibility}, {duration}, {sets}, {reps}, TRUE)"
    values_list.append(value)

# 将所有值连接起来
sql_content = sql_lines[0] + '\n' + sql_lines[1] + '\n' + sql_lines[2] + '\n'
sql_content += ',\n'.join(values_list) + ';\n'

# 写入文件
with open('backend-java/src/main/resources/data.sql', 'w', encoding='utf-8') as f:
    f.write(sql_content)

print(f"成功生成包含 {len(values_list)} 个健身项目的SQL文件!")
print(f"文件已保存到: backend-java/src/main/resources/data.sql")
