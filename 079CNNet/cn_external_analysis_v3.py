# coding:utf-8
"""
create on Apr 25, 2022 By Wayne YU

Function:

新需求，需要研究三大运营商出口互联中，国际网络的数量，两个维度按AS维度以及按企业名称的维度

经统计三大运营商出口AS为：

电信:4134、4809、4812、4813
联通:4808、4837、9929、17621、17623
移动（含铁通）：9394、9808、24400、56041、58453


V2:
通过自治域机构名称字符串匹配，进行统计


V3:
重新捋一捋思路，弄一个万能的程序，根据关键词，提取某org的所有AS网络
并统计该org海外互联关系情况

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


def external_as_analysis(aim_country, aim_str):
    """
    根据输入的国家，统计该某org的ASN 列表以及其国际互联as/org的数量
    :param aim_country:
    :param aim_str
    :return:
    """
    as2country = gain_as2country_caida()
    as2org = gain_as2org_caida()

    print(f"- - - - - - - {aim_str}- - - - - -  - - ")
    print("ORG所属国家:", aim_country)
    print("ORG检索关键字符串：", aim_str)

    # 获取1998-2020年全球BGP互联关系的存储文件
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))

    except_info = []  # 存储异常信息

    aim_org_list = []  # 存储符合关键词检索的目标记录

    for path_item in file_path[-1:]:
        print(path_item)
        aim_org_2abroad_as = []  # 存储目标机构海外互联AS
        aim_org_2abroad_org = []  # 存储目标机构海外互联ORG

        file_read = open(path_item, 'r', encoding='utf-8')
        for line in file_read.readlines():
            if line.strip().find("#") == 0:
                continue
            try:
                left_as = str(line.strip().split('|')[0])
                left_as_country = as2country[left_as]
                left_as_org = as2org[left_as]

                right_as = str(line.strip().split('|')[1])
                right_as_country = as2country[right_as]
                right_as_org = as2org[right_as]

                if left_as_org.upper().find(aim_str) != -1:
                    # print(left_as_org)
                    aim_org_list.append("AS"+str(left_as)+"-"+left_as_org+"-"+left_as_country)
                    if right_as_country != aim_country:
                        aim_org_2abroad_as.append(right_as)
                        aim_org_2abroad_org.append(right_as_org)

                if right_as_org.upper().find(aim_str) != -1:
                    # print(right_as_org)
                    aim_org_list.append("AS"+str(right_as)+"-"+right_as_org+"-"+right_as_country)
                    if left_as_country != aim_country:
                        aim_org_2abroad_as.append(left_as)
                        aim_org_2abroad_org.append(left_as_org)

            except Exception as e:
                except_info.append(e)

        print("ASN Whois画像信息缺失记录:", len(set(except_info)))
        print("符合关键词检索的记录:", len(set(aim_org_list)))
        print(list(set(aim_org_list)))
        print("目标企业海外互联数量-AS维度:", len(set(aim_org_2abroad_as)))
        print("目标企业海外互联数量-ORG维度:", len(set(aim_org_2abroad_org)))


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    big_three_org = ["CHINA TELECOM", "CHINA MOBILE", "CHINA UNICOM"]
    country = "CN"
    for org_str in big_three_org:
        external_as_analysis(country, org_str)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
