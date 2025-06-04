import math
import random
import time

# sin(x) + x + 0.7 = 0 
random.seed(time.time())  

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
    
# 1: x= -0.47840661189839295 y= -0.2387718746796441
# 2: x1= -0.35373247396931085 y= -0.00013406896800716162