# coding: utf-8
"""
create on Nov 22, 2022 By Wayne YU
Function:

根据某个全球AS_Rel快照，提取全球各国活跃AS网络数量，并将其排名

"""
import os
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
        writer = csv.writer(csv_file)
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


def analysis(open_file):
    """
    根据最新全球AS Rel快照，统计全球各国活跃自治域网络数量及其排名
    :param open_file:
    :return:
    """
    print(open_file)
    as2country = gain_as2country_caida()  # 获取每个AS的country信息
    file_read = open(open_file, 'r', encoding='utf-8')
    as_list = []  # 存储当前时间，全部有连接关系的AS
    country_as_dic = {}  # 存储每个国家
    except_info = []  # 存储异常记录
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        # print(line.strip())
        """
        方法1：每新增一个AS记录，就判断是否在AS列表中，在进行操作，耗时124s
        方法2：先转换为字典，再转化为列表，速度还可以
        """
        as0 = line.strip().split('|')[0]
        as1 = line.strip().split('|')[1]
        as0_country = "ZZ"
        as1_country = "ZZ"

        try:
            as0_country = as2country[as0]
        except Exception as e:
            except_info.append(e)

        try:
            as1_country = as2country[as1]
        except Exception as e:
            except_info.append(e)

        as_list.append(as0)
        as_list.append(as1)

        if as0_country not in country_as_dic.keys():
            country_as_dic[as0_country] = [as0]
        else:
            country_as_dic[as0_country].append(as0)

        if as1_country not in country_as_dic.keys():
            country_as_dic[as1_country] = [as1]
        else:
            country_as_dic[as1_country].append(as1)

    as_list = list(set(as_list))  # 先转换为字典，再转化为列表，速度还可以
    as_list.sort(key=lambda elem: int(elem))
    print("Active AS：", len(as_list), " Except Cnt:", len(set(except_info)))
    print("CN:", len(list(set(country_as_dic["CN"]))))
    print("US:", len(list(set(country_as_dic["US"]))))
    """
    将字典，转换为list
    """
    country_as_rank_list = []
    for key in country_as_dic.keys():
        country_as_rank_list.append([key, len(list(set(country_as_dic[key])))])
    country_as_rank_list.sort(reverse=True, key=lambda elem: int(elem[1]))
    print(country_as_rank_list)
    save_path = "../000LocalData/as_cn/global_country_as_rank.csv"
    write_to_csv(country_as_rank_list, save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    analysis(file_path[-1])
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")

