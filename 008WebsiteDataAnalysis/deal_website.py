# coding:utf-8
"""
create on Mar 17,2019 by Wayne
"""
import csv
import time

self_top_domain = []


def write_csv(file_list, file_name):
    """
    写CSV 文件
    :param file_list:
    :return: None
    """
    f = open(file_name, "w", newline='', encoding='GBK')
    writer = csv.writer(f)
    for item in file_list:
        writer.writerow(item)
    f.close()


def process_data(file_name):
    out_file_list = []  # 规定格式存储的数据列表
    file_read = open(file_name, 'r', encoding='utf-8-sig')
    cnt = 0
    for line in file_read.readlines():
        line = line.strip().split(',')
        print(line)
        cnt += 1
        if cnt > 100:
            break
    # write_csv(out_file_list, "处理完成_"+file_name)


if __name__ == "__main__":
    # 读取自主顶级域名列表
    file_domain = open("../000PublicData/domain.csv", 'r', encoding='utf-8-sig')
    for line in file_domain.readlines():
        line = line.strip().split(',')
        print(line)
        self_top_domain.extend(line)
    # 获得全部的自主顶级域名列表
    print(self_top_domain)
    process_file = "../000PublicData/websiteList.csv"
    process_data(process_file)
