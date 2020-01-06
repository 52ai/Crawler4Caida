# coding:utf-8
"""
create on Jan 6, 2020 By Wayne Yu

测试Graph-微博转发关系

"""
import json
import os
import random

from pyecharts import options as opts
from pyecharts.charts import Graph, Page
from pyecharts.globals import ThemeType


def graph_weibo() -> Graph:
    with open(os.path.join("..\\000LocalData\\echart_example\\", "weibo.json"), "r", encoding="utf-8") as f:
        j = json.load(f)
        nodes, links, categories, cont, mid, userl = j
    c = (
        Graph(init_opts=opts.InitOpts(width="1920px", height="900px", page_title="Graph-微博转发关系图", theme=ThemeType.INFOGRAPHIC))
        .add(
            "",
            nodes,
            links,
            categories,
            repulsion=50,
            linestyle_opts=opts.LineStyleOpts(curve=0.2),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="Graph-微博转发关系图"),
        )
    )
    return c


graph_weibo().render("Graph_weibo_render.html")