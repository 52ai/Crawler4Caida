# coding:utf-8
"""
create on Feb 25, 2020 By Wenyan YU

Function:

学习图论与复杂网络建模工具包networkx
networkx是一个用Python语言开发的图论与复杂网络建模工具，内置常用的图与复杂网络分析算法
可以方便的进行复杂网路数据分析、仿真建模等工作

一、支持四种图

Graph:无多重边无向图
DiGraph:无多重边有向图
MultiGraph:有多重边无向图
MultiDiGraph:有多重边有向图

二、绘制网络图的基本步骤

1）导入networkx, matplotlib包
2）建立网络
3）绘制网络nx.draw()
4)建立布局 pos=nx.spring_layout美化作用

"""

import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def random_geometric_graph():
    """
    绘制随机几何图
    :return:
    """
    G = nx.random_geometric_graph(200, 0.125)  # 生成一个随机几何图
    pos = nx.get_node_attributes(G, 'pos')  # 获取图中点的坐标
    # print(pos)

    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5)**2 + (y - 0.5)**2
        if d < dmin:
            ncenter = n
            dmin = d
    p = dict(nx.single_source_shortest_path_length(G, ncenter))
    plt.figure(figsize=(12, 8))
    nx.draw_networkx_edges(G, pos, nodelist=[ncenter], alpha=0.4)
    nx.draw_networkx_nodes(G, pos, nodelist=list(p.keys()),
                           node_size=80,
                           node_color=list(p.values()),
                           cmap=plt.cm.Blues_r)
    plt.xlim(-0.05, 1.05)
    plt.ylim(-0.05, 1.05)
    plt.savefig("../000LocalData/networkx_graph/random_geometric_graph_blue.png", dpi=200)


def random_geometric_graph_3d():
    """
    绘制3D随机几何图
    :return:
    """
    G = nx.random_geometric_graph(100, 0.125, dim=3)  # 生成一个随机几何图
    pos = nx.get_node_attributes(G, 'pos')  # 获取图中点的坐标
    print("All Nodes:", G.nodes())
    print("All Nodes Count:", G.number_of_nodes())
    print("All Edges Count:", G.number_of_edges())
    # print(pos)
    # nx.draw_networkx_nodes(G, pos)
    # plt.savefig("../000LocalData/networkx_graph/random_geometric_graph_blue_3d.png", dpi=200)
    # plt.show()
    fig = plt.figure(figsize=(10, 8))
    # ax = fig.add_subplot(111, projection='3d')
    ax = Axes3D(fig)
    for node_key in pos.keys():
        xs = pos[node_key][0]
        ys = pos[node_key][1]
        zs = pos[node_key][2]
        ax.scatter(xs, ys, zs, c='r', marker='o', s=20)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.savefig("../000LocalData/networkx_graph/random_geometric_graph_blue_3d.png", dpi=200)
    plt.show()


def spring_layout_color():
    """
    绘制颜色渐变的放射性状图
    :return:
    """
    plt.figure(figsize=(12, 8))
    G = nx.star_graph(50)
    pos = nx.spring_layout(G)  # 布局为中心放射状
    colors = range(50)
    nx.draw(G, pos, node_color="#A0CBE2", edge_color=colors, width=4, edge_cmap=plt.cm.Blues, with_labels=False)
    plt.savefig("../000LocalData/networkx_graph/spring_layout_color.png", dpi=200)


if __name__ == "__main__":
    # G = nx.random_graphs.barabasi_albert_graph(1000, 1)  # 生产一个BA无标度网络G
    # nx.draw_spring(G)  # 绘制网络G
    G = nx.Graph()  # 建立一个空的无向图G
    # 增加节点
    G.add_node("a")  # 添加一个节点1
    G.add_nodes_from(['b', 'c', 'd', 'e'])  # 加点集合
    G.add_cycle(['f', 'g', 'h', 'j'])  # 加环
    H = nx.path_graph(10)  # 返回有10个节点的无向图
    # G.add_nodes_from(H)  # 创建一个子图H加入G
    # G.add_node(H)  # 直接将图H作为节点
    plt.figure(figsize=(12, 8))
    nx.draw(G, with_labels=True, node_color='red', node_size=100)
    # print("All Nodes:", G.nodes())
    # print("All Nodes Count:", G.number_of_nodes())
    # print("All Edges Count:", G.number_of_edges())
    plt.savefig("../000LocalData/networkx_graph/graph_test.png", dpi=200)
    plt.close()
    # plt.show()
    # random_geometric_graph()
    random_geometric_graph_3d()
    # spring_layout_color()





