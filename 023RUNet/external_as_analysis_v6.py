# coding:utf-8
"""
create on May 12, 2020 By Wayne YU

Function:

V2：
在研究俄罗斯断网事件的过程，对出口AS网络做了详细的研究
需进一步分析，我国出口AS互联关系中，美国占比的情况
分为两类，一类是全部互联关系；一类是AS TOP 1000的互联关系占比情况


V3:
新需求，需要研究三大运营商出口AS互联关系中，美国占比的情况
分为两类，一类是全部互联关系；一类是AS TOP 1000的互联关系占比情况

经统计三大运营商出口AS(v4部分)为：

电信:4134、4809、4812、4813
联通:4808、4837、9929、17621、17623
移动（含铁通）：9394、9808、24400、56041

V4:
我国互联网网络关键基础设施布局研究-国际通信网络部分数据分析支撑
我国电信运营商AS网络对外互联方向分国家统计图

经统计我国三大运营商主要出口AS为：

电信:4134、4809、4812、4813
联通:4808、4837、9929、17621、17623
移动（含铁通）：9394、9808、24400、56041

V5:
继续支撑我国互联网网络关键基础设施布局研究-国际通信网络部分数据分析支撑
我国电信运营商AS网络对外互联方向分国家统计图

增加输出Excel表，并将国家信息和缩写对应

V6:
继续支撑我国互联网网络关键基础设施布局研究-国际通信网络部分数据分析支撑
限定运营商

1）中国电信，4134（163网）、4809（CN2网）
2）中国联通，4837（169网）、9929（IP承载A网）
3）中国移动，9808（CMNET网）

一次互联，分别统计各运营商出口至全球各国的互联关系
二次互联，分别统计各运营商及其互联单位出口至全球各国的互联关系

"""

import time
import csv
import os
import matplotlib.pyplot as plt


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


def gain_as2country(as_info_file, country):
    """
    根据传入的as info file信息获取AS与国家的对应字典及该国家的所有的AS Info
    :param as_info_file:
    :param country:
    :return country_as_info:
    :return as2country:
    """
    country_as_info = []  # 存储country as 信息
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    # for line in file_read.readlines():
    #     line = line.strip().split("|")
    #     as2country[line[0]] = line[8]  # 生成字典
    #     temp_list = []
    #     if line[8] == country:
    #         temp_list.append(line[0])  # AS Number
    #         temp_list.append(line[1])  # AS All Relationships
    #         temp_list.append(line[5])  # AS Name
    #         temp_list.append(line[7])  # Source
    #         temp_list.append(line[8])  # Country
    #         country_as_info.append(temp_list)

    for line in file_read.readlines():
        line = line.strip().split("\t")
        # print(line)
        as_number = line[0]
        as_name = line[1].strip().split(",")[0].strip()
        as_country = line[1].strip().split(",")[-1].strip()
        as2country[as_number] = as_country
        temp_list = []
        if as_country == country:
            temp_list.append(as_number)
            temp_list.append(as_name)
            temp_list.append(as_country)
            country_as_info.append(temp_list)

    return country_as_info, as2country


def external_as_analysis(country, as2country, as_list, org_name):
    """
    根据输入的国家，统计该国家的出口AS数量及其互联方向的统计分析
    :param country:
    :param country_as_info:
    :param as2country:
    :return external_country_as:
    """
    print(country)
    external_country_as_return = []
    # 获取1998-2020年间全球BGP互联关系的存储文件
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))

    for path_item in file_path[-1:]:
        print(path_item)
        # 遍历一次文件，获取该国出口AS的数量
        file_read = open(path_item, 'r', encoding='utf-8')
        external_cnt = 0  # 存储该国出口连边的数量
        external_as_list = []  # 存储出口AS
        external_country_list = []  # 存储该国出口方向的国家
        external_country_as = []  # 存储该国出口互联关系中，国外AS网络
        for line in file_read.readlines():
            if line.strip().find("#") == 0:
                continue
            try:
                if str(line.strip().split('|')[0]) in as_list:
                    if as2country[str(line.strip().split('|')[1])] != country:
                        external_cnt += 1
                        external_as_list.append(str(line.strip().split('|')[0]))
                        external_country_list.append(as2country[str(line.strip().split('|')[1])])
                        external_country_as.append(str(line.strip().split('|')[1]))

                if as2country[str(line.strip().split('|')[0])] != country:
                    if str(line.strip().split('|')[1]) in as_list:
                        external_cnt += 1
                        external_as_list.append(str(line.strip().split('|')[1]))
                        external_country_list.append(as2country[str(line.strip().split('|')[0])])
                        external_country_as.append(str(line.strip().split('|')[0]))
            except Exception as e:
                pass
        external_country_as_return = external_country_as
        # 统计出口AS的排名
        external_as_rank = {}
        for item in list(set(external_as_list)):
            external_as_rank[item] = 0
        for item in external_as_list:
            external_as_rank[item] += 1
        # 将字典转换为列表
        external_as_rank_list = []
        temp_list = []
        for item in external_as_rank.keys():
            temp_list.append(item)
            temp_list.append(external_as_rank[item])
            external_as_rank_list.append(temp_list)
            temp_list = []
        external_as_rank_list.sort(reverse=True, key=lambda elem: int(elem[1]))
        external_as_list = list(set(external_as_list))
        print("All External Edges Count:", external_cnt)
        print("All External AS Count(Abroad):", len(list(set(external_country_as))))
        external_country_as_country = {}  # 统计三家运营商直联国际网络数量的国家分布
        external_country_as_us = []  # 存储美国AS网络
        for item_as in list(set(external_country_as)):
            # print(as2country[item_as])
            if as2country[item_as] == "US":
                external_country_as_us.append(item_as)

            if as2country[item_as] not in external_country_as_country.keys():
                external_country_as_country[as2country[item_as]] = 1
            else:
                external_country_as_country[as2country[item_as]] += 1
        # 将字典转化为列表
        external_country_as_country_list = []  # 存储三家运营商直联国际网络数量的国家分布
        for key in external_country_as_country.keys():
            external_country_as_country_list.append([key, external_country_as_country[key]])
        external_country_as_country_list.sort(reverse=True, key=lambda elem: elem[1])
        # print(external_country_as_country_list)
        print("All External AS Count(Abroad(US)):", external_country_as_country["US"])
        # print(external_country_as_us)

        print("All External AS Count(Internal):", len(external_as_list))
        # print(external_as_rank_list)
        print("All External Country Count:", len(list(set(external_country_list))))

        # 统计互联国家方向的排名
        external_country_rank = {}
        for item in list(set(external_country_list)):
            external_country_rank[item] = 0
        for item in external_country_list:
            external_country_rank[item] += 1
        # print(len(external_country_rank))

        # 将字典转为列表
        external_country_rank_list = []
        temp_list = []
        for item in external_country_rank.keys():
            temp_list.append(item)
            temp_list.append(external_country_rank[item])
            external_country_rank_list.append(temp_list)
            temp_list = []
        # print(external_country_rank_list)
        external_country_rank_list.sort(reverse=True, key=lambda elem: int(elem[1]))
        gain_external_country_rank_list_plus(external_country_rank_list, country, org_name)
        draw_bar(external_country_rank_list, country, org_name)
    return external_country_as_return


def gain_external_country_rank_list_plus(rank_list, country, org_name):
    """
    根据传入的rank_list，将其国家缩写与国家信息、大洲信息相对应
    :param rank_list:
    :return:
    """
    # print(rank_list)
    geo_file = "..\\000LocalData\\as_geo\\GeoLite2-Country-Locations-zh-CN.csv"
    code2country = {}  # 存储country_iso_code到国家信息的字典
    geo_file_read = open(geo_file, 'r', encoding='utf-8')
    temp_list = []
    for line in geo_file_read.readlines():
        line = line.strip().split(",")
        if line[4]:  # 当国家代码存在
            # print(line)
            temp_list.append(line[5].strip("\""))
            temp_list.append(line[3].strip("\""))
            code2country[line[4]] = temp_list
            temp_list = []
    # print(code2country)
    external_country_rank_list_save = []  # 存储最终输出的带国家详细的排名表
    temp_list = []
    for item in rank_list:
        try:
            # print(item)
            temp_list.append(item[0])
            temp_list.append(item[1])
            temp_list.extend(code2country[item[0]])
            external_country_rank_list_save.append(temp_list)
            temp_list = []
        except Exception as e:
            # print(e)
            external_country_rank_list_save.append(temp_list)
            temp_list = []
    # print(external_country_rank_list_save)
    # 将信息存储到文件中
    save_path = "..\\000LocalData\\RUNet\\External_BGP_Rel" + country + "-ISP(20200201)_" + org_name + ".csv"
    write_to_csv(external_country_rank_list_save, save_path)


def draw_bar(rank_list, country, orgname):
    """
    根据传入的rank_list信息绘制直方图
    :param rank_list:
    :return:
    """
    x_list = []
    y_list = []

    for item in rank_list:
        x_list.append(item[0])
        y_list.append(item[1])
    # 开始绘图
    fig, ax = plt.subplots(1, 1, figsize=(50, 10))
    title_string = "External BGP Relationships Analysis-ISP:" + country + "( Date:20200201 )"
    ax.set_title(title_string)
    color = ['blue']
    plt.bar(x_list, y_list, width=0.7, color=color)
    for x, y in zip(x_list, y_list):
        plt.text(x, y + 0.05, '%.0f' % y, ha='center', va='bottom', fontsize=11)
    ax.set_xlabel('Country')
    ax.set_ylabel('Relationships Nums')
    # plt.grid(True, linestyle=':', color='r', alpha=0.9)
    # plt.show()
    plt.savefig("..\\000LocalData\\RUNet\\External_BGP_Rel" + country + "-ISP(20200201)" + orgname + ".jpg")


if __name__ == "__main__":
    China_Telecom_AS_list = ['4134', '4809']  # 存储中国电信AS网络
    China_Unicom_AS_list = ['4837', '9929']  # 存储中国联通AS网络
    China_Mobile_AS_list = ['9808', '58453']  # 存储中国移动AS网络
    China_All_AS_list = ['4134', '4809', '4837', '9929', '9808', '58453']

    time_start = time.time()  # 记录启动时间
    country = "CN"
    as_info_file_top = '..\\000LocalData\\as_map\\as_core_map_data_new20200201.csv'
    as_info_file_in = '..\\000LocalData\\as_Gao\\asn_info.txt'
    country_as_info, as2country_dict = gain_as2country(as_info_file_in, country)
    # telecom_org = "ChinaTelecom"
    # external_as_analysis(country, as2country_dict, China_Telecom_AS_list, telecom_org)

    # 中国电信直接互联情况
    telecom_org = "ChinaTelecom_direct"
    external_country_as_ChinaTelecom = external_as_analysis(country, as2country_dict, China_Telecom_AS_list, telecom_org)
    # 中国电信间接互联情况
    telecom_org = "ChinaTelecom_indirect"
    external_country_as_ChinaTelecom.extend(China_Telecom_AS_list)
    external_country_as_ChinaTelecom = external_as_analysis(country, as2country_dict, external_country_as_ChinaTelecom, telecom_org)

    # 中国联通直接互联情况
    telecom_org = "ChinaUnicom_direct"
    external_country_as_ChinaUnicom = external_as_analysis(country, as2country_dict, China_Unicom_AS_list, telecom_org)
    # 中国联通间接互联情况
    telecom_org = "ChinaUnicom_indirect"
    external_country_as_ChinaUnicom.extend(China_Unicom_AS_list)
    external_country_as_ChinaUnicom = external_as_analysis(country, as2country_dict, external_country_as_ChinaUnicom, telecom_org)

    # 中国移动直接互联情况
    telecom_org = "ChinaMobile_direct"
    external_country_as_ChinaMobile = external_as_analysis(country, as2country_dict, China_Mobile_AS_list, telecom_org)
    # 中国移动间接互联情况
    telecom_org = "ChinaMobile_indirect"
    external_country_as_ChinaMobile.extend(China_Mobile_AS_list)
    external_country_as_ChinaMobile = external_as_analysis(country, as2country_dict, external_country_as_ChinaMobile, telecom_org)

    # 三家企业直接互联情况
    telecom_org = "ChinaAll_direct"
    external_country_as_ChinaAll = external_as_analysis(country, as2country_dict, China_All_AS_list, telecom_org)
    # 三家企业间接互联情况
    telecom_org = "ChinaAll_indirect"
    external_country_as_ChinaAll.extend(China_All_AS_list)
    external_country_as_ChinaAll = external_as_analysis(country, as2country_dict, external_country_as_ChinaAll, telecom_org)

    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
