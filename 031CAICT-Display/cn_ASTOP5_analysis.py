# coding:utf-8
"""
create on July 14, 2020 By Wayne YU
Email: ieeflsyu@outlook.com
Function:

根据汤姐的建议，研究中国AS TOP5两两之间互联网络对比的情况

CN-TOP5

AS4809(电信CN2网)
AS4134(电信163网)
AS132203(腾讯公司)
AS45102(阿里巴巴）
AS24429(阿里巴巴-淘宝）

- - - - - - - - - -
Plus

AS4837(联通169网)
AS9929(联通IP承载A网)
AS9808(移动CMNET网)

此处可以进行两个实验，
其一，按照汤姐的意思，对中国排名TOP5的AS网络画像及其互联关系进行综合分析。
其二，对我国三家运行商五个AS网络（2+2+1=5）的网络画像及其互联关系进行综合分析。

二者的思路和方法是一样，只是实验时，分组不同而已

第一组（CN-TOP5），4809、4134、132203、45102、24429
第二组（CN-ISP），4809、4134、4837、9929、9808
- - - - - - - - - - - - - - - - - -
需要用到的一些统计数据源
最新的AS互联关系数据，000LocalData/as_relationships/serial-1/20200701.as-rel.txt
AS-Info，000LocalData/as_Gao/asn_info.txt
国家缩写对应关系中文，000LocalData/as_geo/GeoLite2-Country-Locations-zh-CN.csv

以上面的数据作为输入，
1）统计每个AS号的互联关系，包括总的互联数量、对等AS号、客户AS号、提供商AS号
2）绘制每个AS号的网络画像，ASN、ORG、Country、Relationships
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


def as_info_anlysis(as_info_file, country_map_cn):
    """
    根据as info和Country缩写中文映射关系，绘制全球所有AS号的简单画像
    :param as_info_file:
    :param country_map_cn:
    :return:
    """
    # 获取国家缩写与其对应的中文国家名
    # print(country_map_cn)
    country_info_dict = {}
    file_read = open(country_map_cn, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        country_info_dict[line[4]] = line[5]
    # 绘制全球所有AS号的简单画像
    # print(as_info_file)
    as_info_dict = {}
    as_info_file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in as_info_file_read.readlines():
        line = line.strip().split("\t")
        as_number = line[0]
        as_org = line[1][0:-4]
        as_country = country_info_dict[line[1][-2:]].strip("\"")
        # print(as_number, as_org, as_country)
        as_info_dict[as_number] = [as_org, as_country]
    return as_info_dict


def as_rel_anlysis(as_number_list, as_rel_file):
    """
    根据传入的as 号码，统计其互联关系，包括Peer AS, Transit Customer AS, Transit Provider AS
    :param as_rel_file:
    :param as_number_list:
    :return as_rel_dict:
    """
    as_rel_dict = {}
    for item_as in as_number_list:
        peer_as_list = []  # 存储Peer AS list
        transit_customer_as_list = []  # 存储Transit Customer AS list
        transit_provider_as_list = []  # 存储Transit Provider AS list
        file_read = open(as_rel_file, 'r', encoding='utf-8')
        for line in file_read.readlines():
            if line.strip().find('#') == 0:
                continue
            as_0 = line.strip().split('|')[0]
            as_1 = line.strip().split('|')[1]
            rel_type = line.strip().split('|')[2]
            if as_0 == item_as:  # 如果位于第一位
                if rel_type == '0':  # Peer关系，后面是对等网络的AS号
                    peer_as_list.append(as_1)
                if rel_type == '-1':  # Transit关系,后面是客户的AS号
                    transit_customer_as_list.append(as_1)
            if as_1 == item_as:  # 如果位于第二位
                if rel_type == '0':  # Peer关系，前面是对等网络的AS号
                    peer_as_list.append(as_0)
                if rel_type == '-1':  # Transit关系，前面是提供商的AS号
                    transit_provider_as_list.append(as_0)
        as_rel_dict[item_as] = [peer_as_list, transit_customer_as_list, transit_provider_as_list]
    return as_rel_dict


def print_as_set(as_set, as_info_dict):
    """
    根据传入的as_set,结合as_info_dict,按特定格式输出
    若为空集，则还需要进行进行异常处理
    :param as_set:
    :param as_info_dict:
    :return:
    """
    # pass
    # print(as_set)
    if len(as_set) == 0:
        print("None")
    else:
        for item in as_set:
            try:
                print(item, ":", as_info_dict[item])
            except Exception as e:
                print(item, ":[暂无记录]")


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    # as_list = ["4809", "4134", "132203", "45102", "24429"]
    # as_list = ["4809", "4134", "4837", "9929", "9808"]
    as_list = ["4809", "4837"]
    my_as_rel_file = "../000LocalData/as_relationships/serial-1/20200701.as-rel.txt"
    my_as_info_file = "../000LocalData/as_Gao/asn_info.txt"
    my_country_map_cn = "../000LocalData/as_geo/GeoLite2-Country-Locations-zh-CN.csv"
    my_as_info_dict = as_info_anlysis(my_as_info_file, my_country_map_cn)
    my_as_rel_dict = as_rel_anlysis(as_list, my_as_rel_file)
    # print(len(my_as_rel_dict["4809"][0]), len(my_as_rel_dict["4809"][1]), len(my_as_rel_dict["4809"][2]))
    print("=>TOP AS 两两对比分析程序(v1)")
    print("=>输入需要分析TOP AS组，程序可以自动生成该组AS两两之间的BGP互联关系对比分析报告")
    print("TOP AS Group:", as_list)
    for i in range(0, len(as_list)):
        for j in range(i+1, len(as_list)):
            print("- - - - - -  - - - - - - - -")
            print("AS%s VS AS%s" % (as_list[i], as_list[j]))
            as_i_peer = len(my_as_rel_dict[as_list[i]][0])
            as_i_customer = len(my_as_rel_dict[as_list[i]][1])
            as_i_provider = len(my_as_rel_dict[as_list[i]][2])

            as_j_peer = len(my_as_rel_dict[as_list[j]][0])
            as_j_customer = len(my_as_rel_dict[as_list[j]][1])
            as_j_provider = len(my_as_rel_dict[as_list[j]][2])

            as_i_set = set(my_as_rel_dict[as_list[i]][0]
                           + my_as_rel_dict[as_list[i]][1]
                           + my_as_rel_dict[as_list[i]][2])

            as_j_set = set(my_as_rel_dict[as_list[j]][0]
                           + my_as_rel_dict[as_list[j]][1]
                           + my_as_rel_dict[as_list[j]][2])

            print("AS%s Info:%s" % (as_list[i], my_as_info_dict[as_list[i]]))
            print("AS%s Info:%s" % (as_list[j], my_as_info_dict[as_list[j]]))

            print("\n互联关系数量对比")
            print("All Count:", len(as_i_set), "VS", len(as_j_set))
            print("Peer AS Count:", as_i_peer, "VS", as_j_peer)
            print("Transit Customer AS Count:", as_i_customer, "VS", as_j_customer)
            print("Transit Provider AS Count:", as_i_provider, "VS", as_j_provider)
            # print(as_i_set)
            # print(as_j_set)

            print("\n所有互联AS列表集合运算")
            intersection_as_list = as_i_set.intersection(as_j_set)
            print("All-Intersection AS List(%s):" % (len(intersection_as_list)))
            # print(intersection_as_list)
            print_as_set(intersection_as_list, my_as_info_dict)

            left_difference_as_list = as_i_set.difference(as_j_set)
            print("All-Left Difference AS List(%s):" % (len(left_difference_as_list)))
            # print(left_difference_as_list)
            print_as_set(left_difference_as_list, my_as_info_dict)

            right_difference_as_list = as_j_set.difference(as_i_set)
            print("All-Right Difference AS List(%s):" % (len(right_difference_as_list)))
            # print(right_difference_as_list)
            print_as_set(right_difference_as_list, my_as_info_dict)

            print("\n对等AS列表集合运算")
            as_i_set_peer = set(my_as_rel_dict[as_list[i]][0])
            as_j_set_peer = set(my_as_rel_dict[as_list[j]][0])

            intersection_as_list_peer = as_i_set_peer.intersection(as_j_set_peer)
            print("Peer-Intersection AS List(%s):" % (len(intersection_as_list_peer)))
            # print(intersection_as_list_peer)
            print_as_set(intersection_as_list_peer, my_as_info_dict)

            left_difference_as_list_peer = as_i_set_peer.difference(as_j_set_peer)
            print("Peer-Left Difference AS List(%s):" % (len(left_difference_as_list_peer)))
            print_as_set(left_difference_as_list_peer, my_as_info_dict)

            right_difference_as_list_peer = as_j_set_peer.difference(as_i_set_peer)
            print("Peer-Right Difference AS List(%s):" % (len(right_difference_as_list_peer)))
            print_as_set(right_difference_as_list_peer, my_as_info_dict)

            print("\n客户AS列表集合运算")
            as_i_set_customer = set(my_as_rel_dict[as_list[i]][1])
            as_j_set_customer = set(my_as_rel_dict[as_list[j]][1])

            intersection_as_list_customer = as_i_set_customer.intersection(as_j_set_customer)
            print("Customer-Intersection AS List(%s):" % (len(intersection_as_list_customer)))
            print_as_set(intersection_as_list_customer, my_as_info_dict)

            left_difference_as_list_customer = as_i_set_customer.difference(as_j_set_customer)
            print("Customer-Left Difference AS List(%s):" % (len(left_difference_as_list_customer)))
            print_as_set(left_difference_as_list_customer, my_as_info_dict)

            right_difference_as_list_customer = as_j_set_customer.difference(as_i_set_customer)
            print("Customer-Right Difference AS List(%s):" % (len(right_difference_as_list_customer)))
            print_as_set(right_difference_as_list_customer, my_as_info_dict)

            print("\n提供商AS列表集合运算")
            as_i_set_provider = set(my_as_rel_dict[as_list[i]][2])
            as_j_set_provider = set(my_as_rel_dict[as_list[j]][2])

            intersection_as_list_provider = as_i_set_provider.intersection(as_j_set_provider)
            print("Provider-Intersection AS List(%s):" % (len(intersection_as_list_provider)))
            print_as_set(intersection_as_list_provider, my_as_info_dict)

            left_difference_as_list_provider = as_i_set_provider.difference(as_j_set_provider)
            print("Provider-Left Difference AS List(%s):" % (len(left_difference_as_list_provider)))
            print_as_set(left_difference_as_list_provider, my_as_info_dict)

            right_difference_as_list_provider = as_j_set_provider.difference(as_i_set_provider)
            print("Provider-Right Difference AS List(%s):" % (len(right_difference_as_list_provider)))
            print_as_set(right_difference_as_list_provider, my_as_info_dict)

    time_end = time.time()  # 记录结束的时间
    print("\n=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
