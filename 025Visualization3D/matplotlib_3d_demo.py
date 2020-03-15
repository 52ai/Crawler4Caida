# coding:utf-8
"""
create on Feb 17, 2020 By Wenyan YU
Function:

全面向3D可视化进军，第一步调研看看marplotlib绘制3D效果如何

"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin) * np.random.rand(n) + vmin


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 10000


for cnt in range(0, 2):
    xs = randrange(n, 0, 100)
    ys = randrange(n, 0, 100)
    zs = randrange(n, 0, 100)
    ax.scatter(xs, ys, zs, c='r', marker='.', s=2)

x_line = [0, 50]
y_line = [0, 50]
z_line = [0, 50]


ax.plot3D(x_line, y_line, z_line, 'b')
ax.scatter(x_line, y_line, z_line, c='r', marker='^')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()



