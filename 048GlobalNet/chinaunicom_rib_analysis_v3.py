# coding:utf-8
"""
create on Aug 18, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

按照Chinanet rib的分析思路，分析Chinaunicom rib
chinaunicom rib的数据格式相对简单些(在实际处理的时候，发现大量的不规范现象)

V2:

按照chinanet rib v2版本的分析思路，分析chinaunicom rib

V3:
分阶段统计AS中IP规模

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


def chinaunicom_rib_analysis(rib_file, u_as_group):
    """
    根据转入的rib txt信息，统计其最优路由第一跳为U国的占比
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
        line = line.strip()
        line_cnt += 1
        if line.find("/") != -1:
            line = line.strip("*").strip(">").strip("i").strip("?").strip("e").strip()
            line = line.split(" 219")
            if len(line) == 1:
                line = line[0].split(" 202")
            if len(line) == 1:
                line = line[0].split(" 218")
            if len(line) == 1:
                line = line[0].split(" 10")
            if len(line) == 1:
                line = line[0].split(" 220")
            # print(line)
            as_path = []
            ip_prefix = []
            try:
                ip_prefix = line[0].strip().split("/")
                # print(ip_prefix)
                as_path = line[1].strip().split("   ")[-1].split(" ")
            except Exception as e:
                # print(e)
                pass

            if len(as_path) == 1:
                invalid_cnt += 1
                continue
            # print(ip_prefix[-1], as_path[1])
            valid_cnt += 1
            net_len = int(ip_prefix[-1])
            ip_num_cnt += pow(2, (32-net_len))
            first_hop_as = as_path[1]
            last_hop_as = as_path[-1]
            last_hop_as = last_hop_as.strip("{").strip("}")

            if last_hop_as.find(",") != -1:
                # print(last_hop_as)
                last_hop_as = last_hop_as.split(",")[0]
            if last_hop_as.find(".") != -1:
                # print(as_path)
                # print(last_hop_as)
                left_point = last_hop_as.split(".")[0]
                right_point = last_hop_as.split(".")[1]
                last_hop_as = str(int(left_point) * 65536 + int(right_point))
                # print(last_hop_as)

            # 第0阶段操作
            # 存储AS的可达IP规模信息
            if last_hop_as in as_reach_dict_0.keys():
                as_reach_dict_0[last_hop_as] += pow(2, (32 - net_len))
            else:
                as_reach_dict_0[last_hop_as] = pow(2, (32 - net_len))

            # 第1阶段判断
            if first_hop_as in u_as_group:
                prefix_u_cnt += 1
                ip_num_u_cnt += pow(2, (32-net_len))

                try:
                    if (as2country[last_hop_as] != "US") and (as2country[last_hop_as] != "CN"):
                        none_u_c_ip_num_1 += pow(2, (32 - net_len))
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
                    as_reach_dict_1[last_hop_as] += pow(2, (32 - net_len))
                else:
                    as_reach_dict_1[last_hop_as] = pow(2, (32 - net_len))

                try:
                    if as2country[last_hop_as] == "US":
                        ip_num_u_1 += pow(2, (32 - net_len))

                    if as2country[last_hop_as] == "CN":
                        ip_num_c_1 += pow(2, (32 - net_len))

                except Exception as e:
                    pass

            u_flag = 0  # 是否路径是否含U国AS
            for item in as_path[1:]:
                try:
                    item = item.strip("{").strip("}")
                    if item.find(",") != -1:
                        # print(last_hop_as)
                        item = item.split(",")[0]
                    if item.find(".") != -1:
                        # print(as_path)
                        left_point = item.split(".")[0]
                        right_point = item.split(".")[1]
                        item = str(int(left_point) * 65536 + int(right_point))
                        # print(item)
                    if item == "0":
                        continue
                    if as2country[item] == "US":
                        u_flag = 1
                        break
                except Exception as e:
                    print(as_path[1:])
                    print(item)
                    pass

            # 第2阶段判断
            if u_flag == 1:
                prefix_u_cnt_anywhere += 1
                ip_num_u_cnt_anywhere += pow(2, (32 - net_len))
                if last_hop_as in as_reach_dict_2.keys():
                    as_reach_dict_2[last_hop_as] += 0
                else:
                    as_reach_dict_2[last_hop_as] = 0

            if u_flag == 0:
                # 如果某AS网有一个前缀可达，则该AS网可达
                reachable_as_list_second.append(last_hop_as)
                # 存储AS的可达IP规模信息
                if last_hop_as in as_reach_dict_2.keys():
                    as_reach_dict_2[last_hop_as] += pow(2, (32 - net_len))
                else:
                    as_reach_dict_2[last_hop_as] = pow(2, (32 - net_len))

            direct_networks_list.append(first_hop_as)  # 存储直联网络AS
            global_reachable_as_list.append(last_hop_as)  # 存储该条可达前缀所属的AS网络

            try:
                if as2country[first_hop_as] == "US":
                    # print(as2country[first_hop_as])
                    direct_networks_u_list.append(first_hop_as)  # 存储直联网络为U国的网络
                if as2country[first_hop_as] == "CN":
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
        else:
            invalid_cnt += 1

        # if line_cnt > 10:
        #     break
    direct_networks_list = list(set(direct_networks_list))
    direct_networks_u_list = list(set(direct_networks_u_list))
    direct_networks_c_list = list(set(direct_networks_c_list))

    global_reachable_as_list = list(set(global_reachable_as_list))
    reachable_as_list_first = list(set(reachable_as_list_first))
    reachable_as_list_second = list(set(reachable_as_list_second))

    print("RIB文件总的行数:", line_cnt)
    print("无效记录数:", invalid_cnt)
    print("有效记录数:", valid_cnt)
    print("总的IP规模(v4):", ip_num_cnt)
    print("最优路由第一跳为U国的前缀数量:%s, 占比(%.6f)" % (prefix_u_cnt, prefix_u_cnt / valid_cnt))
    print("最优路由第一跳为U国的IP地址数量(V4):%s, 占比(%.6f)" % (ip_num_u_cnt, ip_num_u_cnt / ip_num_cnt))
    print("最优路由任意一跳含U国的前缀数量:%s, 占比(%.6f)" % (prefix_u_cnt_anywhere, prefix_u_cnt_anywhere / valid_cnt))
    print("最优路由任意一跳含U国的IP地址数量(V4):%s, 占比(%.6f)" % (ip_num_u_cnt_anywhere, ip_num_u_cnt_anywhere / ip_num_cnt))

    all_reach = len(global_reachable_as_list)
    reach_first = len(reachable_as_list_first)
    reach_second = len(reachable_as_list_second)
    print("\n该ISP可达的全球AS网络数量:", all_reach)
    print("第一层次操作后，该ISP全球可达的AS网络数量:%s, 占比(%.6f)" % (reach_first, reach_first/all_reach))
    print("第二层次操作后，该ISP全球可达的AS网络数量:%s, 占比(%.6f)" % (reach_second, reach_second/all_reach))
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

    as_reach_info = []
    for key in as_reach_dict_0.keys():
        try:
            as_reach_info.append([key,
                                  as2country[key],
                                  country_info_dict[as2country[key]][0].strip("\""),
                                  country_info_dict[as2country[key]][1].strip("\""),
                                  as_reach_dict_0[key], as_reach_dict_1[key], as_reach_dict_2[key]])
        except Exception as e:
            print(key)
            as_reach_info.append([key,
                                  "/",
                                  "/",
                                  "/",
                                  as_reach_dict_0[key], as_reach_dict_1[key], as_reach_dict_2[key]])
    as_reach_info.sort(reverse=False, key=lambda elem: int(elem[0]))
    save_path = "../000LocalData/as_simulate/as_reach_info(联通).csv"
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
                                       1 - country_reach_0[key] / country_reach_0[key],
                                       1 - country_reach_1[key] / country_reach_0[key],
                                       1 - country_reach_2[key] / country_reach_0[key]])
        except Exception as e:
            print(e)
    country_reach_info.sort(reverse=True, key=lambda elem: elem[7])
    save_path = "../000LocalData/as_simulate/country_reach_info(联通).csv"
    write_to_csv(country_reach_info, save_path)


def gain_u_as_group():
    """
    根据All AS CSV文件，获取u as group
    :return re_list:
    """
    re_list = []  # 存储返回的list
    all_as_file = "../000LocalData/as_simulate/联通-所有企业.CSV"
    all_as_file_read = open(all_as_file, 'r')
    for line in all_as_file_read.readlines():
        line = line.strip().split(",")
        as_item = line[-1].strip("AS")
        # print(as_item)
        re_list.append(as_item)
    # print(len(re_list))
    return re_list


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    us_as_group = gain_u_as_group()
    my_rib_file = "../000LocalData/as_simulate/Chinaunicom RIB.txt"
    chinaunicom_rib_analysis(my_rib_file, us_as_group)
    time_end = time.time()  # 记录结束时间
    print("\nScripts Finish, Time Consuming:", (time_end - time_start), "S")


