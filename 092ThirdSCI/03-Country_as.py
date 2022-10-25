# coding: utf-8
"""
create on Feb 23, 2021 by Wayne Yu
Function:

获取每个时间，US活跃的as号

V2: 20221025
服务于ThirdSCI论文撰写

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


def analysis(open_file, country):
    """
    对数据进行处理
    :param open_file:
    :param country:
    :return:
    """
    as2country = gain_as2country_caida()  # 获取每个AS的country信息
    print(open_file)
    # 处理文件名，提取日期信息
    temp_str = open_file.split('\\')[-1]
    date_str = temp_str.split(".")[0]
    file_read = open(open_file, 'r', encoding='utf-8')
    as_list = []  # 存储当前时间，全部有连接关系的AS
    except_info = []  # 存储异常记录
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
            if as2country[as0] == country:
                as_list.append(as0)
        except Exception as e:
            except_info.append(e)

        try:
            # print(as2country[as1])
            if as2country[as1] == country:
                as_list.append(as1)
        except Exception as e:
            except_info.append(e)

    as_list = list(set(as_list))  # 先转换为字典，再转化为列表，速度还可以
    as_list.sort(key=lambda elem: int(elem))
    # print(as_list)
    print(date_str, " Active AS：", len(as_list), " Except Cnt:", len(set(except_info)))
    return date_str, len(as_list)


def draw(x_list_in, y_list_in, save_name_in):
    """
    对传入的数据进行绘图
    :param x_list_in:
    :param y_list_in:
    :param save_name_in:
    :return:
    """
    fig, ax = plt.subplots(1, 1, figsize=(19.2, 10.8))
    plt.xticks(rotation=32)
    plt.tick_params(labelsize=32)
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    font = {'family': 'Times New Roman',
            'style': 'normal',
            'weight': 'normal',
            'color': 'black',
            'size': 42
            }
    # font_legend = {'family': 'sans-serif',
    #                'style': 'normal',
    #                'weight': 'normal',
    #                'size': 28
    #                }
    tick_spacing = 12
    # title_string = "网络数量增长趋势（19980101-20191201） "
    # ax.set_title(title_string, font)
    ax.plot(x_list_in, y_list_in, ls='-')
    ax.set_xlabel('Time of estimation', font)
    ax.set_ylabel('Number of networks', font)
    # ax.legend(prop=font_legend)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.grid(True)
    fig.tight_layout()
    save_fig_name = "../000LocalData/Paper_Data_Third/03_" + save_name_in + "_en.svg"
    plt.savefig(save_fig_name, dpi=600)
    # plt.show()


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    country_str = "UA"

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
        x_date, y_cnt = analysis(path_item, country_str)
        temp_list.append(x_date)
        x_list.append(x_date)
        temp_list.append(y_cnt)
        y_list.append(y_cnt)
        active_as.append(temp_list)
        # print(temp_list)
        temp_list = []
    # print(active_as)
    """
    自动化处理，同比增长率
    """
    active_as_rate = []
    for i_index in range(len(active_as)):
        # print(i)
        date_string = active_as[i_index][0]
        asn_count = active_as[i_index][1]
        if i_index >= 12:
            asn_rate = round((active_as[i_index][1]-active_as[i_index-12][1])/active_as[i_index-12][1], 3)
            active_as_rate.append([date_string, asn_count, asn_rate])
    save_path = f"../000LocalData/Paper_Data_Third/03_active_as_{country_str}.csv"
    write_to_csv(active_as, save_path)
    draw(x_list, y_list, f"active_as_{country_str}")
    # print(active_as_rate)
    save_path = f"../000LocalData/Paper_Data_Third/03_active_as_{country_str}_rate.csv"
    write_to_csv(active_as_rate, save_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
