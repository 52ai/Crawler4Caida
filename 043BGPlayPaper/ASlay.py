# coding:utf-8
"""
create on  June 17, 2020 By Wayne YU

Function:
通过前期对力引导布局算法的研究，如KK、FR、forceAtlas2、OpenOrd等
这些算法各有优劣，或布局速度快，但是布局效果一般；或布局效果还可以但是，布局速度慢。
因此有必要研究将多种算法进行组合，优化

经调研，暂选用forceAtlas2和OpenOrd作为组合的优化思路，亦可借鉴形成新的算法（尤其是针对全球AS网络的特点优化）
为保证过程可控，所有的算法都得重新用Python实现

最终确定了这个算法暂且称之为ASlay算法
该算法将借鉴Force-directed算法思想，针对全球AS网络的特点进行优化，形成一个适合AS领域内的拓扑算法
布局速度快，布局效果好，能够突出表现网络基础设施的某种意义

"""
import time
from math import sqrt
import numpy
import random
import matplotlib.pyplot as plt
import networkx
import matplotlib.animation as animation


ANIMATION_LIST = []  # 存储过程数据


# 定义节点的数据结构
class Node:
    def __init__(self):
        self.mass = 0  # 点的质量
        self.old_dx = 0  # 点的原x坐标
        self.old_dy = 0  # 点的原y坐标
        self.dx = 0
        self.dy = 0
        self.x = 0
        self.y = 0


# 定义连边的数据结构
class Edge:
    def __init__(self):
        self.node1 = -1  # 边的起始节点
        self.node2 = -1  # 边的目的节点
        self.weight = 0  # 边的权重


# 两点间引力计算模型
def compute_attraction(n1, n2, e, coefficient=0):
    x_dist = n1.x - n2.x
    y_dist = n1.y - n2.y
    factor = -coefficient * e  # 计算引力因子(负号，表示向对方方向移动)
    """
    根据引力因子更新两点的坐标(x1, y1)、(x2, y2)
    """
    n1.dx += x_dist * factor
    n1.dy += y_dist * factor
    n2.dx -= x_dist * factor
    n2.dy -= y_dist * factor


# 两点间斥力计算模型
def compute_repulsion(n1, n2, coefficient=0):
    x_dist = n1.x - n2.x
    y_dist = n1.y - n2.y
    distance2 = x_dist * x_dist + y_dist * y_dist   # 计算两点间距离的平方

    if distance2 > 0:
        factor = coefficient * n1.mass * n2.mass / distance2  # 计算斥力因子（表示斥力的大小）
        """
        根据斥力因子计算两点新的位置坐标（x1, y1）、(x2, y2)
        """
        n1.dx += x_dist * factor
        n1.dy += y_dist * factor
        n2.dx -= x_dist * factor
        n2.dy -= y_dist * factor


"""
空间中的强重力和普通重力的公式，还需要进一步确认
方案一：普通重力，即重力只和节点的质量有关系，而强重力则不仅与节点的质量有关系，还与其离圆心的距离里成正比。
方案二：普通重力，不仅与节点的质量有关系，还与其离圆心的距离成反比，而强重力只与节点的质量有关。

当前算法采用的是方案二
具体选择何种方案，还需要看实际的可视化效果
"""


# 空间点重力计算模型
def compute_gravity(n, g, coefficient=0):
    x_dist = n.x
    y_dist = n.y
    distance = sqrt(x_dist * x_dist + y_dist * y_dist)  # 计算点离圆心的距离

    if distance > 0:
        factor = coefficient * n.mass * g / distance  # 计算重力因子
        """
        根据重力因子更新点的坐标(x, y)
        """
        n.dx -= x_dist * factor
        n.dy -= y_dist * factor


# 空间强重力计算模型
def compute_strong_gravity(n, g, coefficient=0):
    x_dist = n.x
    y_dist = n.y

    if x_dist != 0 and y_dist != 0:
        factor = coefficient * n.mass * g  # 计算强重力因子，重力的大小不随点离圆心距离的变大而变小
        """
        根据强重力因子更新点的坐标(x, y)
        """
        n.dx -= x_dist * factor
        n.dy -= y_dist * factor


# 引力迭代
def apply_attraction(nodes, edges, coefficient, edge_influence):
    # Optimization, since usually edgeWeightInfluence is 0 or 1, and pow is slow
    if edge_influence == 0:
        for edge in edges:
            compute_attraction(nodes[edge.node1], nodes[edge.node2], 1, coefficient)
    elif edge_influence == 1:
        for edge in edges:
            compute_attraction(nodes[edge.node1], nodes[edge.node2], edge.weight, coefficient)
    else:
        for edge in edges:
            compute_attraction(nodes[edge.node1], nodes[edge.node2], pow(edge.weight, edge_influence), coefficient)


# 斥力迭代
def apply_repulsion(nodes, coefficient):
    for i in range(0, len(nodes)):
        for j in range(0, i):
            compute_repulsion(nodes[i], nodes[j], coefficient)


# 重力迭代
def apply_gravity(nodes, gravity, scaling_ratio, use_strong_gravity=False):
    if not use_strong_gravity:
        for i in range(0, len(nodes)):
            compute_gravity(nodes[i], gravity / scaling_ratio, scaling_ratio)
    else:
        for i in range(0, len(nodes)):
            compute_strong_gravity(nodes[i], gravity / scaling_ratio, scaling_ratio)


# ASlay算法主体部分
def aslay(
        G,  # 一个由2D numpy ndarrary格式化的图
        pos=None,  # 初始化位置的数组
        niter=50,  # 主体程序循环迭代的次数niter

        # Behavior alternatives
        outboundAttractionDistribution=False,  # "Dissuade hubs" # NOT (fully) IMPLEMENTED
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # "Prevent overlap" # NOT IMPLEMENTED
        edgeWeightInfluence=0,

        # Performance
        jitterTolerance=1.0,  # "Tolerance"
        barnesHutOptimize=False,  # NOT IMPLEMENTED
        barnesHutTheta=1.2,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=2.0,
        strongGravityMode=False,
        gravity=1.0,

        # plus
        draw_graph=None,  # 阶段性输出图绘制
        draw_gap=10,  # 每个多少次迭代绘制一次图

):
    # 参数检验
    assert isinstance(G, numpy.ndarray), "G is not a numpy ndarray"
    assert G.shape == (G.shape[0], G.shape[0]), "G is not 2D square"
    assert numpy.all(G.T == G), "G is not symmetric.  Currently only undirected graphs are supported"  # 目前支持无向图
    assert isinstance(pos, numpy.ndarray) or (pos is None), "Invalid node positions"
    assert outboundAttractionDistribution == linLogMode == adjustSizes == barnesHutOptimize == False, "You selected a feature that has not been implemented yet..."

    # forceAtlas2布局算法的初始化
    speed = 1
    speedEfficiency = 1

    # 初始化点的数据结构
    nodes = []
    for i in range(0, G.shape[0]):
        n = Node()
        n.mass = 1 + numpy.sum(G[i])
        n.old_dx = 0
        n.old_dy = 0
        n.dx = 0
        n.dy = 0
        if pos is None:
            n.x = random.random()
            n.y = random.random()
        else:
            n.x = pos[i][0]
            n.y = pos[i][1]
        nodes.append(n)

    # 初始化边的数据结构
    edges = []
    es = numpy.asarray(G.nonzero()).T
    for e in es:  # 循环边
        if e[1] <= e[0]:
            continue  # 避免重复边
        edge = Edge()
        edge.node1 = e[0]  # 第一个点在nodes的index
        edge.node2 = e[1]  # 第二个点在nodes的index
        edge.weight = G[tuple(e)]
        edges.append(edge)

    # 主循环开始
    iter_cnt = 1
    for _i in range(0, niter):
        iter_time_start = time.time()
        for n in nodes:
            n.old_dx = n.dx
            n.old_dy = n.dy
            n.dx = 0
            n.dy = 0

        # Barnes Hut优化步骤
        if outboundAttractionDistribution:
            outboundAttCompensation = numpy.mean([n.mass for n in nodes])

        apply_repulsion(nodes, scalingRatio)  # 斥力作用
        apply_gravity(nodes, gravity, scalingRatio, use_strong_gravity=strongGravityMode)  # 重力作用
        apply_attraction(nodes, edges, 1.0, edgeWeightInfluence)  # 引力作用

        # 自动调整速度
        totalSwinging = 0.0  # 有多少不规则的运动
        totalEffectiveTraction = 0.0  # 有多少有效的运动
        for n in nodes:
            swinging = sqrt((n.old_dx - n.dx) * (n.old_dx - n.dx) + (n.old_dy - n.dy) * (n.old_dy - n.dy))
            totalSwinging += n.mass * swinging
            totalEffectiveTraction += .5 * n.mass * sqrt(
                (n.old_dx + n.dx) * (n.old_dx + n.dx) + (n.old_dy + n.dy) * (n.old_dy + n.dy))

        # 优化抖动的限度（大网大抖动，小网小抖动，经验值）
        estimatedOptimalJitterTolerance = .05 * sqrt(len(nodes))
        minJT = sqrt(estimatedOptimalJitterTolerance)
        maxJT = 10
        jt = jitterTolerance * max(minJT, min(maxJT, estimatedOptimalJitterTolerance * totalEffectiveTraction / (
                    len(nodes) * len(nodes))))

        minSpeedEfficiency = 0.05

        # 防止不稳定的行为
        if totalSwinging / totalEffectiveTraction > 2.0:
            if speedEfficiency > minSpeedEfficiency:
                speedEfficiency *= .5
            jt = max(jt, jitterTolerance)

        targetSpeed = jt * speedEfficiency * totalEffectiveTraction / totalSwinging

        if totalSwinging > jt * totalEffectiveTraction:
            if speedEfficiency > minSpeedEfficiency:
                speedEfficiency *= .7
        elif speed < 1000:
            speedEfficiency *= 1.3

        # 速度不能提升的太快，否则收敛的很慢
        maxRise = .5
        speed = speed + min(targetSpeed - speed, maxRise * speed)

        # 更新位置
        factor_list = []
        for n in nodes:
            swinging = n.mass * sqrt((n.old_dx - n.dx) * (n.old_dx - n.dx) + (n.old_dy - n.dy) * (n.old_dy - n.dy))
            factor = speed / (1.0 + sqrt(speed * swinging))
            factor_list.append(factor)
            n.x = n.x + (n.dx * factor)
            n.y = n.y + (n.dy * factor)
        """
        每隔draw_gap次迭代绘图一次
        """
        if iter_cnt % draw_gap == 0:
            layout_2d_save_name = "new_draw_2d_layout_" + str(iter_cnt)
            # print(layout_2d_save_name)
            layout_2d_pos = dict(zip(draw_graph.nodes(), [(n.x, n.y) for n in nodes]))
            draw_2d(draw_graph, layout_2d_pos, layout_2d_save_name, is_draw=False)
            """
            根据各个点的平均速度，判断是否需要停止迭代
            """
            # print("Average speed factor:", numpy.average(factor_list))
        iter_cnt += 1  # 迭代次数自增1
        iter_time_end = time.time()
        print("STEP %s, Time Consuming:%s S" % (str(iter_cnt-1), (iter_time_end - iter_time_start)))

    return [(n.x, n.y) for n in nodes]


def aslay_networkx_layout(G, pos=None, **kwargs):
    draw_gap = 1  # 迭代绘图间隔
    assert isinstance(G, networkx.classes.graph.Graph), "Not a networkx graph"
    assert isinstance(pos, dict) or (pos is None), "pos must be specified as a dictionary, as in networkx"
    M = numpy.asarray(networkx.to_numpy_matrix(G))
    if pos is None:
        layout_2d = aslay(M, pos=None, draw_graph=G, draw_gap=draw_gap, **kwargs)
    else:
        poslist = numpy.asarray([pos[i] for i in G.nodes()])
        layout_2d = aslay(M, pos=poslist, draw_graph=G, draw_gap=draw_gap, **kwargs)
    return dict(zip(G.nodes(), layout_2d))


def draw_2d(G_2d, pos, graph_name, is_draw=True, is_show=False):
    """
    根据传入的2D网络图绘制2d Graph
    :param G_2d:
    :param pos:
    :param graph_name:
    :param is_draw:
    :param is_show:
    :return:
    """
    # 记录过程数据
    temp_list = list()
    temp_list.append(G_2d)
    temp_list.append(pos)
    ANIMATION_LIST.append(temp_list)

    if is_draw:
        print("=>开始绘图- - - - - - - - - - - - - ")
        print("Graph Nodes Count:", G_2d.number_of_nodes())
        print("Graph Edges Count:", G_2d.number_of_edges())
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        # 2D绘点
        for node_key in pos.keys():
            xs = pos[node_key][0]
            ys = pos[node_key][1]
            ax.scatter(xs, ys, c='white', marker='o', s=10)
        # 3D绘线
        x_line = []
        y_line = []
        for line in G_2d.edges():
            # 添加node1, node2的x轴
            x_line.append(pos[line[0]][0])
            x_line.append(pos[line[1]][0])
            # 添加node1, node2的y轴
            y_line.append(pos[line[0]][1])
            y_line.append(pos[line[1]][1])
            # 开始画线
            ax.plot(x_line, y_line, 'white', linewidth=0.1)
            x_line = []
            y_line = []

        ax.set_xlabel('X', color="white")
        ax.set_ylabel('Y', color="white")
        ax.grid(b=False)  # 去除栅栏

        ax.set_title("Force 2D", size=20, color="white")
        ax.set_facecolor('black')
        plt.axis('off')

        save_path = "../000LocalData/BGPlay/" + graph_name + ".png"
        plt.savefig(save_path, dpi=200, facecolor='black')
        if is_show:  # 判断是否需要show
            fig.set_facecolor('black')
            plt.show()
        plt.close()
        print("=>绘图结束- - - - - - - - - - - - - ")


def my_layout_ani():
    """
    根据ANIMATION_LIST的面的数据绘制2D 网络动态布局的animation
    :return:
    """
    data_draw = ANIMATION_LIST
    # 设置画布
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    def init():
        """
        初始化画布
        :return:
        """
        ax.set_title("Force 2D", size=20, color="white")
        ax.set_facecolor('black')
        ax.grid(b=False)  # 去除栅栏
        plt.axis('off')

    def update(i):
        """
        更新函数
        :return:
        """
        ax.clear()
        ax.set_title("Force 2D", size=20, color="white")
        ax.set_facecolor('black')
        ax.grid(b=False)  # 去除栅栏
        plt.axis('off')

        print("i=", i)
        G_2d = data_draw[i][0]
        pos = data_draw[i][1]
        # 2D绘点
        for node_key in pos.keys():
            xs = pos[node_key][0]
            ys = pos[node_key][1]
            ax.scatter(xs, ys, c='white', marker='o', s=10)
        # 3D绘线
        x_line = []
        y_line = []
        for line in G_2d.edges():
            # 添加node1, node2的x轴
            x_line.append(pos[line[0]][0])
            x_line.append(pos[line[1]][0])
            # 添加node1, node2的y轴
            y_line.append(pos[line[0]][1])
            y_line.append(pos[line[1]][1])
            # 开始画线
            ax.plot(x_line, y_line, 'white', linewidth=0.1)
            x_line = []
            y_line = []

    line_ani = animation.FuncAnimation(fig, update, init_func=init, frames=100, interval=50, blit=False)
    line_ani.save('../000LocalData/BGPlay/new_draw_2d_layout_ani.gif', writer="imagemagick",
                  savefig_kwargs={'facecolor': 'black'}, dpi=100)
    # line_ani.save('../000LocalData/BGPlay/new_draw_2d_layout_ani.mp4', writer="ffmpeg",
    #               savefig_kwargs={'facecolor': 'black'}, dpi=360)
    # plt.show()


if __name__ == "__main__":
    time_start = time.time()
    # 使用networkx随机生成无标度网络
    G = networkx.random_geometric_graph(1000, 0.01, dim=2)
    print("=>原始图信息输出")
    print("G Nodes:", G.nodes)
    print("G Nodes Count:", G.number_of_nodes())
    print("G Edges Count:", G.number_of_edges())
    pos = {i: (random.random(), random.random()) for i in G.nodes()}  # 生成一个具有位置信息的字典
    # print(pos)
    draw_2d(G, pos, 'new_draw_2d', is_show=False)  # 绘制随时生成的原始布局

    # 记录起始数据
    temp_list = list()
    temp_list.append(G)
    temp_list.append(pos)
    ANIMATION_LIST.append(temp_list)

    time_layout_start = time.time()
    layout_2d = aslay_networkx_layout(G, pos, niter=100)  # 2d版的aslay算法
    time_layout_end = time.time()
    print("G layout time consuming:", (time_layout_end - time_layout_start), "S")
    draw_2d(G, layout_2d, "new_draw_2d_layout", is_show=False)
    # my_layout_ani()  # 绘制2D网络动态布局的animation动画
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
