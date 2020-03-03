# coding:utf-8
"""
create on Feb 26, 2020 By Wenyan YU
Email:ieeflsyu@outlook.com

Function:
学习matplotlib下动画（animation）的绘制

输出GIF或者MP4时要注意，writer的选择，默认为ffmpeg，可输出mp4；若要输出gif则需要将writer属性修改为imagemagick

"""

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import time
import mpl_toolkits.mplot3d.axes3d as p3


def my_ani():

    # 数据集：X轴数据固定；Y轴的数据更新
    X = np.arange(0, 10, 0.01)  # X shape： (N,)
    Ys = [np.sin(X + k / 10) for k in range(200)]  # Ys shape： (k, N)
    # print("X:", X)
    # print("Ys:", Ys)

    x = X
    ys = Ys

    fig, ax = plt.subplots()
    ax.set_title('y = sin(x + k/10)')
    ax.set_xlim([0, 10]), ax.set_xlabel('X')
    ax.set_ylim([-1, 1]), ax.set_ylabel('Y')
    line, = ax.plot(x, ys[0])  # 绘制原始图像
    ano = plt.annotate('k: 0', (1, 1))

    def animate(i):  # 动画函数，根据传入的i更新数据
        line.set_ydata(ys[i])       # update the data.
        ano.set_text('k: %d' % i)  # update the annotate.
        return line,
    # animation.FuncAnimation 参数说明
    # fig:          figure 对象，即创建的画布
    # func:         动画函数，自定义函数 animate，实现每个时刻需要更新图形对象的函数
    # frames:       总帧数，即模拟多少帧动画，不同时刻的t相当于animate的参数
    # frags:        需要传递的额外参数，使用元组的格式进行传递
    # interval:     间隔时间，ms，刷新频率
    # blit:         告诉动画只重绘修改的部分（默认为false），否则全部重绘（修改为true，会让动画显示的非常快）
    ani = animation.FuncAnimation(fig, animate, frames=20, interval=100, blit=False)
    ani.save('../000LocalData/networkx_graph/my_ani.gif', writer="imagemagick", dpi=300)
    # ani.save('../000LocalData/networkx_graph/my_ani.mp4', writer="ffmpeg", dpi=300)
    plt.show()


def lissajous_figure():
    """
    绘制李萨如图形
    李萨如图形是指由在垂直方向上的两个频率成简单整数比的简谐振动所合成的规则的、稳定的闭合曲线
    :return:
    """
    plt.style.use('dark_background')
    fig = plt.figure()
    ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
    line, = ax.plot([], [], lw=2)

    # 初始化画布
    def init():
        line.set_data([], [])
        return line,

    xdata, ydata = [], []

    # 模拟示波器的ghost效应
    def ghost_image(x, y):
        xdata.append(x)
        ydata.append(y)
        if len(xdata) > 60:
            del xdata[0]
            del ydata[0]
        return xdata, ydata

    # 动画函数
    def animate(i):
        t = i/100.0

        x = 40*np.sin(2*2*np.pi*(t+0.3))
        y = 40*np.cos(3*2*np.pi*t)

        line.set_data(ghost_image(x, y))
        return line,
    plt.title('Lissajous Figure')
    plt.axis('off')
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=400, interval=20, blit=True)
    ani.save('../000LocalData/networkx_graph/lissajous_ani.gif', writer="imagemagick", dpi=100)
    plt.show()


def random_walk_3d():
    """
    绘制3D随机游走动画
    :return:
    """
    np.random.seed(19680801)  # 固定随机种子，实现游走轨迹的重现

    def gen_rand_line(length, dims=2):
        """
        用随机游走算法生成line
        :param length:
        :param dims:
        :return:
        """
        line_data = np.empty((dims, length))
        line_data[:, 0] = np.random.rand(dims)
        for index in range(1, length):
            step = ((np.random.rand(dims) - 0.5) * 0.1)
            line_data[:, index] = line_data[:, index - 1] + step
        return line_data

    def update_lines(num, data_lines, lines):
        for line, data in zip(lines, data_lines):
            line.set_data(data[0:2, :num])
            line.set_3d_properties(data[2, :num])
        return lines

    plt.style.use('dark_background')
    fig = plt.figure(figsize=(10, 8))
    ax = p3.Axes3D(fig)

    data = [gen_rand_line(25, 3) for index in range(50)]

    lines = [ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])[0] for dat in data]

    ax.set_xlim3d([0.0, 1.0])
    ax.set_xlabel('X')

    ax.set_ylim3d([0.0, 1.0])
    ax.set_ylabel('Y')

    ax.set_zlim3d([0.0, 1.0])
    ax.set_zlabel('Z')

    ax.set_title('3D Test')

    line_ani = animation.FuncAnimation(fig, update_lines, frames=25, fargs=(data, lines), interval=50, blit=False)
    line_ani.save('../000LocalData/networkx_graph/rand_walk_3d_ani.gif', writer="imagemagick", dpi=100)
    plt.show()


if __name__ == "__main__":
    start_time = time.time()
    # my_ani()
    lissajous_figure()
    # random_walk_3d()
    end_time = time.time()
    print("Script Finish! Time Consuming: ", (end_time - start_time), "s")

