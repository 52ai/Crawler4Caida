# coding:utf-8
"""
create on Jan 6, 2020 By Wayne Yu

测试Graph les miserables

"""

import json
import os
import random

from pyecharts import options as opts
from pyecharts.charts import Graph, Page
from pyecharts.globals import ThemeType


def graph_les_miserables():
    with open(
        os.path.join("..\\000LocalData\\echart_example\\", "les-miserables.json"), "r", encoding="utf-8"
    ) as f:
        j = json.load(f)
        nodes = j["nodes"]
        links = j["links"]
        categories = j["categories"]

    c = (
        Graph(init_opts=opts.InitOpts(width="1920px", height="900px", page_title="Graph-Les Miserables", theme=ThemeType.INFOGRAPHIC))
        .add(
            "",
            nodes=nodes,
            links=links,
            categories=categories,
            layout="circular",
            is_rotate_label=True,
            linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
            label_opts=opts.LabelOpts(position="right"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Graph-Les Miserables"),
            legend_opts=opts.LegendOpts(
                orient="vertical", pos_left="2%", pos_top="20%"
            ),
        )
    )
    return c


graph_les_miserables().render("Graph_les_miserables_render.html")