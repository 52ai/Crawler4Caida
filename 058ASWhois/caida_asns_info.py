# coding:utf-8
"""
create on Jan 20, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

梳理CAIDA asns数据中的经纬度

"""

import jsonlines
import time
import csv


def write_to_csv(res_list, des_path, title_list):
    """
    把给定的List，写到指定路径文件中
    :param res_list:
    :param des_path:
    :param title_list:
    :return None:
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


def gain_as2info():
    """
    根据as info file信息获取AS对应的info
    :return as2info:
    """
    as2info = {}  # 存储as号到info的映射关系
    as_info_file = 'D:/Code/Crawler4Caida/000LocalData/as_Gao/asn_info.txt'
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        as_number = line[0]
        as_desrc = line[1].strip().split(",")[0:-1]
        as_desrc = ' '.join(as_desrc)
        as_desrc = as_desrc.strip()
        as_country = line[1].strip().split(",")[-1].strip()
        as2info[as_number] = [as_desrc, as_country]
    return as2info


def gain_asns_info():
    """
    根据asns.jsonl提取有用asn信息
    """
    as2info = gain_as2info()
    asns_file = "D:/Code/Crawler4Caida/035NetwrokSimulation/asrank/asns.jsonl"
    cnt = 0  # 统计差集
    cnt_no_geo = 0  # 统计CAIDA ASN中geo信息缺失的记录
    with jsonlines.open(asns_file) as reader:
        for obj in reader:
            asn = obj["asn"]
            # rank = obj["rank"]
            # country = obj["country"]["iso"]
            longitude = obj["longitude"]
            latitude = obj["latitude"]
            if asn not in as2info.keys():
                cnt += 1
                # print(rank, asn, country, longitude, latitude)
            if longitude == 0:
                cnt_no_geo += 1
            
            if asn in as2info.keys() and longitude != 0:
                print(asn, as2info[asn], longitude, latitude)
                temp_list = []
                temp_list = as2info[asn]
                temp_list.append(longitude)
                temp_list.append(latitude)
                as2info[asn] = temp_list

    print("CAIDA ASNS共有%d个异常记录" % cnt)
    print("CAIDA ASNS共有%d个地理信息缺失记录" % cnt_no_geo)
    # print(as2info)
    result_list = []  # 存储结果数据
    for key in as2info.keys():
        temp_list = []
        temp_list.append(key)
        temp_list.extend(as2info[key])
        result_list.append(temp_list)
    save_path = "D:/Code/Crawler4Caida/058ASWhois/asns.csv"
    write_to_csv(result_list, save_path, ["# Whois Geo"])



if __name__ == "__main__":
    time_start = time.time()  # 记录程序启动的时间
    gain_asns_info()
    time_end = time.time()  # 记录程序结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")