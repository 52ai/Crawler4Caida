# coding:utf-8
"""
create on Dec 6, 2019 by Wayne Yu
version:1.0
Function:

实现对as core map data 的处理
"""

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
    csvFile = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csvFile, delimiter="|")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    file_in = "./as_core_map_data_2019120601.csv"
    file_read = open(file_in, 'r', encoding='utf-8')
    file_out_list = []
    for line in file_read.readlines():
        line = line.strip().split(',')
        if len(line) == 5:
            print(line)
            file_out_list.append(line)
        if line[-1] == "0.0":
            print(line)
            file_out_list.append(line)

    save_path = "./abnormal_data.csv"
    write_to_csv(file_out_list, save_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
