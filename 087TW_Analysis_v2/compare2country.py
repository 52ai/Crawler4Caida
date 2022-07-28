# coding:utf-8
"""
create on July 25, 2022, By Wayne YU
Email: ieeflsyu@outlook.com

Function:

为进一步完善报告撰写的数据分析工作，需要针对CN&TW的外部互联关系做个比较

1）构建外部网络互联统计函数
2）构建比对函数

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


def gain_external_as_info(aim_country):
    """
    根据传入的国家或地区简称，返回其外部网络互联列表
    :param aim_country:
    :return external_as_info:
    """
    external_as_info = []
    as2country = gain_as2country_caida()
    as2org = gain_as2org_caida()

    as_rel_file = "../000LocalData/as_relationships/serial-1/20220401.as-rel.txt"
    file_read = open(as_rel_file, 'r', encoding='utf-8')

    except_info = []  # 存储异常信息
    aim_country_as = {}  # 存储目标国家的as网络
    internal_rel_cnt = 0  # 统计该国内部网络互联关系数量
    external_as_list = []  # 存储该国对外连接的网络关系数量及网络数量
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

    print(f"{aim_country}活跃自治域网络数量：", len(aim_country_as.keys()))
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

    for item in external_as_list_rank:
        temp_list = ["AS" + item[0], as2org[str(item[0])], as2country[str(item[0])], item[1]]
        # print(temp_list)
        external_as_info.append(temp_list)

    return external_as_info


def compare():
    """
    CN&TW
    :return:
    """
    cn_external_as_info = gain_external_as_info("CN")
    print("CN External AS COUNT:", len(cn_external_as_info))
    tw_external_as_info = gain_external_as_info("TW")
    print("TW External AS COUNT:", len(tw_external_as_info))

    cn_external_as_info_dict = {}
    for item in cn_external_as_info:
        item_as = item[0]
        as_rel_num = item[-1]
        if item_as not in cn_external_as_info_dict.keys():
            cn_external_as_info_dict[item_as] = as_rel_num

    compare_result_list = []
    aim_as_list = []  # 存储可能的AS对象

    for item in tw_external_as_info:
        item_as = item[0]
        item_as_info = item[1]
        item_as_country = item[2]
        as_rel_num = item[3]

        as_rel_num_cn = 0
        try:
            as_rel_num_cn = cn_external_as_info_dict[item_as]
        except Exception as e:
            # print(e)
            pass

        diff = as_rel_num - as_rel_num_cn

        if diff > 0 and item_as_country == "US":
            aim_as_list.append(item_as.strip("AS"))

        temp_line = [item_as, item_as_info, item_as_country, as_rel_num, as_rel_num_cn, diff]
        compare_result_list.append(temp_line)

    print(f"{len(aim_as_list)}个可能的AS对象：", aim_as_list)

    save_file = "compare_result.csv"
    write_to_csv(compare_result_list, save_file)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    compare()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
