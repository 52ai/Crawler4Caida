# coding:utf-8
"""
create on Nov 16, 2021 By Wayne YU

Function

根据波哥的要求，统计CN&US各自的直接互联网络数量以及其Peer和Transit关系

"""
import time
import csv
import os


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return None:
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter="|")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_as2country():
    """
    根据as info数据，生成AS与国家对应字典
    :return as2country:
    """
    asn_info_file = "../000LocalData/as_Gao/asn_info.txt"
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(asn_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        asn = line[0]
        as_country = line[1].strip().split(",")[-1].strip()
        as2country[asn] = as_country
    return as2country


def external_as_analysis(target_country):
    """
    分析指定国家的对外互联关系
    :param target_country:
    :return:
    """
    as2country = gain_as2country()
    print(target_country)
    # 获取1998至今全球BGP互联关系存储文件
    file_path = []
    for root, dirs, files in os.walk("../000LocalData/as_relationships/serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))

    for path_item in file_path[-1:]:
        print(path_item)
        # 遍历一次文件，获取该国出口AS数量
        file_read = open(path_item, 'r', encoding='utf-8')
        external_cnt = 0  # 存储该国出口互联关系的数量
        external_as_list = []  # 存储该国出口AS
        dire_as = []  # 存储与该国网络直联的网络
        direct_as_peer = []  # 存储与该国网络对等直联的国外网络
        direct_as_transit_customer = []  # 存储与该国网络转接直联的国外客户网络
        direct_as_transit_provider = []  # 存储与该国网络转接直联的国外提供商网络
        country_as_list = []  # 存储该国的活跃AS号
        external_country_list = []  # 存储该国出口互联的国家
        for line in file_read.readlines():
            if line.strip().find("#") == 0:
                continue
            try:
                if as2country[str(line.strip().split('|')[0])] == target_country:
                    country_as_list.append(str(line.strip().split('|')[0]))  # 统计该国活跃as网络数量
                if as2country[str(line.strip().split('|')[1])] == target_country:
                    country_as_list.append(str(line.strip().split('|')[1]))  # 统计该国活跃as网络数量

                if as2country[str(line.strip().split('|')[0])] == target_country:
                    if as2country[str(line.strip().split('|')[1])] != target_country:
                        external_cnt += 1
                        external_as_list.append(str(line.strip().split('|')[0]))
                        external_country_list.append(as2country[str(line.strip().split('|')[1])])
                        if int(line.strip().split('|')[2]) == 0:
                            direct_as_peer.append(str(line.strip().split('|')[1]))
                            dire_as.append(str(line.strip().split('|')[1]))  # 存储国外直联
                        if int(line.strip().split('|')[2]) == -1:
                            direct_as_transit_customer.append(str(line.strip().split('|')[1]))
                            dire_as.append(str(line.strip().split('|')[1]))  # 存储国外直联

                else:
                    if as2country[str(line.strip().split('|')[1])] == target_country:
                        external_cnt += 1
                        external_as_list.append(str(line.strip().split('|')[1]))
                        external_country_list.append(as2country[str(line.strip().split('|')[0])])
                        if int(line.strip().split('|')[2]) == 0:
                            direct_as_peer.append(str(line.strip().split('|')[0]))
                            dire_as.append(str(line.strip().split('|')[0]))  # 存储国外直联
                        if int(line.strip().split('|')[2]) == -1:
                            direct_as_transit_provider.append(str(line.strip().split('|')[0]))
                            dire_as.append(str(line.strip().split('|')[0]))  # 存储国外直联
            except Exception as e:
                # print(e)
                pass
        external_as_list = list(set(external_as_list))
        print("该国活跃AS数量:", len(list(set(country_as_list))))
        print("该国网络与国外网络互联关系数量:", external_cnt)
        print("该国与国外存在互联关系的网络数量:", len(external_as_list))
        print("该国直接互联的国家数量:", len(list(set(external_country_list))))
        print("该国直接互联的网络数量:", len(list(set(dire_as))))
        print("与该国网络对等直联的国外网络数量:", len(list(set(direct_as_peer))))
        print("与该国网络转接直联的国外客户网络数量:", len(list(set(direct_as_transit_customer))))
        print("与该国网络转接直联的国外提供商网络数量:", len(list(set(direct_as_transit_provider))))

        # 统计互联国家方向的排名
        external_country_rank = {}
        for item in list(set(external_country_list)):
            external_country_rank[item] = 0
        for item in external_country_list:
            external_country_rank[item] += 1
        # print(len(external_country_rank))
        # 将字典转为列表
        external_country_rank_list = []
        temp_list = []
        for item in external_country_rank.keys():
            temp_list.append(item)
            temp_list.append(external_country_rank[item])
            external_country_rank_list.append(temp_list)
            temp_list = []
        # print(external_country_rank_list)
        external_country_rank_list.sort(reverse=True, key=lambda elem: int(elem[1]))
        # print(external_country_rank_list)
        temp_str = path_item.split('\\')[-1]
        date_str = str(temp_str).split('.')[0]
        save_path = "./" + target_country + "_external" + str(date_str) + ".csv"
        write_to_csv(external_country_rank_list, save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    country_list = ["CN", "US"]
    for country in country_list:
        external_as_analysis(country)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")

