# coding:utf-8
"""
create on Jan 6,2020 By Wayne Yu

测试pyecharts的3D散点图

"""

import random

from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Scatter3D
from pyecharts.globals import ThemeType


def read_as_info(file_name):
    """
    根据传入的as_core_map_data信息，读取as_info
    :param file_name:
    :return as_info:
    """
    as_info = []
    tempt_list = []
    file_read = open(file_name, 'r', encoding='utf-8')
    max_rel_cnt = 0
    for line in file_read.readlines():
        line = line.strip().split('|')
        print(line)
        lat = 0.0
        long = 0.0
        rel_all = 0
        # if float(line[6]) >= 0.0:
        #     long = float(line[6])
        # else:
        #     long = float(line[6]) + 360.0
        lat = float(line[6])

        # if float(line[7]) >= 0.0:
        #     lat = float(line[7])
        # else:
        #     lat = float(line[7]) + 360.0
        long = float(line[7])

        rel_all = int(line[1])
        if int(line[1]) > max_rel_cnt:
            max_rel_cnt = int(line[1])
        tempt_list.append(long)
        tempt_list.append(lat)
        tempt_list.append(rel_all)
        print(tempt_list)
        as_info.append(tempt_list)
        tempt_list=[]

    return as_info, max_rel_cnt


def scatter3d_base() -> Scatter3D:
    # data = [
    #     [random.randint(0, 100), random.randint(0, 200), random.randint(0, 100)]
    #     for _ in range(10000)
    # ]
    data, max_rel = read_as_info('..\\000LocalData\\as_compare\\as_core_map_data_integrate20191203.csv')
    c = (
        Scatter3D(init_opts=opts.InitOpts(width="1080px", height="1080px", page_title="全球互联网网络3D散点图", theme=ThemeType.ROMANTIC))
        .add("随机散点",
             data,
             grid3d_opts=opts.Grid3DOpts(width=300, height=160, depth=300, rotate_speed=5, is_rotate=True, rotate_sensitivity=2),
             xaxis3d_opts=opts.Axis3DOpts(type_="value", name="经度", min_=180.0, max_=-180.0),
             yaxis3d_opts=opts.Axis3DOpts(type_="value", name="维度", min_=-180.0, max_=180.0),
             zaxis3d_opts=opts.Axis3DOpts(type_="value", name="连通度", min_=0, max_=max_rel+1),
             itemstyle_opts=opts.ItemStyleOpts()

             )
        .set_global_opts(
            title_opts=opts.TitleOpts("全球互联网网络3D散点图"),
            visualmap_opts=opts.VisualMapOpts(range_color=Faker.visual_color),
        )
    )
    print(data)
    print(Faker.visual_color)
    return c


scatter3d_base().render("scatter_render.html")
