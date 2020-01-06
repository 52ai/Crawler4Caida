# coding:utf-8
"""
create on Jan 6, 2020 By Wayne Yu

测试Graph npm dependence

"""

import json
import os
import random

from pyecharts import options as opts
from pyecharts.charts import Graph, Page
from pyecharts.globals import ThemeType


def graph_npm_dependencies() -> Graph:
    with open(os.path.join("..\\000LocalData\\echart_example\\", "npmdepgraph.json"), "r", encoding="utf-8") as f:
        j = json.load(f)
    nodes = [
        {
            "x": node["x"],
            "y": node["y"],
            "id": node["id"],
            "name": node["label"],
            "symbolSize": node["size"],
            "itemStyle": {"normal": {"color": node["color"]}},
        }
        for node in j["nodes"]
    ]

    edges = [
        {"source": edge["sourceID"], "target": edge["targetID"]} for edge in j["edges"]
    ]

    c = (
        Graph(init_opts=opts.InitOpts(width="1920px", height="900px", page_title="Graph-NPM Dependencies", theme=ThemeType.INFOGRAPHIC))
        .add(
            "",
            nodes=nodes,
            links=edges,
            layout="none",
            label_opts=opts.LabelOpts(is_show=False),
            linestyle_opts=opts.LineStyleOpts(width=0.5, curve=0.3, opacity=0.7),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="Graph-NPM Dependencies"))
    )
    return c


graph_npm_dependencies().render("Graph_NPM_dependence_render.html")