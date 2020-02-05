# coding:utf-8
"""
create on Feb 5, 2020 By Wayne YU

Function:

俄罗斯断网事件分析

V1: 俄罗斯TOP100，AS号互联关系变化（总体、国内、国际）（最近2年）
V2: 俄罗斯AS TOP 100 (BGP Transit as Provider) 互联关系变化（总体、国内、国际）（最近2年）

"""
import time
import csv
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def deal_file():
    """

    :return:
    """
    file_in = "..\\000LocalData\\RUNet\\as_ip_info20200120.csv"
    temp_list = []
    as_ip_info = []  # 存储as ip info信息
    file_read = open(file_in, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        temp_list.append(line[0])
        temp_list.append(line[1])
        temp_list.append(line[2])
        temp_list.append(line[-1])
        as_ip_info.append(temp_list)
        temp_list = []
    # save path
    save_path = "..\\000LocalData\\RUNet\\as_ip_info_2_zf.csv"
    write_to_csv(as_ip_info, save_path)


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
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def gain_top_as_ru(as_info):
    """
    根据传入的最新的as info 信息获取ru top as 信息（TOP 100 （BGP Transit as Provider）& AS与国家对应的字典）
    :param as_info:
    :return as_top_100_ru:
    :return as2country:
    """
    ru_as_info = []  # 存储ru as 信息
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        as2country[line[0]] = line[8]  # 生成字典
        if line[8] == "RU":
            ru_as_info.append(line)

    ru_as_info.sort(reverse=True, key=lambda elem: int(elem[3]))  # 以BGP transit as Provider数量作为排序的key
    print("RU Active AS Num:", len(ru_as_info))
    as_top_100_ru = []
    for as_item in ru_as_info[0:100]:
        as_top_100_ru.append(as_item)
    # save path
    save_path = "..\\000LocalData\\RUNet\\as_top_100_ru_transitASProvider.csv"
    write_to_csv(as_top_100_ru, save_path)
    return as_top_100_ru, as2country


def analysis(open_file, as_analysis, as2country):
    """
    对数据进行分析处理
    :param open_file:
    :param as_analysis:
    :return:
    """
    file_read = open(open_file, 'r', encoding='utf-8')
    edge_cnt = 0
    peer_cnt = 0
    transit_provider_cnt = 0
    transit_customer_cnt = 0
    internal_cnt = 0  # 存储与国内AS互联关系数量
    external_cnt = 0  # 存储与国外AS互联关系数量
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        # print(line.strip().split('|'))
        if line.strip().split('|')[0] == as_analysis:  # 如果位于第一位
            if line.strip().split('|')[2] == '0':
                peer_cnt += 1
            if line.strip().split('|')[2] == '-1':
                transit_provider_cnt += 1
            edge_cnt += 1

            # 判断互联对方AS，是否为国内AS号
            try:
                if as2country[str(line.strip().split('|')[1])] == "RU":
                    internal_cnt += 1
                else:
                    external_cnt += 1
            except Exception as e:
                # print("ASN %s Not In Dict!" % (str(line.strip().split('|')[1])))
                pass

        if line.strip().split('|')[1] == as_analysis:  # 如果位于第二位
            if line.strip().split('|')[2] == '0':
                peer_cnt += 1
            if line.strip().split('|')[2] == '-1':
                transit_customer_cnt += 1
            edge_cnt += 1

            # 判断互联对方AS，是否为国内AS号
            try:
                if as2country[str(line.strip().split('|')[1])] == "RU":
                    internal_cnt += 1
                else:
                    external_cnt += 1
            except Exception as e:
                # print("ASN %s Not In Dict!" % (str(line.strip().split('|')[0])))
                pass

        # if edge_cnt > 1000:
        #     break

    return edge_cnt, peer_cnt, transit_provider_cnt + transit_customer_cnt, transit_provider_cnt, transit_customer_cnt, internal_cnt, external_cnt


def draw(draw_date, data_list, as_analysis, as_rank):
    """
    对传入的数据进行绘图
    :param draw_date:
    :param data_list:
    :return:
    """
    dt = 1
    # t = np.arange(0, len(draw_date), dt)
    edge_list = []
    peer_list = []
    transit_list = []
    transit_as_provider_list = []
    transit_as_customer_list = []
    internal_list = []
    external_list = []
    for item in data_list:
        # print(int(item[0]))
        edge_list.append(int(item[0]))
        peer_list.append(int(item[1]))
        transit_list.append(int(item[2]))
        transit_as_provider_list.append(int(item[3]))
        transit_as_customer_list.append(int(item[4]))
        internal_list.append(int(item[5]))
        external_list.append(int(item[6]))

    fig, ax = plt.subplots(1, 1, figsize=(19.2, 10.8))
    plt.xticks(rotation=30)
    # tick_spacing = 6
    title_string = "Russia BGP Analysis Graph(20180201-20201001) AS:" + as_analysis
    ax.set_title(title_string)
    # ax.plot(draw_date, edge_list, linewidth=2, linestyle=':', label='All AS-Relationships', marker='o')
    # ax.plot(draw_date, peer_list, linewidth=2, linestyle=':', label='Peer', marker='o')
    # ax.plot(draw_date, transit_list, linewidth=2, linestyle=':', label='Transit', marker='o')
    ax.plot(draw_date, transit_as_provider_list, linewidth=2, linestyle=':', label='transit_as_provider_list', marker='+')
    # ax.plot(draw_date, transit_as_customer_list, linewidth=1, linestyle=':', label='transit_as_customer_list', marker='o')
    # ax.plot(draw_date, internal_list, linewidth=1, linestyle='--', label='Internal AS-Relationships', marker='o')
    ax.plot(draw_date, external_list, linewidth=2, linestyle='-', label='External AS-Relationships', marker='*')
    # ax.set_xlim(0, len(date_list))
    ax.set_xlabel('Time')
    ax.set_ylabel('Relationships Nums')
    ax.legend()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    # ax.grid(True)
    # cxy, f = axs[1].cohere(peer_list, transit_list, 256, 100. / dt)
    # axs[1].set_ylabel('coherence')
    # fig.tight_layout()
    plt.savefig("..\\000LocalData\\RUNet\\NO" + str(as_rank) + "_RUas(Transit as Provider)_" + as_analysis + ".jpg")
    # plt.show()


def analysis_top_as(as_number, as2country, as_rank):
    """
    根据传入的信息，进行总互联关系数量、国内互联关系数量以及国外互联关系数量变化趋势分析
    :param as_number:
    :param as2country:
    :return:
    """
    # 获取1998-2020年间全球BGP互联关系的存储文件
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-2"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    print(file_path)
    print(as_number)
    result_list = []
    date_list = []
    for path_item in file_path:
        result_list.append(analysis(path_item, as_number, as2country))
        temp_str = path_item.split('\\')[-1]
        date_list.append(temp_str.split('.')[0])
    # print(result_list)
    save_list = []
    temp_list = []
    iter_cnt = 0
    for iter_cnt in range(0, len(result_list)):
        temp_list.append(date_list[iter_cnt])
        temp_list.extend(list(result_list[iter_cnt]))
        save_list.append(temp_list)
        temp_list = []
        iter_cnt += 1
    print(save_list)
    # save path
    save_path = "..\\000LocalData\\RUNet\\RU_as_" + as_number + ".csv"
    write_to_csv(save_list, save_path)
    draw(date_list, result_list, as_number, as_rank)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    as_info_file_in = '..\\000LocalData\\as_map\\as_core_map_data_new20200101.csv'
    top_as_list, as2country_dict = gain_top_as_ru(as_info_file_in)
    # 根据已知的TOP AS列表，逐个的进行总互联关系数量、国内互联关系数量以及国外互联关系数量变化趋势分析
    rank_cnt = 1
    for item_as in top_as_list:
        analysis_top_as(item_as[0], as2country_dict, rank_cnt)
        rank_cnt += 1
    time_end = time.time()
    print("\n=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")

