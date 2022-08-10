# coding:utf-8
"""
create on Mar 24, 2022 By Wayne YU
Email: ieeflsyu@outlook.com

Function:
因Echarts难以发现一些实质上的问题，计划通过Gephi去先构建一个全局的AS可视化图
然后在此图上做相应的研究
甚至可以结合经纬度，做地理位置方面的可视化，（数据质量可以不用那么好，先做出来看看效果再说）
本程序主要用于构建Gephi的输入文件
包含node和edges

输入： asns_geo_all.csv、20220301.as-rel.txt
输出：global_as.gexf

# 20220808 构建pm项目的数据格式

"""
import time
import csv

asns_file = "asns_geo_all.csv"
as_rel_file = "20220301.as-rel.txt"
global_as_gephi_file = "global_as_RU.gexf"


def write_to_csv(res_list, des_path, title):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :param title:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(title)
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def generate_gephi_file():
    """
    根据两个文件生成gephi文件
    :return:
    """
    node_list = []  # 存储node信息，[node_id, node_label, node_name, node_org, node_country, long, lat]
    edge_list = []  # 存储edge信息，[edge_id, source_AS, target_AS, as_rel_type]
    """
    统计活跃AS的集合
    """
    active_as_dict = {}
    with open(as_rel_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.find("#") != -1:
                continue
            line = line.strip().split("|")
            if line[0] not in active_as_dict.keys():
                active_as_dict[line[0]] = 1
            else:
                active_as_dict[line[0]] += 1
            if line[1] not in active_as_dict.keys():
                active_as_dict[line[1]] = 1
            else:
                active_as_dict[line[1]] += 1

    """
    统计节点信息
    """
    node_id = 0  # 存储node_id
    as2id_dict = {}  # 构建as到id的映射关系，供后面统计边的信息使用
    with open(asns_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            if len(line) < 5:
                continue
            # print(line)
            if line[0] not in active_as_dict.keys():
                continue
            node_label = "AS"+line[0]
            node_name = line[1].split(" - ")[0]
            node_org = line[1].split(" - ")[-1]
            # node_label = node_label + "-" + node_name
            node_country = line[2]
            if node_country != "RU":
                continue
            long = line[3]
            lat = line[4]
            temp_line = [node_id, node_label, node_name, node_org, node_country, long, lat]
            as2id_dict[line[0]] = node_id  # 构建as2id的映射关系
            print(temp_line)
            node_id += 1
            node_list.append(temp_line)

    """
    统计边的信息
    """
    edge_id = 0  # 存储edge_id
    except_info_list = []  # 存储异常信息
    with open(as_rel_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.find("#") != -1:
                continue
            line = line.strip().split("|")
            # print(line)
            try:
                source_id = as2id_dict[line[0]]
                target_id = as2id_dict[line[1]]
                as_rel_type = line[2]
            except Exception as e:
                except_info_list.append(e)
                continue
            temp_line = [edge_id, "AS"+str(line[0]), "AS"+str(line[1]), as_rel_type]
            print(temp_line)
            edge_list.append(temp_line)
            edge_id += 1
    """
    生成Gephi文件
    """
    with open(global_as_gephi_file, "w", encoding="utf-8") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                "<gexf xmlns:viz=\"http:///www.gexf.net/1.1draft/viz\" version=\"1.1\" xmlns=\"http://www.gexf.net/1.1draft\">\n"
                "<meta lastmodifieddate=\"2010-03-03+23:44\">\n"
                "<creator>Gephi 0.7</creator>\n"
                "</meta>\n"
                "<graph defaultedgetype=\"undirected\" idtype=\"string\" type=\"static\">\n")
        node_count = len(node_list)
        temp_str = "<nodes count=\"" + str(node_count) + "\">\n"
        f.write(temp_str)
        for item in node_list:
            # temp_str = "<node id=\"%s\" label=\"%s\" node_name=\"%s\" node_org=\"%s\" node_country=\"%s\" long=\"%s\" lat=\"%s\"/>\n" \
            #            % (str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(item[5]), str(item[6]))
            temp_str = "<node id=\"%s\"/>\n" \
                       % (str(item[1]))
            f.write(temp_str)
        f.write("</nodes>\n")

        edge_count = len(edge_list)
        temp_str = "<edges count=\"" + str(edge_count) + "\">\n"
        f.write(temp_str)

        for item in edge_list:
            # temp_str = "<edge id=\"%s\" source=\"%s\" target=\"%s\" type=\"%s\"/>\n" \
            #            % (str(item[0]), str(item[1]), str(item[2]), str(item[3]))
            temp_str = "<edge id=\"%s\" source=\"%s\" target=\"%s\" type=\"undirected\"/>\n" \
                       % (str(item[0]), str(item[2]), str(item[1]))
            f.write(temp_str)
        f.write("</edges>\n</graph>\n</gexf>")


if __name__ == "__main__":
    time_start = time.time()
    generate_gephi_file()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
