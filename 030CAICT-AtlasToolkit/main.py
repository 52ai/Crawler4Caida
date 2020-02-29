# coding:utf-8
"""
create on Feb 29. 2020 By Wenyan YU

Function:

实现CAICT地图绘制工具箱（CAICT-AtlasToolkit）的主界面

"""
from tkinter import *
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog


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
        cv_frame = Frame(root, width=600, height=685)
        cv_frame.grid(row=0, rowspan=5, column=0, sticky=W)
        self.cv = Canvas(cv_frame, width=600, height=685, bg='#fff2cc')
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
        Button(func_frame_mid, text="04极星云图", anchor="e", width=21, fg='white', bg='#9dbb61').grid(row=4, column=0, sticky=W)
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
        # 清空画布
        self.cv.delete(image)

    def return_main(self):
        """
        回到主页
        :return:
        """
        print("Event:回到主页")
        self.__init__(self.root)


if __name__ == "__main__":
    # 创建一个Top Level的根窗口， 并把他们作为参数实例化为App对象
    root = tk.Tk()
    root.title("CAICT地图绘制工具箱（CAICT-AtlasToolkit）")
    center_window(root, 0, 0)  # 设置窗口位置
    # root.maxsize(750, 800)
    root.minsize(770, 690)  # 设置窗口最小尺寸
    root.resizable(0, 0)  # 锁定尺寸
    app = App(root)
    # 开始主事件循环
    root.mainloop()

