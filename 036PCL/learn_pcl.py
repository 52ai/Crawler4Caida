# coding:utf-8
"""
create on Mar 14, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

学习PCL，做点云相关的应用

"""

import pcl.pcl_visualization
import random

# 生成点云数据，[[x,y,z,c], ...]
points = []
temp_list = []
for i in range(0, 100000):
    x = random.uniform(-1, 1)  # 随机生成范围内的浮点数
    y = random.uniform(-1, 1)  # 随机生成范围内的浮点数
    z = random.uniform(-1, 1)  # 随机生成范围内的浮点数
    c = 0.15
    temp_list.append(x)
    temp_list.append(y)
    temp_list.append(z)
    temp_list.append(c)
    points.append(temp_list)
    temp_list = []

# 不带颜色[x,y,z]
# cloud = pcl.PointCloud(points)
# visual = pcl.pcl_visualization.CloudViewing()
# visual.ShowMonochromeCloud(cloud)


# PointCloud_PointXYZRGB 需要点云数据是N*4，分别表示x,y,z,RGB ,其中RGB 用一个整数表示颜色；
color_cloud = pcl.PointCloud_PointXYZRGB(points)
visual = pcl.pcl_visualization.CloudViewing()
visual.ShowColorCloud(color_cloud, b'cloud')

# test_Circle = pcl.pcl_visualization.PCLVisualizering()
# test_Circle.AddCircle()

flag = True
while flag:
    flag != visual.WasStopped()
