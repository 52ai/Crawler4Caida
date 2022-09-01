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
    :return cn2global_result:
    """
    cn2global_result = []  # 存储最终输出的结果数据
    cn2global_result_simple = []  # 存储简洁的结果
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
        cn_isp = as_path[0]
        if str(v4_prefix).find("0.0.0.0/0") != -1:
            print(v4_prefix)
            continue

        if cn_isp not in ["9808"]:
            continue

        all_prefix_num += 1
        v4_num = len(IP(v4_prefix))
        origin_as = as_path[-1]
        if as_path[-1].find("{") != -1:
            origin_as = as_path[-1].strip("{").strip("}").split(",")[0]

        origin_as_country = "ZZ"
        try:
            origin_as_country = as2country_dic[str(origin_as)]
            if len(origin_as_country) == 0:
                origin_as_country = "ZZ"
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
                if len(temp_country) == 0:
                    temp_country = "ZZ"
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
        temp_line_simple = ["as"+cn_isp, "as"+origin_as, origin_as_country, v4_num,
                            "P"+str((len(country_path_deal) - 1)),
                            country_path_deal,
                            as_path]

        cn2global_result.append(temp_line)
        cn2global_result_simple.append(temp_line_simple)

    print("国内节点采集路由条目总数：", all_prefix_num)
    save_file = "../000LocalData/as_cn/cn2global_result_simple_AS9808.csv"
    write_to_csv(cn2global_result_simple, save_file)
    return cn2global_result


def final_analysis(cn2global_result):
    """
    根据基础结果数据，做二次分析
    1、CN 网络去往全球各国的路径，中有多少直达，有多少绕转，比例各是多少
    2、分CN运营商看，直达、绕转，及其比例
    3、分国家看，针对某国我们直达和绕转情况，及其比例
    4、分自治域网络看，针对某自治域网络，我们直达和绕转，及其比例
    :param cn2global_result:
    :return:
    """
    print("- - - - -  - - - - CN2GLOBAL 二次分析- - - - - - - - - - - - - ")
    path_cnt_dict = {}  # CN网络通往全球各国直达或绕转的统计分布情况
    v4_num_cnt_dict = {}  # CN网络通往全球各国直达或绕转的IP地址数量统计分布情况

    for line in cn2global_result:
        # print(line)
        path_cnt = line[6]
        v4_num_cnt = line[2]
        if path_cnt not in path_cnt_dict.keys():
            path_cnt_dict[path_cnt] = 1
            v4_num_cnt_dict[path_cnt] = v4_num_cnt
        else:
            path_cnt_dict[path_cnt] += 1
            v4_num_cnt_dict[path_cnt] += v4_num_cnt

    print(path_cnt_dict)
    print(v4_num_cnt_dict)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    cn2global = rib_analysis("..\\000LocalData\\RU&UA\\rib\\z20220320.txt")
    final_analysis(cn2global)

    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
