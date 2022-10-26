# coding:utf-8
"""
create on Oct 26, 2022 By Wayne YU

Function:
根据05_CountryAll_as_trend.csv数据，绘制全球TOP国家或读取的活跃AS增长趋势图
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time


def draw():
    """
    读取数据绘图
    :return:
    """

    """"
    获取as trend
    """
    file_in = "../000LocalData/Paper_Data_Third/05_CountryAll_as_trend.txt"
    file_read = open(file_in, 'r', encoding='utf-8')
    draw_date = []  # 存储绘图的时间
    country_as_trend_list = []  # 存储每个国家as变化趋势列表
    for line in file_read.readlines():
        line = line.strip().split("	")
        # print(line)
        if line[0] == "country":
            draw_date = line[1:]
        else:
            country_as_trend_list.append(line)
    country_as_trend_list.sort(reverse=True, key=lambda elem: int(elem[-1]))
    # print(country_as_trend_list[0:5])
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

    country_list = ["CN", "US", "JP", "DE", "GB",
                    "IN", "FR", "IT", "CA", "KR",
                    "RU", "BR", "AU", "ES", "MX",
                    "ID", "NL", "SA", "TR", "CH",
                    "PL", "SE", "BE", "TH", "IE",
                    "AR", "NO", "IL", "AT", "NG",
                    "ZA", "BD", "EG", "DK", "SG",
                    "PH", "MY", "HK", "VN", "PK"]

    # country_list = ["CN", "US", "NG"]
    """
    按国家列表，开始绘图
    """
    for country_str in country_list:
        print("Draw:", country_str)
        tick_spacing = 1  # 设置横坐标的刻度间隔
        # 1.创建画布
        fig, axes = plt.subplots(2, 1, sharex='col', figsize=(12, 8))
        # 2.绘制图像
        axes[0].plot(draw_date, country_as_trend_dict[country_str])
        axes[0].set_xlabel("Time of estimation")
        axes[0].set_ylabel("Number of networks")
        axes[0].set_title(country_str)
        axes[0].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
        axes[0].grid(True)

        axes[1].plot(draw_date_gdp, country_gdp_trend_dict[country_str])
        axes[1].set_xlabel("Time of estimation")
        axes[1].set_ylabel("GDP($)")
        # axes[1].set_title('CN')
        axes[1].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
        axes[1].grid(True)

        plt.xticks(rotation=32)
        save_path_fig = f"..\\000LocalData\\Paper_Data_Third\\05_CountryAll_as_trend\\05_CountryAll_as_{country_str}.png"
        plt.savefig(save_path_fig, dpi=600)
        plt.close()
        # plt.show()

    """
    按国家列表，分析自治域网络增长与GDP数据的相关性，按相关系数进行排名
    """


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    draw()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
