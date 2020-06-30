# coding:utf-8
"""
create on June 30. 2020 By Wenyan YU

Function:

将CAICT地图绘制工具箱（CAICT-AtlasToolkit）本地版程序移植至服务器端
在"/collect/tomcat_API/tomcat_caictpic_API8097/webapps/datafile/"
共有四个文件夹

上传文件夹（upload）
历史上传文件夹（upload_history）
下载文件夹（download）
历史下载文件夹（download_history）

上传文件夹存放用户绘图原始数据，后端采用Python定时监控，处理完一个绘图数据就将其移至历史上传文件夹
下载文件夹放置绘图结果(.html格式)，用户下载完后，定期将其移至历史下载文件夹

Python脚本处理逻辑如下

每隔一定时间，扫描上传文件夹
若发现存在文件，则读取该文件组，按照规定的图例编号，分别调用不同的绘图算法
绘图完成，将绘图结果保存至下载文件夹，并将原文件移至历史上传文件夹


01-小规模网络拓扑
02-大规模网络拓扑
03-极图
041-中国地图
042-世界地图
05-词云图
06-主题河流图

"""
import os
from pyecharts import options as opts
from pyecharts.charts import Graph, ThemeRiver, Polar, WordCloud, Map
from pyecharts.globals import ThemeType
import json
import time


def graph_2d(open_file) -> Graph:
    """
    网络拓扑图2D
    :param open_file:
    :return:
    """
    title_str = str(open_file).strip().split("/")[-1].split(".")[0]
    title_str = "Graph<" + title_str + ">"
    with open(open_file, "r", encoding="utf-8") as f:
        j = json.load(f)
        nodes, links, categories = j
    c = (
        Graph(init_opts=opts.InitOpts(width="1900px", height="900px", page_title=title_str, theme=ThemeType.DARK))
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
            legend_opts=opts.LegendOpts(
                orient="vertical",
                pos_left="1%",
                pos_top="5%",
            ),
            title_opts=opts.TitleOpts(title=title_str),
        )
    )
    return c


def graph_starcloud(open_file) -> Graph:
    """
    绘制星云图
    :param open_file:
    :return:
    """
    title_str = str(open_file).strip().split("/")[-1].split(".")[0]
    title_str = "Graph_星云图<" + title_str + ">"
    with open(open_file, "r", encoding="utf-8") as f:
        j = json.load(f)
        nodes, links, categories = j
    c = (
        Graph(init_opts=opts.InitOpts(width="1900px", height="900px", page_title=title_str, theme=ThemeType.DARK))
        .add(
            "",
            nodes,
            links,
            categories,
            # layout="circular",
            is_rotate_label=True,
            gravity=0.2,
            repulsion=50,
            linestyle_opts=opts.LineStyleOpts(width=0.1, opacity=0.8, color='source', curve=0),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title_str, title_textstyle_opts=opts.TextStyleOpts(color="#fff"), pos_left="2%"),
            legend_opts=opts.LegendOpts(
                orient="vertical",
                pos_left="2%",
                pos_top="5%",
                pos_bottom="5"
            )
        )
    )
    return c


def polar(open_file) -> Polar:
    """
    根据定义好的数据格式，利用pyecharts绘制极坐标图，格式为极径、极角（0-360）
    :param open_file:
    :return:
    """
    title_str = str(open_file).strip().split("/")[-1].split(".")[0]
    title_str = "极坐标图<" + title_str + ">"
    # 打开文件读取数据
    data = []
    file_in = open(open_file, "r", encoding="utf-8")
    for line in file_in.readlines():
        line = line.strip().split(",")
        data.append(line)

    c = (
        Polar(init_opts=opts.InitOpts(width="1900px", height="900px", page_title=title_str, theme=ThemeType.DARK))
        .add_schema(
            angleaxis_opts=opts.AngleAxisOpts(
                type_="value",  boundary_gap=False, start_angle=0, min_=0, max_=360
            )
        )
        .add(
            "",
            data,
            type_="scatter",
            symbol="circle",
            symbol_size=10,
            label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title=title_str))
    )
    return c


def map_china(open_file) -> Map:
    """
    绘制中国地图
    :param open_file:
    :return:
    """
    title_str = str(open_file).strip().split("/")[-1].split(".")[0]
    title_str = "中国地图<" + title_str + ">"
    # 打开文件读取数据
    data = []
    file_in = open(open_file, "r", encoding="utf-8")
    visual_map_max = 0
    for line in file_in.readlines():
        line = line.strip().split(",")
        data.append(line)
        if int(line[1]) > visual_map_max:
            visual_map_max = int(line[1])

    c = (
        Map(init_opts=opts.InitOpts(width="1900px", height="900px", page_title=title_str, theme=ThemeType.WESTEROS))
        .add(series_name="该省份累计确诊病例", data_pair=data, maptype="china", is_map_symbol_show=True, zoom=1.1)
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title_str),
            visualmap_opts=opts.VisualMapOpts(
                pieces=[{"max": 9, "min": 1, 'label': '1-9', 'color': '#FFEBCD'},
                        {"max": 99, "min": 10, 'label': '10-99', 'color': '#F5DEB3'},
                        {"max": 499, "min": 100, 'label': '100-499', 'color': '#F4A460'},
                        {"max": 999, "min": 500, 'label': '500-999', 'color': '#FA8072'},
                        {"max": 9999, "min": 1000, 'label': '1000-9999', 'color': '#ee2c0f'},
                        {"min": 10000, 'label': '≥10000', 'color': '#5B5B5B'}],
                is_piecewise=True, item_width=45, item_height=30, textstyle_opts=opts.TextStyleOpts(font_size=20)),
        )
    )
    return c


def map_world(open_file) -> Map:
    """
    绘制世界地图
    :param open_file:
    :return:
    """
    title_str = str(open_file).strip().split("/")[-1].split(".")[0]
    title_str = "世界地图<" + title_str + ">"
    # 打开文件读取数据
    data = []
    file_in = open(open_file, "r", encoding="utf-8")
    visual_map_max = 0
    for line in file_in.readlines():
        line = line.strip().split(",")
        data.append(line)
        if int(line[1]) > visual_map_max:
            visual_map_max = int(line[1])

    c = (
        Map(init_opts=opts.InitOpts(width="1900px", height="900px", page_title=title_str, theme=ThemeType.LIGHT))
        .add(series_name="该国家（地区）累计确诊病例", data_pair=data, maptype="world", is_map_symbol_show=False, zoom=1.1)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title_str),
            visualmap_opts=opts.VisualMapOpts(
                pieces=[{"max": 99, "min": 1, 'label': '1-99', 'color': '#FFEBCD'},
                        {"max": 999, "min": 100, 'label': '100-999', 'color': '#F5DEB3'},
                        {"max": 4999, "min": 1000, 'label': '1000-4999', 'color': '#F4A460'},
                        {"max": 9999, "min": 5000, 'label': '5000-9999', 'color': '#FA8072'},
                        {"max": 99999, "min": 10000, 'label': '10000-99999', 'color': '#ee2c0f'},
                        {"min": 100000, 'label': '≥100000', 'color': '#5B5B5B'}],
                is_piecewise=True, item_width=45, item_height=30, textstyle_opts=opts.TextStyleOpts(font_size=20)
            )
        )
    )
    return c


def words_cloud(open_file)->WordCloud:
    """
    根据定义好的数据格式，利用pyecharts绘制词云图
    :param open_file:
    :return:
    """
    title_str = str(open_file).strip().split("/")[-1].split(".")[0]
    title_str = "词汇云图<" + title_str + ">"
    # 打开文件读取数据
    words_data = []
    file_in = open(open_file, "r", encoding="utf-8")
    for line in file_in.readlines():
        line = line.strip().split(",")
        words_data.append(line)

    c = (
         WordCloud(init_opts=opts.InitOpts(width="1900px", height="900px", page_title=title_str, theme=ThemeType.SHINE))
         .add("", words_data, word_size_range=[10, 200])
         .set_global_opts(title_opts=opts.TitleOpts(title=title_str))
         )
    return c


def theme_river(open_file)->ThemeRiver:
    """
    根据定义好的格式，利用pyecharts绘制主题河流图
    :param open_file:
    :return:
    """
    title_str = str(open_file).strip().split("/")[-1].split(".")[0]
    title_str = "主题河流图<" + title_str + ">"
    # 打开文件读取数据
    theme_list = []
    res_list = []
    file_in = open(open_file, "r", encoding="utf-8")
    for line in file_in.readlines():
        line = line.strip().split(",")
        res_list.append(line)
        if line[-1] not in theme_list:
            theme_list.append(line[-1])
    c = (
         ThemeRiver(init_opts=opts.InitOpts(width="1900px", height="900px", page_title=title_str, theme=ThemeType.SHINE))
         .add(theme_list,
              res_list,
              label_opts=opts.LabelOpts(is_show=False),
              singleaxis_opts=opts.SingleAxisOpts(type_="time", pos_bottom="10%"))
         .set_global_opts(title_opts=opts.TitleOpts(title=title_str))
         )
    return c


def do_draw(file_path, download_dir):
    """
    根据传入的文件，调用不用的绘图算法，进行绘图
    :param file_path:
    :param download_dir:
    :return:
    """
    file_path_split = file_path.strip().split("/")
    # print(file_path_split)
    save_path_name = file_path_split[-1].split(".")[0] + ".html"
    save_path_html = os.path.join(download_dir, save_path_name)
    draw_flag = file_path_split[-1].split("-")[0]
    print(save_path_html)
    # print(draw_flag)
    if draw_flag == "01":
        try:
            graph_2d(file_path).render(save_path_html)
            print("Event：绘图成功！graph_2d()")
        except Exception as e:
            print("文件格式有误，绘图失败：", e)
    elif draw_flag == "02":
        try:
            graph_starcloud(file_path).render(save_path_html)
            print("Event：绘图成功！graph_starcloud()")
        except Exception as e:
            print("文件格式有误，绘图失败：", e)
    elif draw_flag == "03":
        try:
            polar(file_path).render(save_path_html)
            print("Event：绘图成功！polar()")
        except Exception as e:
            print("文件格式有误，绘图失败：", e)
    elif draw_flag == "041":
        try:
            map_china(file_path).render(save_path_html)
            print("Event：绘图成功！map_china()")
        except Exception as e:
            print("文件格式有误，绘图失败：", e)
    elif draw_flag == "042":
        try:
            map_world(file_path).render(save_path_html)
            print("Event：绘图成功！map_world()")
        except Exception as e:
            print("文件格式有误，绘图失败：", e)
    elif draw_flag == "05":
        try:
            words_cloud(file_path).render(save_path_html)
            print("Event：绘图成功！world_cloud()")
        except Exception as e:
            print("文件格式有误，绘图失败：", e)
    elif draw_flag == "06":
        try:
            theme_river(file_path).render(save_path_html)
            print("Event：绘图成功！theme_river()")
        except Exception as e:
            print("文件格式有误，绘图失败：", e)
    else:
        print("Event:无该绘图文件对应的图例！")


def loop_draw(upload_dir, download_dir):
    """
    每隔10s中执行一次draw操作
    :param upload_dir:
    :param download_dir:
    :return:
    """
    while True:
        for root, dirs, files in os.walk(upload_dir):
            # print(root), print(dirs), print(files)
            for file_item in files:
                file_path = os.path.join(root, file_item)
                # print(file_path)
                do_draw(file_path, download_dir)
        # 每隔10s中执行一次
        print("............sleep...........")
        time.sleep(10)


if __name__ == "__main__":
    main_upload_dir = "./samples/upload/"
    main_download_dir = "./samples/download/"
    # 定时监控upload_dir里面的文件信息，并执行绘图操作
    loop_draw(main_upload_dir, main_download_dir)
