# coding:utf-8
"""
create on Jun 3, 2022 By Wayne YU

Function:
简化劫持事件的推演，根据RIB信息统计我自治域网络对外直联互联网络数量、直联前缀数量、直联IP地址数量

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


def rib_analysis(rib_file):
    """
    分析RIB数据，统计我国际路由获取情况，输出Excel中间值，规范化处理
    :return:
    """
    print(rib_file)

    as2country = gain_as2country_caida()
    as2org = gain_as2org_caida()

    file_read = open(rib_file, 'r', encoding='utf-8')
    all_v4_prefix = []  # 存储国内节点采集到的全部路由条目
    all_v4_num = 0  # 存储全部的v4量
    except_info_list = []  # 存储异常记录信息
    direct_as_list = []  # 存储直联网络
    as2prefix = {}  # 存储as起源的prefix

    for line in file_read.readlines():
        line = line.strip().split("|")
        # if line[4] != "4134":
        #     continue
        v4_prefix = line[5]
        as_path = line[-2].split(" ")
        if str(v4_prefix).find("0.0.0.0/0") != -1:
            print(v4_prefix)
            continue
        origin_as = as_path[-1]  # 起源as
        country_path = []  # 将as_path转换成国家path
        for as_item in as_path:
            if as_item.find("{") != -1:
                as_item = as_item.strip("{").strip("}").split(",")[0]
            country_str = "ZZ"
            try:
                country_str = as2country[str(as_item)]
            except Exception as e:
                except_info_list.append(e)
            country_path.append(country_str)

        all_v4_prefix.append(v4_prefix)
        all_v4_num += len(IP(v4_prefix))
        # print(v4_prefix, as_path)
        # print(country_path)
        """
        构建直联网络
        """
        direct_route_as = as_path[0]
        path_index = 0
        for country_item in country_path:
            if country_item != "CN":
                direct_route_country = country_item
                break
            path_index += 1
        if path_index < len(as_path):
            direct_route_as = as_path[path_index]
            if direct_route_as not in direct_as_list:
                direct_as_list.append(direct_route_as)
        """
        构建每个网络的路由前缀以及IP地址数量
        """
        if origin_as not in as2prefix.keys():
            as2prefix[origin_as] = [v4_prefix]
        else:
            as2prefix[origin_as].append(v4_prefix)

    print("国内节点采集路由条目总数：", len(all_v4_prefix))
    print("国内节点采集路由条目总数(去重后)：", len(set(all_v4_prefix)))
    print("国内各骨干节点采集v4地址总量：", all_v4_num)
    print("ASN字典异常记录：", len(set(except_info_list)))

    print("全球ASN数量：", len(as2prefix.keys()))
    print("我国际直联自治域网络数量（RIB探测)：", len(direct_as_list), "占比:", 1-len(direct_as_list)/len(as2prefix.keys()))

    direct_prefix_num = 0  # 存储直联网络的路由条目
    direct_ip_num = 0  # 存储直联网络IP地址规模
    direct_as_info_result = []  # 存储直联网络信息，含ASN、prefix_num、ip_num
    tier1_list = ['3356', '174', '2914', '6939', '3257',
                  '701', '7018', '1239', '3549', '7922',
                  '3320', '6830', '5511', '3491', '6762',
                  '1299', '12956', '6461']

    for item_as in as2prefix.keys():
        if item_as in direct_as_list and item_as not in tier1_list:
            temp_prefix_num = len(as2prefix[item_as])
            temp_ip_num = 0
            for item_prefix in as2prefix[item_as]:
                temp_ip_num += len(IP(item_prefix))
            temp_line = [item_as, temp_prefix_num, temp_ip_num]
            direct_prefix_num += temp_prefix_num
            direct_ip_num += temp_ip_num
            # print(temp_line)
            direct_as_info_result.append(temp_line)

    print("直联网络的路由条目总计：", direct_prefix_num, "占比：", 1-direct_prefix_num/len(all_v4_prefix))
    print("直联网络的IP地址规模：", direct_ip_num, "占比：", 1-direct_ip_num/all_v4_num)

    save_file = "direct_as_info.csv"
    write_to_csv(direct_as_info_result, save_file)


if __name__ == "__main__":
    time_start = time.time()  # 记录程序启动时间
    rib_analysis("..\\000LocalData\\RU&UA\\rib\\z20220320.txt")
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start))
