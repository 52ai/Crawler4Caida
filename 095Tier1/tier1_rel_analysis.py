# coding:utf-8
"""
create on Feb 10, 2023 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

依托全球AS Rel数据集，研究18家Tier1运营商的网络互联现状
1）每个Tier1 ISP网络互联现状，all rel、peer、provider、customer；
2）针对每个Tier1 ISP 做进一步分析。分析所有的peer/customer的国家、大洲分布，研究其服务范围；
3）从时间维度，研究每个Tier1 ISP的网络互联及其服务范围的变化，从中总结规律；
4）结合路由表数据，研究每个Tier1 ISP的路由通告量，路由条目、IP地址量。


tier1_list = ['3356', '174', '2914', '6939', '3257',
              '701', '7018', '1239', '3549', '7922',
              '3320', '6830', '5511', '3491', '6762',
              '1299', '12956', '6461']

tier1_list = ['3356', '174', '2914', '6939', '3257',
              '701', '7018', '1239', '3549', '7922',
              '3320', '6830', '5511', '3491', '6762',
              '1299', '12956', '6461']

美国(13家):
Level3, AS3356
Cogent, AS174 (---)
NTT America, AS2914
HE, AS6939 （---）
GTT, AS3257
Zayo, AS6461
TATA America, AS6451(***)
PCCW, AS3491
Sprint, AS1239
Verizon, AS701
AT&T, AS7018
Comcast, AS7922 (---)
Lumen/level3, AS3549 (---)

欧洲（5家）：
瑞典电信Telia Carrier, AS1299
意大利电信Sparkle, AS6762
法国电信Orange, AS5511
西班牙电信Telefonica, AS12956
德国电信DT, AS3320
荷兰电信	Liberty Global B.V., AS6830 (***)


wikipedia数据共15家

01)美国Lumen(原Level3+Centurylink), AS3356
02)瑞典Arelion(原Telia), AS1299
03)日本NTT，AS2914
04)意大利Sparkle, AS6762
05)美国GTT，AS3257
06)印度TATA，AS6453
07)美国Zaya,AS6461
08)中国香港PCCW，AS3491
09)法国Orange,AS5511
10)西班牙Telefonica,AS12956
11)美国Verizon,AS701
12)美国T-Mobile(原Sprint),AS1239
13)美国AT&T, AS7018
14)德国DT，AS3320
15)荷兰Liberty Global, AS6830

以维基百科的15家为研究对象

"""
import os
import time
import csv

Tier1_list = ["3356", "1299", "2914", "6762", "3257",
              "6453", "6461", "3491", "5511", "12956",
              "701", "1239", "7018", "3320", "6830",
              "174", "6939", "4134"]


def write_to_csv(res_list, des_path, title_line):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :param title_line:
    :return None:
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file)
        writer.writerow(title_line)
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_as2info_caida():
    """
    根据Caida asn info获取as对应的信息，as_name、as_org、as_country
    :return as2info_result:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2info_result = {}  # 存储as号到info的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_name = line[1]
        as_org = line[2].strip("\"")
        as_country = line[-1]
        as2info_result[as_number] = [as_name, as_org, as_country]
    return as2info_result


def analysis(open_file):
    """
    根据全球AS Rel快照，分析全球Tier1 rel的特征
    :param open_file:
    :return:
    """
    print(open_file)
    as2info = gain_as2info_caida()  # 获取每个ASN的详细信息
    except_info = []  # 存储异常记录
    as_rel_dict = {}  # 存储as互联关系统计结果
    # dict_value = [0, 0, 0, 0]  # all rel、peer、provider、customer
    """
    第一遍扫描，构建字典keys
    """
    with open(open_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.strip().find("#") == 0:
                continue
            line = line.strip().split("|")
            as_left = line[0]
            as_right = line[1]
            rel_type = line[2]
            # print(as_left, as_right, rel_type)

            if as_left not in as_rel_dict.keys():
                as_rel_dict.setdefault(as_left, []).append(0)
                as_rel_dict.setdefault(as_left, []).append(0)
                as_rel_dict.setdefault(as_left, []).append(0)
                as_rel_dict.setdefault(as_left, []).append(0)

            if as_right not in as_rel_dict.keys():
                as_rel_dict.setdefault(as_right, []).append(0)
                as_rel_dict.setdefault(as_right, []).append(0)
                as_rel_dict.setdefault(as_right, []).append(0)
                as_rel_dict.setdefault(as_right, []).append(0)
    """
    第二遍扫描，构建字典Values
    """
    with open(open_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.strip().find("#") == 0:
                continue
            line = line.strip().split("|")
            as_left = line[0]
            as_right = line[1]
            rel_type = line[2]
            # print(as_left, as_right, rel_type)
            if rel_type == '0':
                # 如果该关系为peer关系
                # 总连接数自增1
                # print("PEER")
                as_rel_dict[as_left][0] += 1
                as_rel_dict[as_right][0] += 1
                # Peer连接数自增1
                as_rel_dict[as_left][1] += 1
                as_rel_dict[as_right][1] += 1
            elif rel_type == "-1":
                # 否则该条关系为transit关系
                # 总连接数自增1
                # print("TRANSIT")
                as_rel_dict[as_left][0] += 1
                as_rel_dict[as_right][0] += 1
                # provider-customer, transit关系分别自增1
                as_rel_dict[as_left][3] += 1  # as left的客户加1
                as_rel_dict[as_right][2] += 1  # as right的提供商加1

    print("Global AS Count:", len(as_rel_dict.keys()))
    # print(as_rel_dict)
    tier1_rel_result_list = []
    temp_line = []
    for item in Tier1_list:
        temp_line.append("AS"+item)
        temp_line.extend(as2info[item])
        temp_line.extend(as_rel_dict[item])
        print(temp_line)
        tier1_rel_result_list.append(temp_line)
        temp_line = []
    title_str = ["ASN", "AS NAME", "AS ORG", "AS COUNTRY", "all rel", "peer", "provider", "customer"]
    save_path = "../000LocalData/tier1/tier1_rel_result.csv"
    write_to_csv(tier1_rel_result_list, save_path, title_str)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    analysis(file_path[-2])
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
