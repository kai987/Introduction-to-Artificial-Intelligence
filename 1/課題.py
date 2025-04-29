import math
import random

# sin(x) + x + 0.7 = 0 


for i in range(0, 100000):
    x = random.uniform(-30.0, 30.0)
    y = math.sin(x) + x + 0.7
    if -1.0 < y and y < 1.0:
        print("1: x=", x, "y=", y)
        break

for i in range(0, 100000):
    x1 = random.uniform(x - 1, x + 1)
    y = math.sin(x1) + x1 + 0.7
    if -0.001 < y and y < 0.001:
        print("2: x1=", x1, "y=", y)
        break