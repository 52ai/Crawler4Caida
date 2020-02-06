# coding:utf-8
"""
create on Feb 6, 2020 By Wayne YU

Function:
根据TJ AS 列表，获取1-2个可以ping通的ip地址

"""

import time
import csv
import struct
import socket
import subprocess
import re
import random


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
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def find_ips(start, end):
    """
    根据传入的IP地址段，寻找有效ip地址
    :param start:
    :param end:
    :return ips:
    """
    ip_struct = struct.Struct('>I')
    start, = ip_struct.unpack(socket.inet_aton(start))
    end, = ip_struct.unpack(socket.inet_aton(end))
    ips = [socket.inet_ntoa(ip_struct.pack(i)) for i in range(start, end+1)]
    return ips


def shuffle_string_list(str_list):
    """
    对传入的str_list进行随机
    :param str_list:
    :return re_list:
    """
    re_list = []
    for iter_n in range(0, len(str_list)):
        index_n = random.randint(0, len(str_list)-1)
        # print(index_n)
        # print("str_list Length", len(str_list))
        re_list.append(str_list[index_n])
        del(str_list[index_n])
    return re_list


def find_ping_ac(ips):
    """
    根据传入的有效IP,进行ping测试，寻找能够ping通的ip地址
    :param ips:
    :return ips:
    """
    ips_ac = []
    ips = shuffle_string_list(ips)
    for ip_item in ips[0:10]:
        print("ping test:", ip_item)
        ftp_sub = subprocess.Popen("ping %s -n 1" % ip_item,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        ret = ftp_sub.stdout.read()
        str_ret = ret.decode('gbk')
        try:
            time_delay = re.findall('\d+ms', str_ret)[-1]
        except IndexError:
            time_delay = "INFINITE"
        if time_delay != "INFINITE":
            print("Accept!", ip_item, time_delay)
            ips_ac.append(ip_item)
        if len(ips_ac) == 1:
            return ips_ac
    ips_ac.append(ips[9])
    return ips_ac


def get_ip(as_number):
    """
    根据传入的as_number 获取可以ping的ip地址
    :param as_number:
    :return:
    """
    ip_list = []
    asn2ip_file = "..\\000LocalData\\as_Gao\\asn2ip.txt"
    file_read = open(asn2ip_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        if line[0] == as_number:
            ip_seg = line[1].split(",")[0].split("-")
            ips = find_ips(ip_seg[0], ip_seg[1])
            ips = find_ping_ac(ips)  # 在有效IP中，寻找能够ping通的地址
            # print(ips[0:3])
            ip_list = ips
    return ip_list


def as2ip(top_as_file):
    """
    根据传入的top_as列表，获取可以ping同的ip
    :param as_list:
    :return:
    """
    as_info_list = []
    temp_list = []
    file_read = open(top_as_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        print(line)
        as_item = line[0]
        ip_list = get_ip(as_item)
        temp_list.append("AS"+line[0])
        temp_list.append(line[1])
        temp_list.extend(ip_list)
        as_info_list.append(temp_list)
        print(temp_list)
        temp_list = []
    return as_info_list


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    as_info_file_in = '..\\000LocalData\\RUNet\\as_info_2_zf_Ping.csv'
    as_ip_info = as2ip(as_info_file_in)
    # save path
    save_path = "..\\000LocalData\\RUNet\\as_ip_info_2_zf_TJ.csv"
    write_to_csv(as_ip_info, save_path)
    time_end = time.time()
    print("\n=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")