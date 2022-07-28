# coding: utf-8
"""
create on Jul 28, 2022 by Wayne YU

Function:

根据要求，需要统计cn 2 Global的路由信息

原始数据：z20220320.txt
基础结果：
CN_ISP，v4前缀，v4地址量，目的网络，所属机构，所属国家，所属大洲，直达，[D国]
CN_ISP，v4前缀，v4地址量，目的网络，所属机构，所属国家，所属大洲，绕转，[A国、B国、D国]

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


def gain_country2continent():
    """
    获取国家对应的大洲信息
    :return country2contient:
    """
    location_file = '..\\000LocalData\\as_geo\\GeoLite2-Country-Locations-zh-CN.csv'
    country2continent = {}  # 存储国家到大洲的映射关系
    file_read = open(location_file, 'r', encoding='gbk')
    for line in file_read.readlines():
        line = line.strip().split(",")
        country_code = line[4]
        continent_code = line[2]
        country2continent[country_code] = continent_code
    return country2continent


def rib_analysis(rib_file):
    """
    分析RIB数据，统计CN去往全球各国的路由路径，含直达和绕转等
    :param rib_file:
    :return:
    """
    cn2global_result = []  # 存储最终输出的结果数据
    as2country_dic = gain_as2country_caida()
    as2org_dic = gain_as2org_caida()
    country2contient_dic = gain_country2continent()
    print(f"AS4134's Country is {as2country_dic['4134']}")
    file_read = open(rib_file, 'r', encoding='utf-8')
    all_prefix_num = 0  # 统计国内节点总的条目
    except_info_list = []  # 存储异常记录信息
    for line in file_read.readlines():
        line = line.strip().split("|")
        v4_prefix = line[5]
        as_path = line[-2].split(" ")
        if str(v4_prefix).find("0.0.0.0/0") != -1:
            print(v4_prefix)
            continue
        all_prefix_num += 1
        cn_isp = as_path[0]
        v4_num = len(IP(v4_prefix))
        origin_as = as_path[-1]

        origin_as_country = "ZZ"
        try:
            origin_as_country = as2country_dic[str(origin_as)]
        except Exception as e:
            except_info_list.append(e)

        origin_as_org = "ZZ"
        try:
            origin_as_org = as2org_dic[str(origin_as)]
        except Exception as e:
            except_info_list.append(e)

        origin_as_continent = "ZZ"
        try:
            origin_as_continent = country2contient_dic[str(origin_as_country)]
        except Exception as e:
            except_info_list.append(e)

        """
        构建Country Path
        """
        country_path = []  # 将as path转换为country path
        for as_item in as_path:
            temp_country = "ZZ"
            try:
                temp_country = as2country_dic[str(as_item)]
            except Exception as e:
                except_info_list.append(e)
            country_path.append(temp_country)
        """
        处理Country Path，将某个国家中的多跳，处理为1跳
        """
        country_path_deal = []  # 存储处理后的国家path
        flag_country = country_path[0]
        country_path_deal.append(flag_country)
        for i in range(len(country_path)):
            if country_path[i] != flag_country:
                flag_country = country_path[i]
                country_path_deal.append(flag_country)

        # temp_line = [cn_isp, v4_prefix, v4_num,
        #              origin_as, origin_as_org, origin_as_country, origin_as_continent,
        #              (len(country_path_deal) - 1),
        #              country_path_deal,
        #              as_path,
        #              country_path]
        temp_line = [cn_isp, v4_prefix, v4_num,
                     origin_as, origin_as_country, origin_as_continent,
                     (len(country_path_deal) - 1),
                     country_path_deal]
        # print(temp_line)
        cn2global_result.append(temp_line)

    print("国内节点采集路由条目总数：", all_prefix_num)
    save_file = "../000LocalData/as_cn/cn2global_result.csv"
    write_to_csv(cn2global_result, save_file)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    rib_analysis("..\\000LocalData\\RU&UA\\rib\\z20220320.txt")
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
