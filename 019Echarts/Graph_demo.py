# coding:utf-8
"""
create on Jan 6,2020 By Wayne

测试pyecharts的关系图绘制

"""

import json
import os
import random

from pyecharts import options as opts
from pyecharts.charts import Graph, Page
from pyecharts.globals import ThemeType


def graph_base() -> Graph:
    # nodes = [
    #     {"name": "结点1", "symbolSize": 10},
    #     {"name": "结点2", "symbolSize": 20},
    #     {"name": "结点3", "symbolSize": 30},
    #     {"name": "结点4", "symbolSize": 40},
    #     {"name": "结点5", "symbolSize": 50},
    #     {"name": "结点6", "symbolSize": 40},
    #     {"name": "结点7", "symbolSize": 30},
    #     {"name": "结点8", "symbolSize": 20},
    # ]
    # links = []
    # for i in nodes:
    #     for j in nodes:
    #         links.append({"source": i.get("name"), "target": j.get("name")})

    # links = [
    #     opts.GraphLink(source="结点1", target="结点2", value=2),
    #     opts.GraphLink(source="结点2", target="结点3", value=3),
    #     opts.GraphLink(source="结点3", target="结点4", value=4),
    #     opts.GraphLink(source="结点4", target="结点5", value=5),
    #     opts.GraphLink(source="结点5", target="结点1", value=7),
    # ]
    nodes = []
    links = []

    for node_index in range(1, 20):
        temp_dict = {}
        name_str = "节点" + str(node_index)
        temp_dict["name"] = name_str
        temp_dict["symbolSize"] = random.randint(1, 10)
        # print(temp_dict)
        nodes.append(temp_dict)
    print(nodes)
    for i in nodes:
        print(i)
        for j in nodes:
            # if random.random() > 0.8:
            links.append({"source": i.get("name"), "target": j.get("name")})
    print(links)
    c = (
        Graph(init_opts=opts.InitOpts(width="1920px", height="900px", page_title="全球互联网网络BGP互联图", theme=ThemeType.INFOGRAPHIC))
        .add("",
             nodes,
             links,
             repulsion=8000,
             is_draggable=True,
             is_rotate_label=False,
             # layout="circular",
             layout="force",
             # edge_label=opts.LabelOpts(
             #     is_show=True,
             #     position="middle",
             #     # formatter="{b}的数据{c}",
             # )
             )
        .set_global_opts(title_opts=opts.TitleOpts(title="全球互联网网络BGP互联图"))
    )
    return c


graph_base().render("Graph_render.html")