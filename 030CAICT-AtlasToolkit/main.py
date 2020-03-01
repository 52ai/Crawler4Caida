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
from pyecharts.charts import Graph, Page
from pyecharts.globals import ThemeType
import json


def graph_2d(open_file) -> Graph:
    title_str = str(open_file).strip().split("/")[-1].split(".")[0]
    title_str = "Graph<" + title_str + ">"
    with open(open_file, "r", encoding="utf-8") as f:
        j = json.load(f)
        nodes, links, categories = j
    c = (
        Graph(init_opts=opts.InitOpts(width="1920px", height="900px", page_title=title_str, theme=ThemeType.INFOGRAPHIC))
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
        Button(func_frame_top, text="作品一览", anchor="e", width=21, fg='white', bg='#4bacc6').grid(row=2, column=0, sticky=N)
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
        Button(func_frame_bottom, text="关于", anchor="e", width=21, fg='white', bg='#4bacc6').grid(row=8, column=0, sticky=S)

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
            tool_list = ["01-网络拓扑图（2D）",
                         "02-网络拓扑图（3D）"]

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
            tool_list = ["07-地理图绘制系列"]
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
                       "01-02": {"nodes": ["name", "symbolSize",  "..."], "links": ["source", "target"], "categories": ["name"]},
                       "02-04": {"nodes": ["name", "symbolSize",  "..."], "links": ["source", "target"], "categories": ["name"]},
                       "03-03": {"line": ["node_name", "angle", "radius"]},
                       "04-07": {"line": ["node_name", "longitude", "latitude"]},
                       "05-05": {"line": ["words", "frequency"]},
                       "06-06": {"line": ["date", "values", "theme"]}}
        # 导出绘图数据格式
        export_frame = LabelFrame(self.cv_frame, text="第三步：导出数据格式", width=600, height=580, bg='#fff2cc')
        export_frame.grid(row=0, column=0, sticky=W)
        export_frame.grid_propagate(0)  # 组件大小不变

        format_label = Label(export_frame, text=str(data_format[str(self.aim_tool_number)]), anchor="w", width=72, bg='#fff2cc')
        format_label.grid(row=0, column=0, sticky=W, padx=5)

        if self.aim_tool_number == "01-01":
            format_file = "./samples/01-01(01).json"
            grou_sb_text = "绘图数据示例："+str(format_file)
            # 添加显示文本的信息框
            group_sb = LabelFrame(export_frame, text=grou_sb_text, width=500, height=500, bg='#fff2cc', padx=5, pady=5)
            group_sb.grid(row=1, column=0, columnspan=2, sticky=W)
            sb = Scrollbar(group_sb)
            sb.pack(side=RIGHT, fill=Y)
            lb = Listbox(group_sb, yscrollcommand=sb.set, width=80, height=24)
            format_file = "./samples/01-01(01).json"
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
        process_tips_str = "支持EXCEL、TXT、CSV、Json"
        process_label = Label(process_frame, text=process_tips_str, anchor="w", width=72, bg='#fff2cc')
        process_label.grid(row=1, column=0, sticky=W, padx=5)

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
                graph_2d(file_name).render("./image/current.html")
                print("Event:绘图成功")
            except Exception as e:
                print("文件格式有误，绘图失败：", e)
                self.call_process_btn()
        else:
            print("该图例绘制算法尚未集成！")

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

        entry_str = StringVar(value=str("绘图结果为./image/current.html，已为您打开绘图结果本地下载目录"))
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
        feedback_tips_str = "更多内容请联系yuwneyan@caict.ac.cn"
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

