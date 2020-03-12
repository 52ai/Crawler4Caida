# coding:utf-8
"""
create on Mar 11, 2020 By Wayne YU

Function:

统计全球各主要国家从1998-2019，国家内部互联关系的变化趋势

"""

import time
import csv
import os


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
        writer = csv.writer(csvFile, delimiter="|")
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


def external_as_analysis(country, country_as_info, as2country):
    """
    根据输入的国家，统计该国家的出口AS数量及其互联方向的统计分析
    :param country:
    :param country_as_info:
    :param as2country:
    :return:
    """
    print(country)
    # 获取1998-2020年间全球BGP互联关系的存储文件
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))

    return_list = []
    temp_list = []
    for path_item in file_path:
        print(path_item)
        # 遍历一次文件，获取该国出口AS的数量
        file_read = open(path_item, 'r', encoding='utf-8')
        internal_cnt = 0  # 存储该国内部连边的数量
        for line in file_read.readlines():
            if line.strip().find("#") == 0:
                continue
            try:
                if as2country[str(line.strip().split('|')[0])] == country:
                    if as2country[str(line.strip().split('|')[1])] == country:
                        internal_cnt += 1
            except Exception as e:
                pass

        print("internal Edges Count:", internal_cnt)
        temp_str = path_item.split('\\')[-1]
        date_str = temp_str.split('.')[0]
        temp_list.append(date_str)
        temp_list.append(internal_cnt)
        print(temp_list)
        return_list.append(temp_list)
        temp_list = []
    save_path = "../000LocalData/caict_display/internal_BGP_Rel_" + country + ".csv"
    write_to_csv(return_list, save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    country = ["CN", "US", "RU", "JP", "KR"]
    as_info_file_in = '..\\000LocalData\\as_Gao\\asn_info.txt'
    country_as_info, as2country_dict = gain_as2country(as_info_file_in, country)
    for country_item in country:
        external_as_analysis(country_item, country_as_info, as2country_dict)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
