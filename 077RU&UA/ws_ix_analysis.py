# coding:utf-8
"""
create on Mar 15, 2022 By Wenyan YU

Function:

研究网宿8个国际交换中心RIB的数据
分析对俄网络中断，会影响多少个网络（除俄罗斯外）

"""
import time
import csv
import os
from IPy import IP


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csvFile = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def gain_as2country_caida():
    """
    根据Caida asninfo获取as对应的国家信息
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
    分析RIB信息
    :param rib_file:
    :return:
    """
    as2country_dic = gain_as2country_caida()
    print("AS12389's Country:", as2country_dic['12389'])
    print(rib_file)
    except_info = []   # 存储异常信息
    affect_as_list = []  # 存储受影响的as网络
    affect_as_list_except_ru = []  # 存储受影响的as网络，去除俄罗斯的网络
    global_ip_prefix = []  # 存储全球所有经交换中心的ip地址段
    global_ip_list = []  # 存储全球所有经交换中心的ip地址
    global_ip_num = 0  # 存储ip地址数量
    file_read = open(rib_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        # print(line)
        v4_prefix = line[5]
        print(v4_prefix)
        global_ip_prefix.append(v4_prefix)
        as_path = line[-2].split(" ")
        # print(v4_prefix, as_path)
        if len(as_path) < 3:
            continue
        link_as = as_path[2]
        link_as_country = "ZZ"
        try:
            link_as_country = as2country_dic[str(link_as)]
        except Exception as e:
            except_info.append(e)

        origin_as = as_path[-1]
        origin_as_country = "ZZ"
        try:
            origin_as_country = as2country_dic[str(origin_as)]
        except Exception as e:
            except_info.append(e)

        if link_as_country == "RU":
            affect_as_list.append(as_path[-1])
            if origin_as_country != "RU":
                affect_as_list_except_ru.append(as_path[-1])
    print("全球经交换中心通达的IP前缀（去重前）：", len(global_ip_prefix))
    print("全球经交换中心通达的IP前缀（去重后）：", len(set(global_ip_prefix)))
    for item in set(global_ip_prefix):
        print(item)
        global_ip_num += len(IP(item))
        # for x in IP(item):
        #     global_ip_list.append(x)
    print("全球经交换中心通达的IP地址（去重前）：", len(global_ip_list))
    print("全球经交换中心通达的IP地址（去重后）：", len(set(global_ip_list)))
    print("经交换中心的地址数量（简单方法）:", global_ip_num)

    print("在全球IX中停止俄网络接入服务的影响（网宿八个国际交换中心）：")
    print("--含俄网络")
    print("受影响的自治域网络数量：", len(affect_as_list))
    print("受影响的自治域网络数量（去重后）：", len(set(affect_as_list)))

    print("---不含俄网络")
    print("受影响的自治域网络数量：", len(affect_as_list_except_ru))
    print("受影响的自治域网络数量（去重后）：", len(set(affect_as_list_except_ru)))

    print("受影响俄网络占俄总网络的比例:", (len(set(affect_as_list))-len(set(affect_as_list_except_ru)))/5100)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\RU&UA\\rib_ws"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    for path_item in file_path[-1:]:
        rib_analysis(path_item)
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
