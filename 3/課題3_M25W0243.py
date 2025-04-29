# 学籍番号と名前： M25W0243   袁　青凱
import math
import random

# 課題１
# ランダムアルゴリズムを使って、次の方程式を解を探してください
# sin(x) + x + 0.7 = 0 

for i in range(0, 100000):
    x = random.uniform(-30.0, 30.0)
    y = math.sin(x) + x + 0.7
    if -1.0 < y and y < 1.0:
        print("1: x=", x, "y=", y)
        break
#予測される値の範囲を狭め、精度を向上させます。
for i in range(0, 100000):
    # x値の範囲を狭め、精度を向上させます。
    x1 = random.uniform(x - 1, x + 1)
    y = math.sin(x1) + x1 + 0.7
    # y値の範囲を狭め、精度を向上させます。
    if -0.001 < y and y < 0.001:
        print("2: x1=", x1, "y=", y)
        break
    
# 1: x= -0.27038739888986285 y= 0.16250782067055725
# 2: x1= -0.3537354753082924 y= -0.00013988582045476594

'''
課題２
●シンボルセット＝ {A,B,C,D,E}  それぞれのシンボルの起こる確率:
●   A = 0.5
●   B = 0.2
●   C = 0.1
●   D = 0.1
●   E = 0.1
このシンボルセットの平均情報量を求めてください。
●計算式、計算値、どうやって答えを出したかわかるようにしてください

つづき、
●   {A, B, C, D} = {0.4, 0.3, 0.1, 0.2} の
ときの平均情報量をプログラムを作成して求めてください
'''

# 計算式
def shannon_entropy(probs):
    """
    平均情報量を計算する関数:
        H(X) = -sum(p * log2(p) for p in probs)
    """
    return -sum(p * math.log2(p) for p in probs if p > 0)

probs_1 = [0.5, 0.2, 0.1, 0.1, 0.1]
probs_2 = [0.4, 0.3, 0.1, 0.2]
entropy_value_1 = shannon_entropy(probs_1)
entropy_value_2 = shannon_entropy(probs_2)

# 計算値
print(f"平均情報量 {probs_1}: {entropy_value_1:.4f} bits")
print(f"平均情報量 {probs_2}: {entropy_value_2:.4f} bits")
#平均情報量 {A, B, C, D, E} = {0.5, 0.2, 0.1, 0.1, 0.1}: 1.9610 bits
#平均情報量 {A, B, C, D} = {0.4, 0.3, 0.1, 0.2}: 1.8464 bits


'''
課題3
'''
from math import log2

import numpy as np
import pandas as pd

# ------------------------------
# 1. 元データの作成
# ------------------------------
df = pd.DataFrame([
    (1, 'Sunny',  'Hot',  'High',   'Weak',   'No'),
    (2, 'Cloudy', 'Hot',  'High',   'Weak',   'Yes'),
    (3, 'Sunny',  'Mild', 'Normal', 'Strong', 'Yes'),
    (4, 'Cloudy', 'Mild', 'High',   'Strong', 'Yes'),
    (5, 'Rainy',  'Mild', 'High',   'Strong', 'No'),
    (6, 'Rainy',  'Cool', 'Normal', 'Strong', 'No'),
    (7, 'Rainy',  'Mild', 'High',   'Weak',   'Yes'),
    (8, 'Sunny',  'Hot',  'High',   'Strong', 'No'),
    (9, 'Cloudy', 'Hot',  'Normal', 'Weak',   'Yes'),
    (10,'Rainy',  'Mild', 'High',   'Strong', 'No'),
], columns=['Day','Weather','Temperature','Humidity','Wind','Play'])

print("元データ:", df)

# ------------------------------
# 2. ヘルパー関数：エントロピー＆情報利得
# ------------------------------
def entropy(series: pd.Series) -> float:
    """ 二値分類 (Yes/No) 列のシャノンエントロピーを計算する）"""
    counts = series.value_counts()
    total  = counts.sum()
    probs  = counts / total
    return -np.sum(probs * np.log2(probs + 1e-9))  # 小さな値を加えて log(0) を回避

def info_gain(df: pd.DataFrame, attr: str, target: str='Play') -> float:
    """元のエントロピー"""
    h_orig = entropy(df[target])
    # 条件付きエントロピーの計算
    cond_entropy = 0.0
    for v, sub in df.groupby(attr):
        weight = len(sub) / len(df)
        cond_entropy += weight * entropy(sub[target])
    return h_orig - cond_entropy

# ------------------------------
# 3. 属性ごとの条件付きエントロピー明細 & 利得計算
# ------------------------------
attributes = ['Weather', 'Wind', 'Temperature', 'Humidity']
gain_list = []

for attr in attributes:
    h_details = []
    cond_entropy = 0.0
    for v, sub in df.groupby(attr):
        weight = len(sub)/len(df)
        h_sub   = entropy(sub['Play'])
        cond_entropy += weight * h_sub
        h_details.append({
            attr: v,
            '件数': len(sub),
            'Yes数':  (sub['Play']=='Yes').sum(),
            'No数' :  (sub['Play']=='No').sum(),
            'エントロピー': round(h_sub, 3),
            '重み': round(weight, 3),
            '加重エントロピー': round(weight*h_sub, 3)
        })
    print(f"{attr} の条件付きエントロピー明細:")
    print(pd.DataFrame(h_details))
    # 情報利得を記録
    gain_list.append({'属性': attr,
                      '情報利得': round(entropy(df['Play']) - cond_entropy, 3)})

# ------------------------------
# 4. 属性情報利得の比較表
gain_df = pd.DataFrame(gain_list).sort_values('情報利得', ascending=False).reset_index(drop=True)
print("属性ごとの情報利得比較:", gain_df)
'''
0      Weather  0.400
1         Wind  0.125
2  Temperature  0.115
3     Humidity  0.035
'''

# 結論
# 天気は最も重要度が高く、手動で計算した 0.400 に最も近いため、ルート ノードとして最適な選択であることが確認できます。
# 他の機能の順序も、以前の手動計算と一致しています: 風 > 温度 > 湿度。