# coding:utf-8
"""
create on Jan 2, 2020 By Wayne Yu

Function:
基于Pyecharts的Geo图

"""
from pyecharts.faker import Faker
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType
from pyecharts.charts import Map
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


def geo_base() -> Geo:
    c = (
        Geo()
            .add_schema(maptype="china")
            .add("geo", [list(z) for z in zip(Faker.provinces, Faker.values())])
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title="Geo-基本示例"),
        )
    )
    return c


def map_world() -> Map:
    data = [list(z) for z in zip(Faker.country, Faker.values())]
    print(data)
    sava_path = "map_world_render.csv"
    write_to_csv(data, sava_path)
    c = (
        Map(init_opts=opts.InitOpts(width="1920px", height="960px", page_title="Map_世界地图", theme=ThemeType.WESTEROS))
        .add("商家A", data, "world")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Map-世界地图"),
            visualmap_opts=opts.VisualMapOpts(max_=200),
        )
    )
    return c


def map_visualmap() -> Map:
    data = [list(z) for z in zip(Faker.provinces, Faker.values())]
    print(data)
    sava_path = "map_china_render.csv"
    write_to_csv(data, sava_path)

    c = (
        Map(init_opts=opts.InitOpts(width="1920px", height="960px", page_title="Map_中国地图", theme=ThemeType.WESTEROS))
        .add("商家A", data, "china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Map_中国地图"),
            visualmap_opts=opts.VisualMapOpts(max_=200),
        )
    )
    return c


map_world().render("map_world_render.html")
map_visualmap().render("map_china_render.html")
