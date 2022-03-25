# coding:utf-8
"""
create on Mar 25, 2022 By Wayne YU

Function:

测试桑基图的绘制

"""
from pyecharts import options as opts
from pyecharts.charts import Sankey
from pyecharts.globals import ThemeType


nodes = [
    {"name": "category1"},
    {"name": "category2"},
    {"name": "category3"},
    {"name": "category4"},
    {"name": "category5"},
    {"name": "category6"},
]

links = [
    {"source": "category1", "target": "category2", "value": 10},
    {"source": "category2", "target": "category3", "value": 15},
    {"source": "category3", "target": "category4", "value": 20},
    {"source": "category5", "target": "category6", "value": 25},
]
c = (
    Sankey(init_opts=opts.InitOpts(width="1900px",
                                   height="900px",
                                   page_title="Sankey",
                                   theme=ThemeType.ROMA))
    .add(
        "sankey",
        nodes,
        links,
        linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source"),
        label_opts=opts.LabelOpts(position="right"),
    )
    .set_global_opts(title_opts=opts.TitleOpts(title="Sankey-基本示例"))
    .render("sankey_base.html")
)
