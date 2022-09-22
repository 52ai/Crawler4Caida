# coding:utf-8
"""
create on Sep 22, 2022 By Wayne YU
Email: ieeflsyu@outlook.com

Function:

按国家或公司输出graphistry的绘图数据

输入： asns_geo_all.csv、20220301.as-rel.txt
输出：global_as.csv

未来需要根据全局出入度、国别以及其他图特征，来设定节点和连边的大小、颜色等，把可视化进行到底

"""
import time
import csv

asns_file = "../../077RU&UA/Gephi/asns_geo_all.csv"
as_rel_file = "../../077RU&UA/Gephi/20220301.as-rel.txt"
result_file = "mgfb.csv"


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


def generate_graphistry_file():
    """
    根据两个文件生成graphistry文件，按照国家、机构等内容筛选
    :return:
    """

    """
    构建as画像
    """
    as2info_dic = {}  # 存储ASN到具体信息的映射
    with open(asns_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            if len(line) < 5:
                continue
            # print(line)

            node_name = line[1].split(" - ")[0]
            node_org = line[1].split(" - ")[-1]
            node_country = line[2]

            long = line[3]
            lat = line[4]
            node_org = "".join(filter(str.isalnum, node_org))
            node_label = "AS" + line[0] + "-" + node_org + "-" + node_country
            temp_line = [node_label, node_name, node_org, node_country, long, lat]
            as2info_dic[line[0]] = temp_line
            print(temp_line)

    """
    根据连边，构建graphistry信息
    """
    except_info_list = []  # 存储异常信息
    result_list = []   # 存储最终的结果
    with open(as_rel_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.find("#") != -1:
                continue
            line = line.strip().split("|")
            # print(line)
            try:
                source_as_info = as2info_dic[line[0]]
                target_as_info = as2info_dic[line[1]]
                as_rel_type = line[2]
            except Exception as e:
                except_info_list.append(e)
                continue

            country_group = ["CN", "JP", "KR"]

            if source_as_info[2].find("DoD") != -1 and target_as_info[2].find("DoD") != -1:
                temp_line = [source_as_info[0], target_as_info[0], as_rel_type]
                print(temp_line)
                result_list.append(temp_line)
            else:
                pass
            # temp_line = [source_as_info[0], target_as_info[0], as_rel_type]
            # print(temp_line)
            # result_list.append(temp_line)

    write_to_csv(result_list, result_file, ['source', 'target', 'value'])


if __name__ == "__main__":
    time_start = time.time()
    generate_graphistry_file()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
