# coding:utf-8
"""
create on May 16， 2021 By Wenyan Yu
Email: ieeflsyu@outlook.com

Function:

近期领导安排的任务对IX的统计提出了新的需求，包括了更多维度的关联分析
本程序先完成目前亟待完成的任务，针对IX的接入成员的AS网络，按照国别统计相关数据

"""
import csv
import time


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


def gain_as2country():
    """
    根据as info file信息获取AS与国家的对应字典
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info.txt'
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        # print(line)
        as_number = line[0]
        # as_info = line[1]
        as_country = line[1].strip().split(",")[-1].strip()
        as2country[as_number] = as_country
    return as2country


def deal_peers(file_path):
    """
    根据传入的file_path处理peers关系数据，ASN，AS Name
    :param file_path:
    :return:
    """
    as2country_dic = gain_as2country()
    country_list = []
    file_read = open(file_path, 'r', encoding='utf-8')
    for line in file_read.readlines():
        as_number = line.strip().split(",")[0]
        as_country = "other"
        try:
            as_country = as2country_dic[as_number]
        except Exception as e:
            # print(e)
            pass
        # print(as_number, as_country)
        country_list.append(as_country)
    all_count = len(country_list)  # 存储全部的成员数量
    print("全部接入成员数量：", all_count)
    # print(country_list)

    country_list_dict = {}
    for item in country_list:
        if item in country_list_dict.keys():
            country_list_dict[item] += 1
        else:
            country_list_dict[item] = 1

    # print(country_list_dict)

    country_list_order = []
    for key in country_list_dict.keys():
        country_list_order.append([key, country_list_dict[key], int(country_list_dict[key])/all_count])

    country_list_order.sort(reverse=True, key=lambda elem: int(elem[1]))
    # print(country_list_order)
    for item in country_list_order:
        print(item)


if __name__ == "__main__":
    time_start = time.time()
    # print(gain_as2country())
    file_in = "./data/seattleix-peers.csv"
    deal_peers(file_in)
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")

