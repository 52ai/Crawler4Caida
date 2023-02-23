# coding: utf-8

import time
import csv


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='gbk')
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
    file_read = open(as_info_file, 'r', encoding='gbk')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_country = line[-1]
        as_info = line[1] + "-" + line[2] + "-" + as_country
        as2country[as_number] = as_info
    return as2country


def find_country():
    """
    根据asn info信息查找国家
    :return:
    """
    c_file = "../000LocalData/Support4WZF/c_cm_ct.CSV"
    as2country = gain_as2country_caida()
    file_read = open(c_file, 'r', encoding='GBK')
    result_list = []
    for line in file_read.readlines():
        line = line.strip().split(",")
        try:
            line_temp = [line[0], line[1], line[2], line[3], as2country[line[1].strip("AS")]]
            print(line_temp)
            result_list.append(line_temp)
        except Exception as e:
            print(e)
    write_to_csv(result_list, "../000LocalData/Support4WZF/c_cm_ct_info.csv")


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    find_country()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")