# coding:utf-8
"""
create on Jan 8, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

根据AS的国别，输出颜色

"""

import csv
import time


def write_to_csv(res_list, des_path, title_list):
    """
    把给定的List，写到指定路径文件中
    :param res_list:
    :param des_path:
    :param title_list:
    :return None:
    """
    print("write file <%s>.." % des_path)
    csv_file = open(des_path, "w", newline='', encoding='gbk')
    try:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        writer.writerow(title_list)
        for i in res_list:
            writer.writerow(i)
    except Exception as e_csv:
        print(e_csv)
    finally:
        csv_file.close()
    print("write finish!")


def gain_as2country():
    """
    根据as info file信息获取AS对应的国家
    :return as2country:
    """
    as2country = {}  # 存储as号到info的映射关系
    as_info_file = '../000LocalData/as_Gao/asn_info.txt'
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        as_number = line[0]
        as_country = line[1].strip().split(",")[-1].strip()
        as2country[as_number] = as_country
    return as2country


def gain_country2c():
    """
    根据国家信息获取国家对应的大洲信息
    :return country2c:
    """
    country2c = {}
    country_file = '../000LocalData/GlobalNetSimulate/deal/GeoLite2-Country-Locations-zh-CN.csv'
    file_read = open(country_file, 'r', encoding='gbk')
    for line in file_read.readlines():
        line = line.strip().split(",")
        print(line)
        country = line[4]
        con = line[3]
        country2c[country] = con
    return country2c


def judge_color():
    """
    根据as号的国别，获取颜色
    :return:
    """
    c2c = gain_country2c()
    as2c = gain_as2country()
    as_file = '../000LocalData/GlobalNetSimulate/deal/as_list.txt'
    file_read = open(as_file, 'r', encoding='utf-8')
    result_list = []
    for line in file_read.readlines():
        line = line.strip()
        as_item = line
        as_country = as2c[as_item]
        as_con = c2c[as_country]
        color = "G"
        if as_country == "US":
            color = "R"
        elif as_con == "欧洲":
            color = "B"
        print(as_item, as_country, as_con.strip("\""), color)
        result_list.append([as_item, as_country, as_con.strip("\""), color])
    save_path = "../000LocalData/GlobalNetSimulate/deal/result.csv"
    write_to_csv(result_list, save_path, ["AS", "Country", "Con", "Color"])


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    judge_color()
    time_end = time.time()  # 记录结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
