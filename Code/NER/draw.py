import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import pandas as pd
import json
from scipy.stats import gaussian_kde

# 假设这是你的数据

def get_data():

    Datasets_name = "CoNLL2003"
    dataset_path = './{}/'.format(Datasets_name)

    OutputPath = "./"
    E_Setting = "0shot"
    Process_name = "E_With_Diff_Conf"

    outfile_name = OutputPath+Datasets_name+"_"+E_Setting+"_"+Process_name+".json"

    confidence = list()
    difficulty = list()

    with open(outfile_name, "r") as file:
        data = json.loads(file.read())
        for instance in data:
            confidence.append(instance['ChatGPT CConf'])
            difficulty.append(instance['ChatGPT CDiff'])

    assert len(confidence)==len(difficulty),"length is not equal"
    print(f'instances length is {len(confidence)}')
    return confidence,difficulty

def scatter (df):
    # 计算密度
    x = df['difficulty']
    y = df['confidence']
    xy = np.vstack([x,y])
    z = gaussian_kde(xy)(xy)

    # 对数据点进行排序
    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]

    ax = plt.subplots(figsize=(12, 8))
    # 创建散点图，并且保存引用scatter，用于创建颜色条
    scatter = ax.scatter(x, y, c=z, s=70, alpha=0.1)

    # 创建颜色条，并且将散点图的引用传递给colorbar
    plt.colorbar(scatter, label='density')

    # 设置标签和标题
    ax.set_xlabel('difficulty')
    ax.set_ylabel('confidence')
    plt.title('Scatter plot with density color coding')
    plt.show()

def heatmap(pd):

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

def hexbin(df):
    # 绘制六边形箱图（hexbin）
    x = df['difficulty']
    y = df['confidence']

    plt.figure(figsize=(10, 8))
    plt.hexbin(x, y, gridsize=30, cmap='Blues', edgecolors='none')
    # 增加颜色条
    plt.colorbar(label='Count in bin')
    plt.show()

def kdeplot(df):
    # 绘制密度图
    x = df['difficulty']
    y = df['confidence']
    plt.figure(figsize=(10, 8))

    sns.kdeplot(x=x, y=y, cmap="Blues", fill=True, bw_adjust=0.5, label='Density')

    plt.legend()

    plt.show()

if __name__ == "__main__":
    confidence, difficulty = get_data()
    
    df = pd.DataFrame({'difficulty': difficulty, 'confidence': confidence})
    df['difficulty'] = pd.to_numeric(df['difficulty'], errors='coerce')
    df['confidence'] = pd.to_numeric(df['confidence'], errors='coerce')

    df = df.dropna()

    heatmap(pd)