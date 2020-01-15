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


def polar_scatter() -> Polar:
    data = []
    for i in range(1001):
        theta = i / 100 * 360
        r = random.randint(1,100) * (1 + math.sin(theta/180 * math.pi))
        data.append([r, theta])

    print(data)
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
            symbol="arrow",
            label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="Polar Map"))
    )
    return c


polar_scatter().render("polar_map.html")