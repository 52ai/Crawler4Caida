# coding:utf-8
"""
create on Jan 3, 2020 By Wayne Yu

3D 地球

"""
import pyecharts.options as opts
from pyecharts.faker import POPULATION
from pyecharts.charts import MapGlobe, Grid
from pyecharts.globals import ThemeType

high = max([x for _, x in POPULATION[1:]])
low = min([x for _, x in POPULATION[1:]])


m = (
    MapGlobe(init_opts=opts.InitOpts(width="1920px", height="900px", page_title="全球互联网网络地图", theme=ThemeType.WALDEN))
    .add_schema()
    .add(
        maptype="world",
        series_name="World Population",
        data_pair=POPULATION[1:],
        is_map_symbol_show=False,
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_global_opts(
        # title_opts=opts.TitleOpts(title="全球互联网网络AS号分布图"),
        visualmap_opts=opts.VisualMapOpts(
            min_=low,
            max_=high,
            range_text=["max", "min"],
            is_calculable=True,
            # is_piecewise=True,
            orient="horizontal",
            pos_right="20%",
            range_color=["lightskyblue", "yellow", "orangered"],
        )
    )
)
m.render("geo_global_3D.html")

