# coding:utf-8
"""
create on Mar 13, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com
Function:

最近在搞OPNET网络仿真的实验，想着利用基于networkx包，Python其实在网络仿真方面也能做点事，尤其是网络拓扑方面
其实通信网，撇开网络协议不谈，就是一张由节点和连边的加权有向图

节点代表AS
连边代表互联关系，互联边的权重代表带宽（流量）
如果路径上还有加权的时延，则可通过路径大小，计算出时延性能参数

以上，只是Python程序建模的一个初步猜想

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import networkx as nx
import random

fig, ax = plt.subplots()

G = nx.Graph()
G.add_edge(0, 1)


def init_network():
    # nx.draw(G, node_size=10, node_color='c')
    return G,


def animate_network(i):
    # 定义网络动态变化的几种形式，分别代表删除边，删除节点，维持不动，增加节点，增加边
    d = [-2, -1, 0, 1, 2]
    # 从中随机选择一种操作
    c = random.randint(0, len(d) - 1)

    edges = list(G.edges())
    nodes = list(G.nodes())
    if d[c] == -2:
        if edges:
            u, v = random.choice(edges)
            G.remove_edge(u, v)
    if d[c] == -1:
        if nodes:
            node = random.choice(nodes)
            G.remove_node(node)
    if d[c] == 0:
        # 网络不发生变化
        pass
    if d[c] == 1:
        G.add_node(len(nodes))
    if d[c] == 2:
        if nodes:
            G.add_edge(len(nodes), random.choice(nodes))

    nx.draw(G, pos=nx.spring_layout(G), node_size=10, node_color='c', edge_color='grey')
    return G,


ani = animation.FuncAnimation(fig=fig, func=animate_network, frames=30, init_func=init_network, interval=100, blit=False, )
ani.save('../000LocalData/networkx_graph/basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()
