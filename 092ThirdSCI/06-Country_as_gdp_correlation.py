# coding:utf-8
"""
create on Oct 26, 2022 By Wayne YU

Function:

采用Pearson相关性系数，分析国家维度AS与GDP间的相关性，分别从时间维度和空间维度展开分析

"""

import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
import numpy as np
import pandas as pd
import seaborn as sns
import scipy.stats as stats
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


def analysis():
    """
    读数据分析相关信息

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

    # country_list = ["CN", "US", "RU"]
    """
    从时间维度，按国家列表分析相关性
    """
    country_cor_time = []  # 存储全球GDP TOP国家，其active as与GDP在时间维度上的关联关系
    for country_str in country_list:
        print("Analysis:", country_str)
        s_as_list = country_as_trend_dict[country_str][0:-1]
        s_gdp_list = country_gdp_trend_dict[country_str]
        print("s_as_list length:", len(s_as_list))
        print("s_as_list:", s_as_list)

        print("s_gdp_list length:", len(s_gdp_list))
        print("s_gdp_list:", s_gdp_list)

        r, p = stats.pearsonr(s_as_list, s_gdp_list)
        print(f"Scipy computed Pearson r: {r} and p-value: {p}")
        country_cor_time.append([country_str, r, p])
    print(country_cor_time)
    save_path = "..\\000LocalData\\Paper_Data_Third\\06_country_cor_time.csv"
    write_to_csv(country_cor_time, save_path, ["country", "r", "p-value"])
    """
    从空间维度，分析as与GDP的关系
    """
    country_cor_space = []  # 存储空间维度，as与GDP的相关性
    for i in range(len(draw_date_gdp)):
        # print(draw_date_gdp[i])
        country_as_list = []  # 存储当前状态下，TOP国家的AS记录
        country_gdp_list = []  # 存储当前状态下，TOP国家的gdp记录
        for country_str in country_list:
            country_as_list.append(country_as_trend_dict[country_str][0:-1][i])
            country_gdp_list.append(country_gdp_trend_dict[country_str][i])

        r, p = stats.pearsonr(country_as_list, country_gdp_list)
        print(f"{draw_date_gdp[i]}:Scipy computed Pearson r: {r} and p-value: {p}")
        country_cor_space.append([draw_date_gdp[i], r, p])
    save_path = "..\\000LocalData\\Paper_Data_Third\\06_country_cor_space.csv"
    write_to_csv(country_cor_time, save_path, ["year", "r", "p-value"])


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    analysis()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
