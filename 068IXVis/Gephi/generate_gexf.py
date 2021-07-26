# coding:utf-8
"""
create on July 26, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:
根据ix-as的信息，生成Gephi绘图格式数据.gexf

"""
import time
import csv


ix_list_file = "../../000LocalData/IXVis/ix_list_new.csv"
as_list_file = "../../000LocalData/IXVis/as_list_new.csv"
ix_as_rel_file = "../../000LocalData/IXVis/ix_as_rel.csv"
ix_as_gephi_file = "../../000LocalData/IXVis/ix_as.gexf"


def write_to_csv(res_list, des_path, title=[]):
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
    根据三个文件生成gephi文件
    :return:
    """
    node_list = []  # 存储node信息, [node_id, label]
    edge_list = []  # 存储edge信息, [edge_id, source_id, target_id]
    """
    统计节点的信息
    """
    with open(ix_list_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            # print(line)
            ix_id = "ix_"+str(line[0])
            node_list.append([ix_id, line[1]])
    with open(as_list_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            # print(line)
            as_id = "as_"+str(line[0])
            as_str = "AS"+str(line[1])
            node_list.append([as_id, as_str])
    """
    统计边的信息
    """
    with open(ix_as_rel_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            ix_id = "ix_"+str(line[0])
            as_id = "as_"+str(line[1])
            edge_list.append([ix_id, as_id])
    """
    生成gephi文件
    """
    node_out_list = []
    node2id = {}  # 存储node和id间的映射关系
    with open(ix_as_gephi_file, "w", encoding="utf-8") as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
                "<gexf xmlns:viz=\"http:///www.gexf.net/1.1draft/viz\" version=\"1.1\" xmlns=\"http://www.gexf.net/1.1draft\">\n"
                "<meta lastmodifieddate=\"2010-03-03+23:44\">\n"
                "<creator>Gephi 0.7</creator>\n"
                "</meta>\n"
                "<graph defaultedgetype=\"undirected\" idtype=\"string\" type=\"static\">\n")
        node_count = len(node_list)
        temp_str = "<nodes count=\"" + str(node_count) + "\">\n"
        f.write(temp_str)
        node_itn = 0  # 统计id
        for item in node_list:
            temp_str = "<node id=\"" + str(node_itn) + "\" label=\"" + str(item[1]) + "\"/>\n"
            f.write(temp_str)
            node2id[item[0]] = node_itn  # 存储节点的对应关系
            node_out_list.append([str(node_itn), str(item[1])])
            node_itn += 1

        # print(node2id)

        f.write("</nodes>\n")
        edge_count = len(edge_list)
        temp_str = "<edges count=\"" + str(edge_count) + "\">\n"
        f.write(temp_str)
        itn = 0  # 统计值
        edge_out_list = []
        for item in edge_list:
            temp_str = "<edge id=\""+str(itn)+"\" source=\""+str(node2id[item[0]])+"\" target=\""+str(node2id[item[1]])+"\"/>\n"
            f.write(temp_str)
            edge_out_list.append([str(itn), str(node2id[item[0]]), str(node2id[item[1]])])
            itn += 1
        f.write("</edges>\n</graph>\n</gexf>")
        node_out_file = "node_out.csv"
        write_to_csv(node_out_list, node_out_file, ["node_id", "label"])
        edge_out_file = "edge_out.csv"
        write_to_csv(edge_out_list, edge_out_file, ["edge_id", "source", "target"])


if __name__ == "__main__":
    time_start = time.time()
    generate_gephi_file()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
