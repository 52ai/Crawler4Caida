# coding:utf-8
"""
create on Jan 4, 2021 By Wenyan YU
Email: ieefls@outlook.com

Function:

根据商业关系，推断任意两个网络间的备份路由

思路：
1）先根据全球AS网络商业关系，构建图模型；
2）利用经典的图算法，求出给定两个网络间的所有路径；
3）根据商业关系规则，判断2）中的有效路径。

因为网络模型复杂，计算资源有限，算法提供了限定路由搜索的最大长度选项，以避免过度绕转的现象。
这样的限定亦符合实际的路由寻址过程。（AS PATH不会过长）

为方便先暴力搜索，拿到有效路径
判断规则：无谷理论（一旦出现山谷，则判定为无效路径；否则为有效路径）。
具体为判断是否出现如下三元组，如出现则为无效路径，否则为有效路径
1）P2C + C2P
2）P2P + P2P
3）P2C + P2P
4）P2P + C2P


"""

import time
import networkx as nx
import csv


log_file = []  # 存储所有的日志文件


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csvFile = open(des_path, 'w', newline='', encoding='gbk')
    try:
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def gain_all_paths(sour_as, des_as, max_as_path):
    """
    根据传入的源目as对，输出所有可能的路径
    :param sour_as:
    :param des_as:
    :param max_as_path:
    :return:
    """
    global_as_graph = nx.DiGraph()  # 生成空有向图，用于在内存中构建全球网络拓扑图
    as_rel_file = "../000LocalData/as_relationships/serial-1/20201101.as-rel.txt"
    file_read = open(as_rel_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        as_0 = str(line.strip().split('|')[0])
        as_1 = str(line.strip().split('|')[1])
        as_rel = str(line.strip().split('|')[2])
        # 根据边构建全球互联网网络拓扑图
        if as_rel == 0:
            global_as_graph.add_edge(as_0, as_1, rel="P2P")
            global_as_graph.add_edge(as_1, as_0, rel="P2P")
        else:
            global_as_graph.add_edge(as_0, as_1, rel="P2C")
            global_as_graph.add_edge(as_1, as_0, rel="C2P")
    print("=>根据构建的全球AS网络拓扑图，统计全球网络特征")
    print("=>全球互联网网络拓扑图（原始）")
    print("拓扑图节点数量:", global_as_graph.number_of_nodes())
    print("拓扑图连边数量:", global_as_graph.number_of_edges())
    print("测试图连边权值:(%s,%s)(%s)" % (sour_as, des_as, global_as_graph.edges[sour_as, des_as]['rel']))
    # print("计算源(AS%s)目AS(AS%s)之间不相交的节点路径: " % (sour_as, des_as))
    # paths = []
    # for item in list(nx.node_disjoint_paths(global_as_graph, sour_as, des_as)):
    #     print(item)
    #     paths.append(item)
    # print("路径数量:", len(paths))
    print("=>计算源(AS%s)目AS(AS%s)之间Simple节点路径" % (sour_as, des_as))
    print("最大路径长度限定为:", max_as_path)
    paths = []
    for item in list(nx.all_simple_paths(global_as_graph, sour_as, des_as, cutoff=max_as_path)):
        # print(item)
        paths.append(item)
    print("全部路径数量:", len(paths))
    print("有效路径数量:", len(gain_valid_paths(global_as_graph, paths)))


def gain_valid_paths(as_graph, all_paths):
    """
    拿到所有可能的路径后，根据商业关系规提取有效路径
    :param as_graph:
    :param all_paths:
    :return valid_paths:
    """
    valid_paths = []  # 存储最终的有效路径
    """
    为方便先暴力搜索，拿到有效路径
    判断规则：无谷理论（一旦出现山谷，则判定为无效路径；否则为有效路径）
    """
    type_rel = [['P2C', "C2P"], ['P2P', "P2P"], ['P2C', "P2P"], ['P2P', "C2P"]]
    for path_item in all_paths:
        # print(path_item)
        log_file.append([path_item])
        path_type = []  # 存储链路的商业关系
        for i in range(len(path_item)-1):
            s = path_item[i]
            t = path_item[i+1]
            # print(s, t, as_graph.edges[s, t]['rel'])
            log_file.append([s, t, as_graph.edges[s, t]['rel']])
            path_type.append(as_graph.edges[s, t]['rel'])
        # print(path_type)
        log_file.append([path_type])
        flag = True  # 默认路径为有效
        for i in range(len(path_type)-1):
            if [path_type[i], path_type[i+1]] in type_rel:
                flag = False  # 违反商业关系，该路径无效
                break

        if flag is True:
            valid_paths.append(path_item)
            # print("This Path is Valid!")
            log_file.append(["This Path is Valid!"])
        else:
            log_file.append(["This Path is Invalid!"])
            # print("This Path is Invalid!")
        log_file.append(["- - - -  - - - - - - - - - - - - - -  -"])

    return valid_paths


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    gain_all_paths("4134", "3356", 3)
    save_path = "log.csv"
    write_to_csv(log_file, save_path)
    time_end = time.time()  # 记录结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")


