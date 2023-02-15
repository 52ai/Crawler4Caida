# coding:utf-8
"""
create on Feb 10, 2023 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

依托全球AS Rel数据集，研究18家Tier1运营商的网络互联现状

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


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return None:
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file)
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
        as_org = line[2]
        as_country = line[3]
        as2info_result[as_number] = [as_name, as_org, as_country]
    return as2info_result


def analysis(open_file):
    """
    根据全球AS Rel快照，分析全球Tier1 rel的特诊
    :param open_file:
    :return:
    """
    print(open_file)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    analysis(file_path[-2])
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
