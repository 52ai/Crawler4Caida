# coding:utf-8
"""
create on Nov 3, 2022 By Wayne YU
Function:

画好一张BGP网络生态演化的整体图，多尝试尝试

这里需要分析各国每BGP的GDP产值的变化情况


"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
import math


def draw():
    """
    将GDP TOP40国家的24年间BGP网络数量变化趋势，画在一张图上
    :return:
    """
    """
    获取as trend
    """
    file_in = "../000LocalData/Paper_Data_Third/05_CountryAll_as_trend.txt"
    file_read = open(file_in, 'r', encoding='utf-8')
    country_as_trend_list = []  # 存储每个国家as变化趋势列表
    draw_date = []
    for line in file_read.readlines():
        line = line.strip().split("	")
        # print(line)
        if line[0] == "country":
            draw_date.extend(line[1:])
        else:
            country_as_trend_list.append(line)
    country_as_trend_list.sort(reverse=True, key=lambda elem: int(elem[-1]))
    # print(country_as_trend_list)
    country_as_trend_dict = {}  # 存储每个国家的as变化趋势
    for item in country_as_trend_list:
        temp_list = [int(elem) for elem in item[1:]]
        country_as_trend_dict[item[0]] = temp_list
    """
    获取gdp trend
    """
    file_in_gdp = "../000LocalData/Paper_Data_Third/05_CountryAll_as_trend_GDP.txt"
    file_read_gdp = open(file_in_gdp, 'r', encoding='utf-8')
    draw_date_gdp = []  # 存储绘图时间
    country_gdp_trend_list = []  # 存储每个国家gdp变化趋势列表
    for line in file_read_gdp.readlines():
        line = line.strip().split("	")
        if line[0] == "country":
            draw_date_gdp = line[1:]
        else:
            country_gdp_trend_list.append(line)
    # print(country_gdp_trend_list[0:5])
    # country_gdp_trend_list.sort(reverse=True, key=lambda elem: float(elem[-1]))
    country_gdp_trend_dict = {}  # 存储每个国家的as变化趋势
    for item in country_gdp_trend_list:
        temp_list = [int(elem.strip()) for elem in item[1:]]
        country_gdp_trend_dict[item[0]] = temp_list

    country_list = ["US", "CN", "JP", "DE", "GB",
                    "IN", "FR", "IT", "CA", "KR",
                    "RU", "BR", "AU", "ES", "MX",
                    "ID", "NL", "SA", "TR", "CH",
                    "PL", "SE", "BE", "TH", "IE",
                    "AR", "NO", "IL", "AT", "NG",
                    "ZA", "BD", "EG", "DK", "SG",
                    "PH", "MY", "HK", "VN", "PK"]

    # country_list = ["CN", "US", "NG"]
    # country_list = ["CN", "US", "JP", "DE", "GB",
    #                 "IN", "FR", "IT", "CA", "KR"]
    """
    统计各国历年每BGP的GDP产值变化
    """
    country_per_trend_dict = {}  # 存储每个国家历年没BGP的GDP变化
    for country_item in country_list:
        country_gdp = country_gdp_trend_dict[country_item]
        country_as = country_as_trend_dict[country_item]
        temp_list = []  # 存储该国1998-2021年的per_value
        for i in range(len(country_gdp)):
            per_value = country_gdp[i]/country_as[i]
            temp_list.append(per_value)
        country_per_trend_dict[country_item] = temp_list

    """
    开始制图
    """
    print(draw_date)
    print(country_as_trend_dict["CN"])
    print(country_gdp_trend_dict["CN"])

    font = {'family': 'Times New Roman',
            'style': 'normal',
            'weight': 'normal',
            'color': 'black',
            'size': 10
            }

    font_legend = {'family': 'Times New Roman',
                   'style': 'normal',
                   'weight': 'normal',
                   'size': 12
                   }
    tick_spacing = 5  # 设置横坐标的刻度间隔
    plt.tick_params(labelsize=5)
    line_cnt = 10  # 每行有几个
    # 1.创建画布
    fig, axes = plt.subplots(len(country_list)//line_cnt, line_cnt, sharex='all', figsize=(21, 8))
    # 2.绘制图像

    for i in range(len(country_list)):
        print(i//line_cnt, i % line_cnt)
        axes[i//line_cnt][i % line_cnt].bar(draw_date[0:-1],
                                            country_per_trend_dict[country_list[i]],
                                            label=country_list[i]+"-"+str(i+1))
        # axes[i].set_title(country_list[i], font)
        axes[i//line_cnt][i % line_cnt].legend(prop=font_legend)
        # axes[i % 4][i//4].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
        axes[i//line_cnt][i % line_cnt].axis('off')

    # plt.suptitle('TOP 40 BGP Networks Trends (1998-2022)', fontsize=20)
    # fig.tight_layout()
    # plt.xticks(rotation=32)
    save_path_fig = f"..\\000LocalData\\Paper_Data_Third\\08_Country_GDP_per_AS_1_picture.png"
    plt.savefig(save_path_fig, dpi=600)
    plt.close()


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    draw()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
