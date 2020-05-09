# coding:utf-8
"""
create on May 8, 2020 By Wayne YU

Function:

统计全球各主要国家从1998-2019，国家全部互联关系的变化趋势（分为转接互联（Transit）和对等互联(Peer)）
统计网络排名前20名的国家（AS号码的分配）

美国、巴西、俄罗斯、德国、英国、
澳大利亚、波兰、印度、乌克兰、加拿大、
法国、印度尼西亚、中国、荷兰、罗马尼亚
意大利、西班牙、阿根廷、中国香港、孟加拉国

瑞士、韩国、日本、瑞典、保加利亚、
捷克、土耳其、伊朗、奥地利、新西兰、
南非、新加坡、泰国、墨西哥、菲律宾、
丹麦、挪威、芬兰、比利时、越南、

country = ["US", "BR", "RU", "DE", "GB", "AU", "PL", "IN", "UA", "CA",
            "FR", "ID", "CN", "NL", "RO", "IT", "ES", "AR", "HK", "BD", "CH", "KR", "JP", "SE", "BG"]

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


def gain_as2country(as_info_file):
    """
    根据传入的as info file信息获取AS与国家的对应字典
    :param as_info_file:
    :return as2country:
    """
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        # print(line)
        as_number = line[0]
        as_country = line[1].strip().split(",")[-1].strip()
        as2country[as_number] = as_country

    return as2country


def external_as_analysis(country, as2country):
    """
    根据输入的国家，统计该国家的出口AS数量及其互联方向的统计分析
    :param country:
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
        # 遍历一次文件，获取该国AS参与互联的关系，并对，Transit和Peer关系进行分类，包含国内、国外
        file_read = open(path_item, 'r', encoding='utf-8')
        all_cnt = 0  # 存储该国AS所有的互联关系
        peer_cnt = 0  # 存储该国AS所有互联关系中对等互联的数量
        transit_cnt = 0  # 存储该国AS所有互联关系中转接互联的数量
        for line in file_read.readlines():
            if line.strip().find("#") == 0:
                continue
            try:
                as0_country = as2country[str(line.strip().split('|')[0])]
                as1_country = as2country[str(line.strip().split('|')[1])]
                if (as0_country == country) or (as1_country == country):
                    all_cnt += 1
                    if str(line.strip().split('|')[2]) == "0":
                        peer_cnt += 1
                    else:
                        transit_cnt += 1
            except Exception as e:
                # print(e)
                pass

        print("ALL REL|PEER|TRANSIT:", all_cnt, peer_cnt, transit_cnt)
        temp_str = path_item.split('\\')[-1]
        date_str = temp_str.split('.')[0]
        temp_list.append(date_str)
        temp_list.append(all_cnt)
        temp_list.append(peer_cnt)
        temp_list.append(transit_cnt)
        print(temp_list)
        return_list.append(temp_list)
        temp_list = []
    save_path = "../000LocalData/caict_display/All_BGP_Rel_" + country + ".csv"
    write_to_csv(return_list, save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    country = ["US", "BR", "RU", "DE", "GB", "AU", "PL", "IN", "UA", "CA",
               "FR", "ID", "CN", "NL", "RO", "IT", "ES", "AR", "HK", "BD", "CH", "KR", "JP", "SE", "BG"]
    as_info_file_in = '..\\000LocalData\\as_Gao\\asn_info.txt'
    as2country_dict = gain_as2country(as_info_file_in)
    for country_item in country:
        external_as_analysis(country_item, as2country_dict)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
