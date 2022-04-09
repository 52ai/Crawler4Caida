# coding:utf-8
"""
create on Apr 9, 2022 By Wayne YU

Function:

统计国内节点的路由，两端都是国内，但需要去国外绕转的情况

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


def rib_analysis(rib_file):
    """
    分析RIB数据，统计两端都是国内，中间有出国的情况
    :param rib_file:
    :return:
    """
    as2country_dic = gain_as2country_caida()
    print("AS4134's Country:", as2country_dic['4134'])
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
            print(v4_prefix)
            continue
        all_prefix_num += 1
        left_country = "ZZ"
        right_country = "ZZ"

        try:
            left_country = as2country_dic[str(as_path[0])]
            right_country = as2country_dic[str(as_path[-1])]
        except Exception as e:
            except_info_list.append(e)

        if left_country == "CN" and right_country == "CN":
            internal_prefix_list.append(v4_prefix)
            for item_as in as_path[1:-1]:
                temp_country = "ZZ"
                try:
                    temp_country = as2country_dic[str(item_as)]
                except Exception as e:
                    except_info_list.append(e)
                if temp_country == "":
                    temp_country = "ZZ"

                if temp_country != "CN" and temp_country != "ZZ":
                    print(v4_prefix, as_path, temp_country)
                    bypass_abroad.append([v4_prefix, as_path, temp_country])
                    bypass_abroad_prefix_list.append(v4_prefix)
                    break
    print("国内节点采集路由条目总数：", all_prefix_num)
    print("两端都在国内的路由条目数量:", len(internal_prefix_list), "去重后：", len(set(internal_prefix_list)))
    print("两端在国内，中间经过国外的路由条目数量：", len(bypass_abroad_prefix_list), "去重后:", len(set(bypass_abroad_prefix_list)))
    """
    统计IP地址
    """
    internal_ip_num = 0  # 统计两端都在国内的IP量
    for item in list(set(internal_prefix_list)):
        internal_ip_num += len(IP(item))

    bypass_abroad_ip_num = 0  # 统计需要去国外绕转的IP量
    for item in list(set(bypass_abroad_prefix_list)):
        bypass_abroad_ip_num += len(IP(item))

    print("两端都在国内的IP地址数量：", internal_ip_num)
    print("需要经过国外的IP地址数量:", bypass_abroad_ip_num, "占比：", bypass_abroad_ip_num/internal_ip_num)

    save_file = "..\\000LocalData\\RU&UA\\bypass_abroad.csv"
    write_to_csv(bypass_abroad, save_file)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    rib_analysis("..\\000LocalData\\RU&UA\\rib\\z20220220.txt")
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
