# coding:utf-8
"""
create on June 20, 2020 By Wenyan YU
Function:

根据as2ip数据，统计每个AS所拥有的v4地址数量和v6地址数量（实际路由通告的监测数据）

"""
import time
import csv
import struct
import socket


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
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


def gain_as2ip_quantity():
    """
    统计每个AS网内的v4和v6地址数量
    :return:
    """
    as2ip_quantity = []  # 存储AS号，v4地址数量，v6地址数量（/64）
    as2ip_file = "..\\000LocalData\\as_Gao\\asn2ip.txt"
    as2ip_file_read = open(as2ip_file, 'r')
    line_cnt = 0
    for line in as2ip_file_read.readlines():
        line = line.strip().split("\t")
        prefix_list = line[1].split(',')
        print("AS%s" % line[0])
        v4_seg_cnt = 0  # 统计该AS v4地址段的IP地址数
        v6_seg_cnt = 0  # 统计该AS v6地址段的IP地址数
        for item in prefix_list:
            # print(item.find("/"))
            if item.find("/") == -1:
                # print("V4")
                """
                V4地址数的统计直接计算前后IP区间内的有效IP数目即可
                """
                ip_seg = item.split("-")
                ips = find_ips(ip_seg[0], ip_seg[1])
                # print(len(ips))
                v4_seg_cnt += len(ips)
            else:
                # print("V6")
                """
                V6地址数的统计直接获取网络号的长度，用128减去网络号长度，大约为2的N次方个地址
                由于地址空间巨大，按照/64地址块的数量进行统计
                """
                net_len = int(item.split("/")[-1])
                # print(net_len)
                v6_seg_cnt += pow(2, (64-net_len))
        print("V4（%s）, V6(%s)" % (v4_seg_cnt, v6_seg_cnt))
        as_name = "AS"+str(line[0])
        as2ip_quantity.append([as_name, v4_seg_cnt, v6_seg_cnt])
        # if line_cnt > 100:
        #     break
        line_cnt += 1
    save_path = "../000LocalData/caict_display/as2ip_quantity.csv"
    write_to_csv(as2ip_quantity, save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    gain_as2ip_quantity()
    time_end = time.time()  # 记录结束的时间
    print("\n=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
