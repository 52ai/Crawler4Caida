# coding: utf-8
"""
create on Feb 23, 2021 by Wayne Yu
Function:

获取每个时间，中国活跃的as号

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
        as_desrc = line[1].strip().split(",")[0:-1]
        as_desrc = ' '.join(as_desrc)
        as_desrc = as_desrc.strip()
        as_country = line[1].strip().split(",")[-1].strip()
        as2info[as_number] = as_country
    return as2info


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
    对数据进行处理
    :param open_file:
    :return:
    """
    as2country = gain_as2country_caida()  # 获取每个AS的country信息
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
            if as2country[as0] == "CN":
                as_list.append(as0)
        except Exception as e:
            # print(e)
            pass

        try:
            # print(as2country[as1])
            if as2country[as1] == "CN":
                as_list.append(as1)
        except Exception as e:
            # print(e)
            pass
    as_list = list(set(as_list))  # 先转换为字典，再转化为列表，速度还可以
    as_list.sort(key=lambda i: int(i))
    # print(as_list)
    # print("Active AS：", len(as_list))
    return date_str, len(as_list)


def draw(x_list, y_list, save_name):
    """
    对传入的数据进行绘图
    :param x_list:
    :param y_list:
    :param date_str:
    :return:
    """
    fig, ax = plt.subplots(1, 1, figsize=(30.0, 10.8))
    plt.xticks(rotation=90)
    tick_spacing = 4
    title_string = "CN Active AS Graph "
    ax.set_title(title_string)
    ax.plot(x_list, y_list)
    ax.set_xlabel('Date')
    ax.set_ylabel('ACTIVE AS COUNT')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    save_fig_name = save_name + ".jpg"
    plt.savefig(save_fig_name, dpi=1000)
    # plt.show()


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    active_as = []  # 记录活跃的as号
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    # print(file_path)
    temp_list = []
    x_list = []
    y_list = []
    for path_item in file_path[-120:]:
        # print(analysis(path_item))
        x_date, y_cnt = analysis(path_item)
        temp_list.append(x_date)
        x_list.append(x_date)
        temp_list.append(y_cnt)
        y_list.append(y_cnt)
        active_as.append(temp_list)
        print(temp_list)
        temp_list = []
    print(active_as)
    """
    自动化处理，同比增长率
    """
    active_as_rate = []
    for i in range(len(active_as)):
        print(i)
        date_string = active_as[i][0]
        asn_count = active_as[i][1]
        if i >= 12:
            asn_rate = round((active_as[i][1]-active_as[i-12][1])/active_as[i-12][1], 3)
            active_as_rate.append([date_string, asn_count, asn_rate])
    save_path = "./active_as_cn.csv"
    write_to_csv(active_as, save_path)
    draw(x_list, y_list, "active_as_cn")
    print(active_as_rate)
    save_path = "./active_as_cn_rate.csv"
    write_to_csv(active_as_rate, save_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
