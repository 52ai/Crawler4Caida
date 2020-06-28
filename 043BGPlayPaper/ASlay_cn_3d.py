# coding:utf-8
"""
create on  June 28, 2020 By Wayne YU

Function:

自研AS布局算法ASlay需要针对AS网络互联的特点进行相应的布局研究
该程序是希望借助中国AS互联真实数据开展布局


常规版的ASlay 2D算法已初步完成，接下来分两步走
第一步，完成ASlay 3D常规版本
第二步，完成ASlay 2D/3D不重叠版本网络布局，并结合已制定的地图基础课题第二篇输出框架开展相关实验

基于以上实验结果，最终实现地图基础课题第二篇论文的撰写

"""
import time
from math import sqrt
import numpy
import random
import matplotlib.pyplot as plt
import networkx
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import csv


ANIMATION_LIST = []  # 存储过程数据


# 定义节点的数据结构（3D比2D多了z轴的维度）
class Node:
    def __init__(self):
        self.mass = 0  # 点的质量
        self.old_dx = 0  # 点的原x坐标位移量
        self.old_dy = 0  # 点的原y坐标位移量
        self.old_dz = 0  # 点的原z坐标位移量
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.x = 0
        self.y = 0
        self.z = 0


# 定义连边的数据结构(3D与2D相一致)
class Edge:
    def __init__(self):
        self.node1 = -1  # 边的起始节点
        self.node2 = -1  # 边的目的节点
        self.weight = 0  # 边的权重


# 两点间引力计算模型（3D）
def compute_attraction(n1, n2, e, coefficient=0):
    x_dist = n1.x - n2.x
    y_dist = n1.y - n2.y
    z_dist = n1.z - n2.z
    factor = -coefficient * e  # 计算引力因子(负号，表示向对方方向移动)
    """
    根据引力因子更新两点的坐标(x1, y1, z1)、(x2, y2, z2)
    """
    n1.dx += x_dist * factor
    n1.dy += y_dist * factor
    n1.dz += z_dist * factor

    n2.dx -= x_dist * factor
    n2.dy -= y_dist * factor
    n2.dz -= z_dist * factor


# 两点间斥力计算模型(3D)
def compute_repulsion(n1, n2, coefficient=0):
    x_dist = n1.x - n2.x
    y_dist = n1.y - n2.y
    z_dist = n1.z - n2.z
    distance2 = x_dist * x_dist + y_dist * y_dist + z_dist * z_dist  # 计算两点间距离的平方

    if distance2 > 0:
        factor = coefficient * n1.mass * n2.mass / distance2  # 计算斥力因子（表示斥力的大小）
        """
        根据斥力因子计算两点新的位置坐标（x1, y1, z1）、(x2, y2, z2)
        """
        n1.dx += x_dist * factor
        n1.dy += y_dist * factor
        n1.dz += z_dist * factor

        n2.dx -= x_dist * factor
        n2.dy -= y_dist * factor
        n2.dz -= z_dist * factor


"""
空间中的强重力和普通重力的公式，还需要进一步确认
方案一：普通重力，不仅与节点的质量有关系，还与其离圆心的距离里成反比。
方案二：强重力，强重力只与节点的质量有关。

当前算法采用的是方案二
具体选择何种方案，还需要看实际的可视化效果
"""


# 空间点重力计算模型（3D）
def compute_gravity(n, g, coefficient=0):
    x_dist = n.x
    y_dist = n.y
    z_dist = n.z
    distance = sqrt(x_dist * x_dist + y_dist * y_dist + z_dist * z_dist)  # 计算点离圆心的距离

    if distance > 0:
        factor = coefficient * n.mass * g / distance  # 计算重力因子
        """
        根据重力因子更新点的坐标(x, y, z)
        """
        n.dx -= x_dist * factor
        n.dy -= y_dist * factor
        n.dz -= z_dist * factor


# 空间强重力计算模型(3D)
def compute_strong_gravity(n, g, coefficient=0):
    x_dist = n.x
    y_dist = n.y
    z_dist = n.z

    if x_dist != 0 and y_dist != 0 and z_dist != 0:
        factor = coefficient * n.mass * g  # 计算强重力因子，重力的大小不随点离圆心距离的变大而变小
        """
        根据强重力因子更新点的坐标(x, y, z)
        """
        n.dx -= x_dist * factor
        n.dy -= y_dist * factor
        n.dz -= z_dist * factor


# 引力迭代(3D)
def apply_attraction(nodes, edges, coefficient, edge_influence):
    # 通常edge_weight_influence为0或者1，pow为折中方案
    if edge_influence == 0:
        for edge in edges:
            compute_attraction(nodes[edge.node1], nodes[edge.node2], 1, coefficient)
    elif edge_influence == 1:
        for edge in edges:
            compute_attraction(nodes[edge.node1], nodes[edge.node2], edge.weight, coefficient)
    else:
        for edge in edges:
            compute_attraction(nodes[edge.node1], nodes[edge.node2], pow(edge.weight, edge_influence), coefficient)


# 斥力迭代(3D)
def apply_repulsion(nodes, coefficient):
    for i in range(0, len(nodes)):
        for j in range(0, i):
            compute_repulsion(nodes[i], nodes[j], coefficient)


# 重力迭代(3D)
def apply_gravity(nodes, gravity, scaling_ratio, use_strong_gravity=False):
    if not use_strong_gravity:
        for i in range(0, len(nodes)):
            compute_gravity(nodes[i], gravity / scaling_ratio, scaling_ratio)
    else:
        for i in range(0, len(nodes)):
            compute_strong_gravity(nodes[i], gravity / scaling_ratio, scaling_ratio)


# ASlay算法主体部分(3D)
def aslay(
        G,  # 一个由2D numpy ndarrary格式化的图
        pos=None,  # 初始化位置的数组
        niter=50,  # 主体程序循环迭代的次数niter

        # 可选参数
        outbound_attraction_distribution=False,  # 集线器阻碍机制（高出度和高入度的区分）
        lin_log_mode=False,  # 处理度为0的节点，Fa(n1,n2)=log(1+d(n1,n2))
        adjust_sizes=False,  # 防止节点重叠
        edge_weight_influence=0,  # 处理带权边，是否影响引力，0代表不影响，1代表影响，pow代表轻微影响

        # 布局速度
        jitter_tolerance=1.0,  # 容忍度，容忍度越大，步子越大，速度越快，精确度越小
        barneshut_optimize=False,  # 采用Barnes-Hut算法优化布局速率 NOT IMPLEMENTED
        barneshut_theta=1.2,  # Barnes-Hut优化算法参数选择 NOT IMPLEMENTED

        # 布局效果
        scaling_ratio=2.0,  # 重力因素缩放，越大，网络布局越向四周扩散
        strong_gravity_mode=False,  # 强重力模式
        gravity=1.0,  # 重力大小

        # 附加参数
        draw_graph=None,  # 阶段性输出图绘制
        draw_gap=10,  # 每隔多少次迭代绘制一次图

):
    # 参数检验
    assert isinstance(G, numpy.ndarray), "G is not a numpy ndarray"
    assert G.shape == (G.shape[0], G.shape[0]), "G is not 2D square"
    assert numpy.all(G.T == G), "G is not symmetric.  Currently only undirected graphs are supported"  # 目前支持无向图
    assert isinstance(pos, numpy.ndarray) or (pos is None), "Invalid node positions"
    assert outbound_attraction_distribution == lin_log_mode == adjust_sizes == barneshut_optimize == False, "You selected a feature that has not been implemented yet..."

    # ASlay布局算法的初始化
    speed = 1  # 输出速度
    speed_efficiency = 1  # 速度效率

    # 初始化点的数据结构
    nodes = []
    for i in range(0, G.shape[0]):
        n = Node()
        n.mass = 1 + numpy.sum(G[i])  # 用degree(ni) + 1代表点的质量
        # 设置点的原节点位移量
        n.old_dx = 0
        n.old_dy = 0
        n.old_dz = 0
        # 设置点的位移量
        n.dx = 0
        n.dy = 0
        n.dz = 0
        if pos is None:
            # 如果位置信息为空，则自行初始化个点的初始位置
            n.x = random.random()
            n.y = random.random()
            n.z = random.random()
        else:
            n.x = pos[i][0]
            n.y = pos[i][1]
            n.z = pos[i][2]
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

    # 主循环开始(3D)
    iter_cnt = 1
    for _i in range(0, niter):
        iter_time_start = time.time()
        for n in nodes:
            # 保存当前节点坐标位移量
            n.old_dx = n.dx
            n.old_dy = n.dy
            n.old_dz = n.dz

            # 重置节点位移量为0
            n.dx = 0
            n.dy = 0
            n.dz = 0

        # Barnes Hut优化步骤
        # if outbound_attraction_distribution:
        #     outboundAttCompensation = numpy.mean([n.mass for n in nodes])

        apply_repulsion(nodes, scaling_ratio)  # 斥力作用
        apply_gravity(nodes, gravity, scaling_ratio, use_strong_gravity=strong_gravity_mode)  # 重力作用
        apply_attraction(nodes, edges, 1.0, edge_weight_influence)  # 引力作用

        # 自动调整速度（3D）
        """
        研究表明
        高连接的节点需要高振荡，以获取高准确性，收敛慢
        低连接的节点需要低振荡，准确性稍稍低些，收敛快
        """
        total_swinging = 0.0  # 有多少不规则的运动，统计总的抖动量
        total_effective_traction = 0.0  # 有多少有效的运动，统计总的有效牵引力量
        for n in nodes:
            # 振荡量swinging，即点前后位移量的欧氏距离
            swinging = sqrt((n.old_dx - n.dx) * (n.old_dx - n.dx) + (n.old_dy - n.dy) * (n.old_dy - n.dy) +
                            (n.old_dz - n.dz) * (n.old_dz - n.dz))
            # 总的抖动量等于每个点的质量*其前后位移量欧式距离之和
            total_swinging += n.mass * swinging
            # 总的有效牵引量等于(每个点的质量)*(前后两步有效位移距离/2)
            total_effective_traction += .5 * n.mass * sqrt(
                (n.old_dx + n.dx) * (n.old_dx + n.dx) + (n.old_dy + n.dy) * (n.old_dy + n.dy) +
                (n.old_dz + n.dz)*(n.old_dz+n.dz))

        # 优化抖动的限度（大网大抖动，小网小抖动，研究表明）
        estimated_optimal_jitter_tolerance = .05 * sqrt(len(nodes))
        min_jt = sqrt(estimated_optimal_jitter_tolerance)
        max_jt = 10
        jt = jitter_tolerance * max(min_jt, min(max_jt, estimated_optimal_jitter_tolerance * total_effective_traction /
                                                (len(nodes) * len(nodes))))

        min_speed_efficiency = 0.05

        # 防止不稳定的行为
        if total_swinging / total_effective_traction > 2.0:
            if speed_efficiency > min_speed_efficiency:
                speed_efficiency *= .5
            jt = max(jt, jitter_tolerance)

        target_speed = jt * speed_efficiency * total_effective_traction / total_swinging

        if total_swinging > jt * total_effective_traction:
            if speed_efficiency > min_speed_efficiency:
                speed_efficiency *= .7
        elif speed < 1000:
            speed_efficiency *= 1.3

        # 速度不能提升的太快，否则收敛的很慢
        max_rise = .5
        speed = speed + min(target_speed - speed, max_rise * speed)

        # 更新位置(3D)
        factor_list = []
        for n in nodes:
            swinging = n.mass * sqrt((n.old_dx - n.dx) * (n.old_dx - n.dx) + (n.old_dy - n.dy) * (n.old_dy - n.dy) +
                                     (n.old_dz - n.dz)*(n.old_dz - n.dz))
            factor = speed / (1.0 + sqrt(speed * swinging))
            factor_list.append(factor)
            n.x = n.x + (n.dx * factor)
            n.y = n.y + (n.dy * factor)
            n.z = n.z + (n.dz * factor)
        """
        每隔draw_gap次迭代绘图一次
        """
        if iter_cnt % draw_gap == 0:
            layout_3d_save_name = "new_draw_3d_layout_" + str(iter_cnt)
            # print(layout_3d_save_name)
            layout_3d_pos = dict(zip(draw_graph.nodes(), [(n.x, n.y, n.z) for n in nodes]))
            draw_3d(draw_graph, layout_3d_pos, layout_3d_save_name, is_draw=False)
            """
            根据各个点的平均速度，判断是否需要停止迭代
            """
            # print("Average speed factor:", numpy.average(factor_list))
        iter_cnt += 1  # 迭代次数自增1
        iter_time_end = time.time()
        print("STEP %s, Time Consuming:%s S" % (str(iter_cnt-1), (iter_time_end - iter_time_start)))

    return [(n.x, n.y, n.z) for n in nodes]


# ASlay 3d基于networkx内容布局
def aslay_networkx_layout(G, pos=None, **kwargs):
    draw_gap = 1  # 迭代绘图间隔
    assert isinstance(G, networkx.classes.graph.Graph), "Not a networkx graph"
    assert isinstance(pos, dict) or (pos is None), "pos must be specified as a dictionary, as in networkx"
    M = numpy.asarray(networkx.to_numpy_matrix(G))
    if pos is None:
        layout_3d = aslay(M, pos=None, draw_graph=G, draw_gap=draw_gap, **kwargs)
    else:
        poslist = numpy.asarray([pos[i] for i in G.nodes()])
        layout_3d = aslay(M, pos=poslist, draw_graph=G, draw_gap=draw_gap, **kwargs)
    return dict(zip(G.nodes(), layout_3d))


def draw_3d(G_3d, pos, graph_name, is_draw=True, is_show=False):
    """
    根据传入的3D网络图绘制3d Graph
    :param G_3d:
    :param pos:
    :param graph_name:
    :param is_draw:
    :param is_show:
    :return:
    """
    # 记录过程数据
    temp_list = list()
    temp_list.append(G_3d)
    temp_list.append(pos)
    ANIMATION_LIST.append(temp_list)

    if is_draw:
        print("=>开始绘图- - - - - - - - - - - - - ")
        print("Graph Nodes Count:", G_3d.number_of_nodes())
        print("Graph Edges Count:", G_3d.number_of_edges())
        fig = plt.figure(figsize=(10, 8))
        ax = Axes3D(fig)
        # 3D绘点
        for node_key in pos.keys():
            # 获取Graph Nodes的颜色恶属性
            # print(networkx.get_node_attributes(G_3d, 'color')[node_key])
            node_color = networkx.get_node_attributes(G_3d, 'color')[node_key]
            node_size = networkx.get_node_attributes(G_3d, 'size')[node_key]
            xs = pos[node_key][0]
            ys = pos[node_key][1]
            zs = pos[node_key][2]
            ax.scatter(xs, ys, zs, c=node_color, marker='o', s=node_size)
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
            ax.plot3D(x_line, y_line, z_line, 'white', linewidth=0.1)
            x_line = []
            y_line = []
            z_line = []

        ax.set_xlabel('X', color="white")
        ax.set_ylabel('Y', color="white")
        ax.set_zlabel('Z', color="white")
        ax.grid(b=False)  # 去除栅栏

        ax.set_title("ASlay 3D", size=20, color="white")
        ax.set_facecolor('black')
        plt.axis('off')

        save_path = "../000LocalData/BGPlay/" + graph_name + ".png"
        plt.savefig(save_path, dpi=200, facecolor='black')
        print("绘图成功:", save_path)
        if is_show:  # 判断是否需要show
            fig.set_facecolor('black')
            plt.show()
        plt.close()
        print("=>绘图结束- - - - - - - - - - - - - ")


def my_layout_ani():
    """
    根据ANIMATION_LIST的面的数据绘制3D 网络动态布局的animation
    :return:
    """
    data_draw = ANIMATION_LIST
    # 设置画布
    fig = plt.figure(figsize=(10, 8))
    ax = Axes3D(fig)

    def init():
        """
        初始化画布
        :return:
        """
        ax.set_title("ASlay 3D", size=20, color="white")
        ax.set_facecolor('black')
        ax.grid(b=False)  # 去除栅栏
        plt.axis('off')

    def update(i):
        """
        更新函数
        :return:
        """
        ax.clear()
        ax.set_title("ASlay 3D", size=20, color="white")
        ax.set_facecolor('black')
        ax.grid(b=False)  # 去除栅栏
        plt.axis('off')

        print("i=", i)
        G_3d = data_draw[i][0]
        pos = data_draw[i][1]
        # 3D绘点
        for node_key in pos.keys():
            # 获取Graph Nodes的颜色恶属性
            # print(networkx.get_node_attributes(G_3d, 'color')[node_key])
            node_color = networkx.get_node_attributes(G_3d, 'color')[node_key]
            node_size = networkx.get_node_attributes(G_3d, 'size')[node_key]
            xs = pos[node_key][0]
            ys = pos[node_key][1]
            zs = pos[node_key][2]
            ax.scatter(xs, ys, zs, c=node_color, marker='o', s=node_size)
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
            ax.plot3D(x_line, y_line, z_line, 'white', linewidth=0.1)
            x_line = []
            y_line = []
            z_line = []

    line_ani = animation.FuncAnimation(fig, update, init_func=init, frames=50, interval=50, blit=False)
    line_ani.save('../000LocalData/BGPlay/as_draw_3d_layout_ani.gif', writer="imagemagick",
                  savefig_kwargs={'facecolor': 'black'}, dpi=100)
    # line_ani.save('../000LocalData/BGPlay/new_draw_2d_layout_ani.mp4', writer="ffmpeg",
    #               savefig_kwargs={'facecolor': 'black'}, dpi=360)
    # plt.show()


def gain_country_info():
    """
    根据国家的缩写，翻译为中文
    :return country_info_dict:
    """
    geo_file = '../000LocalData/as_geo/GeoLite2-Country-Locations-zh-CN.csv'
    country_info_dict = {}
    file_read = open(geo_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(',')
        # print(line)
        country_info_dict[line[4]] = line[5]
    return country_info_dict


def gain_as_cn():
    """
    获取as互联相关信息
    :return as_list:
    :return as_links:
    """
    print("- - - - - - - -获取AS互联相关信息- - - - - - - - ")
    en2cn_country = gain_country_info()
    time_str = "2019"  # 存储需要统计年份信息
    file_in = '..\\000LocalData\\as_map\\as_core_map_data_new' + time_str + '1001.csv'
    bgp_file = "..\\000LocalData\\as_relationships\\serial-1\\" + time_str + "1001.as-rel.txt"
    # 统计互联点
    as_info = []  # 存储需要绘制的as信息
    as_list = []  # 存储as list
    country_group = ["中国（大陆）", "日本", "韩国"]
    country_group_dict = {}  # 存储各国的as_list
    file_in_read = open(file_in, 'r', encoding='utf-8')
    for line in file_in_read.readlines():
        line = line.strip().split("|")
        try:
            country_cn = en2cn_country[line[8]].strip("\"")
            # print(country_cn)
        except Exception as e:
            print(e)
            continue
        # print(country_cn)
        if country_cn in country_group:
            as_info.append(line)
            as_list.append(line[0])
            country_group_dict.setdefault(country_cn, []).append(line[0])

    print("绘图AS网络数量统计:", len(as_list))
    # print(country_group_dict)
    # 统计互联边
    as_links = []
    bgp_file_read = open(bgp_file, 'r', encoding='utf-8')
    for line in bgp_file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        line = line.strip().split('|')
        if line[0] in as_list and line[1] in as_list:
            as_links.append((line[0], line[1]))
    print("绘图AS关系数量统计:", len(as_links))
    return as_list, as_links, country_group_dict


def generating_graph(country_as_dict, as_links):
    """
    根据AS列表和AS间的互联关系构建Graph
    :param country_as_dict:
    :param as_links:
    :return as_graph:
    """
    print("- - - - - - - -构建AS无向图G- - - - - - - - ")
    as_graph = networkx.Graph()  # 新建一个空的无向图as_graph
    # as_graph.add_nodes_from(as_list)
    color_list = ['red', 'green', 'blue', 'yellow']
    color_cnt = 0
    for key in country_as_dict.keys():
        as_graph.add_nodes_from(country_as_dict[key],
                                color=color_list[color_cnt % len(country_as_dict.keys())],
                                size=10,
                                weight=0.4)
        color_cnt += 1
    as_graph.add_edges_from(as_links)
    # print(networkx.get_node_attributes(as_graph, 'color'))
    return as_graph


def analyzing_graph(as_graph):
    """
    对图进行相关分析
    :param as_graph:
    :return:
    """
    print("G Nodes:", as_graph.number_of_nodes())
    print("G Edges:", as_graph.number_of_edges())
    print("- - - - - - - -已构建的图分析- - - - - - - - ")
    # print(sorted(d for n, d in as_graph.degree()))
    # print(list(networkx.connected_components(as_graph)))
    # print(networkx.clustering(as_graph))


def drawing_graph(as_graph):
    """
    采用networkx原生绘图功能（大概率是matplotlib包）对Graph进行可视化
    实时证明networks的绘图功能并不是很好
    没有自主实现的力引导布局算法+Echarts前端输出(或Matplotlib)的可视化组合好
    :param as_graph: 
    :return: 
    """
    print("- - - - - - - -已构建的图可视化- - - - - - - - ")
    options = {
        'node_color': 'black',
        'node_size': 4,
        'edge_color': 'black',
        'width': 0.1,
    }
    networkx.draw_random(as_graph, **options)
    plt.show()


def save_graph_info(G_3d, pos, graph_name):
    """
    持久化进行网络布局之后的图数据
    :param G_3d:
    :param pos:
    :param graph_name:
    :return:
    """
    # 记录数据Graph数据，包括节点，节点三维坐标，颜色，大小以及互联关系
    print("=>持久化图数据- - - - - - - - - - - - - ")
    print("Graph Nodes Count:", G_3d.number_of_nodes())
    print("Graph Edges Count:", G_3d.number_of_edges())
    graph_nodes_list = []  # 存储节点信息
    graph_edges_list = []  # 存储连边信息
    for node_key in pos.keys():
        xs = pos[node_key][0]
        ys = pos[node_key][1]
        zs = pos[node_key][2]
        node_color = networkx.get_node_attributes(G_3d, 'color')[node_key]
        node_size = networkx.get_node_attributes(G_3d, 'size')[node_key]
        graph_nodes_list.append([node_key, xs, ys, zs, node_color, node_size])
    for line in G_3d.edges():
        graph_edges_list.append(line)

    save_path_nodes = "../000LocalData/BGPlay/" + graph_name + "_nodes.csv"
    save_path_edges = "../000LocalData/BGPlay/" + graph_name + "_edges.csv"
    write_to_csv(graph_nodes_list, save_path_nodes)
    write_to_csv(graph_edges_list, save_path_edges)


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


if __name__ == "__main__":
    time_start = time.time()
    # 构建AS图
    my_as_list, my_as_links, my_country_as_dict = gain_as_cn()
    my_as_graph = generating_graph(my_country_as_dict, my_as_links)
    # analyzing_graph(my_as_graph)
    # drawing_graph(my_as_graph)

    # 使用networkx随机生成无标度网络
    # G = networkx.random_geometric_graph(100, 0.1, dim=3)
    G = my_as_graph
    print("=>原始图信息输出")
    # print("G Nodes:", G.nodes)
    print("G Nodes Count:", G.number_of_nodes())
    print("G Edges Count:", G.number_of_edges())
    pos = {i: (random.random(), random.random(), random.random()) for i in G.nodes()}  # 生成一个具有位置信息的字典
    # print(pos)
    draw_3d(G, pos, 'as_draw_3d', is_show=False)  # 绘制随机生成的原始布局

    # 记录起始数据
    temp_list = list()
    temp_list.append(G)
    temp_list.append(pos)
    ANIMATION_LIST.append(temp_list)

    time_layout_start = time.time()
    layout_3d = aslay_networkx_layout(G, pos, niter=50)  # 3d版的aslay算法
    time_layout_end = time.time()
    print("G layout time consuming:", (time_layout_end - time_layout_start), "S")
    # print(layout_3d)
    draw_3d(G, layout_3d, "as_draw_3d_layout", is_show=False)
    save_graph_info(G, layout_3d, "as_graph_3d")
    my_layout_ani()  # 绘制3D网络动态布局的animation动画
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
