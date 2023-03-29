# coding:utf-8
"""
create on Mar 29, 2022 By Wayne YU

Function:

针对CNNIC的数据做回应分析
CN TOP100 AS（按IPv4地址数量排名）间的通路：通过三大运营商骨干网RIB，获取全部路径，然后进一步分析国外绕转的情况

"""
import time
import csv
from IPy import IP


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


def gain_as2org_caida():
    """
    根据Caida asn info获取as对应的org信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2org_dic = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_org = line[2] + "," + line[1]
        as2org_dic[as_number] = as_org
    return as2org_dic


def gain_cn_topn_as(topn):
    """
    根据IPv4地址量排名，获取cn top n自治域列表
    :param topn:
    :return cn_topn_as_list:
    """
    cn_topn_as_list = []
    with open("../000LocalData/ReCNNIC/cn_as.csv", "r", encoding="utf-8") as f:
        for item in f.readlines():
            item = item.strip().split(",")
            asn = item[1].strip("AS")
            rank_id = int(item[0])
            cn_topn_as_list.append(asn)
            if rank_id >= topn:
                break
    return cn_topn_as_list


def rib_analysis(rib_file):
    """
    分析RIB数据，统计两端都是国内，中间有出国的情况
    :param rib_file:
    :return:
    """
    as2country_dic = gain_as2country_caida()
    as2org_dic = gain_as2org_caida()
    left_as_list = ["4134", "4837", "9808"]
    cn_top100_as_list = gain_cn_topn_as(590)  # 获取CN TOP 100的列表
    # print("CN TOP100 AS:", cn_top100_as_list)
    # print("AS4134's Country:", as2country_dic['4134'])

    file_read = open(rib_file, 'r', encoding='utf-8')
    all_prefix_num = 0  # 统计国内节点采集到的全部路由条目
    internal_prefix_list = []  # 统计国内节点采集到的两端都在国内的路由条目
    bypass_abroad = []  # 统计两端在国内，中间经过国外的路由前缀及AS PATH
    bypass_abroad_prefix_list = []  # 统计两端在国内，中间经过国外的路由前缀
    except_info_list = []  # 存储异常记录信息
    for line in file_read.readlines():
        line = line.strip().split("|")
        v4_prefix = line[5]
        as_path = line[-2].split(" ")
        if str(v4_prefix).find("0.0.0.0/0") != -1:
            # 剔除全零路由
            # print(v4_prefix)
            continue
        all_prefix_num += 1
        left_country = "ZZ"
        right_country = "ZZ"

        try:
            left_country = as2country_dic[str(as_path[0])]
            right_country = as2country_dic[str(as_path[-1])]
        except Exception as e:
            except_info_list.append(e)

        if str(as_path[0]) in left_as_list and str(as_path[-1]) in cn_top100_as_list:  # 找出CN top100 AS间的总的路由路径
            internal_prefix_list.append(v4_prefix)
            for item_as in as_path[1:-1]:  # 遍历as path，获取每一跳的国别
                temp_country = "ZZ"
                try:
                    temp_country = as2country_dic[str(item_as)]
                except Exception as e:
                    except_info_list.append(e)

                if temp_country == "":
                    temp_country = "ZZ"

                if temp_country != "CN" and temp_country != "ZZ":  # 找出中间出境绕的路

                    right_as_org = "ZZ"  # 获取源AS的机构信息
                    try:
                        right_as_org = as2org_dic[str(as_path[-1])]
                    except Exception as e:
                        except_info_list.append(e)

                    # print(v4_prefix, as_path, temp_country, as_path[-1], right_as_org)
                    bypass_abroad.append([v4_prefix, as_path, item_as, temp_country, as_path[-1], right_as_org])
                    bypass_abroad_prefix_list.append(v4_prefix)
                    break

    print("三家运营商骨干网采集路由总数：", all_prefix_num)
    print("CN TOP100 AS间的路由路径数量:", len(internal_prefix_list), "——去重后：", len(set(internal_prefix_list)))
    print("CN TOP100 AS间经境外绕转的路由路径数量：", len(bypass_abroad_prefix_list), "——去重后:", len(set(bypass_abroad_prefix_list)))
    print("CN TOP100 AS间经境外绕转的路由路径数量（去重后）占比：", len(set(bypass_abroad_prefix_list))/len(set(internal_prefix_list)))

    """
    统计IP地址
    """
    internal_ip_num = 0  # CN TOP100 AS间的路由路径，换算成IP地址数量
    for item in list(set(internal_prefix_list)):
        internal_ip_num += len(IP(item))

    bypass_abroad_ip_num = 0  # CN TOP100 AS间经境外绕转的路由路径，换算成IP地址数量
    for item in list(set(bypass_abroad_prefix_list)):
        bypass_abroad_ip_num += len(IP(item))

    print("CN TOP100 AS间的路由路径，换算成IP地址数量：", internal_ip_num)
    print("CN TOP100 AS间经境外绕转的路由路径，换算成IP地址数量:", bypass_abroad_ip_num, "占比：", bypass_abroad_ip_num/internal_ip_num)

    save_file = "..\\000LocalData\\ReCNNIC\\bypass_abroad.csv"
    write_to_csv(bypass_abroad, save_file)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    rib_analysis("..\\000LocalData\\BGPData\\rib_live\\rib_2023-01-13_181.txt")
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
