# coding:utf-8
"""
create on May 21, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

对IP地址进行定位

"""

from ipdb import City
import time
import csv


def write_to_csv(res_list, des_path, title_line):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :param title_line:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='gbk')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(title_line)
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def deal():
    """
    处理并保存
    :return:
    """
    result_list = []
    db = City("../000LocalData/ipdb/caict_full.ipdb")
    print("ipdb.build.time:", db.build_time())
    print(db.find("221.183.94.26", "CN"))
    file_in = "../000LocalData/ipdb/trace.csv"
    file_read = open(file_in, 'r', encoding='gbk')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        ip_temp = line[4]
        ip_info_temp = db.find_info(ip_temp, "CN").city_name
        line.append(ip_info_temp)
        print(line)
        result_list.append(line)
    save_path = "../000LocalData/ipdb/trace_new.csv"
    write_to_csv(result_list,
                 save_path,
                 [])


def once_query():
    """
    查询一次IP地址
    :return:
    """
    db = City("../000LocalData/ipdb/caict_ipv4.ipdb")
    print("ipdb.build.time:", db.build_time())
    print(db.find("223.255.207.197", "CN"))


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    # deal()
    once_query()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")


