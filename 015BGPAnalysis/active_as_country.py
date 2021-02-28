# coding: utf-8
"""
create on Feb 28, 2021 by Wayne Yu
Function:

根据国家列表，获取每个国家的历年的活跃ASN数量
中国、美国、德国、日本、韩国、巴西、印度、俄罗斯、南非、新加坡、马来西亚、印尼、越南、法国、泰国

CN、US、DE、JP、KR、BR、IN、RU、ZA、SG、MY、ID、VN、FR、TH

"""
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
    csvFile = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csvFile)
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def gain_as2country():
    """
    根据as info file信息获取AS对应的country
    :return as2info:
    """
    as2info = {}  # 存储as号到info的映射关系
    as_info_file = 'D:/Code/Crawler4Caida/000LocalData/as_Gao/asn_info.txt'
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        as_number = line[0]
        as_country = line[1].strip().split(",")[-1].strip()
        as2info[as_number] = as_country
    return as2info


def analysis(open_file, country_str):
    """
    对数据进行处理
    :param open_file:
    :param country_str:
    :return:
    """
    as2country = gain_as2country()  # 获取每个AS的country信息
    print(open_file)
    # 处理文件名，提取日期信息
    temp_str = open_file.split('\\')[-1]
    date_str = temp_str.split(".")[0]
    file_read = open(open_file, 'r', encoding='utf-8')
    as_list = []  # 存储当前时间，全部有连接关系的AS
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        # print(line.strip())
        """
        每新增一个AS记录，就判断是否在AS列表中，在进行操作，耗时124s
        """
        # if line.strip().split('|')[0] not in as_list:
        #     as_list.append(line.strip().split('|')[0])
        # if line.strip().split('|')[1] not in as_list:
        #     as_list.append(line.strip().split('|')[1])
        as0 = line.strip().split('|')[0]
        as1 = line.strip().split('|')[1]

        try:
            # print(as2country[as0])
            if as2country[as0] == country_str:
                as_list.append(as0)
        except Exception as e:
            print(e)

        try:
            # print(as2country[as1])
            if as2country[as1] == country_str:
                as_list.append(as1)
        except Exception as e:
            print(e)
    as_list = list(set(as_list))  # 先转换为字典，再转化为列表，速度还可以
    as_list.sort(key=lambda i: int(i))
    # print(as_list)
    # print("Active AS：", len(as_list))
    return date_str, len(as_list)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    country_list = ["CN", "US", "DE", "JP", "KR",
                    "BR", "IN", "RU", "ZA", "SG",
                    "MY", "ID", "VN", "FR", "TH"]
    for country_item in country_list:
        active_as = []  # 记录活跃的as号
        file_path = []
        for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
            for file_item in files:
                file_path.append(os.path.join(root, file_item))
        # print(file_path)
        temp_list = []
        x_list = []
        y_list = []
        for path_item in file_path:
            # print(analysis(path_item))
            x_date, y_cnt = analysis(path_item, country_item)
            temp_list.append(x_date)
            x_list.append(x_date)
            temp_list.append(y_cnt)
            y_list.append(y_cnt)
            active_as.append(temp_list)
            print(temp_list)
            temp_list = []
        # print(active_as)
        save_path = "./active_as_"+country_item+".csv"
        write_to_csv(active_as, save_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")