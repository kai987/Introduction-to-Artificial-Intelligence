import random

'''
ランダム探索：

Y=f(u) = u = (0.5 * w0) + (0.1 * w1) + (0.2 * w2)

1.7 < Y < 2.3 になるような、 w0、w1、w2の値を求めてください。

講義では、たしか違ったYの値を言ったと思いますが、講義の条件でもOKです。
'''

# 条件設定
lower, upper = 1.7, 2.3
max_attempts = 100000

# 条件を満たす w1, w2, w3 を探索
solution = None
for _ in range(max_attempts):
    w1 = random.uniform(-10, 10)
    w2 = random.uniform(-10, 10)
    w3 = random.uniform(-10, 10)
    val = 0.5 * w1 + 0.1 * w2 + 0.2 * w3
    if lower <= val <= upper:
        solution = {'w1': round(w1, 4), 'w2': round(w2, 4), 'w3': round(w3, 4), '結果': round(val, 4)}
        break

print(solution)

# {'w1': -1.6363, 'w2': 9.2697, 'w3': 9.353, '結果': 1.9794}