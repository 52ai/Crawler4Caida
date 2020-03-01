# coding:utf-8
"""
create on Feb 29. 2020 By Wenyan YU

Function:

实现CAICT地图绘制工具箱（CAICT-AtlasToolkit）的主界面

"""
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog
from ttkthemes import ThemedTk, ThemedStyle

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
        self.aim_v_radio = tk.IntVar()  # 绘图目标单选按钮值
        self.tool_v_radio = tk.IntVar()  # 绘图工具单选按钮值
        self.root = root
        # 增加菜单栏
        menu_bar = Menu(root)
        root.config(menu=menu_bar)
        # #增加文件一级菜单
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="文件(F)", menu=file_menu)
        file_menu.add_command(label="新建画布")
        file_menu.add_command(label="打开文件")
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.quit)

        # #增加工作区一级菜单
        workplace_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="工作区", menu=workplace_menu)
        workplace_menu.add_command(label="返回主页", command=self.return_main)

        # #增加视图一级菜单
        view_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="视图(V)", menu=view_menu)
        view_menu.add_command(label="全屏")

        # #增加工具一级菜单
        tool_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="工具(T)", menu=tool_menu)
        tool_menu.add_command(label="选项")
        tool_menu.add_command(label="在线文档和支持")

        # #增加窗口一级菜单
        window_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="窗口(W)", menu=window_menu)
        window_menu.add_command(label="配置")

        # #增加帮助一级菜单
        help_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="帮助(H)", menu=help_menu)
        help_menu.add_command(label="检查更新")
        help_menu.add_command(label="关于")

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
        Button(func_frame_top, text="作品一览", anchor="e", width=21, fg='white', bg='#4bacc6').grid(row=1, column=0, sticky=N)

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
        aim_frame = LabelFrame(self.cv_frame, text="第一步：确定绘图目标", width=600, height=60, bg='#fff2cc')
        aim_frame.grid(row=0, column=0, sticky=W)
        aim_frame.grid_propagate(0)  # 组件大小不变
        # #给绘图目标Label Frame里面添加Radiobutton
        aim_list = ["希望展示数据间的关联关系（小规模网络拓扑）",
                    "希望展示数据间的关联关系（大规模网络拓扑）",
                    "希望展示数据间的地位排名",
                    "希望进行数据地理位置展示",
                    "希望分析文本数据词频信息",
                    "希望展示多类时间序列数据"]

        # for i in range(0, len(aim_list)):
        #     Radiobutton(aim_frame, text=aim_list[i], command=self.call_aim_rb, variable=self.aim_v_radio, value=i, bg='#fff2cc').grid(row=i, column=0, sticky=W)

        comvalue_aim = StringVar()
        c_aim = ttk.Combobox(aim_frame, textvariable=comvalue_aim, width=80)
        c_aim["values"] = aim_list
        c_aim.current(1)
        c_aim.grid(row=0, column=0, sticky=W)

        # 根据第一步的选择自动给出绘图实例

    def call_aim_rb(self):
        """
        绘图目标单选按钮单击事件，生成绘图工具选择、导出绘图数据格式、个性化数据处理、用户上传绘图数据、用户获取绘图结果（绘图参数调优）、目标反馈与评价
        :return:
        """
        tool_frame = LabelFrame(self.cv_frame, text="第二步：选择绘图工具", width=600, height=80, bg='#fff2cc')
        tool_frame.grid(row=1, column=0, sticky=W)
        tool_frame.grid_propagate(0)  # 组件大小不变

        # 导出绘图数据格式
        export_frame = LabelFrame(self.cv_frame, text="第三步：导出数据格式", width=600, height=50, bg='#fff2cc')
        export_frame.grid(row=2, column=0, sticky=W)
        export_frame.grid_propagate(0)  # 组件大小不变

        if self.aim_v_radio.get() == 0:
            # 希望展示数据间的关联关系（小规模网络拓扑）, 01 02图例均可
            # 先清空tool_frame
            for widget in tool_frame.winfo_children():
                widget.destroy()
            tool_list = ["01网络拓扑图（2D）",
                         "02网络拓扑图（3D）"]
            for i in range(0, len(tool_list)):
                Radiobutton(tool_frame, text=tool_list[i], variable=self.tool_v_radio, value=i, bg='#fff2cc').grid(row=i, column=0, sticky=W)
        elif self.aim_v_radio.get() == 1:
            # 希望展示数据间的关联关系（大规模网络拓扑）, 04图例
            # 先清空tool_frame
            for widget in tool_frame.winfo_children():
                widget.destroy()
            tool_list = ["04星云图"]
            for i in range(0, len(tool_list)):
                Radiobutton(tool_frame, text=tool_list[i], variable=self.tool_v_radio, value=i, bg='#fff2cc').grid(row=i, column=0, sticky=W)
        elif self.aim_v_radio.get() == 2:
            # 希望展示数据间的地位排名, 03图例
            # 先清空tool_frame
            for widget in tool_frame.winfo_children():
                widget.destroy()
            tool_list = ["03极坐标图"]
            for i in range(0, len(tool_list)):
                Radiobutton(tool_frame, text=tool_list[i], variable=self.tool_v_radio, value=i, bg='#fff2cc').grid(row=i, column=0, sticky=W)
        elif self.aim_v_radio.get() == 3:
            # 希望进行数据地理位置展示, 07图例
            # 先清空tool_frame
            for widget in tool_frame.winfo_children():
                widget.destroy()
            tool_list = ["07地理图绘制系列"]
            for i in range(0, len(tool_list)):
                Radiobutton(tool_frame, text=tool_list[i], variable=self.tool_v_radio, value=i, bg='#fff2cc').grid(row=i, column=0, sticky=W)
        elif self.aim_v_radio.get() == 4:
            # 希望分析文本数据词频信息, 05图例
            # 先清空tool_frame
            for widget in tool_frame.winfo_children():
                widget.destroy()
            tool_list = ["05词汇云图"]
            for i in range(0, len(tool_list)):
                Radiobutton(tool_frame, text=tool_list[i], variable=self.tool_v_radio, value=i, bg='#fff2cc').grid(row=i, column=0, sticky=W)
        elif self.aim_v_radio.get() == 5:
            # 希望展示多类时间序列数据, 06图例
            # 先清空tool_frame
            for widget in tool_frame.winfo_children():
                widget.destroy()
            tool_list = ["06主题河流图"]
            for i in range(0, len(tool_list)):
                Radiobutton(tool_frame, text=tool_list[i], variable=self.tool_v_radio, value=i, bg='#fff2cc').grid(row=i, column=0, sticky=W)

        # 个性化数据处理
        process_frame = LabelFrame(self.cv_frame, text="第四步：个性数据处理", width=600, height=100, bg='#fff2cc')
        process_frame.grid(row=3, column=0, sticky=W)
        process_frame.grid_propagate(0)  # 组件大小不变

        # 用户上传绘图数据
        upload_frame = LabelFrame(self.cv_frame, text="第五步：上传绘图数据", width=600, height=50, bg='#fff2cc')
        upload_frame.grid(row=4, column=0, sticky=W)
        upload_frame.grid_propagate(0)  # 组件大小不变

        # 用户获取绘图结果（绘图参数调优）
        result_frame = LabelFrame(self.cv_frame, text="第六步：获取绘图结果", width=600, height=50, bg='#fff2cc')
        result_frame.grid(row=5, column=0, sticky=W)
        result_frame.grid_propagate(0)  # 组件大小不变

        # 目标反馈与评价
        feedback_frame = LabelFrame(self.cv_frame, text="第七步：目标反馈评价", width=600, height=50, bg='#fff2cc')
        feedback_frame.grid(row=6, column=0, sticky=W)
        feedback_frame.grid_propagate(0)  # 组件大小不变

    def return_main(self):
        """
        回到主页
        :return:
        """
        print("Event:回到主页")
        self.__init__(self.root)


if __name__ == "__main__":
    # 创建一个Top Level的根窗口， 并把他们作为参数实例化为App对象
    # root = tk.Tk()
    root = ThemedTk(theme="arc")
    root.title("CAICT地图绘制工具箱（CAICT-AtlasToolkit）")
    center_window(root, 0, 0)  # 设置窗口位置
    # root.maxsize(750, 800)
    root.minsize(770, 690)  # 设置窗口最小尺寸
    root.resizable(0, 0)  # 锁定尺寸
    # root.attributes("-alpha", 0.80)
    app = App(root)
    # 开始主事件循环
    root.mainloop()

