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

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

# 1. 元のデータを生成
data = {
    'Weather':   ['Sunny','Cloudy','Sunny','Cloudy','Rainy','Rainy','Rainy','Sunny','Cloudy','Rainy'],
    'Temperature':['Hot','Hot','Mild','Mild','Mild','Cool','Mild','Hot','Hot','Mild'],
    'Humidity':  ['High','High','Normal','High','High','Normal','High','High','Normal','High'],
    'Wind':      ['Weak','Weak','Strong','Strong','Strong','Strong','Weak','Strong','Weak','Strong'],
    'Play':      ['No','Yes','Yes','Yes','No','No','Yes','No','Yes','No']
}
df = pd.DataFrame(data)

# 2. カテゴリ変数を数値にエンコード
le = LabelEncoder()
df_encoded = df.apply(le.fit_transform)

# 特徴量とラベルに分割
X = df_encoded.drop(columns='Play')
y = df_encoded['Play']

# 3. 決定木 (エントロピー基準) によって特徴重要度（情報利得）を計算
clf = DecisionTreeClassifier(criterion='entropy')
clf.fit(X, y)

# 4. 結果を整理して表示
importances = pd.Series(clf.feature_importances_, index=X.columns)
df_gain = importances.reset_index()
df_gain.columns = ['Attribute', 'Importance']
print("使用DecisionTreeClassifier计算的信息利得:")
print(df_gain)

# 結論
# 天気は最も重要度が高く、手動で計算した 0.400 に最も近いため、ルート ノードとして最適な選択であることが確認できます。
# 他の機能の順序も、以前の手動計算と一致しています: 湿度 > 温度 > 風。