# coding:utf-8
"""
create on Dec 25, 2019 By Wayne Yu
测试下matplotlib画图的背景色
"""

import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)

dt = 0.01
t = np.arange(0, 30, dt)
nse1 = np.random.randn(len(t))  # white noise 1
nse2 = np.random.randn(len(t))  # white noise 2
s1 = np.sin(2 * np.pi * 10 * t) + nse1
s2 = np.sin(2 * np.pi * 10 * t) + nse2
s3 = np.sin(2 * np.pi * 10 * t) + nse1
s4 = np.sin(2 * np.pi * 10 * t) + nse2

fig = plt.figure(1)  # 创建图表1
axs0 = plt.subplot(221, fc='#FFDAB9', projection='polar')  # 在图标1中创建子图
axs0.plot(t, s1)  # 横轴与纵轴数据
axs0.set_xlim(0, 2)  # 限制x轴的取值范围
axs1 = plt.subplot(222, fc='#7FFF00', projection='polar')
axs1.plot(t, s2)
axs1.set_xlim(0, 2)
axs2 = plt.subplot(223, fc='#FF7F50', projection='polar')
axs2.plot(t, s3)
axs2.set_xlim(0, 2)
axs3 = plt.subplot(224, fc='#A9A9A9', projection='polar')
axs3.plot(t, s4)
axs3.set_xlim(0, 2)

plt.show()