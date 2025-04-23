import math
import random
import time

import matplotlib.pyplot as plt
import numpy as np

# 设定随机种子
random.seed(time.time())

# 🎨 1. 绘制函数图形
x_vals = np.linspace(-5, 2, 500)
y_vals = [math.sin(x) + x + 0.7 for x in x_vals]

plt.figure(figsize=(10, 5))
plt.plot(x_vals, y_vals, label='y = sin(x) + x + 0.7', color='blue')
plt.axhline(0, color='gray', linestyle='--', label='y = 0')
plt.title('函数图形：y = sin(x) + x + 0.7')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()

# 🔍 2. 随机算法找近似解
x_rough = None
for i in range(100000):
    x = random.uniform(-5, 2)  # 缩小范围更快收敛
    y = math.sin(x) + x + 0.7
    if abs(y) < 0.0001:
        x_rough = x
        print(f"✅ 初步解：x = {x:.10f}, y = {y:.2e}")
        plt.plot(x, y, 'ro', label='粗略解')  # 图上标记
        break

# 🎯 3. 精细搜索
if x_rough is not None:
    for i in range(10000):
        x_fine = random.uniform(x_rough - 0.1, x_rough + 0.1)
        y = math.sin(x_fine) + x_fine + 0.7
        if abs(y) < 0.000001:
            print(f"🎉 精细解：x = {x_fine:.10f}, y = {y:.2e}")
            plt.plot(x_fine, y, 'go', label='精细解')  # 图上标记
            break

plt.legend()
plt.show()
