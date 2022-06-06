import time
import csv
import os


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


def find_country(aim_country):
    """
    根据asn info信息查找国家
    :return:
    """
    c_file = "c_cm_ct.CSV"
    as2country = gain_as2country_caida()
    file_read = open(c_file, 'r', encoding='GBK')
    aim_country_as = []  # 存储尼泊尔的AS
    for line in file_read.readlines():
        line = line.strip().split(",")
        try:
            print(line[1], as2country[line[1].strip("AS")])
            if as2country[line[1].strip("AS")] == aim_country:
                aim_country_as.append(line[1])
        except Exception as e:
            print(e)
    print(aim_country, "客户数量统计:", len(aim_country_as))


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    country = "NP"
    find_country(country)
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
