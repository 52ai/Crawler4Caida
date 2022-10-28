# coding:utf-8
"""
create on Oct 26, 2022 By Wayne YU

Function:

本程序拟统计自1998年至今，全球各国的自治域网络数量的变化情况，形成按时间演化的矩阵图

CN, 19980101...20221001
.
.
.
US, 19980101...20221001

"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
import csv


def write_to_csv(res_list, des_path, title_str):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :param title_str:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file)
        writer.writerow(title_str)
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
    print(date_str, " Active AS：", len(as_list), " Except Cnt:", len(set(except_info)))
    print("CN:", len(list(set(country_as_dic["CN"]))))
    print("US:", len(list(set(country_as_dic["US"]))))
    return date_str, len(as_list), country_as_dic


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
    active_as = []  # 记录活跃的as号
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    """
    date_list:存储整个时间序列
    as_cnt_list:存储全球AS的增长序列
    country_as_cnt_dict:按照date_list的顺序，用字典存储全球每个国家的增长序列
    """

    date_list = []
    as_cnt_list = []
    country_as_cnt_dict = {}

    for path_item in file_path:
        if path_item.find("1001.as-rel.txt") == -1:
            continue
        date_str_out, as_cnt, country_as_dict_out = analysis(path_item)
        date_list.append(date_str_out)
        as_cnt_list.append(as_cnt)
        for key in country_as_dict_out.keys():
            if key not in country_as_cnt_dict.keys():
                country_as_cnt_dict[key] = [len(list(set(country_as_dict_out[key])))]
            else:
                country_as_cnt_dict[key].append(len(list(set(country_as_dict_out[key]))))

    """
    将country_as_cnt_dict，转换为list，便于存储
    """
    result_list = []
    temp_list = []
    for key in country_as_cnt_dict.keys():
        temp_list.append(key)
        temp_list.extend(country_as_cnt_dict[key])
        result_list.append(temp_list)
        temp_list = []
    title_list = ["country"]
    title_list.extend(date_list)

    global_as_list = ["Global"]
    global_as_list.extend(as_cnt_list)
    result_list.append(global_as_list)
    save_file = "../000LocalData/Paper_Data_Third/05_CountryAll_as_trend.csv"
    write_to_csv(result_list, save_file, title_list)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
