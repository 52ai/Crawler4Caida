# coding:utf-8
"""
create on Aug 17, 2020 By Wenyan YU
Email：ieeflsyu@outlook.com

Function:

用公开的BGP数据源，可能存在前缀数据的失真的情况，因此最好的方式就是拿C公司的RIB，直接分析其到全球前缀可达的信息
结合AS Path可分析出较为准确的全球可达比例，及其对U国的依赖性

本程序要是通过分析C公司RIB(prefix, as path)，统计其全球可达前缀（IP规模）中第一跳为U国所占的比例
prefix_U_rate、ip_U_rate


V2:
除了占比以外，还需要进一步分析出，剔除U国的影响后，有哪些AS是可达的，可达的前缀都是什么？
然后再把AS信息映射为国家，并在图中标识
操作后，分为两张图，AS网络的打点图以及全球各国AS可达性色块图

影响操作分为两个层次：
第一个层次，最优路由第一跳为U国的；
第二个层次，最优路由AS Path中只要存在U国的AS，则该前缀不可达。

此外还得分析下，三家企业直连网络的数量以及直联网络中U国的数量

以上均为学术研究探讨

V3:
只统计chinanet 两个层次操作后，全球各个国家受影响的占比
新增统计各个AS号分阶段的可达IP规模


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
    csvFile = open(des_path, 'w', newline='', encoding='gbk')
    try:
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def extract_as_info():
    """
    根据asn_info文件，提取as info 信息
    :return:
    """
    file_in = "../000LocalData/as_Gao/asn_info.txt"
    file_in_read = open(file_in, 'r', encoding='utf-8')
    as2country_dict = {}  # 存储as号和国家对应关系的字典
    for line in file_in_read.readlines():
        line = line.strip().split("\t")
        as2country_dict[line[0]] = line[1].split(",")[-1].strip()
    return as2country_dict


def gain_country_cn():
    """
    根据GeoLite2-Country-Locations-zh-CN.csv 获取国家简写到大洲和国家信息
    :return country_info_dict:
    """
    country_info_file = "../000LocalData/as_geo/GeoLite2-Country-Locations-zh-CN.csv"
    country_info_file_read = open(country_info_file, "r", encoding="utf-8")
    country_info_dict = {}
    for line in country_info_file_read.readlines():
        line = line.strip().split(",")
        # print(line[4], line[5], line[3])
        country_info_dict[line[4]] = [line[5], line[3]]
    # print(country_info_dict)
    return country_info_dict


def chinanet_rib_analysis(rib_file, u_as_group):
    """
    根据传入的rib CSV信息，统计在最优路由第一跳为U国的占比
    :param rib_file:
    :param u_as_group:
    :return:
    """
    as2country = extract_as_info()
    country_info_dict = gain_country_cn()
    # print(as2country)
    rib_file_read = open(rib_file, 'r')
    line_cnt = 0  # 记录行数
    invalid_cnt = 0  # 记录无效记录数
    valid_cnt = 0  # 记录有效记录数
    ip_num_cnt = 0  # 根据前缀统计IP规模，用32减去网络号的长度，大约为2的N次方个地址
    prefix_u_cnt = 0  # 记录最优路由第一跳为U国的前缀数量
    ip_num_u_cnt = 0  # 记录最优路由第一跳为U国的IP地址数量
    prefix_u_cnt_anywhere = 0  # 记录最优路由任意一跳含U国的前缀数量
    ip_num_u_cnt_anywhere = 0  # 记录最优路由任意一跳含U过的IP地址数量
    direct_networks_list = []  # 存储该ISP直联网络的列表
    direct_networks_u_list = []  # 存储该ISP直联属于U国的网络列表
    direct_networks_c_list = []  # 存储该ISP直联属于C国的网络列表

    global_reachable_as_list = []  # 存储总的全球可达网络的AS列表
    reachable_as_list_first = []  # 存储第一层次可达的AS列表
    reachable_as_list_second = []  # 存储第二层次可达的AS列表

    as_reach_dict_0 = dict()  # 存储0阶段的as可达IP规模表
    as_reach_dict_1 = dict()  # 存储1阶段的as可达IP规模表
    as_reach_dict_2 = dict()  # 存储2阶段的as可达IP规模表

    country_reach_0 = dict()  # 存储0阶段的国家可达IP规模表
    country_reach_1 = dict()  # 存储1阶段的国家可达IP规模表
    country_reach_2 = dict()  # 存储2阶段的国家可达IP规模表

    none_u_c_ip_num_0 = 0  # 统计0阶段非U和C的IP地址
    none_u_c_ip_num_1 = 0  # 统计1阶段非U和C的IP地址

    ip_num_u_0 = 0  # 统计0阶段U国IP地址量
    ip_num_c_0 = 0  # 统计0阶段C国IP地址量

    ip_num_u_1 = 0  # 统计1阶段U国IP地址量
    ip_num_c_1 = 0  # 统计1阶段C国IP地址量

    for line in rib_file_read.readlines():
        line = line.strip().split(",")
        line_cnt += 1
        # print(line)
        if line[0].find("/") == -1:
            # print(line)
            invalid_cnt += 1
            continue
        if len(line[1].strip()) == 0:
            invalid_cnt += 1
            continue

        ip_prefix = line[0].split("/")
        net_len = int(ip_prefix[1])
        ip_num_cnt += pow(2, (32-net_len))
        valid_cnt += 1
        # print(line[1].strip().split(" "))
        as_path_as = line[1].strip().split(" ")
        # print(as_path_as)
        first_hop_as = as_path_as[0]
        last_hop_as = as_path_as[-1].strip("{").strip("}")
        # 第0阶段操作
        # 存储AS的可达IP规模信息
        if last_hop_as in as_reach_dict_0.keys():
            as_reach_dict_0[last_hop_as] += pow(2, (32-net_len))
        else:
            as_reach_dict_0[last_hop_as] = pow(2, (32-net_len))

        # 第1阶段判断
        if first_hop_as in u_as_group:
            # print(first_hop_as)
            prefix_u_cnt += 1
            ip_num_u_cnt += pow(2, (32-net_len))
            try:
                if (as2country[last_hop_as] != "US") and (as2country[last_hop_as] != "CN"):
                    none_u_c_ip_num_1 += pow(2, (32-net_len))
            except Exception as e:
                pass

            if last_hop_as in as_reach_dict_1.keys():
                as_reach_dict_1[last_hop_as] += 0
            else:
                as_reach_dict_1[last_hop_as] = 0

        if first_hop_as not in u_as_group:
            # 如果某AS网有一个前缀可达，则该AS网可达
            reachable_as_list_first.append(last_hop_as)
            # 存储AS的可达IP规模信息
            if last_hop_as in as_reach_dict_1.keys():
                as_reach_dict_1[last_hop_as] += pow(2, (32-net_len))
            else:
                as_reach_dict_1[last_hop_as] = pow(2, (32-net_len))

            try:
                if as2country[last_hop_as] == "US":
                    ip_num_u_1 += pow(2, (32 - net_len))
                elif as2country[last_hop_as] == "CN":
                    ip_num_c_1 += pow(2, (32 - net_len))
            except Exception as e:
                pass

        u_flag = 0  # 是否路径是否含U国AS
        for item in as_path_as:
            try:
                item = item.strip("{").strip("}").strip("\"")
                if len(item) != 0:
                    if as2country[item] == "US":
                        u_flag = 1
                        break
            except Exception as e:
                # print(as_path_as)
                pass
        # 第2阶段判断
        if u_flag == 1:
            # 如果路径含U国AS
            # print(intersection_hop_set)
            prefix_u_cnt_anywhere += 1
            ip_num_u_cnt_anywhere += pow(2, (32-net_len))
            if last_hop_as in as_reach_dict_2.keys():
                as_reach_dict_2[last_hop_as] += 0
            else:
                as_reach_dict_2[last_hop_as] = 0

        if u_flag == 0:
            # 如果某AS网有一个前缀可达，则该AS网可达
            reachable_as_list_second.append(last_hop_as)
            # 存储AS的可达IP规模信息
            if last_hop_as in as_reach_dict_2.keys():
                as_reach_dict_2[last_hop_as] += pow(2, (32-net_len))
            else:
                as_reach_dict_2[last_hop_as] = pow(2, (32-net_len))

        direct_networks_list.append(first_hop_as)  # 存储直联网络AS
        global_reachable_as_list.append(last_hop_as)  # 存储该条可达前缀所属的AS网络
        try:
            if as2country[first_hop_as] == "US":
                # print(as2country[first_hop_as])
                direct_networks_u_list.append(first_hop_as)  # 存储直联网络为U国的网络
            elif as2country[first_hop_as] == "CN":
                direct_networks_c_list.append(first_hop_as)  # 存储直联网络为C国的网络
        except Exception as e:
            # print(e)
            pass

        try:
            if as2country[last_hop_as] == "US":
                ip_num_u_0 += pow(2, (32 - net_len))
            elif as2country[last_hop_as] == "CN":
                ip_num_c_0 += pow(2, (32 - net_len))
            if (as2country[last_hop_as] != "US") and (as2country[last_hop_as] != "CN"):
                none_u_c_ip_num_0 += pow(2, (32 - net_len))
        except Exception as e:
            # print(e)
            none_u_c_ip_num_0 += pow(2, (32 - net_len))
            pass

    # print(len(direct_networks_list))
    # print(len(direct_networks_u_list))
    direct_networks_list = list(set(direct_networks_list))
    direct_networks_u_list = list(set(direct_networks_u_list))
    direct_networks_c_list = list(set(direct_networks_c_list))

    global_reachable_as_list = list(set(global_reachable_as_list))
    reachable_as_list_first = list(set(reachable_as_list_first))
    reachable_as_list_second = list(set(reachable_as_list_second))

    """
    根据0阶段、1阶段、2阶段的各个AS网络，统计分阶段各个国家可达AS网络，然后计算其可达性
    根据可达性，分级统计
    
    然后再根据各大洲各方向，统计3级及其以上的国家个数
    
    分大洲，非洲、亚洲、欧洲、大洋洲、南美洲、北美洲
    分方向，东盟、一带、一路、G20、OECD
    
    
    """

    print("Excel总的行数:", line_cnt)
    print("无效记录数:", invalid_cnt)
    print("有效记录数:", valid_cnt)
    print("总的IP规模(v4):", ip_num_cnt)
    print("最优路由第一跳为U国的前缀数量:%s, 占比(%.6f)" % (prefix_u_cnt, prefix_u_cnt/valid_cnt))
    print("最优路由第一跳为U国的IP地址数量(V4):%s, 占比(%.6f)" % (ip_num_u_cnt, ip_num_u_cnt/ip_num_cnt))
    print("最优路由任意一跳含U国的前缀数量:%s, 占比(%.6f)" % (prefix_u_cnt_anywhere, prefix_u_cnt_anywhere/valid_cnt))
    print("最优路由任意一跳含U国的IP地址数量(V4):%s, 占比(%.6f)" % (ip_num_u_cnt_anywhere, ip_num_u_cnt_anywhere/ip_num_cnt))

    all_reach = len(global_reachable_as_list)
    reach_first = len(reachable_as_list_first)
    reach_second = len(reachable_as_list_second)
    print("\n该ISP可达的全球AS网络数量%s %s:" % (all_reach, len(as_reach_dict_0)))
    print("第一层次操作后，该ISP全球可达的AS网络数量:%s, 占比(%.6f), %s" % (reach_first, reach_first/all_reach, len(as_reach_dict_1)))
    print("第二层次操作后，该ISP全球可达的AS网络数量:%s, 占比(%.6f), %s" % (reach_second, reach_second/all_reach, len(as_reach_dict_2)))
    print("注：某AS网络只要有一个前缀可达，则该AS网络可达")

    print("\n该ISP直联网络的数量:", len(direct_networks_list))
    print("该ISP直联网络中为U国的数量:", len(direct_networks_u_list))
    print("该ISP直联网络中为C国的数量:", len(direct_networks_c_list))

    print("\n0阶段，U国通告IP地址量:", ip_num_u_0)
    print("1阶段，U国可达IP地址量:", ip_num_u_1)
    print("0阶段，C国通告IP地址量:", ip_num_c_0)
    print("1阶段，C国可达IP地址量:", ip_num_c_1)

    print("\n第一层次操作后，非U&C 不可达IP规模（%s）占非U&C 原始IP规模(%s)比例：%.6f\n"
          % (none_u_c_ip_num_1, none_u_c_ip_num_0, none_u_c_ip_num_1/none_u_c_ip_num_0))

    # print(u_as_group)
    # print(direct_networks_u_list)
    # direct_networks_u_set = set(direct_networks_u_list)
    # u_as_group_set = set(u_as_group)
    # print(len(u_as_group_set))
    # print(direct_networks_u_set.difference(u_as_group_set))

    # print(as_reach_dict_0)

    as_reach_info = []
    for key in as_reach_dict_0.keys():
        try:
            as_reach_info.append([key,
                                  as2country[key],
                                  country_info_dict[as2country[key]][0].strip("\""),
                                  country_info_dict[as2country[key]][1].strip("\""),
                                  as_reach_dict_0[key], as_reach_dict_1[key], as_reach_dict_2[key]])
        except Exception as e:
            # print(key)
            as_reach_info.append([key,
                                  "/",
                                  "/",
                                  "/",
                                  as_reach_dict_0[key], as_reach_dict_1[key], as_reach_dict_2[key]])
    as_reach_info.sort(reverse=False, key=lambda elem: int(elem[0]))
    save_path = "../000LocalData/as_simulate/as_reach_info(电信).csv"
    write_to_csv(as_reach_info, save_path)

    # 统计国家的可达IP规模表
    for item in as_reach_info:
        # 0阶段国家可达IP规模表
        if item[1] in country_reach_0.keys():
            country_reach_0[item[1]] += int(item[4])
        else:
            country_reach_0[item[1]] = int(item[4])

        # 1阶段国家可达IP规模表
        if item[1] in country_reach_1.keys():
            country_reach_1[item[1]] += int(item[5])
        else:
            country_reach_1[item[1]] = int(item[5])

        # 2阶段国家可达IP规模表
        if item[1] in country_reach_2.keys():
            country_reach_2[item[1]] += int(item[6])
        else:
            country_reach_2[item[1]] = int(item[6])

    country_reach_info = []
    for key in country_reach_0.keys():
        try:
            country_reach_info.append([key,
                                       country_info_dict[key][0].strip("\""),
                                       country_info_dict[key][1].strip("\""),
                                       country_reach_0[key],
                                       country_reach_1[key],
                                       country_reach_2[key],
                                       1-country_reach_0[key]/country_reach_0[key],
                                       1-country_reach_1[key]/country_reach_0[key],
                                       1-country_reach_2[key]/country_reach_0[key]])
        except Exception as e:
            # 某些AS在whois中没有相关信息
            # print(e)
            pass
    country_reach_info.sort(reverse=True, key=lambda elem: elem[7])
    save_path = "../000LocalData/as_simulate/country_reach_info(电信).csv"
    write_to_csv(country_reach_info, save_path)


def gain_u_as_group():
    """
    根据All AS CSV文件，获取u as group
    :return re_list:
    """
    re_list = []  # 存储返回的list
    all_as_file = "../000LocalData/as_simulate/电信-所有企业.CSV"
    all_as_file_read = open(all_as_file, 'r')
    for line in all_as_file_read.readlines():
        line = line.strip().split(",")
        as_item = line[-1].strip("AS")
        # print(as_item)
        re_list.append(as_item)
    # print(len(re_list))
    return re_list


def gain_country_group():
    """
    获取国家组团信息
    :return:
    """
    country_group_dict = dict()  # 存储各个组织的国家列表
    country_group_file = "../000LocalData/as_geo/international_organization.csv"
    country_group_file_read = open(country_group_file, 'r')
    for line in country_group_file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        if line[0] in country_group_dict.keys():
            country_group_dict[line[0]].append(line[2])
        else:
            country_group_dict[line[0]] = [line[2]]
    print(country_group_dict)
    return country_group_dict


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    # us_as_group = gain_u_as_group()
    us_as_group = ['12008', '14537', '32590', '2687', '2686',
                   '54600', '8075', '714', '2828', '11164',
                   '6939', '20940', '13786', '3356', '45102',
                   '4385', '22769', '26484', '40065', '2914',
                   '3491', '21928', '7342', '6453', '174',
                   '11158', '36678', '22773', '19551', '19809',
                   '63199', '7922', '32782', '6421', '7018',
                   '40676', '32098', '7843', '46844', '62587',
                   '1351', '13335', '21859', '1820', '16815',
                   '703', '16509', '701', '112', '6461',
                   '30132', '32097', '15169', '14340', '20150']
    # print(gain_u_as_group())
    my_rib_file = "../000LocalData/as_simulate/v4-route.csv"
    chinanet_rib_analysis(my_rib_file, us_as_group)
    # gain_country_cn()
    # gain_country_group()
    time_end = time.time()  # 记录结束时间
    print("\n=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")

