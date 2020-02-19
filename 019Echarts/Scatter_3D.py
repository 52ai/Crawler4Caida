# coding:utf-8
"""
create on Jan 6,2020 By Wayne Yu

测试pyecharts的3D散点图

"""

import random

from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Scatter3D, Surface3D
from pyecharts.globals import ThemeType
import numpy as np


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
    data = [
        [random.randint(-10000, 10000), random.randint(-10000, 10000), random.randint(-10000, 10000)]
        for _ in range(100)
    ]
    # 求莫比乌斯环数据
    # v_mobius = np.linspace(-1.0, 1.0, num=20, endpoint=True)
    # u_mobius = np.linspace(0, 2 * np.pi, num=20, endpoint=True)
    # x_3d = (1. + v_mobius/2. * np.cos(u_mobius/2.)) * np.cos(u_mobius)
    # print(x_3d)
    # y_3d = (1. + v_mobius/2. * np.cos(u_mobius/2.)) * np.sin(u_mobius)
    # print(y_3d)
    # z_3d = v_mobius/2. * np.sin(v_mobius/2.)
    # print(z_3d)
    # data = [[0, 0, 0], [100, 100, 100], [100, -100, -100]]
    # print(data)
    # data = []
    # temp_list = []
    # for iter_cnt in range(0, len(list(x_3d))):
    #     temp_list.append(x_3d[iter_cnt])
    #     temp_list.append(y_3d[iter_cnt])
    #     temp_list.append(x_3d[iter_cnt])
    #     data.append(temp_list)
    #     temp_list = []
    print(data)
    # data, max_rel = read_as_info('..\\000LocalData\\as_compare\\as_core_map_data_integrate20191203.csv')
    assert isinstance(
        Scatter3D(init_opts=opts.InitOpts(width="1920px", height="960px", page_title="3D散点图", theme=ThemeType.DARK))
        .add("3D散点可视化",
             data,
             grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100, rotate_speed=5, is_rotate=False,
                                         rotate_sensitivity=2),
             xaxis3d_opts=opts.Axis3DOpts(type_="value", name="x", textstyle_opts=opts.TextStyleOpts(color="white")),
             yaxis3d_opts=opts.Axis3DOpts(type_="value", name="y", textstyle_opts=opts.TextStyleOpts(color="white")),
             zaxis3d_opts=opts.Axis3DOpts(type_="value", name="z", textstyle_opts=opts.TextStyleOpts(color="white")),
             itemstyle_opts=opts.ItemStyleOpts(color="white", border_width=0.01, border_color="red", area_color="blue"),
             # label_opts=opts.LabelOpts(color="objectwhite")

             )
        .set_global_opts, )
    c = (
        Scatter3D(init_opts=opts.InitOpts(width="1920px", height="960px", page_title="3D散点图", theme=ThemeType.DARK))
        .add("3D散点可视化",
             data,
             grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100, rotate_speed=5, is_rotate=False, rotate_sensitivity=2),
             xaxis3d_opts=opts.Axis3DOpts(type_="value", name="x", textstyle_opts=opts.TextStyleOpts(color="white")),
             yaxis3d_opts=opts.Axis3DOpts(type_="value", name="y", textstyle_opts=opts.TextStyleOpts(color="white")),
             zaxis3d_opts=opts.Axis3DOpts(type_="value", name="z", textstyle_opts=opts.TextStyleOpts(color="white")),
             itemstyle_opts=opts.ItemStyleOpts(color="white", border_width=0.01, border_color="red", area_color="blue"),

             # label_opts=opts.LabelOpts(color="white")

             )
        .set_global_opts(
            title_opts=opts.TitleOpts("3D散点图"),
            # visualmap_opts=opts.VisualMapOpts(range_color=Faker.visual_color),

        )
    )
    print(data)
    print(Faker.visual_color)
    return c


scatter3d_base().render("scatter_3d_render.html")