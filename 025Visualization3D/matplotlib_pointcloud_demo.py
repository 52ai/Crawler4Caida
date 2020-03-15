# coding:utf-8
"""
create on Mar 15,2020 By Wenyan YU
Email: ieeflsyu@outlook

Function:

尝试在Matplotlib上展示点云

"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random


if __name__ == "__main__":
    # 生成点云数据，[[x,y,z,c], ...]
    x, y, z = [], [], []
    for i in range(0, 100000):
        x.append(random.uniform(-1, 1))  # 随机生成范围内的浮点数
        y.append(random.uniform(-1, 1))  # 随机生成范围内的浮点数
        z.append(random.uniform(-1, 1))  # 随机生成范围内的浮点数

    # 开始绘图
    fig = plt.figure(dpi=120)
    ax = fig.add_subplot(111, projection='3d')
    # 标题
    plt.title('point cloud')
    # 利用xyz的值，生成每个点的相应坐标（x,y,z）
    ax.scatter(x, y, z, c='b', marker='.', s=2, linewidth=0, alpha=1, cmap='spectral')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    # 显示
    plt.show()