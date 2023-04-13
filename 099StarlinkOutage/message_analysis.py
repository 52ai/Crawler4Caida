# coding:utf-8
"""
create on Apr 13, 2023 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

分析下UTC时间20230408 00：20-00:35之间的前缀撤销信息

"""

import time
import csv
from IPy import IP


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return None:
    """
    print("write file<%s> ..." % des_path)
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


def analysis():
    """
    根据message报文，分析前缀撤销的信息
    :return:
    """
    file_in_rib = "../000LocalData/BGPData/rib_live/rib_2023-01-13_181.txt"
    as14593_prefix = []
    with open(file_in_rib, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.find("#") != -1:
                continue
            line = line.strip().split("|")
            # print(line)
            origin_as = line[-2].split(" ")[-1]
            v4_prefix = line[5]
            # print(origin_as, v4_prefix)
            if origin_as == "14593":
                as14593_prefix.append(v4_prefix)
    print("AS14593前缀总数：", len(set(as14593_prefix)))
    as14593_ip_num = 0
    for prefix in set(as14593_prefix):
        as14593_ip_num += len(IP(prefix))
    print("AS14593地址总数：", as14593_ip_num)

    file_in = "../000LocalData/BGPData/message_live/birdmrt_messages_2023-04-08_08_35_19.txt"
    w_prefix_list = []
    with open(file_in, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split("|")
            if line[2] == "W":
                # print(line)
                w_prefix_list.append(line[-1])
    print(file_in)
    print("Message报文撤销前缀总记录数:", len(w_prefix_list))
    print("Message报文撤销前缀总记录数（去重后）:", len(set(w_prefix_list)))

    match_prefix = set(w_prefix_list).intersection(set(as14593_prefix))
    print("反查匹配出AS14593被撤销的前缀总数:", len(match_prefix), "占比：", len(match_prefix)/len(set(as14593_prefix)))

    """
    计算被撤销的总的地址量
    """
    w_ip_num = 0
    w_ip_list = []  # 存储所有被撤销的IP地址
    for prefix in match_prefix:
        w_ip_num += len(IP(prefix))
        w_ip_list.extend(IP(prefix))
    print("反查匹配出AS14593被撤销的地址总数:", w_ip_num, "占比:", w_ip_num/as14593_ip_num)

    result_list = []
    for item in match_prefix:
        result_list.append(["as14593", item])

    save_path = "./match_withdraw_prefix.csv"
    write_to_csv(result_list, save_path)

    """
    参考feed数据（https://geoip.starlinkisp.net/feed.csv），做两个事：
    1）feed数据中所有IP地址的总量，国家或城市分布；
    2）此次事件被撤销的IP地址中，国家或城市分布。
    """
    feed_file = "./feed_v4.csv"
    feed_ip_list = []  # 存储feed文件中所有的IP地址
    ip_geo_dic = {}  # 存储IP地址的国家信息
    with open(feed_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            feed_ip_list.extend(IP(line[0]))
            for ip_item in IP(line[0]):
                if ip_item not in ip_geo_dic.keys():
                    ip_geo_dic[ip_item] = [line[1], line[3]]

    print("Starlink Geo 数据集IP总量:", len(ip_geo_dic.keys()))
    # print(ip_geo_dic)
    feed_ip_country = {}  # 统计feed数据中国家分布
    feed_ip_city = {}  # 统计feed数据中城市分布
    for key in ip_geo_dic.keys():
        if ip_geo_dic[key][0] not in feed_ip_country.keys():
            feed_ip_country[ip_geo_dic[key][0]] = 1
        else:
            feed_ip_country[ip_geo_dic[key][0]] += 1

        if ip_geo_dic[key][1] not in feed_ip_city.keys():
            feed_ip_city[ip_geo_dic[key][1]] = 1
        else:
            feed_ip_city[ip_geo_dic[key][1]] += 1

    print("Starlink(AS14593)地面站涉及的国家或地区：", len(feed_ip_country.keys()))
    print("Starlink(AS14593)地面站涉及的城市：", len(feed_ip_city.keys()))

    print("Geo IP数据集与被撤销IP地址的匹配量:", len(set(feed_ip_list).intersection(set(w_ip_list))),
          "匹配度为:", len(set(feed_ip_list).intersection(set(w_ip_list)))/w_ip_num)

    """
    将地面站涉及的国家或城市的IP地址量进行排名
    """
    feed_ip_country_list = []
    for key in feed_ip_country.keys():
        feed_ip_country_list.append([key, feed_ip_country[key]])

    feed_ip_city_list = []
    for key in feed_ip_city.keys():
        feed_ip_city_list.append([key, feed_ip_city[key]])

    feed_ip_country_list.sort(reverse=True, key=lambda elem: int(elem[1]))
    save_path = "./infect_country_rank.csv"
    write_to_csv(feed_ip_country_list, save_path)

    feed_ip_city_list.sort(reverse=True, key=lambda elem: int(elem[1]))
    save_path = "./infect_city_rank.csv"
    write_to_csv(feed_ip_city_list, save_path)


if __name__ == "__main__":
    time_start = time.time()
    analysis()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
