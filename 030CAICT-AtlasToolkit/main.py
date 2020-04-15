# coding:utf-8
"""
create on Feb 30. 2020 By Wenyan YU

Function:

实现CAICT地图绘制工具箱（CAICT-AtlasToolkit）的主界面
比上一版做一个界面上的优化

"""
import os
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog
from ttkthemes import ThemedTk

from pyecharts import options as opts
from pyecharts.charts import Graph, ThemeRiver, Polar, WordCloud, Map
from pyecharts.globals import ThemeType
import json
from tk_html_widgets import HTMLLabel, HTMLText, HTMLScrolledText


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


def get_screen_size(window):

    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 8, (screenheight - height) / 8)
    # print(size)
    root.geometry(size)


class App:
    def __init__(self, root):
        """
        初始化界面
        :param root:
        """
        # 初始化参数
        self.tool_v_radio = tk.IntVar()  # 绘图工具单选按钮值
        self.c_tv_aim = tk.StringVar()   # 绘图目的下拉列表框的值
        self.c_tv_tool = tk.StringVar()  # 绘图工具下拉列表框的值
        self.root = root
        self.aim_tool_number = ""  # 全局唯一定位为哪个算法
        self.download_dir = "./image"
        self.sample_list_dir = "./GOOD"
        self.new_draw_html = "./image/current.html"
        self.new_draw_png = "./image/current.png"

        # # 增加菜单栏
        # menu_bar = Menu(root)
        # root.config(menu=menu_bar)
        # # #增加文件一级菜单
        # file_menu = Menu(menu_bar, tearoff=0)
        # menu_bar.add_cascade(label="文件(F)", menu=file_menu)
        # file_menu.add_command(label="新建画布")
        # file_menu.add_command(label="打开文件")
        # file_menu.add_separator()
        # file_menu.add_command(label="退出", command=self.quit)
        #
        # # #增加工作区一级菜单
        # workplace_menu = Menu(menu_bar, tearoff=0)
        # menu_bar.add_cascade(label="工作区", menu=workplace_menu)
        # workplace_menu.add_command(label="返回主页", command=self.return_main)
        #
        # # #增加视图一级菜单
        # view_menu = Menu(menu_bar, tearoff=0)
        # menu_bar.add_cascade(label="视图(V)", menu=view_menu)
        # view_menu.add_command(label="全屏")
        #
        # # #增加工具一级菜单
        # tool_menu = Menu(menu_bar, tearoff=0)
        # menu_bar.add_cascade(label="工具(T)", menu=tool_menu)
        # tool_menu.add_command(label="选项")
        # tool_menu.add_command(label="在线文档和支持")
        #
        # # #增加窗口一级菜单
        # window_menu = Menu(menu_bar, tearoff=0)
        # menu_bar.add_cascade(label="窗口(W)", menu=window_menu)
        # window_menu.add_command(label="配置")
        #
        # # #增加帮助一级菜单
        # help_menu = Menu(menu_bar, tearoff=0)
        # menu_bar.add_cascade(label="帮助(H)", menu=help_menu)
        # help_menu.add_command(label="检查更新")
        # help_menu.add_command(label="关于")

        # 增加左边画布 Frame
        self.cv_frame = Frame(root, width=600, height=685, bg='#fff2cc')
        self.cv_frame.grid(row=0, rowspan=5, column=0, sticky=W)
        self.cv = Canvas(self.cv_frame, width=600, height=685, bg='#fff2cc')
        self.cv.grid(row=0, column=0)
        """
        显示画布中的图片
        """
        global image
        global cv_bg
        cv_bg = PhotoImage(file="./cv_bg.PNG")
        image = self.cv.create_image(600, 685, ancho='se', image=cv_bg)

        # 增加右边功能 Frame
        func_frame_top = Frame(root, width=160)
        func_frame_top.grid(row=0, column=1, sticky=N)
        func_frame_mid = Frame(root, width=160)
        func_frame_mid.grid(row=1, column=1, sticky=N)
        func_frame_bottom = Frame(root, width=160)
        func_frame_bottom.grid(row=4, column=1, sticky=S)

        # # 增加绘图向导Button
        Button(func_frame_top, command=self.draw_guide_init, text="绘图向导", anchor="e", width=21, fg='white', bg='#4bacc6').grid(row=0, column=0, sticky=N)
        # # 增加作品一览Button
        Button(func_frame_top, command=self.open_download_dir, text="查看下载", anchor="e", width=21, fg='white', bg='#4bacc6').grid(row=1, column=0, sticky=N)
        Button(func_frame_top, command=self.sample_list, text="作品一览", anchor="e", width=21, fg='white', bg='#4bacc6').grid(row=2, column=0, sticky=N)
        # 增加回到主页按钮
        Button(func_frame_top, command=self.return_main, text="回到主页", anchor="e", width=21, fg='white', bg='#4bacc6').grid(row=3, column=0, sticky=N)

        # # 增加绘图工具Button
        Button(func_frame_mid, text="绘图工具", anchor="e", width=21, fg='white', bg='#c05046').grid(row=0, column=0, sticky=S)
        # # 增加绘图工具 01网络拓扑图（2D）Button
        Button(func_frame_mid, text="01网络拓扑图（2D）", anchor="e", width=21, fg='white', bg='#9dbb61').grid(row=1, column=0, sticky=W)
        # # 增加绘图工具 02网络拓扑图（3D）Button
        Button(func_frame_mid, text="02网络拓扑图（3D）", anchor="e", width=21, fg='white', bg='#9dbb61').grid(row=2, column=0, sticky=W)
        # # 以此类推
        Button(func_frame_mid, text="03极坐标图", anchor="e", width=21, fg='white', bg='#9dbb61').grid(row=3, column=0, sticky=W)
        Button(func_frame_mid, text="04星云图", anchor="e", width=21, fg='white', bg='#9dbb61').grid(row=4, column=0, sticky=W)
        Button(func_frame_mid, text="05词汇云图", anchor="e", width=21, fg='white', bg='#9dbb61').grid(row=5, column=0, sticky=W)
        Button(func_frame_mid, text="06主题河流图", anchor="e", width=21, fg='white', bg='#9dbb61').grid(row=6, column=0, sticky=W)
        Button(func_frame_mid, text="07地理图绘制系列", anchor="e", width=21, fg='white', bg='#9dbb61').grid(row=7, column=0, sticky=W)
        # #添加关于按钮
        Button(func_frame_bottom, text="关于", command=self.about_toolkit, anchor="e", width=21, fg='white', bg='#4bacc6').grid(row=8, column=0, sticky=S)

    def quit(self):
        # 结束主事件循环
        self.root.quit()  # 关闭窗口
        self.root.destroy()  # 将所有的窗口小部件进行销毁，回收内存
        exit()

    def draw_guide_init(self):
        """"
        点击绘图向导后，界面的初始化
        """
        print("Event:绘图向导")
        # # 清空画布
        # self.cv.delete(image)
        # 初始化绘图向导UI frame
        for widget in self.cv_frame.winfo_children():
            widget.destroy()
        # 开始添加绘图向导界面相关控件
        # 增加绘图目标Label Frame
        self.cv_frame = Frame(root, width=600, height=685, bg='#fff2cc')
        self.cv_frame.grid(row=0, rowspan=5, column=0, sticky=N)
        aim_frame = LabelFrame(self.cv_frame, text="第一步：确定绘图目标", width=600, height=60, background='#fff2cc')
        aim_frame.grid(row=0, column=0, sticky=W)
        aim_frame.grid_propagate(0)  # 组件大小不变
        # #给绘图目标Label Frame里面添加Radiobutton
        aim_list = ["01-希望展示数据间的关联关系（小规模网络拓扑）",
                    "02-希望展示数据间的关联关系（大规模网络拓扑）",
                    "03-希望展示数据间的地位排名",
                    "04-希望进行数据地理位置展示",
                    "05-希望分析文本数据词频信息",
                    "06-希望展示多类时间序列数据"]

        c_aim = ttk.Combobox(aim_frame, textvariable=self.c_tv_aim, width=70)
        c_aim["values"] = aim_list
        c_aim.current(0)
        c_aim.grid(row=0, column=0, sticky=W, padx=5)
        # # 添加下一步按钮
        btn_aim = ttk.Button(aim_frame, text="下一步", width=8, command=self.call_aim_comb)
        btn_aim.grid(row=0, column=1, sticky=W, padx=5)

        # 根据第一步的选择自动给出绘图实例

    def call_aim_comb(self):
        """
        绘图目标下拉框单击事件，生成绘图工具选择、导出绘图数据格式、个性化数据处理、用户上传绘图数据、用户获取绘图结果（绘图参数调优）、目标反馈与评价
        :return:
        """
        # 初始化绘图向导UI frame
        for widget in self.cv_frame.winfo_children():
            widget.destroy()

        tool_frame = LabelFrame(self.cv_frame, text="第二步：选择绘图工具", width=600, height=60, bg='#fff2cc')
        tool_frame.grid(row=0, column=0, sticky=W)
        tool_frame.grid_propagate(0)  # 组件大小不变
        # print("c_tv_aim:", self.c_tv_aim.get())
        aim_number = self.c_tv_aim.get().strip().split("-")[0]
        # print("aim_number:", aim_number)

        # 设置ttk样式
        style = ttk.Style()
        style.configure("Toolbutton", foreground="black", background="#fff2cc", width=72)

        if aim_number == "01":
            # 希望展示数据间的关联关系（小规模网络拓扑）, 01 02图例均可
            # 先清空tool_frame
            for widget in tool_frame.winfo_children():
                widget.destroy()
            tool_list = ["01-网络拓扑图（2D）", "02-网络拓扑图（3D）"]

            c_tool = ttk.Combobox(tool_frame, textvariable=self.c_tv_tool, width=70)
            c_tool["values"] = tool_list
            c_tool.current(0)
            c_tool.grid(row=0, column=0, sticky=W, padx=5)
        elif aim_number == "02":
            # 希望展示数据间的关联关系（大规模网络拓扑）, 04图例
            # 先清空tool_frame
            for widget in tool_frame.winfo_children():
                widget.destroy()
            tool_list = ["04-星云图"]
            c_tool = ttk.Combobox(tool_frame, textvariable=self.c_tv_tool, width=70)
            c_tool["values"] = tool_list
            c_tool.current(0)
            c_tool.grid(row=0, column=0, sticky=W, padx=5)
        elif aim_number == "03":
            # 希望展示数据间的地位排名, 03图例
            # 先清空tool_frame
            for widget in tool_frame.winfo_children():
                widget.destroy()
            tool_list = ["03-极坐标图"]
            c_tool = ttk.Combobox(tool_frame, textvariable=self.c_tv_tool, width=70)
            c_tool["values"] = tool_list
            c_tool.current(0)
            c_tool.grid(row=0, column=0, sticky=W, padx=5)
        elif aim_number == "04":
            # 希望进行数据地理位置展示, 07图例
            # 先清空tool_frame
            for widget in tool_frame.winfo_children():
                widget.destroy()
            tool_list = ["071-地理图绘制系列(中国地图)", "072-地理图绘制系列(世界地图)"]
            c_tool = ttk.Combobox(tool_frame, textvariable=self.c_tv_tool, width=70)
            c_tool["values"] = tool_list
            c_tool.current(0)
            c_tool.grid(row=0, column=0, sticky=W, padx=5)
        elif aim_number == "05":
            # 希望分析文本数据词频信息, 05图例
            # 先清空tool_frame
            for widget in tool_frame.winfo_children():
                widget.destroy()
            tool_list = ["05-词汇云图"]
            c_tool = ttk.Combobox(tool_frame, textvariable=self.c_tv_tool, width=70)
            c_tool["values"] = tool_list
            c_tool.current(0)
            c_tool.grid(row=0, column=0, sticky=W, padx=5)
        elif aim_number == "06":
            # 希望展示多类时间序列数据, 06图例
            # 先清空tool_frame
            for widget in tool_frame.winfo_children():
                widget.destroy()
            tool_list = ["06-主题河流图"]
            c_tool = ttk.Combobox(tool_frame, textvariable=self.c_tv_tool, width=70)
            c_tool["values"] = tool_list
            c_tool.current(0)
            c_tool.grid(row=0, column=0, sticky=W, padx=5)

        # # 添加下一步按钮
        btn_tool = ttk.Button(tool_frame, text="下一步", width=8, command=self.call_tool_comb)
        btn_tool.grid(row=0, column=1, sticky=W, padx=5)

        """
        根据tool frame中下一步按钮，Click事件，获取最终的绘图数据格式，让用户自行导出
        """

    def call_tool_comb(self):
        """
        根据绘图目的和绘图工具的选择，既可以确定到单个的绘图实例，将此绘图实例的绘图数据格式推送给用户
        :return:
        """
        # 初始化绘图向导UI frame
        for widget in self.cv_frame.winfo_children():
            widget.destroy()

        aim_number = self.c_tv_aim.get().strip().split("-")[0]
        tool_number = self.c_tv_tool.get().strip().split("-")[0]
        self.aim_tool_number = ("%s-%s" % (aim_number, tool_number))
        # print("aim_number+tool_number: %s" % self.aim_tool_number)
        """
        根据aim_number + tool_number,定义好绘图的数据接口格式 
        """
        data_format = {"01-01": {"nodes": ["name", "symbolSize",  "..."], "links": ["source", "target"], "categories": ["name"]},
                       "01-02": {"nodes": ["name", "symbolSize", "..."], "links": ["source", "target"], "categories": ["name"]},
                       "02-04": {"nodes": ["name", "symbolSize",  "..."], "links": ["source", "target"], "categories": ["name"]},
                       "03-03": {"line": ["node_name", "radius", "angle"]},
                       "04-071": {"line": ["location", "value"]},
                       "04-072": {"line": ["location", "value"]},
                       "05-05": {"line": ["words", "frequency"]},
                       "06-06": {"line": ["date", "values", "theme"]}}
        # 导出绘图数据格式
        export_frame = LabelFrame(self.cv_frame, text="第三步：导出数据格式", width=600, height=580, bg='#fff2cc')
        export_frame.grid(row=0, column=0, sticky=W)
        export_frame.grid_propagate(0)  # 组件大小不变
        format_label_text = "<B><i>" + str(data_format[str(self.aim_tool_number)]) + "</i></B>"
        # format_label = HTMLLabel(export_frame, text=format_label_text, anchor="w", width=72, bg='#fff2cc')
        format_label = HTMLLabel(export_frame, html=format_label_text, width=72, height=6)
        format_label.grid(row=0, column=0, sticky=W, padx=5)

        if self.aim_tool_number == "01-01":
            format_file = "./samples/01-01(01).json"
            grou_sb_text = "绘图数据示例："+str(format_file)

            # 添加显示文本的信息框
            group_sb = LabelFrame(export_frame, text=grou_sb_text, width=500, height=500, bg='#fff2cc', padx=5, pady=5)
            # s = ttk.Style()
            # s.configure('TLabelframe.Label', font='arial 14 bold', background='#fff2cc')
            # group_sb = ttk.LabelFrame(export_frame, text=grou_sb_text, width=500, height=500)
            group_sb.grid(row=1, column=0, columnspan=2, sticky=W, pady=10)
            sb = ttk.Scrollbar(group_sb)
            sb.pack(side=RIGHT, fill=Y)
            lb = Listbox(group_sb, yscrollcommand=sb.set, width=80, height=24)
            file_in = open(format_file, 'r', encoding='utf-8')

            for line in file_in.readlines():
                # print(line, end="")
                lb.insert(END, line)
            lb.pack(side=LEFT, fill=BOTH)
            sb.config(command=lb.yview)
        if self.aim_tool_number == "01-02":
            self.return_main()  # 暂未实现

        if self.aim_tool_number == "02-04":
            format_file = "./samples/02-04(01).json"
            grou_sb_text = "绘图数据示例："+str(format_file)
            # 添加显示文本的信息框
            group_sb = LabelFrame(export_frame, text=grou_sb_text, width=500, height=500, bg='#fff2cc', padx=5, pady=5)
            group_sb.grid(row=1, column=0, columnspan=2, sticky=W, pady=10)
            sb = Scrollbar(group_sb)
            sb.pack(side=RIGHT, fill=Y)
            lb = Listbox(group_sb, yscrollcommand=sb.set, width=80, height=24)
            file_in = open(format_file, 'r', encoding='utf-8')
            for line in file_in.readlines():
                # print(line, end="")
                lb.insert(END, line)
            lb.pack(side=LEFT, fill=BOTH)
            sb.config(command=lb.yview)

        if self.aim_tool_number == "03-03":
            format_file = "./samples/03-03(01).csv"
            grou_sb_text = "绘图数据示例：" + str(format_file)
            # 添加显示文本的信息框
            group_sb = LabelFrame(export_frame, text=grou_sb_text, width=500, height=500, bg='#fff2cc', padx=5, pady=5)
            group_sb.grid(row=1, column=0, columnspan=2, sticky=W, pady=10)
            sb = Scrollbar(group_sb)
            sb.pack(side=RIGHT, fill=Y)
            lb = Listbox(group_sb, yscrollcommand=sb.set, width=80, height=24)
            file_in = open(format_file, 'r', encoding='utf-8')
            for line in file_in.readlines():
                # print(line, end="")
                lb.insert(END, line)
            lb.pack(side=LEFT, fill=BOTH)
            sb.config(command=lb.yview)

        if self.aim_tool_number == "04-071":
            format_file = "./samples/04-071(01).csv"
            grou_sb_text = "绘图数据示例：" + str(format_file)
            # 添加显示文本的信息框
            group_sb = LabelFrame(export_frame, text=grou_sb_text, width=500, height=500, bg='#fff2cc', padx=5, pady=5)
            group_sb.grid(row=1, column=0, columnspan=2, sticky=W, pady=10)
            sb = Scrollbar(group_sb)
            sb.pack(side=RIGHT, fill=Y)
            lb = Listbox(group_sb, yscrollcommand=sb.set, width=80, height=24)
            file_in = open(format_file, 'r', encoding='utf-8')
            for line in file_in.readlines():
                # print(line, end="")
                lb.insert(END, line)
            lb.pack(side=LEFT, fill=BOTH)
            sb.config(command=lb.yview)

        if self.aim_tool_number == "04-072":
            format_file = "./samples/04-072(01).csv"
            grou_sb_text = "绘图数据示例：" + str(format_file)
            # 添加显示文本的信息框
            group_sb = LabelFrame(export_frame, text=grou_sb_text, width=500, height=500, bg='#fff2cc', padx=5, pady=5)
            group_sb.grid(row=1, column=0, columnspan=2, sticky=W, pady=10)
            sb = Scrollbar(group_sb)
            sb.pack(side=RIGHT, fill=Y)
            lb = Listbox(group_sb, yscrollcommand=sb.set, width=80, height=24)
            file_in = open(format_file, 'r', encoding='utf-8')
            for line in file_in.readlines():
                # print(line, end="")
                lb.insert(END, line)
            lb.pack(side=LEFT, fill=BOTH)
            sb.config(command=lb.yview)

        if self.aim_tool_number == "05-05":
            format_file = "./samples/05-05(01).csv"
            grou_sb_text = "绘图数据示例：" + str(format_file)
            # 添加显示文本的信息框
            group_sb = LabelFrame(export_frame, text=grou_sb_text, width=500, height=500, bg='#fff2cc', padx=5, pady=5)
            group_sb.grid(row=1, column=0, columnspan=2, sticky=W, pady=10)
            sb = Scrollbar(group_sb)
            sb.pack(side=RIGHT, fill=Y)
            lb = Listbox(group_sb, yscrollcommand=sb.set, width=80, height=24)
            file_in = open(format_file, 'r', encoding='utf-8')
            for line in file_in.readlines():
                # print(line, end="")
                lb.insert(END, line)
            lb.pack(side=LEFT, fill=BOTH)
            sb.config(command=lb.yview)

        if self.aim_tool_number == "06-06":
            format_file = "./samples/06-06(01).csv"
            grou_sb_text = "绘图数据示例："+str(format_file)
            # 添加显示文本的信息框
            group_sb = LabelFrame(export_frame, text=grou_sb_text, width=500, height=500, bg='#fff2cc', padx=5, pady=5)
            group_sb.grid(row=1, column=0, columnspan=2, sticky=W, pady=10)
            sb = Scrollbar(group_sb)
            sb.pack(side=RIGHT, fill=Y)
            lb = Listbox(group_sb, yscrollcommand=sb.set, width=80, height=24)
            file_in = open(format_file, 'r', encoding='utf-8')
            for line in file_in.readlines():
                # print(line, end="")
                lb.insert(END, line)
            lb.pack(side=LEFT, fill=BOTH)
            sb.config(command=lb.yview)

        # # 添加下一步按钮
        btn_format = ttk.Button(export_frame, text="下一步", width=8, command=self.call_format_btn)
        btn_format.grid(row=0, column=1, sticky=W, padx=5)

    def call_format_btn(self):
        """
        用户获取到绘图数据格式后，开始个性化数据处理
        :return:
        """
        # 初始化绘图向导UI frame
        for widget in self.cv_frame.winfo_children():
            widget.destroy()

        # 个性化数据处理
        process_frame = LabelFrame(self.cv_frame, text="第四步：个性数据处理", width=600, height=100, bg='#fff2cc')
        process_frame.grid(row=0, column=0, sticky=W)
        process_frame.grid_propagate(0)  # 组件大小不变
        process_tips_str = "用户根据导出的绘图数据格式进行线下个性化数据处理(如:Excel、Python等)"
        process_label = Label(process_frame, text=process_tips_str, anchor="w", width=72, bg='#fff2cc')
        process_label.grid(row=0, column=0, sticky=W, padx=5)
        process_tips_str = "支持EXCEL、TXT、CSV、Json<参考绘图数据样例>"
        process_label = Label(process_frame, text=process_tips_str, anchor="w", width=72, bg='#fff2cc')
        process_label.grid(row=1, column=0, sticky=W, padx=5)

        # process_label_text = "<B>用户根据导出的绘图数据格式进行线下个性化数据处理(如:Excel、Python等)\n支持EXCEL、TXT、CSV、Json<参考绘图数据样例></i></B>"
        # process_label = HTMLLabel(process_frame, html=process_label_text, width=72, height=6)
        # process_label.grid(row=0, column=0, sticky=W, padx=5)
        # # 添加下一步按钮
        btn_process = ttk.Button(process_frame, text="下一步", width=8, command=self.call_process_btn)
        btn_process.grid(row=0, column=1, sticky=W, padx=5)

    def call_process_btn(self):
        """
        用户进行个性化数据处理后，进行绘图数据上传
        :return:
        """
        # 初始化绘图向导UI frame
        for widget in self.cv_frame.winfo_children():
            widget.destroy()

        # 用户上传绘图数据
        upload_frame = LabelFrame(self.cv_frame, text="第五步：上传绘图数据", width=600, height=100, bg='#fff2cc')
        upload_frame.grid(row=0, column=0, sticky=W)
        upload_frame.grid_propagate(0)  # 组件大小不变
        entry_str = StringVar(value="upload file...")
        upload_entry = Entry(upload_frame, textvariable=entry_str, width=72)
        upload_entry.grid(row=0, column=0, sticky=W, padx=5)
        upload_btn = ttk.Button(upload_frame, text='上传文件', width=8, command=self.open_file2upload)  # 文件打开对话框
        upload_btn.grid(row=0, column=1, sticky=W, padx=5)

    def open_file2upload(self):
        """
        打开文件, 准备上传文件并绘图
        :return:
        """
        # 初始化绘图向导UI frame
        for widget in self.cv_frame.winfo_children():
            widget.destroy()

        file_name = tk.filedialog.askopenfilename()
        if len(str(file_name)) != 0:
            print("Event:上传文件成功")
        else:
            print("Event:文件上传失败，重新上传")
            self.call_process_btn()

        # 用户上传绘图数据
        upload_frame = LabelFrame(self.cv_frame, text="第五步：上传绘图数据", width=600, height=100, bg='#fff2cc')
        upload_frame.grid(row=0, column=0, sticky=W)
        upload_frame.grid_propagate(0)  # 组件大小不变
        entry_str = StringVar(value=str(file_name))
        upload_entry = Entry(upload_frame, textvariable=entry_str, width=72)
        upload_entry.grid(row=0, column=0, sticky=W, padx=5)
        # upload_btn = ttk.Button(upload_frame, text='上传文件', width=8, command=self.open_file2upload)  # 文件打开对话框
        # upload_btn.grid(row=0, column=1, sticky=W)
        btn_upload = ttk.Button(upload_frame, text='下一步', width=8, command=self.call_upload_btn)
        btn_upload.grid(row=0, column=2, sticky=W, padx=5)

        # 确定下一步后，根据传入的文件名开始绘图
        # print("self.aim_tool_number:", self.aim_tool_number)
        if self.aim_tool_number == "01-01":
            try:
                graph_2d(file_name).render(self.new_draw_html)
                print("Event:绘图成功")
            except Exception as e:
                print("文件格式有误，绘图失败：", e)
                self.call_process_btn()
        elif self.aim_tool_number == "02-04":
            try:
                graph_starcloud(file_name).render(self.new_draw_html)
                print("Event:绘图成功")
            except Exception as e:
                print("文件格式有误，绘图失败：", e)
                self.call_process_btn()
        elif self.aim_tool_number == "03-03":
            try:
                polar(file_name).render(self.new_draw_html)
                print("Event:绘图成功")
            except Exception as e:
                print("文件格式有误，绘图失败：", e)
                self.call_process_btn()
        elif self.aim_tool_number == "04-071":
            try:
                map_china(file_name).render(self.new_draw_html)
                print("Event:绘图成功")
            except Exception as e:
                print("文件格式有误，绘图失败：", e)
                self.call_process_btn()
        elif self.aim_tool_number == "04-072":
            try:
                map_world(file_name).render(self.new_draw_html)
                print("Event:绘图成功")
            except Exception as e:
                print("文件格式有误，绘图失败：", e)
                self.call_process_btn()
        elif self.aim_tool_number == "05-05":
            try:
                words_cloud(file_name).render(self.new_draw_html)
                print("Event:绘图成功")
            except Exception as e:
                print("文件格式有误，绘图失败：", e)
                self.call_process_btn()
        elif self.aim_tool_number == "06-06":
            try:
                theme_river(file_name).render(self.new_draw_html)
                print("Event:绘图成功")
            except Exception as e:
                print("文件格式有误，绘图失败：", e)
                self.call_process_btn()
        else:
            print("该图例绘制算法尚未集成！")
            self.call_process_btn()

    def call_upload_btn(self):
        """
        用户上传绘图数据文件后，后台进行绘图，并在文件中生成图，返回给用户
        :return:
        """
        # 初始化绘图向导UI frame
        for widget in self.cv_frame.winfo_children():
            widget.destroy()

        # 用户获取绘图结果（绘图参数调优）
        result_frame = LabelFrame(self.cv_frame, text="第六步：获取绘图结果", width=600, height=100, bg='#fff2cc')
        result_frame.grid(row=0, column=0, sticky=W)
        result_frame.grid_propagate(0)  # 组件大小不变

        entry_str = StringVar(value="download file...")
        download_entry = Entry(result_frame, textvariable=entry_str, width=72)
        download_entry.grid(row=0, column=0, sticky=W, padx=5)
        download_btn = ttk.Button(result_frame, text='下载结果', width=8, command=self.down_load2save_file)
        download_btn.grid(row=0, column=1, sticky=W, padx=5)

    def down_load2save_file(self):
        """
        绘图结果文件另存为
        :return:
        """
        # 初始化绘图向导UI frame
        for widget in self.cv_frame.winfo_children():
            widget.destroy()

        self.open_download_dir()  # 打开下载文件夹
        # file_name = tk.filedialog.asksaveasfilename()
        # 用户获取绘图结果（绘图参数调优）
        result_frame = LabelFrame(self.cv_frame, text="第六步：获取绘图结果", width=600, height=100, bg='#fff2cc')
        result_frame.grid(row=0, column=0, sticky=W)
        result_frame.grid_propagate(0)  # 组件大小不变

        entry_str_value = "绘图结果为 " + str(self.new_draw_html) + "，已为您打开绘图结果本地下载目录"
        entry_str = StringVar(value=entry_str_value)
        download_entry = Entry(result_frame, textvariable=entry_str, width=72)
        download_entry.grid(row=0, column=0, sticky=W, padx=5)
        # download_btn = ttk.Button(result_frame, text='下载结果', width=8, command=self.down_load2save_file)  # 文件打开对话框
        # download_btn.grid(row=0, column=1, sticky=W)
        btn_download = ttk.Button(result_frame, text='下一步', width=8, command=self.call_download_btn)  # 文件打开对话框
        btn_download.grid(row=0, column=2, sticky=W, padx=5)

    def call_download_btn(self):
        """
        用户获取结果后，需要对绘图目标进行评价与反馈
        :return:
        """
        # 初始化绘图向导UI frame
        for widget in self.cv_frame.winfo_children():
            widget.destroy()

        # 目标反馈与评价
        feedback_frame = LabelFrame(self.cv_frame, text="第七步：目标反馈评价", width=600, height=100, bg='#fff2cc')
        feedback_frame.grid(row=0, column=0, sticky=W)
        feedback_frame.grid_propagate(0)  # 组件大小不变
        feedback_tips_str = "更多内容请联系规划所互联网网络研究部余文艳（yuwenyan@caict.ac.cn）"
        feedback_label = Label(feedback_frame, text=feedback_tips_str, anchor="w", width=72, bg='#fff2cc')
        feedback_label.grid(row=0, column=0, sticky=W, pady=10)

    def return_main(self):
        """
        回到主页
        :return:
        """
        print("Event:回到主页")
        self.__init__(self.root)

    def open_download_dir(self):
        # print("本地下载目录绝对路径: %s", os.path.abspath(self.download_dir))
        print("Event:打开本地下载目录")
        os.startfile(os.path.abspath(self.download_dir))

    def sample_list(self):
        """
        用html的形式查看作品
        :return:
        """
        print("Event:查看作品一览目录")
        os.startfile(os.path.abspath(self.sample_list_dir))

    def about_toolkit(self):
        """
        绘图工具的关于说明
        :return:
        """
        print("Event:关于页面")
        tk.messagebox.showinfo("CAICT-AtlasToolkit V0.1", "Using Python+Tkinter+Pyecharts+Matplotlib"
                                                          "\n亮点1：按照数给定数据格式，上传数据即可实现一键绘图；"
                                                          "\n亮点2：自主实现了ForceAtlas2的网络布局算法，并将其推广至3D；"
                                                          "\n亮点3：支持多种复杂图的绘制。\n"
                                                          "\n指导人员：李原、李想、张子飞\n开发人员：余文艳(yuwenyan@caict.ac.cn)"
                                                          "\n开发时间：2020年3月")


if __name__ == "__main__":
    # 创建一个Top Level的根窗口， 并把他们作为参数实例化为App对象
    # root = tk.Tk()
    root = ThemedTk(theme="elegant")
    root.title("CAICT地图绘制工具箱（CAICT-AtlasToolkit）")
    center_window(root, 0, 0)  # 设置窗口位置
    # root.maxsize(750, 800)
    root.minsize(770, 690)  # 设置窗口最小尺寸
    root.resizable(0, 0)  # 锁定尺寸
    # root.attributes("-alpha", 0.80)
    app = App(root)
    # 开始主事件循环
    root.mainloop()

