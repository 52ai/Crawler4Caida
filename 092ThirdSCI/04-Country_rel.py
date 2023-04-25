# coding:utf-8
"""
create on Oct 25, 2022 By Wayne YU
Function:

从国家维度，分析其BGP网络生态，本程序主要从网络互联关系出发
包含:
rel_cnt, transit_cnt, peer_cnt
inner_rel_cnt, inner_transit_cnt, inner_peer_cnt
outer_rel_cnt, outer_transit_cnt, outer_peer_cnt

统计从19980101至20221001

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
    对数据进行分析处理
    :param open_file:
    :param country:
    :return:
    """
    as2country = gain_as2country_caida()  # 获取每个AS的country信息
    file_read = open(open_file, 'r', encoding='utf-8')
    date_str = str(open_file.split('\\')[-1]).split('.')[0]
    edge_cnt = 0
    peer_cnt = 0
    transit_cnt = 0
    inner_rel_cnt = 0
    outer_rel_cnt = 0
    except_info = []  # 存储异常信息
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        as0 = line.strip().split('|')[0]
        as1 = line.strip().split('|')[1]
        rel_type = line.strip().split('|')[2]
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

        if as0_country == country or as1_country == country:
            if rel_type == '0':
                peer_cnt += 1
            if rel_type == '-1':
                transit_cnt += 1
            edge_cnt += 1

            if as0_country == country and as1_country == country:
                inner_rel_cnt += 1
            else:
                outer_rel_cnt += 1
    res = [date_str, edge_cnt, peer_cnt, transit_cnt, inner_rel_cnt, outer_rel_cnt]
    print(res)
    return res


def draw(data_list, country):
    """
    对传入的数据进行绘图
    :param data_list:
    :param country:
    :return:
    """
    # print(data_list)
    # 存储绘图数据
    save_path_data_list = f"../000LocalData/Paper_Data_Third/04_Country_rel/04_draw_rel_{country}.csv"
    write_to_csv(data_list, save_path_data_list)

    # dt = 1
    # t = np.arange(0, len(draw_date), dt)
    draw_date = []
    edge_list = []
    peer_list = []
    transit_list = []
    inner_rel_list = []
    outer_rel_list = []
    for item in data_list:
        # print(int(item[0]))
        draw_date.append(item[0])
        edge_list.append(int(item[1]))
        peer_list.append(int(item[2]))
        transit_list.append(int(item[3]))
        inner_rel_list.append(int(item[4]))
        outer_rel_list.append(int(item[5]))

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
    font_legend = {'family': 'Times New Roman',
                   'style': 'normal',
                   'weight': 'normal',
                   'size': 36
                   }
    tick_spacing = 15
    # ax.set_title("BGP互联趋势分析(19980101-20221001)", font)
    ax.plot(draw_date, edge_list, ls='-', marker='.', label='overall relationships')
    ax.plot(draw_date, inner_rel_list, ls='-.', marker='.', label='national relationships')
    ax.plot(draw_date, outer_rel_list, ls='-.', marker='.', label='transnational relationships')
    ax.plot(draw_date, peer_list, ls=':', marker='+', label='peering relationships')
    ax.plot(draw_date, transit_list, ls='-.', marker='+', label='transit relationships')
    ax.set_xlabel('Time of estimation (Year)', font)
    ax.set_ylabel('Interconnected relationship', font)
    ax.legend(prop=font_legend)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.grid(True)
    fig.tight_layout()
    save_path_fig = f"..\\000LocalData\\Paper_Data_Third\\04_Country_rel\\04_draw_rel_en_{country}.png"
    plt.savefig(save_path_fig, dpi=600)
    # plt.show()
    plt.close()


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间

    # country_list = ["CN", "US", "JP", "DE", "GB",
    #                 "IN", "FR", "IT", "CA", "KR",
    #                 "RU", "BR", "AU", "ES", "MX",
    #                 "ID", "NL", "SA", "TR", "CH",
    #                 "PL", "SE", "BE", "TH", "IE",
    #                 "AR", "NO", "IL", "AT", "NG",
    #                 "ZA", "BD", "EG", "DK", "SG",
    #                 "PH", "MY", "HK", "VN", "PK"]
    country_list = ["RU"]

    for country_str in country_list:
        # country_str = "UA"
        file_path = []
        for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
            for file_item in files:
                file_path.append(os.path.join(root, file_item))
        result_list = []
        for path_item in file_path:
            result_list.append(analysis(path_item, country_str))
        draw(result_list, country_str)

    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
