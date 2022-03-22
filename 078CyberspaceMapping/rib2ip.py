# coding:utf-8
"""
create on Mar 22, 2022 By Wayne YU
Function:

随着对BGP研究的不断深入，对于网络空间测绘的需求呼之欲出。
凡事”行胜于言“，与其坐而论道，不如去实践。
牢牢把握“在干中学，在学中干”的策略。


基于BGP RIB数据，分析现网可见的IP地址，及其归属情况，通过对全球IP地址进行拆分，然后逐一分析研究

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
        if len(as_country) != 0:
            as2country[as_number] = as_country
    return as2country


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
    分析RIB数据
    :param rib_file:
    :return result_list_final:
    """
    print(rib_file)
    as2country_dic = gain_as2country_caida()  # AS与国家的对应关系
    country2continent_dic = gain_country2continent()  # 国家与大洲的对应关系
    except_info_list = []  # 记录异常信息
    file_read = open(rib_file, 'r', encoding='utf-8')
    """
    Step1:统计到达所有AS网络的前缀及其AS PATH
    以目的ASN作为key，[[ip_prefix, as_path], ...]作为value
    构建中国去往全球目的ASN的前缀和路径
    """
    as_dict = {}
    for line in file_read.readlines():
        line = line.strip().split("|")
        v4_prefix = line[5]
        """
        剔除0.0.0.0/0的通告
        """
        if str(v4_prefix).find("0.0.0.0/0") != -1:
            print(v4_prefix)
            continue
        as_path = line[-2].split(" ")
        origin_as = as_path[-1]
        if origin_as.find("{") != -1:
            origin_as = origin_as.strip("{").strip("}").split(",")[0]
        if origin_as not in as_dict.keys():
            as_dict[origin_as] = [[v4_prefix, as_path]]
        else:
            as_dict[origin_as].append([v4_prefix, as_path])
    print("GLOBAL ORIGIN ASN COUNT:", len(as_dict.keys()))

    """
    STEP2:构建基础表(1)
    asn, country, v4_prefix_list
    """
    result_list = []  # 存储结果数据
    for key in as_dict.keys():
        asn = key
        country = "ZZ"
        try:
            country = as2country_dic[asn]
        except Exception as e:
            except_info_list.append(e)

        v4_prefix_list = []  # 存储所有v4的前缀，去重后
        for line in as_dict[key]:
            v4_prefix = line[0]
            if v4_prefix not in v4_prefix_list:
                v4_prefix_list.append(v4_prefix)
        result_list.append([asn, country, v4_prefix_list])

    """
    STEP3:构建基础表(2)
    asn, country, v4_num, continent, v4_prefix_list
    """
    result_list_final = []  # 存储最终结果数据
    for item in result_list:
        v4_num = 0  # 存储该网络的IPv4地址
        for v4_prefix in item[2]:
            v4_num += len(IP(v4_prefix))

        contient_code = "ZZ"
        try:
            contient_code = country2continent_dic[item[1]]
        except Exception as e:
            except_info_list.append(e)

        v4_prefix_string = ""
        for v4_p_s in item[2]:
            v4_prefix_string = v4_prefix_string + str(v4_p_s) + " "
        temp_line = [item[0], item[1], contient_code, v4_num, len(item[2]), v4_prefix_string]

        result_list_final.append(temp_line)
        # print(temp_line)
    save_file = "..\\000LocalData\\CyberspaceMapping\\rib2ip.txt"
    write_to_csv(result_list_final, save_file)
    return result_list_final


def ip_scan():
    """
    根据rib分析的IP数据，构建ip扫描元程序
    :return:
    """
    path_item = '..\\000LocalData\\RU&UA\\rib\\z20220320.txt'
    rib2ip_list = rib_analysis(path_item)
    """
    根据rib2ip结果数据构建对应国家的网络空间IP资产
    """

    aim_country = "RU"
    print("- - - - - - 开展%s的网络IP地址分析- - - - - - - - " % aim_country)
    ip_list = []
    for item in rib2ip_list:
        if item[1] == aim_country:
            for v4_prefix in item[-1].strip().split(" "):
                # print(v4_prefix)
                for x in IP(v4_prefix):
                    ip_list.append(x)
    print("%s的IPv4地址规模为:%s" % (aim_country, len(ip_list)))
    ip_list_unique = set(ip_list)
    print("%s的IPv4地址规模为:%s(去重后)" % (aim_country, len(ip_list_unique)))
    save_file = "..\\000LocalData\\CyberspaceMapping\\"+aim_country+"_ip.txt"
    write_to_csv(ip_list_unique, save_file)

    aim_country = "UA"
    print("- - - - - - 开展%s的网络IP地址分析- - - - - - - - " % aim_country)
    ip_list = []
    for item in rib2ip_list:
        if item[1] == aim_country:
            for v4_prefix in item[-1].strip().split(" "):
                # print(v4_prefix)
                for x in IP(v4_prefix):
                    ip_list.append(x)
    print("%s的IPv4地址规模为:%s" % (aim_country, len(ip_list)))
    ip_list_unique = set(ip_list)
    print("%s的IPv4地址规模为:%s(去重后)" % (aim_country, len(ip_list_unique)))
    save_file = "..\\000LocalData\\CyberspaceMapping\\" + aim_country + "_ip.txt"
    write_to_csv(ip_list_unique, save_file)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    ip_scan()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
