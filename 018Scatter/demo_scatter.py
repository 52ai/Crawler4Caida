# coding:utf-8
"""
create on Dec 4,2019 by Wayne Yu
Function:

测试matplotlib画极坐标的功能

"""

import numpy as np
import matplotlib.pyplot as plt

N = 500
r = 10 * np.random.rand(N)
theta = 2 * np.pi * np.random.rand(N)

area = 20
colors = theta

ax = plt.subplot(111, projection='polar')
c = ax.scatter(theta, r, c=colors, marker='s', s=area, cmap='hsv', alpha=0.75)
ax.set_ylim(0, 10)  # 设置极坐标半径r的最大刻度
print(r)
print(theta)
p1_theta = theta[0]
p1_r = r[0]

p2_theta = theta[1]
p2_r = r[1]

x1 = p1_r * np.cos(p1_theta)
x2 = p2_r * np.cos(p2_theta)

y1 = p1_r * np.sin(p1_theta)
y2 = p2_r * np.sin(p2_theta)

print("p1:", x1, y1)
print("p2:", x2, y2)
ax.plot([theta[0], theta[1]], [r[0], r[1]], linewidth='0.2')

for i in range(0, len(theta)):
    ax.plot([theta[0], theta[i]], [r[0], r[i]],linewidth='0.2')


for i in range(0, len(theta)):
    ax.plot([theta[10], theta[i]], [r[0], r[i]],linewidth='0.2')

plt.show()
