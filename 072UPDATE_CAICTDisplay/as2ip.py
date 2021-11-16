# coding:utf-8
"""
create on Nov 3, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

通过RIPE RRC00节点的RIB来提取每个AS的路由通告，包括v4和v6

"""
import time
import csv
from IPy import IP


rrc00_rib_file = "../000LocalData/BGPData/bview.20211026.0000.txt"


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


def rib_analysis():
    """
    处理rib文件
    :return:
    """
    rib_dict = {}  # 存储ASN:[[],...]
    file_read = open(rrc00_rib_file, 'r', encoding="utf-8")
    for line in file_read.readlines():
        line = line.strip().split("|")
        ip_prefix = line[5]
        origin_as = line[6].split(" ")[-1]
        if origin_as not in rib_dict.keys():
            rib_dict[origin_as] = [ip_prefix]
        else:
            if ip_prefix not in rib_dict[origin_as]:
                rib_dict[origin_as].append(ip_prefix)
            else:
                pass
    print("RIB AS COUNT:", len(rib_dict.keys()))

    as2ip_quantity = []  # 存储as2ip字段，as,v4_prefix_num, v4_num, v6 prefix num, v6_num
    for key in rib_dict.keys():
        v4_prefix_num = 0
        v4_num = 0
        v6_prefix_num = 0
        v6_num = 0
        for item in rib_dict[key]:
            # print(item)
            if item.find(":") == -1:
                # print("V4")
                """
                V4的地址数大约为32减去网络号长度，大约为2的N次方个地址
                """
                net_len_v4 = int(item.split("/")[-1])
                if net_len_v4 == 0:
                    continue
                v4_num += pow(2, (32-net_len_v4))
                v4_prefix_num += 1
            else:
                # print("V6")
                """
                V6地址数的统计直接获取网络号的长度，用128减去网络号长度，大约为2的N次方个地址
                由于地址空间巨大，按照/64地址块的数量进行统计
                """
                net_len_v6 = int(item.split("/")[-1])
                if net_len_v6 == 0:
                    continue
                v6_num += pow(2, (64-net_len_v6))
                v6_prefix_num += 1
        as_name = "AS" + str(key)
        print(as_name)
        print("V4 Prefix(%s), V4（%s）, V6 Prefix(%s), V6(%s)" % (v4_prefix_num, v4_num, v6_prefix_num, v6_num))
        as2ip_quantity.append([as_name, v4_prefix_num, v4_num, v6_prefix_num, v6_num])
    save_path = "./as2ip_quantity.csv"
    write_to_csv(as2ip_quantity, save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    rib_analysis()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
