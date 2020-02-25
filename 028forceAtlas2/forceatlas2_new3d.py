# coding:utf-8
"""
create on Feb 24, 2020 By Wenyan YU

Function:

注释forceAtlas2算法(https://bazaar.launchpad.net/~mwshinn/forceatlas2-python/trunk/files/head:/forceatlas2)
并在此基础上形成3D版的网络布局算法
NOTES: Currently, this only works for unweighted, undirected graphs. //仅适用于未加权的无向图
Copyright 2016 Max Shinn <mws41@cam.ac.uk>
Gephi版：https://github.com/gephi/gephi/blob/master/modules/LayoutPlugin/src/main/java/org/gephi/layout/plugin/forceAtlas2/ForceAtlas2.java

新版本1：需要调通forceAtlas2算法，并能够在此基础上做相应的改进和推广
新版本2：在forceAtlas2算法的基础上，开始向三维推广forceAtlas3d


"""
from math import sqrt
import numpy
import random
import matplotlib.pyplot as plt
import networkx
from mpl_toolkits.mplot3d import Axes3D


# 定义点的数据结构(3D比2D多了z轴的维度)
class Node:
    def __init__(self):
        self.mass = 0  # 点的质量
        self.old_dx = 0  # 点的原x坐标
        self.old_dy = 0  # 点的原y坐标
        self.old_dz = 0  # 点的原z坐标
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.x = 0
        self.y = 0
        self.z = 0


# 定义边的数据结构(3D与2D相一致)
class Edge:
    def __init__(self):
        self.node1 = -1
        self.node2 = -1
        self.weight = 0


# 计算两点间斥力（3D）
def linRepulsion(n1, n2, coefficient=0):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    zDist = n1.z - n2.z
    distance2 = xDist * xDist + yDist * yDist + zDist * zDist  # 计算两点间距离的平方

    if distance2 > 0:
        factor = coefficient * n1.mass * n2.mass / distance2  # 计算斥力因子
        """
        根据斥力因子计算两点新的位置坐标（x1, y1, z1）、(x2, y2, z1)
        """
        n1.dx += xDist * factor
        n1.dy += yDist * factor
        n1.dz += zDist * factor

        n2.dx -= xDist * factor
        n2.dy -= yDist * factor
        n2.dz -= zDist * factor


# 计算重力(3D)
def linGravity(n, g, coefficient=0):
    xDist = n.x
    yDist = n.y
    zDist = n.z
    distance = sqrt(xDist * xDist + yDist * yDist + zDist * zDist)  # 计算点离圆心的距离

    if distance > 0:
        factor = coefficient * n.mass * g / distance  # 计算重力因子
        """
        根据重力因子更新点的坐标(x, y, z)
        """
        n.dx -= xDist * factor
        n.dy -= yDist * factor
        n.dz -= zDist * factor


# 计算强重力(3D)
def strongGravity(n, g, coefficient=0):
    xDist = n.x
    yDist = n.y
    zDist = n.z

    if xDist != 0 and yDist != 0 and zDist !=0:
        factor = coefficient * n.mass * g  # 计算强重力因子，重力的大小不随点离圆心距离的变大而变小
        """
        根据强重力因子更新点的坐标(x, y, z)
        """
        n.dx -= xDist * factor
        n.dy -= yDist * factor
        n.dz -= zDist * factor


# 计算两点间的引力(3D)
def linAttraction(n1, n2, e, coefficient=0):
    xDist = n1.x - n2.x
    yDist = n1.y - n2.y
    zDist = n1.z - n2.z
    factor = -coefficient * e  # 计算引力因子(负号，表示向对方方向移动)
    """
    根据引力因子更新两点的坐标(x1, y1, z1)、(x2, y2, z2)
    """
    n1.dx += xDist * factor
    n1.dy += yDist * factor
    n1.dz += zDist * factor

    n2.dx -= xDist * factor
    n2.dy -= yDist * factor
    n2.dz -= zDist * factor


# 斥力迭代(3D)
def apply_repulsion(nodes, coefficient):
    for i in range(0, len(nodes)):
        for j in range(0, i):
            linRepulsion(nodes[i], nodes[j], coefficient)


# 重力迭代（3D）
def apply_gravity(nodes, gravity, scalingRatio, useStrongGravity=False):
    if not useStrongGravity:
        for i in range(0, len(nodes)):
            linGravity(nodes[i], gravity / scalingRatio, scalingRatio)
    else:
        for i in range(0, len(nodes)):
            strongGravity(nodes[i], gravity / scalingRatio, scalingRatio)


# 引力迭代（3D）
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


# forceatlas3d算法主体部分（3D）
def forceatlas3d(
                G,  # 一个由3D numpy ndarrary格式化的图
                pos=None,  # 初始化位置的数组
                niter=10,  # 主体程序循环迭代的次数niter

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

    # forceAtlas3d布局算法的初始化
    speed = 1 
    speedEfficiency = 1

    # 初始化点的数据结构(3D)
    nodes = []
    for i in range(0, G.shape[0]):
        n = Node()
        n.mass = 1 + numpy.sum(G[i])  # 计算点的度作为质量mass
        n.old_dx = 0
        n.old_dy = 0
        n.old_dz = 0
        n.dx = 0
        n.dy = 0
        n.dz = 0

        if pos is None:  # 如果位置信息为空，则自行初始化各点的初始位置
            n.x = random.random()
            n.y = random.random()
            n.z = random.random()
        else:
            n.x = pos[i][0]
            n.y = pos[i][1]
            n.z = pos[i][2]
        nodes.append(n)

    # 初始化边的数据结构(3D)
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

    # 主循环开始(3D)
    iter_cnt = 1
    for _i in range(0, niter):
        print("iter_cnt:,", iter_cnt)
        for n in nodes:
            n.old_dx = n.dx
            n.old_dy = n.dy
            n.old_dz = n.dz

            n.dx = 0
            n.dy = 0
            n.dz = 0
    
        # # Barnes Hut优化步骤
        # if outboundAttractionDistribution:
        #     outboundAttCompensation = numpy.mean([n.mass for n in nodes])

        apply_repulsion(nodes, scalingRatio)  # 斥力作用
        apply_gravity(nodes, gravity, scalingRatio, useStrongGravity=strongGravityMode)  # 重力作用
        apply_attraction(nodes, edges, 1.0, edgeWeightInfluence)  # 引力作用

        # 自动调整速度(3D)
        totalSwinging = 0.0  # 有多少不规则的运动
        totalEffectiveTraction = 0.0  # 有多少有效的运动
        for n in nodes:
            swinging = sqrt((n.old_dx - n.dx)*(n.old_dx - n.dx) + (n.old_dy - n.dy)*(n.old_dy - n.dy) + (n.old_dz - n.dz) * (n.old_dz - n.dz))
            totalSwinging += n.mass * swinging
            totalEffectiveTraction += .5 * n.mass * sqrt((n.old_dx + n.dx)*(n.old_dx + n.dx) + (n.old_dy + n.dy)*(n.old_dy + n.dy) + (n.old_dz + n.dz)*(n.old_dz+n.dz))

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

        # 更新位置(3D)
        factor_list = []
        for n in nodes:
            swinging = n.mass * sqrt((n.old_dx - n.dx)*(n.old_dx - n.dx) + (n.old_dy - n.dy)*(n.old_dy - n.dy) + (n.old_dz - n.dz)*(n.old_dz - n.dz))
            factor = speed / (1.0 + sqrt(speed * swinging))
            factor_list.append(factor)
            n.x = n.x + (n.dx * factor)
            n.y = n.y + (n.dy * factor)
            n.z = n.z + (n.dz * factor)

        """
        每隔draw_gap次迭代绘图一次
        """
        if iter_cnt % draw_gap == 0:
            layout_3d_save_name = "draw_3d_layout_" + str(iter_cnt)
            print(layout_3d_save_name)
            layout_3d_pos = dict(zip(draw_graph.nodes(), [(n.x, n.y, n.z) for n in nodes]))
            draw_3d(draw_graph, layout_3d_pos, layout_3d_save_name)
            """
            根据各个点的平均速度，判断是否需要停止迭代
            """
            print("Average speed factor:", numpy.average(factor_list))

        iter_cnt += 1  # 迭代次数自增1

    return [(n.x, n.y, n.z) for n in nodes]


# forceAtlas3d基于networkx内容布局
def forceatlas3d_networkx_layout(G, pos=None, **kwargs):
    draw_gap = 10  # 迭代绘图间隔,总共绘约五张图
    assert isinstance(G, networkx.classes.graph.Graph), "Not a networkx graph"
    assert isinstance(pos, dict) or (pos is None), "pos must be specified as a dictionary, as in networkx"
    M = numpy.asarray(networkx.to_numpy_matrix(G))
    if pos is None:
        layout_3d = forceatlas3d(M, pos=None, draw_graph=G, draw_gap=draw_gap, **kwargs)
    else:
        poslist = numpy.asarray([pos[i] for i in G.nodes()])
        layout_3d = forceatlas3d(M, pos=poslist,  draw_graph=G, draw_gap=draw_gap, **kwargs)
    return dict(zip(G.nodes(), layout_3d))


def draw_3d(G_3d, pos, graph_name):
    """
    根据传入的3D网络图绘制3d Graph
    :param G_3d:
    :return:
    """
    # pos = networkx.get_node_attributes(G, 'pos')  # 获取图中点的坐标
    # print("All Nodes:", G.nodes())
    print("All Nodes Count:", G.number_of_nodes())
    # print("All Edges:", G.edges())
    print("All Edges Count:", G.number_of_edges())
    fig = plt.figure(figsize=(10, 8))
    ax = Axes3D(fig)
    # 3D绘点
    for node_key in pos.keys():
        xs = pos[node_key][0]
        ys = pos[node_key][1]
        zs = pos[node_key][2]
        ax.scatter(xs, ys, zs, c='r', marker='o', s=10)
    # 3D绘线
    x_line = []
    y_line = []
    z_line = []
    for line in G_3d.edges():
        # 添加node1, node2的x轴
        x_line.append(pos[line[0]][0])
        x_line.append(pos[line[1]][0])
        # 添加node1, node2的y轴
        y_line.append(pos[line[0]][1])
        y_line.append(pos[line[1]][1])
        # 添加node1, node2的z轴
        z_line.append(pos[line[0]][2])
        z_line.append(pos[line[1]][2])
        # 开始画线
        ax.plot3D(x_line, y_line, z_line, 'b', linewidth=0.1)
        x_line = []
        y_line = []
        z_line = []

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    save_path = "../000LocalData/networkx_graph/" + graph_name + ".png"
    plt.savefig(save_path, dpi=200)
    # plt.show()
    plt.close()


if __name__ == "__main__":
    G = networkx.random_geometric_graph(500, 0.2, dim=3)
    # pos= networkx.get_node_attributes(G, 'pos')  # 获取图中点的坐标
    pos = {i: (random.random(), random.random(), random.random()) for i in G.nodes()}  # 生成一个具有位置信息的字典
    # print(pos)
    draw_3d(G, pos, "draw_3d")
    layout_3d = forceatlas3d_networkx_layout(G, pos, niter=50)  # 采用自己编写的3D布局算法
    # print(layout_3d)
    draw_3d(G, layout_3d, "draw_3d_layout")
