import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import pandas as pd
import json
from scipy.stats import gaussian_kde

# 假设这是你的数据

Datasets_name = "ACE05"
dataset_path = './{}/'.format(Datasets_name)

OutputPath = "./"
E_Setting = "0shot"
Process_name = "E_With_Diff_Conf"

outfile_name = OutputPath+Datasets_name+"_"+E_Setting+"_"+Process_name+".json"

i = 0
confidence = list()
difficulty = list()
outfile_name = 'test.json'

with open(outfile_name, "r") as file:
    data = json.loads(file.read())
    for instance in data:
        confidence.append(instance['ChatGPT CConf'])
        difficulty.append(instance['ChatGPT CDiff'])

r = list()
for c,d in zip(confidence,difficulty):
    r.append((c,d))
    

df = pd.DataFrame({'difficulty': difficulty, 'confidence': confidence})
difficulty_counts = df.groupby('difficulty')['confidence'].mean()
# # 计算密度
# x = df['difficulty']
# y = df['confidence']
# xy = np.vstack([x,y])
# z = gaussian_kde(xy)(xy)

# # 对数据点进行排序
# idx = z.argsort()
# x, y, z = x[idx], y[idx], z[idx]

# fig, ax = plt.subplots()
# # 创建散点图，并且保存引用scatter，用于创建颜色条
# scatter = ax.scatter(x, y, c=z, s=50, alpha=0.3)

# # 创建颜色条，并且将散点图的引用传递给colorbar
# plt.colorbar(scatter, label='density')

# # 设置标签和标题
# ax.set_xlabel('difficulty')
# ax.set_ylabel('confidence')
# plt.title('Scatter plot with density color coding')
# plt.show()

# # 绘制柱状图
# plt.figure(figsize=(11, 6))
# plt.bar(difficulty_counts.index, difficulty_counts.values, color='teal', alpha=0.4)

# print(f'difficulty {difficulty_counts.index}')
# # 添加标题和标签
# plt.title('Average Confidence per Difficulty Level')
# plt.xlabel('Difficulty Level')
# plt.ylabel('Average Confidence')
# plt.xticks(ticks=np.arange(1, 11), labels=np.arange(1, 11))  # 假设difficulty是1到8的等级
# plt.show()


# 创建一个网格并计算每个单元中的点数
heatmap_data = pd.pivot_table(df, values='confidence', index='confidence', columns='difficulty', aggfunc=len, fill_value=0)

# 绘制热图
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='viridis', annot=True, fmt='.0f')
plt.title('heatmap')
plt.xlabel('difficulty')
plt.ylabel('confidence')
ax = plt.gca()
ax.invert_yaxis()
plt.show()
