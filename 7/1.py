import random

# 条件設定
lower, upper = 1.5, 2.3
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

# {'w1': 6.5943, 'w2': -3.7353, 'w3': -4.9228, '結果': 1.939}
