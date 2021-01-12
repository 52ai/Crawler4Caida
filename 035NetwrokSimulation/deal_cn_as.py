# coding:utf-8
"""
create on Jan 12, 2021 By Wenyan YU
Email：ieeflsyu@outlook.com

根据asn info ，输出全国的中国已申请AS网络信息

"""

import csv
import time 


def write_to_csv(res_list, des_path, title_list):
    """
    把给定的List，写到指定路径文件中
    :param res_list:
    :param des_path:
    :param title_list:
    :return None
    """
    print("write file <%s>.." % des_path)
    csv_file = open(des_path, "w", newline='', encoding='utf-8')
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


def gain_cn_as_info():
    """
    根据 as info file信息获取中国全部已申请AS信息
    """
    cn_as_list = []  # 存储中国的已申请as网络
    as_info_file = '../000LocalData/as_Gao/asn_info.txt'
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        as_country = line[1].strip().split(",")[-1].strip()
        if as_country == "CN":
            print(line)
            cn_as_list.append(line)
    save_file = "../000LocalData/GlobalNetSimulate/deal/cn_as_list.csv"
    write_to_csv(cn_as_list, save_file, ["ASN", "ASN INFO"])


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    gain_cn_as_info()
    time_end = time.time()  # 记录结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_end), "S")