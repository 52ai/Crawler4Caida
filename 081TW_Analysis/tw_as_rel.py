# coding:utf-8
"""
create on May 6, 2022 By Wayne YU
Email:ieeflsyu@outlook.com

Functon:

分析TW地区活跃自治域数量、自治域网络通告的IP地址规模、自治域网络的互联关系情况

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


def gain_country2group():
    """
    根据geo信息，输出每个国家对应的Group信息，如欧洲、亚太、一带一路等
    :return country2group:
    """
    country_2_group_file = '..\\000LocalData\\as_geo\\Country-Locations-Group-4wx.csv'
    country2group_dict = {}  # 存储国家到Group的映射关系
    file_read = open(country_2_group_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        if line[0] == "ID":
            # print(line)
            continue
        if line[4] not in country2group_dict.keys():
            country2group_dict[line[4]] = line
    return country2group_dict


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


def as_analysis(aim_country):
    """
    根据输入国家，获取该国家的自治域网络数量、以及各自的互联关系
    :param aim_country:
    :return:
    """
    as2country = gain_as2country_caida()
    as2org = gain_as2org_caida()
    country2group = gain_country2group()

    # 获取1998-2022年全球BGP互联关系的存储文件
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))

    for path_item in file_path[-4:-3]:
        print(f"- - - - - - - {aim_country}国家网络地图统计报告（网络连接）- - - - - -  - - ")
        print("0.数据统计源：", path_item)

        except_info = []  # 存储异常信息
        aim_country_as = {}  # 存储目标国家的as网络
        internal_rel_cnt = 0  # 统计该国内部网络互联关系数量
        external_as_list = []  # 存储该国对外连接的网络关系数量及网络数量

        file_read = open(path_item, 'r', encoding='utf-8')
        for line in file_read.readlines():
            if line.strip().find("#") == 0:
                continue
            try:
                left_as = str(line.strip().split('|')[0])
                left_as_country = as2country[left_as]
                left_as_org = as2org[left_as]

                right_as = str(line.strip().split('|')[1])
                right_as_country = as2country[right_as]
                right_as_org = as2org[right_as]

                """
                统计内部网络情况            
                """
                if left_as_country == aim_country:
                    # print(left_as, left_as_country, left_as_org)
                    if left_as not in aim_country_as.keys():
                        aim_country_as[left_as] = [left_as_org, left_as_country, 1]
                    else:
                        aim_country_as[left_as][-1] += 1

                if right_as_country == aim_country:
                    # print(right_as, right_as_country, right_as_org)
                    if right_as not in aim_country_as.keys():
                        aim_country_as[right_as] = [right_as_org, right_as_country, 1]
                    else:
                        aim_country_as[right_as][-1] += 1

                """
                统计内部网络互联关系
                """
                if left_as_country == aim_country and right_as_country == aim_country:
                    internal_rel_cnt += 1
                """
                统计对外互联情况
                """
                if left_as_country == aim_country and right_as_country != aim_country:
                    external_as_list.append(right_as)
                if left_as_country != aim_country and right_as_country == aim_country:
                    external_as_list.append(left_as)

            except Exception as e:
                except_info.append(e)

        print(f"1.{aim_country}活跃自治域网络数量：", len(aim_country_as.keys()))
        country_as_info_list = []  # 存储目标国家详细的AS列表信息
        for key in aim_country_as.keys():
            # print(key, aim_country_as[key])
            temp_list = ["AS"+key]
            temp_list.extend(aim_country_as[key])
            # print(temp_list)
            country_as_info_list.append(temp_list)
        """
        对country_as_info_list列表按互联关系数量排序，再输出
        """
        country_as_info_list.sort(reverse=True, key=lambda elem: int(elem[3]))
        print("2.TOP 10 自治域网络(按照网络互联关系数量维度排名):")
        for item in country_as_info_list[0:11]:
            print(item)

        save_file = "country_as_list.csv"
        write_to_csv(country_as_info_list, save_file)
        """
        以国家维度，统计目标国家对外互联关系以及对内互联关系
        """
        print(f"3.{aim_country}内部网络互联关系数量:", internal_rel_cnt)
        print(f"4.{aim_country}与外部{len(set(external_as_list))}个自治域网络，产生了{len(external_as_list)}条互联关系")
        """
        统计对外互联涉及的国家情况
        """
        external_country_dic = {}  # 统计目标国家与他国的互联网络的数量以及互联关系的数量信息
        external_as_dic = {}  # 统计对外互联网络紧密度
        for item in external_as_list:

            if item not in external_as_dic.keys():
                external_as_dic[item] = 1
            else:
                external_as_dic[item] += 1

            try:
                item_country = as2country[str(item)]
                # print(item, item_country)
                if item_country not in external_country_dic:
                    external_country_dic[item_country] = [item]  # 初始化国家字典的as值
                else:
                    external_country_dic[item_country].append(item)  # 直接将as网络添加到国家字典的值中
            except Exception as e:
                except_info.append(e)
        """
        将对外互联网络紧密度字典转为列表，筛选与TW紧密合作的国际网络
        """
        external_as_list_rank = []
        for item in external_as_dic.keys():
            external_as_list_rank.append([item, external_as_dic[item]])
        external_as_list_rank.sort(reverse=True, key=lambda elem: int(elem[1]))

        print(f"5.{aim_country}与全球{len(external_country_dic.keys())}个国家或地区存在网络直联关系")
        external_country_list = []  # 将对外互联涉及的国家字典转换为列表
        for item in external_country_dic.keys():
            external_country_list.append([item,
                                          len(set(external_country_dic[item])),
                                          len(external_country_dic[item])])

        external_country_list.sort(reverse=True, key=lambda elem: int(elem[2]))
        print(f"6.TOP 10 国际直联国家或地区（按照直联网络数量排名）:")
        direct_rel_country_result = []
        for item in external_country_list:
            continent = country2group[str(item[0])][3]
            country_name = country2group[str(item[0])][5]
            is_belt_and_road = country2group[str(item[0])][7]
            is_asia_pacific = country2group[str(item[0])][8]
            belt_and_road_str = "其他"
            asia_pacific_str = "其他"

            if is_belt_and_road == "1":
                belt_and_road_str = "一带一路"
            if is_asia_pacific == "1":
                asia_pacific_str = "亚太"

            temp_line = [item[0], country_name, continent, belt_and_road_str, asia_pacific_str, item[1], item[2], round(item[2]/len(external_as_list), 4)]
            direct_rel_country_result.append(temp_line)
            print(temp_line)
        save_file = "direct_rel_country_result.csv"
        write_to_csv(direct_rel_country_result, save_file)
        print(f"7.TOP 10 国际直联网络：")
        external_as_info = []
        for item in external_as_list_rank:
            temp_list = ["AS"+item[0], as2org[str(item[0])], as2country[str(item[0])], item[1]]
            # print(temp_list)
            external_as_info.append(temp_list)
        save_file = "external_as_info.csv"
        write_to_csv(external_as_info, save_file)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    country = "CN"
    as_analysis(country)
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
