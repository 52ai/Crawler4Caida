# coding:utf-8
"""
create on  June 30, 2020 By Wayne YU

Function:

自研AS布局算法ASlay需要针对AS网络互联的特点进行相应的布局研究
该程序是希望借助中国AS互联真实数据开展布局


常规版的ASlay 2D算法已初步完成，接下来分两步走
第一步，完成ASlay 3D常规版本
第二步，完成ASlay 2D/3D不重叠版本网络布局，并结合已制定的地图基础课题第二篇输出框架开展相关实验

基于以上实验结果，最终实现地图基础课题第二篇论文的撰写

20200630
因在本机（win10+小黑）跑全球所有互联网网络数据的时候，出现内存不足以及算力不足的情况
因此计划将该将脚本简化，省去绘图的功能，只出全球互联网网络互联三维模型三维坐标
待服务器端出了三维坐标，再在本地结合Mayavi进行可视化

"""
import time
from math import sqrt
import numpy
import random
import networkx
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
    print("主循环开始（3D）")
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
            layout_3d_pos = dict(zip(draw_graph.nodes(), [(n.x, n.y, n.z) for n in nodes]))
            ANIMATION_LIST.append([draw_graph, layout_3d_pos])
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


def gain_country_info(geo_file):
    """
    根据国家的缩写，翻译为中文
    :param geo_file:
    :return country_info_dict:
    """
    country_info_dict = {}
    file_read = open(geo_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(',')
        # print(line)
        country_info_dict[line[4]] = line[5]
    return country_info_dict


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
    color_list_source = [[255, 0, 0], [255, 128, 0], [255, 255, 0],
                         [0, 255, 0], [0, 255, 255], [0, 0, 255],
                         [128, 0, 255]]
    color_list = list()
    for item in color_list_source:
        color_list.append((item[0]/255, item[1]/255, item[2]/255))

    color_cnt = 0
    for key in country_as_dict.keys():
        color_temp = color_list[color_cnt % len(color_list)]
        print(key, int(color_temp[0]*255), int(color_temp[1]*255), int(color_temp[2]*255))
        as_graph.add_nodes_from(country_as_dict[key],
                                color=color_list[color_cnt % len(color_list)],
                                size=10,
                                weight=0.4)
        color_cnt += 1
    as_graph.add_edges_from(as_links)
    # print(networkx.get_node_attributes(as_graph, 'color'))
    return as_graph


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

    # 在当前文件夹下生成节点和边的数据
    save_path_nodes = "./" + graph_name + "_nodes.csv"
    save_path_edges = "./" + graph_name + "_edges.csv"
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
        writer = csv.writer(csv_file, delimiter="|")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_as_cn(country_group, file_in, bgp_file, geo_file):
    """
    获取as互联相关信息
    :param country_group:
    :param file_in:
    :param bgp_file:
    :param geo_file:
    :return as_list:
    :return as_links:
    """
    print("- - - - - - - -获取AS互联相关信息- - - - - - - - ")
    en2cn_country = gain_country_info(geo_file)
    # 统计互联点
    as_info = []  # 存储需要绘制的as信息
    as_list = []  # 存储as list
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


if __name__ == "__main__":
    time_start = time.time()
    # 构建AS图
    my_country_group = ["中国（大陆）", "日本", "韩国", "中国（香港）", "中国（台湾）", "新加坡", "德国"]
    my_file_in = '../000LocalData/as_map/as_core_map_data_new20191001.csv'
    my_bgp_file = '../000LocalData/as_relationships/serial-1/20191001.as-rel.txt'
    my_geo_file = '../000LocalData/as_geo/GeoLite2-Country-Locations-zh-CN.csv'
    my_as_list, my_as_links, my_country_as_dict = gain_as_cn(my_country_group, my_file_in, my_bgp_file, my_geo_file)
    my_as_graph = generating_graph(my_country_as_dict, my_as_links)

    G = my_as_graph
    print("=>原始图信息输出")
    print("G Nodes Count:", G.number_of_nodes())
    print("G Edges Count:", G.number_of_edges())
    pos = {i: (random.random(), random.random(), random.random()) for i in G.nodes()}  # 生成一个具有位置信息的字典

    # 记录起始数据
    ANIMATION_LIST.append([G, pos])

    time_layout_start = time.time()
    layout_3d = aslay_networkx_layout(G, pos, niter=50)  # 3d版的aslay算法
    time_layout_end = time.time()
    print("G layout time consuming:", (time_layout_end - time_layout_start), "S")
    save_graph_info(G, layout_3d, "as_graph_3d")
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")

"""
- - - - - - - -获取AS互联相关信息- - - - - - - - 
绘图AS网络数量统计: 4773
绘图AS关系数量统计: 11053
- - - - - - - -构建AS无向图G- - - - - - - - 
日本 255 0 0 红
德国 255 128 0 橙
韩国 255 255 0 黄
中国（台湾） 0 255 0 绿
新加坡 0 255 255 青
中国（香港） 0 0 255 蓝
中国（大陆） 128 0 255 紫
"""