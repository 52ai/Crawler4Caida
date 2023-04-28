# coding:utf-8
"""
create on Apr 28, 2023 By Wayne YU

Function:

在ReCNNIC任务的基础上，另起一个数据分析的任务

一、国家层面

1）该国国对外直连网络关系数量，去重后的国际直连网络数量，直连国家的数量；
2）按照Group统计，该国直连某Group的路径数量，直连网络占该区域网络总数的比例；该国直连该Group的国家数量。

Group示例:us_ca、asean、belt_and_road、af、eu、nato、bay、ocean

二、企业层面

企业AS示例：4134、9808（58453）、4837、3356

统计该企业国际互联关系的数量，折合成直连网络的数量，进一步映射为直连国家的数量。

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
    根据geo信息，输出每个国家对应的Group信息等item[7]:asean, item[8]:bay, item[9]:belt_and_road, item[10]:nato
    :return country2group:
    """
    country_2_group_file = '../000LocalData/ReCNNIC/Country-Locations-Group - ReCNNIC.csv'
    country2group_dict = {}  # 存储国家到Group的映射关系
    file_read = open(country_2_group_file, 'r', encoding='gbk')
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


def rel_analysis():
    """
    根据格局as rel数据，从国家层面和企业层面开展数据分析
    :return:
    """
    as2country = gain_as2country_caida()
    country2group = gain_country2group()

    # 获取1998-2022年全球BGP互联关系的存储文件
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    print(file_path[-1])
    rel_file_path = file_path[-1]
    """
    第一遍扫表：获取各个Group的活跃网络数量
    """
    global_as_list = []  # 存储全球自治域网络列表
    with open(rel_file_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.strip().find("#") == 0:
                continue
            line = line.strip().split("|")
            # print(line)
            left_as = line[0]
            right_as = line[1]
            global_as_list.append(left_as)
            global_as_list.append(right_as)
    global_as_list = list(set(global_as_list))
    print("全球活跃自治域网络数量:", len(global_as_list))
    group_country_dict = {"asean": [],
                          "bay": [],
                          "belt_and_road": [],
                          "nato": [],
                          "us_ca": [],
                          "eu": [],
                          "af": [],
                          "sa": [],
                          "as": [],
                          "na": []}
    except_info = []  # 存储异常信息
    for item_as in global_as_list:
        try:
            item_as_country = as2country[item_as]
            country_info = country2group[item_as_country]
            if country_info[7] == "1":
                group_country_dict["asean"].append(item_as)
            if country_info[8] == "1":
                group_country_dict["bay"].append(item_as)
            if country_info[9] == "1":
                group_country_dict["belt_and_road"].append(item_as)
            if country_info[10] == "1":
                group_country_dict["nato"].append(item_as)
            if item_as_country in ["US", "CA"]:
                group_country_dict["us_ca"].append(item_as)
            if country_info[2] == "EU":
                group_country_dict["eu"].append(item_as)
            if country_info[2] == "AF":
                group_country_dict["af"].append(item_as)
            if country_info[2] == "SA":
                group_country_dict["sa"].append(item_as)
            if country_info[2] == "AS":
                group_country_dict["as"].append(item_as)
            if country_info[2] == "NA":
                group_country_dict["na"].append(item_as)
        except Exception as e:
            except_info.append(e)
    print("欧洲活跃自治域网络数量:", len(set(group_country_dict["eu"])))
    print("非洲活跃自治域网络数量:", len(set(group_country_dict["af"])))
    print("南美活跃自治域网络数量:", len(set(group_country_dict["sa"])))
    print("北美活跃自治域网络数量:", len(set(group_country_dict["us_ca"])))
    print("一带一路活跃自治域网络数量:", len(set(group_country_dict["belt_and_road"])))
    """
    第二遍扫表：统计CN国家的对外互联情况
    """
    print("---（一）----")
    aim_country_list = ["CN", "US", "RU", "DE", "JP", "IN"]
    for aim_country in aim_country_list:
        print(f"=> 统计{aim_country}的情况")
        external_as_list = []  # 存储该国对外连接的网络关系数量及网络数量
        with open(rel_file_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if line.strip().find("#") == 0:
                    continue
                line = line.strip().split("|")
                # print(line)
                left_as = line[0]
                right_as = line[1]
                try:
                    left_as_country = as2country[left_as]
                    right_as_country = as2country[right_as]
                    # print(left_as_country, right_as_country)
                    """
                    统计对外互联情况
                    """
                    if left_as_country == aim_country and right_as_country != aim_country:
                        external_as_list.append(right_as)
                    if left_as_country != aim_country and right_as_country == aim_country:
                        external_as_list.append(left_as)
                except Exception as e:
                    except_info.append(e)
        print(f"{aim_country}与外部{len(set(external_as_list))}个自治域网络，产生了{len(external_as_list)}条互联关系")
        """
        统计对外互联涉及的Group情况
        """
        group_country_rel_dict = {"asean": [],
                                  "bay": [],
                                  "belt_and_road": [],
                                  "nato": [],
                                  "us_ca": [],
                                  "eu": [],
                                  "af": [],
                                  "sa": [],
                                  "as": [],
                                  "na": []}
        external_country_list = []  # 存储对外互联涉及的国家
        for item_as in external_as_list:
            try:
                item_as_country = as2country[item_as]
                external_country_list.append(item_as_country)
                country_info = country2group[item_as_country]
                if country_info[7] == "1":
                    group_country_rel_dict["asean"].append(item_as)
                if country_info[8] == "1":
                    group_country_rel_dict["bay"].append(item_as)
                if country_info[9] == "1":
                    group_country_rel_dict["belt_and_road"].append(item_as)
                if country_info[10] == "1":
                    group_country_rel_dict["nato"].append(item_as)
                if item_as_country in ["US", "CA"]:
                    group_country_rel_dict["us_ca"].append(item_as)
                if country_info[2] == "EU":
                    group_country_rel_dict["eu"].append(item_as)
                if country_info[2] == "AF":
                    group_country_rel_dict["af"].append(item_as)
                if country_info[2] == "SA":
                    group_country_rel_dict["sa"].append(item_as)
                if country_info[2] == "AS":
                    group_country_rel_dict["as"].append(item_as)
                if country_info[2] == "NA":
                    group_country_rel_dict["na"].append(item_as)
            except Exception as e:
                except_info.append(e)
        print("直连北美的网络数量:", len(set(group_country_rel_dict["us_ca"])),
              ",其中直连的网络占该区域网络的的比例:", round(len(set(group_country_rel_dict["us_ca"]))/len(set(group_country_dict["us_ca"])), 6))
        print("直连欧洲的网络数量:", len(set(group_country_rel_dict["eu"])),
              ",其中直连的网络占该区域网络的的比例:", round(len(set(group_country_rel_dict["eu"]))/len(set(group_country_dict["eu"])), 6))
        print("直连亚洲的网络数量:", len(set(group_country_rel_dict["as"])),
              ",其中直连的网络占该区域网络的的比例:", round(len(set(group_country_rel_dict["as"]))/len(set(group_country_dict["as"])), 6))
        print("直连非洲的网络数量:", len(set(group_country_rel_dict["af"])),
              ",其中直连的网络占该区域网络的的比例:", round(len(set(group_country_rel_dict["af"]))/len(set(group_country_dict["af"])), 6))
        print("直连南美的网络数量:", len(set(group_country_rel_dict["sa"])),
              ",其中直连的网络占该区域网络的的比例:", round(len(set(group_country_rel_dict["sa"]))/len(set(group_country_dict["sa"])), 6))

        # 统计belt_and_road国家的数量
        belt_and_road_country_list = []
        for item_as in group_country_rel_dict["belt_and_road"]:
            item_as_country = as2country[item_as]
            country_info = country2group[item_as_country]
            if country_info[9] == "1":
                belt_and_road_country_list.append(item_as_country)
        print(f"{aim_country}与全球{len(set(external_country_list))}个国家或地区存在网络直联关系，其中直连belt_and_road沿线国家数量{len(set(belt_and_road_country_list))}个")

    """
    第3遍扫表，统计4134、58453、4837、3356对外互联的情况
    """
    as_rel_as_dict = {"4134": [],
                      "4809": [],
                      "58453": [],
                      "4837": [],
                      "9929": [],
                      "3356": [],
                      "701": []}
    with open(rel_file_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.strip().find("#") == 0:
                continue
            line = line.strip().split("|")
            left_as = str(line[0])
            right_as = str(line[1])
            try:
                left_as_country = as2country[left_as]
                right_as_country = as2country[right_as]
                if left_as_country != right_as_country:
                    if left_as in as_rel_as_dict.keys():
                        as_rel_as_dict[left_as].append(right_as)
                    if right_as in as_rel_as_dict.keys():
                        as_rel_as_dict[right_as].append(left_as)
            except Exception as e:
                except_info.append(e)
    for key_as in as_rel_as_dict.keys():
        temp_country_list = []
        for item_as in as_rel_as_dict[key_as]:
            try:
                item_as_country = as2country[item_as]
                temp_country_list.append(item_as_country)
            except Exception as e:
                except_info.append(e)
        print("AS:", key_as,
              ", 国际互联关系数量：", len(as_rel_as_dict[key_as]),
              ", 国际直联网络数量：", len(set(as_rel_as_dict[key_as])),
              ", 直连国家数量：", len(set(temp_country_list)))


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    rel_analysis()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
