# coding:utf-8
"""
由Wayne 创建于2019年9月11日
版本V4:主要在V3版本基础之上实现了一个UI界面
"""

from tkinter import *
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import ttk

class App:
    def __init__(self, root):
        # 用两个LabelFrame将TopView分为两个区
        # 左部区域
        group_left = LabelFrame(root, text="INPUT", padx=5, pady=5)
        group_left.grid(row=0, column=0, sticky=W)
        Label(group_left, text="City：").grid(row=0, column=0, sticky=W, padx=10, pady=5)
        Label(group_left, text="Company：").grid(row=1, column=0, sticky=W, padx=10, pady=5)
        Label(group_left, text="Thread：").grid(row=2, column=0, sticky=W, padx=10, pady=5)
        Button(group_left, text="Run", width=10, command=self.run).grid(row=3, column=0, sticky=W, padx=10, pady=5)
        Button(group_left, text="Sop", width=10, command=self.stop).grid(row=3, column=1, sticky=E, padx=10, pady=5)
        Button(group_left, text="Exit", width=10, command=root.quit).grid(row=3, column=2, sticky=W, padx=10, pady=5)

        v1 = StringVar()
        v2 = StringVar()
        self.e1 = Entry(group_left, text=v1, validate="focusout", width=31)
        self.e2 = Entry(group_left, text=v2, validate="focusout", width=31)
        comvalue = StringVar()
        self.c_tread = ttk.Combobox(group_left, textvariable=comvalue, width=10)
        self.c_tread["values"] = ("33", "11", "1")
        self.c_tread.current(0)  # 选择第一个

        self.e1.grid(row=0, column=1, sticky=W, padx=10, pady=5)
        self.e2.grid(row=1, column=1, sticky=W, padx=10, pady=5)
        self.c_tread.grid(row=2, column=1, sticky=W, padx=10, pady=5)

        # 右部区域
        group_right = LabelFrame(root, text="OUTPUT", padx=5, pady=5)
        group_right.grid(row=1, column=0, sticky=W)

        sb_r = Scrollbar(group_right)
        sb_r.pack(side=RIGHT, fill=Y)
        self.lb_r = Listbox(group_right, yscrollcommand=sb_r.set, width=60)
        self.lb_r.pack(side=LEFT, fill=BOTH)
        sb_r.config(command=self.lb_r.yview)



    def run(self):
        print("City: %s " % self.e1.get())
        print("Company: %s" % self.e2.get())
        print("Thread: %s" % self.c_tread.get())

    def stop(self):
        pass


if __name__ == "__main__":
    # 创建一个top level的根窗口，并把他作为参数实例化APP对象
    root = tk.Tk()
    root.title("International Network Speed Tools-V4.0(By Wayne Yu)")
    root.minsize(400, 400)  # 设置最小尺寸
    app = App(root)
    # 开始主事件循环
    root.mainloop()



