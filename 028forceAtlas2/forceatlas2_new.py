# coding:utf-8
"""
create on Feb 24, 2020 By Wenyan YU

Function:

注释forceAtlas2算法(https://bazaar.launchpad.net/~mwshinn/forceatlas2-python/trunk/files/head:/forceatlas2)
并在此基础上形成3D版的网络布局算法
NOTES: Currently, this only works for unweighted, undirected graphs. //仅适用于未加权的无向图
Copyright 2016 Max Shinn <mws41@cam.ac.uk>
Gephi版：https://github.com/gephi/gephi/blob/master/modules/LayoutPlugin/src/main/java/org/gephi/layout/plugin/forceAtlas2/ForceAtlas2.java

新版本：需要调通forceAtlas2算法，并能够在此基础上做相应的改进和推广

"""
from math import sqrt
import numpy
import random
import matplotlib.pyplot as plt
import networkx


# 定义点的数据结构
class Node:
    def __init__(self):
        self.mass = 0  # 点的质量
        self.old_dx = 0  # 点的原x坐标
        self.old_dy = 0  # 点的原y坐标
        self.dx = 0
        self.dy = 0
        self.x = 0
        self.y = 0


# 定义边的数据结构
class Edge:
    def __init__(self):
        self.node1 = -1
        self.node2 = -1
        self.weight = 0


# 计算两点间斥力
def linRepulsion(n1, n2, coefficient=0):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    distance2 = xDist * xDist + yDist * yDist   # 计算两点间距离的平方

    if distance2 > 0:
        factor = coefficient * n1.mass * n2.mass / distance2  # 计算斥力因子
        """
        根据斥力因子计算两点新的位置坐标（x1, y1）、(x2, y2)
        """
        n1.dx += xDist * factor
        n1.dy += yDist * factor
        n2.dx -= xDist * factor
        n2.dy -= yDist * factor


# 计算重力
def linGravity(n, g, coefficient=0):
    xDist = n.x
    yDist = n.y
    distance = sqrt(xDist * xDist + yDist * yDist)  # 计算点离圆心的距离

    if distance > 0:
        factor = coefficient * n.mass * g / distance  # 计算重力因子
        """
        根据重力因子更新点的坐标(x, y)
        """
        n.dx -= xDist * factor
        n.dy -= yDist * factor


# 计算强重力
def strongGravity(n, g, coefficient=0):
    xDist = n.x
    yDist = n.y

    if xDist != 0 and yDist != 0:
        factor = coefficient * n.mass * g  # 计算强重力因子，重力的大小不随点离圆心距离的变大而变小
        """
        根据强重力因子更新点的坐标(x, y)
        """
        n.dx -= xDist * factor
        n.dy -= yDist * factor


# 计算两点间的引力
def linAttraction(n1, n2, e, coefficient=0):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    factor = -coefficient * e  # 计算引力因子(负号，表示向对方方向移动)
    """
    根据引力因子更新两点的坐标(x1, y1)、(x2, y2)
    """
    n1.dx += xDist * factor
    n1.dy += yDist * factor
    n2.dx -= xDist * factor
    n2.dy -= yDist * factor


# 斥力迭代
def apply_repulsion(nodes, coefficient):
    for i in range(0, len(nodes)):
        for j in range(0, i):
            linRepulsion(nodes[i], nodes[j], coefficient)


# 重力迭代
def apply_gravity(nodes, gravity, scalingRatio, useStrongGravity=False):
    if not useStrongGravity:
        for i in range(0, len(nodes)):
            linGravity(nodes[i], gravity / scalingRatio, scalingRatio)
    else:
        for i in range(0, len(nodes)):
            strongGravity(nodes[i], gravity / scalingRatio, scalingRatio)


# 引力迭代
def apply_attraction(nodes, edges, coefficient, edgeWeightInfluence):
    # Optimization, since usually edgeWeightInfluence is 0 or 1, and pow is slow
    if edgeWeightInfluence == 0:
        for edge in edges:
            linAttraction(nodes[edge.node1], nodes[edge.node2], 1, coefficient)
    elif edgeWeightInfluence == 1:
        for edge in edges:
            linAttraction(nodes[edge.node1], nodes[edge.node2], edge.weight, coefficient)
    else:
        for edge in edges:
            linAttraction(nodes[edge.node1], nodes[edge.node2], pow(edge.weight, edgeWeightInfluence), coefficient)


# forceatlas2算法主体部分
def forceatlas2(
                G,  # 一个由2D numpy ndarrary格式化的图
                pos=None,  # 初始化位置的数组
                niter=100,  # 主体程序循环迭代的次数niter

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
                gravity=1.0
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
    for _i in range(0, niter):
        for n in nodes:
            n.old_dx = n.dx
            n.old_dy = n.dy
            n.dx = 0
            n.dy = 0
    
        # Barnes Hut优化步骤
        if outboundAttractionDistribution:
            outboundAttCompensation = numpy.mean([n.mass for n in nodes])

        apply_repulsion(nodes, scalingRatio)  # 斥力作用
        apply_gravity(nodes, gravity, scalingRatio, useStrongGravity=strongGravityMode)  # 重力作用
        apply_attraction(nodes, edges, 1.0, edgeWeightInfluence)  # 引力作用

        # 自动调整速度
        totalSwinging = 0.0  # 有多少不规则的运动
        totalEffectiveTraction = 0.0  # 有多少有效的运动
        for n in nodes:
            swinging = sqrt((n.old_dx - n.dx)*(n.old_dx - n.dx) + (n.old_dy - n.dy)*(n.old_dy - n.dy))
            totalSwinging += n.mass * swinging
            totalEffectiveTraction += .5 * n.mass * sqrt((n.old_dx + n.dx)*(n.old_dx + n.dx) + (n.old_dy + n.dy)*(n.old_dy + n.dy))

        # 优化抖动的限度（大网大抖动，小网小抖动，经验值）
        estimatedOptimalJitterTolerance = .05 * sqrt(len(nodes))
        minJT = sqrt(estimatedOptimalJitterTolerance)
        maxJT = 10
        jt = jitterTolerance * max(minJT, min(maxJT, estimatedOptimalJitterTolerance * totalEffectiveTraction / (len(nodes)*len(nodes))))
        
        minSpeedEfficiency = 0.05

        # 防止不稳定的行为
        if totalSwinging/totalEffectiveTraction > 2.0:
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
        for n in nodes:
            swinging = n.mass * sqrt((n.old_dx - n.dx)*(n.old_dx - n.dx) + (n.old_dy - n.dy)*(n.old_dy - n.dy))
            factor = speed / (1.0 + sqrt(speed * swinging))
            n.x = n.x + (n.dx * factor)
            n.y = n.y + (n.dy * factor)
    return [(n.x, n.y) for n in nodes]


def forceatlas2_networkx_layout(G, pos=None, **kwargs):
    assert isinstance(G, networkx.classes.graph.Graph), "Not a networkx graph"
    assert isinstance(pos, dict) or (pos is None), "pos must be specified as a dictionary, as in networkx"
    M = numpy.asarray(networkx.to_numpy_matrix(G))
    if pos is None:
        l = forceatlas2(M, pos=None, **kwargs)
    else:
        poslist = numpy.asarray([pos[i] for i in G.nodes()])
        l = forceatlas2(M, pos=poslist, **kwargs)
    return dict(zip(G.nodes(), l))


if __name__ == "__main__":
    plt.figure(figsize=(12, 8))
    # G = networkx.karate_club_graph()
    G = networkx.random_geometric_graph(300, 0.125)
    print("G Nodes:", G.nodes)
    print("G Nodes Count:", G.number_of_nodes())
    print("G Edges Count:", G.number_of_edges())
    pos = {i: (random.random(), random.random()) for i in G.nodes()}  # 生成一个具有位置信息的字典
    # print(pos)
    networkx.draw_networkx(G, pos, node_size=10, width=0.05, with_labels=False)  # 绘制随机生成的聚类原图
    plt.savefig("../000LocalData/networkx_graph/0_forceatlas2.png", dpi=600)
    plt.close()

    plt.figure(figsize=(12, 8))
    l = forceatlas2_networkx_layout(G, pos, niter=300)  # 采用自己编写的布局算法
    networkx.draw_networkx(G, l, node_size=10, width=0.05, with_labels=False)
    plt.savefig("../000LocalData/networkx_graph/1_forceatlas2.png", dpi=600)
    plt.close()

    plt.figure(figsize=(12, 8))
    networkx.draw_networkx(G, pos=networkx.spring_layout(G), node_size=10, width=0.05, with_labels=False)  # 绘制随机生成的聚类原图-采用networkx自带布局算法（spring）
    plt.savefig("../000LocalData/networkx_graph/2_forceatlas2.png", dpi=600)
    plt.close()
