from math import log2

import numpy as np
import pandas as pd

# 1. トレーニングデータの作成（11 サンプル）
data = [
    (0, 'Sunny',    'Hot',  'High',   'Weak',   'No'),
    (1, 'Sunny',    'Hot',  'High',   'Strong', 'No'),
    (2, 'Overcast', 'Hot',  'High',   'Weak',   'Yes'),
    (3, 'Rain',     'Mild', 'High',   'Weak',   'Yes'),
    (4, 'Rain',     'Cool', 'Normal', 'Weak',   'Yes'),
    (5, 'Rain',     'Cool', 'Normal', 'Strong', 'No'),
    (6, 'Overcast', 'Cool', 'Normal', 'Strong', 'Yes'),
    (7, 'Sunny',    'Mild', 'High',   'Weak',   'No'),
    (8, 'Sunny',    'Cool', 'Normal', 'Weak',   'Yes'),
    (9, 'Rain',     'Mild', 'Normal', 'Weak',   'Yes'),
    (11,'Overcast', 'Mild', 'High',   'Strong', 'Yes'),
]
df_train = pd.DataFrame(data, columns=['Day','天気','温度','湿度','風','テニスしない'])
print("課題3-1 トレーニングデータ", df_train)

# エントロピー計算関数
def entropy(series: pd.Series) -> float:
    counts = series.value_counts()
    probs  = counts / counts.sum()
    return -np.sum(probs * np.log2(probs + 1e-9))

# 属性ごとの条件付きエントロピーと情報利得
attributes = ['天気','温度','湿度','風']
h_orig = entropy(df_train['テニスしない'])
results = []

for attr in attributes:
    cond = 0.0
    details = []
    for val, subgroup in df_train.groupby(attr):
        p = len(subgroup) / len(df_train)
        h_sub = entropy(subgroup['テニスしない'])
        cond += p * h_sub
        details.append({
            attr: val,
            '件数': len(subgroup),
            'Yes数': int((subgroup['テニスしない']=='Yes').sum()),
            'No数': int((subgroup['テニスしない']=='No').sum()),
            'エントロピー': round(h_sub, 3),
            '重み': round(p, 3),
            '加重エントロピー': round(p * h_sub, 3)
        })
    gain = round(h_orig - cond, 3)
    print(f"{attr} の条件付きエントロピー詳細", pd.DataFrame(details))
    results.append({'属性': attr, '条件付きエントロピー': round(cond, 3), '情報利得': gain})

df_gain = pd.DataFrame(results).sort_values('情報利得', ascending=False).reset_index(drop=True)
print("属性ごとの情報利得比較", df_gain)


import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier, export_text

# 1. データの準備
data = [
    ('Sunny',    'Hot',  'High',   'Weak',   'No'),
    ('Sunny',    'Hot',  'High',   'Strong', 'No'),
    ('Overcast', 'Hot',  'High',   'Weak',   'Yes'),
    ('Rain',     'Mild', 'High',   'Weak',   'Yes'),
    ('Rain',     'Cool', 'Normal', 'Weak',   'Yes'),
    ('Rain',     'Cool', 'Normal', 'Strong', 'No'),
    ('Overcast', 'Cool', 'Normal', 'Strong', 'Yes'),
    ('Sunny',    'Mild', 'High',   'Weak',   'No'),
    ('Sunny',    'Cool', 'Normal', 'Weak',   'Yes'),
    ('Rain',     'Mild', 'Normal', 'Weak',   'Yes'),
    ('Overcast', 'Mild', 'High',   'Strong', 'Yes'),
]
columns = ['天気', '温度', '湿度', '風', 'テニス']
df = pd.DataFrame(data, columns=columns)

# 2. カテゴリ変数を数値に変換
enc = OrdinalEncoder()
X = enc.fit_transform(df[['天気', '温度', '湿度', '風']])
feature_names = enc.get_feature_names_out(['天気','温度','湿度','風'])

# 3. 目的変数を 0/1 に変換
y = df['テニス'].map({'No': 0, 'Yes': 1}).values

# 4. 決定木モデルを「エントロピー」基準で学習
clf = DecisionTreeClassifier(criterion='entropy', random_state=0)
clf.fit(X, y)

# 5. 各特徴の重要度（情報利得の相対尺度）を確認
importances = pd.Series(clf.feature_importances_, index=feature_names)
print("★ 特徴重要度 (情報利得に比例):")
print(importances.sort_values(ascending=False))

# 6. 決定木のルールをテキストで出力
print("\n★ 決定木のルール:")
print(export_text(clf, feature_names=list(feature_names)))
