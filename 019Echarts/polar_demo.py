# coding:utf-8
"""
create on Jan 15, 2020 By Wayne YU

测试echarts中的极图

"""

import math
import random

from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Page, Polar
from pyecharts.globals import ThemeType
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
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def polar_scatter() -> Polar:
    data = []
    for i in range(360):
        theta = i
        r = theta*theta
        data.append([r, theta])

    print(data)
    save_path = "./polar_demo.csv"
    write_to_csv(data, save_path)

    c = (
        Polar(init_opts=opts.InitOpts(width="1920px", height="960px", page_title="Graph-Global AS Core Map", theme=ThemeType.DARK))
        .add_schema(
            angleaxis_opts=opts.AngleAxisOpts(
                type_="value",  boundary_gap=False, start_angle=0, min_=0, max_=360
            )
        )
        .add(
            "",
            data,
            type_="scatter",
            # effect_opts=opts.EffectOpts(scale=10, period=5),
            symbol="circle",
            symbol_size=10,
            label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="Polar Map"))
    )
    return c


polar_scatter().render("polar_map.html")