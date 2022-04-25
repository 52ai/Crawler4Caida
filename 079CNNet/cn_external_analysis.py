# coding:utf-8
"""
create on Apr 25, 2022 By Wayne YU

Function:

新需求，需要研究三大运营商出口互联中，国际网络的数量，两个维度按AS维度以及按企业名称的维度

经统计三大运营商出口AS为：

电信:4134、4809、4812、4813
联通:4808、4837、9929、17621、17623
移动（含铁通）：9394、9808、24400、56041、58453


"""

import time
import csv
import os


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


def gain_as2country_caida():
    """
    根据Caida asn info获取as对应的国家信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_country = line[-1]
        as2country[as_number] = as_country
    return as2country


def gain_as2org_caida():
    """
    根据Caida asn info获取as对应的org信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2org_dic = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_org = line[2] + "," + line[1]
        as2org_dic[as_number] = as_org.split(",")[0]
    return as2org_dic


def external_as_analysis(aim_country):
    """
    根据输入的国家，统计该国家的出口AS数量及其国际互联as/org的数量
    :param aim_country:
    :return:
    """
    as2country = gain_as2country_caida()
    as2org = gain_as2org_caida()

    big_three_net = ['4134', '4809', '4812', '4813',
                     '4808', '4837', '9929', '17621', '17623',
                     '9394', '9808', '24400', '56041', '58453']

    ct_as = ['4134', '4809', '4812', '4813']
    cu_as = ['4808', '4837', '9929', '17621', '17623']
    cm_as = ['9394', '9808', '24400', '56041', '58453']

    print(country)
    # 获取1998-2020年全球BGP互联关系的存储文件
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))

    except_info = []  # 存储异常信息
    for path_item in file_path[-1:]:
        print(path_item)
        # 遍历一次文件，获取该国出口AS的数量
        file_read = open(path_item, 'r', encoding='utf-8')
        external_cnt = 0  # 存储该国出口连边的数量(Abroad)
        external_as_list = []  # 存储出口AS(CN)
        external_country_list = []  # 存储该国出口方向的国家(Abroad)
        external_country_as = []  # 存储该国出口互联关系中，国外AS网络(Abroad)

        ct_2abroad_as = []  # 存储电信的海外互联网络数量
        ct_2abroad_org = []  # 存储电信海外互联企业数量
        cu_2abroad_as = []  # 存储联通的海外互联网络数量
        cu_2abroad_org = []  # 存储联通的海外互联企业数量
        cm_2abroad_as = []  # 存储移动的海外互联网络数量
        cm_2abroad_org = []  # 存储移动的海外互联企业数量

        for line in file_read.readlines():
            if line.strip().find("#") == 0:
                continue
            try:
                if str(line.strip().split('|')[0]) in big_three_net:
                    if as2country[str(line.strip().split('|')[1])] != aim_country:
                        external_cnt += 1
                        external_as_list.append(str(line.strip().split('|')[0]))
                        external_country_list.append(as2country[str(line.strip().split('|')[1])])
                        external_country_as.append(str(line.strip().split('|')[1]))

                        if line.strip().split('|')[0] in ct_as:
                            ct_2abroad_as.append(str(line.strip().split('|')[1]))
                            ct_2abroad_org.append(as2org[str(line.strip().split('|')[1])])

                        if line.strip().split('|')[0] in cu_as:
                            cu_2abroad_as.append(str(line.strip().split('|')[1]))
                            cu_2abroad_org.append(as2org[str(line.strip().split('|')[1])])

                        if line.strip().split('|')[0] in cm_as:
                            cm_2abroad_as.append(str(line.strip().split('|')[1]))
                            cm_2abroad_org.append(as2org[str(line.strip().split('|')[1])])

                if as2country[str(line.strip().split('|')[0])] != aim_country:
                    if str(line.strip().split('|')[1]) in big_three_net:
                        external_cnt += 1
                        external_as_list.append(str(line.strip().split('|')[1]))
                        external_country_list.append(as2country[str(line.strip().split('|')[0])])
                        external_country_as.append(str(line.strip().split('|')[0]))

                        if line.strip().split('|')[1] in ct_as:
                            ct_2abroad_as.append(str(line.strip().split('|')[0]))
                            ct_2abroad_org.append(as2org[str(line.strip().split('|')[0])])

                        if line.strip().split('|')[1] in cu_as:
                            cu_2abroad_as.append(str(line.strip().split('|')[0]))
                            cu_2abroad_org.append(as2org[str(line.strip().split('|')[0])])

            except Exception as e:
                except_info.append(e)

        print("CT 2 Abroad AS:", len(list(set(ct_2abroad_as))))
        print("CT 2 Abroad Org:", len(list(set(ct_2abroad_org))))

        print("CU 2 Abroad AS:", len(list(set(cu_2abroad_as))))
        print("CU 2 Abroad Org:", len(list(set(cu_2abroad_org))))

        print("CM 2 Abroad AS:", len(list(set(cm_2abroad_as))))
        print("CM 2 Abroad Org:", len(list(set(cm_2abroad_org))))

        # print(external_as_list)
        # 统计出口AS的排名
        external_as_rank = {}
        for item in list(set(external_as_list)):
            external_as_rank[item] = 0

        for item in external_as_list:
            external_as_rank[item] += 1

        # 将字典转换为列表
        external_as_rank_list = []
        temp_list = []
        for item in external_as_rank.keys():
            temp_list.append(item)
            temp_list.append(external_as_rank[item])
            external_as_rank_list.append(temp_list)
            temp_list = []
        external_as_rank_list.sort(reverse=True, key=lambda elem: int(elem[1]))
        external_as_list = list(set(external_as_list))

        print("All External Edges Count:", external_cnt)
        print("All External AS Count(Abroad):", len(list(set(external_country_as))))
        print("All External AS Count(Internal):", len(external_as_list))

        print(external_as_rank_list)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    country = "CN"
    external_as_analysis(country)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
