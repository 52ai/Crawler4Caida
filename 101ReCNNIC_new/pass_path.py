# coding:utf-8
"""
create on Apr 28, 2023 By Wayne YU

Function:

借助RIB的分析，研究对关键网络的依赖（18家Tier1）

1）统计，去往全球的所有路径中，有多少需要经过这18家Tier1，占比多少；
2）其中依赖占比最高的是哪三家，涉及的路由路径数量分别是多少，占比分别是多少；
3）统计去往“一带一路”，东盟、欧洲、南美、非洲方向，对美的依赖占比；
4）如果TOP3的断了，我有多少路由路径数量被阻断（占比多少），将影响我与全球多少的网络互联（占比多少）；
5）更进一步当13家USTier1断了，影响间进一步扩大至多少。
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


def gain_country2group():
    """
    根据geo信息，输出每个国家对应的Group信息等item[7]:asean, item[8]:bay, item[9]:belt_and_road, item[10]:nato
    :return country2group:
    """
    country_2_group_file = '../000LocalData/ReCNNIC/Country-Locations-Group - ReCNNIC.csv'
    country2group_dict = {}  # 存储国家到Group的映射关系
    file_read = open(country_2_group_file, 'r', encoding='gbk')
    for line in file_read.readlines():
        line = line.strip().split(",")
        if line[0] == "ID":
            # print(line)
            continue
        if line[4] not in country2group_dict.keys():
            country2group_dict[line[4]] = line
    return country2group_dict


def gain_as2country_caida():
    """
    根据Caida asn info获取as对应的国家信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_country = line[-1]
        as2country[as_number] = as_country
    return as2country


def rib_analysis(rib_file):
    """
    分析as path情况，按需要统计数据
    :param rib_file:
    :return:
    """
    print(rib_file)
    as2country = gain_as2country_caida()
    country2group = gain_country2group()

    tier1_list = ['3356', '174', '2914', '6939', '3257',
                  '701', '7018', '1239', '3549', '7922',
                  '3320', '6830', '5511', '3491', '6762',
                  '1299', '12956', '6461']

    all_path_num = 0  # 统计所有去国外的路径
    pass_tier1_as_list = []  # 存储所有需要经过tier1去往的网络数量
    tier1_rely_dict = {}
    group_country_as_dict = {"asean": [],
                             "belt_and_road": [],
                             "eu": [],
                             "sa": [],
                             "af": []}

    group_country_as_pass_us_dict = {"asean": [],
                                     "belt_and_road": [],
                                     "eu": [],
                                     "sa": [],
                                     "af": []}
    except_info = []  # 存储异常记录
    with open(rib_file, 'r', encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split("|")
            v4_prefix = line[5]
            as_path = line[-2].split(" ")
            if str(v4_prefix).find("0.0.0.0/0") != -1:
                # 剔除全零路由
                continue
            all_path_num += 1
            for item_as in as_path:
                if item_as in tier1_list:
                    pass_tier1_as_list.append(as_path[-1])
                    if item_as not in tier1_rely_dict.keys():
                        tier1_rely_dict[item_as] = [as_path[-1]]
                    else:
                        tier1_rely_dict[item_as].append(as_path[-1])

            # 判断这条路径的起源AS是否为目标方向
            try:
                item_as_country = as2country[as_path[-1]]
                country_info = country2group[item_as_country]
                if country_info[7] == "1":
                    group_country_as_dict["asean"].append(as_path)
                if country_info[9] == "1":
                    group_country_as_dict["belt_and_road"].append(as_path)
                if country_info[2] == "EU":
                    group_country_as_dict["eu"].append(as_path)
                if country_info[2] == "SA":
                    group_country_as_dict["sa"].append(as_path)
                if country_info[2] == "AF":
                    group_country_as_dict["af"].append(as_path)
            except Exception as e:
                except_info.append(e)

    print("采集所有路由路径数量：", all_path_num)
    print(f"其中{len(pass_tier1_as_list)}条路由路径需要经过18家Tier1,约占总路由路径的{round(len(pass_tier1_as_list) / all_path_num, 6)}")
    print(f"其中{len(set(pass_tier1_as_list))}个网络需要经过18家Tier1,约占全球网络的{round(len(set(pass_tier1_as_list))/74000, 6)}(初步考虑：有一条路径过了就算过了)")
    tier1_rely_list = []  # 存储Tier1依赖的数据, [Tier1 ASN, 涉及到的路由路径数量，占全部路由路径比例]
    for item_tier1 in tier1_rely_dict.keys():
        tier1_rely_list.append(["AS"+item_tier1, len(tier1_rely_dict[item_tier1]), round(len(tier1_rely_dict[item_tier1])/all_path_num, 6)])
    tier1_rely_list.sort(reverse=True, key=lambda elem: elem[2])
    print("我国网络路由路径依赖度最高网络排名：")
    for item in tier1_rely_list[0:5]:
        print(item)

    for item_key in group_country_as_dict.keys():
        for item_path in group_country_as_dict[item_key]:
            for item_as in item_path:
                try:
                    item_as_country = as2country[item_as]
                    if item_as_country == "US":
                        group_country_as_pass_us_dict[item_key].append(item_path)
                        break
                except Exception as e:
                    except_info.append(e)

    print("一带一路方向总路径:", len(group_country_as_dict["belt_and_road"]),
          ", 经美网络的路径数量:", len(group_country_as_pass_us_dict["belt_and_road"]),
          ", 占比：", round(len(group_country_as_pass_us_dict["belt_and_road"])/len(group_country_as_dict["belt_and_road"]), 6))

    print("东盟方向总路径:", len(group_country_as_dict["asean"]),
          ", 经美网络的路径数量:", len(group_country_as_pass_us_dict["asean"]),
          ", 占比：", round(len(group_country_as_pass_us_dict["asean"])/len(group_country_as_dict["asean"]), 6))

    print("欧洲方向总路径:", len(group_country_as_dict["eu"]),
          ", 经美网络的路径数量:", len(group_country_as_pass_us_dict["eu"]),
          ", 占比：", round(len(group_country_as_pass_us_dict["eu"])/len(group_country_as_dict["eu"]), 6))

    print("南美方向总路径:", len(group_country_as_dict["sa"]),
          ", 经美网络的路径数量:", len(group_country_as_pass_us_dict["sa"]),
          ", 占比：", round(len(group_country_as_pass_us_dict["sa"])/len(group_country_as_dict["sa"]), 6))

    print("非洲方向总路径:", len(group_country_as_dict["af"]),
          ", 经美网络的路径数量:", len(group_country_as_pass_us_dict["af"]),
          ", 占比：", round(len(group_country_as_pass_us_dict["af"])/len(group_country_as_dict["af"]), 6))

    top3_rate = round((len(tier1_rely_dict["3356"]) + len(tier1_rely_dict["174"]) + len(tier1_rely_dict["3257"]))/all_path_num, 6)
    top3_rely_as_list = []
    top3_rely_as_list.extend(tier1_rely_dict["3356"])
    top3_rely_as_list.extend(tier1_rely_dict["174"])
    top3_rely_as_list.extend(tier1_rely_dict["3257"])
    top3_rate_as = round(len(set(top3_rely_as_list))/74000, 6)
    print("TOP3中断(涉及路由路径):", top3_rate)
    print("TOP3中断(初步考虑：影响的网络，有一个前缀影响了就算影响了):", top3_rate_as)

    tier1_list_us = ['3356', '174', '2914', '6939', '3257',
                     '6461', '6451', '3491', '1239', '701',
                     '7018', '7922', '3549']
    us13_rate = 0
    us13_rely_as_list = []
    for item_key in tier1_rely_dict.keys():
        if item_key in tier1_list_us:
            us13_rate += round(len(tier1_rely_dict[item_key])/all_path_num, 6)
            us13_rely_as_list.extend(tier1_rely_dict[item_key])
    us13_rate_as = round(len(set(us13_rely_as_list))/74000, 6)
    print("US13中断(涉及路由路径):", us13_rate)
    print("US13中断(初步考虑：影响的网络，有一个前缀影响了就算影响了):", us13_rate_as)



if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    rib_analysis("..\\000LocalData\\BGPData\\rib_live\\rib_2023-01-13_181.txt")
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
