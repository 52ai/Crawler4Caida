# coding:utf-8
"""
create on 30 Aug,2019 by Wayne Yu

这是一个可以把所有Tkinter的控件都用上的综合界面，少即是多，用Tkinter简单、方便、快捷。

"""

from tkinter import *
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from ttkthemes import ThemedTk


class App:
    def __init__(self, root):

        # 登录的Frame
        group_login = LabelFrame(root, text="用户登录", padx=5, pady=5)
        group_login.grid(row=1, column=0, columnspan=3, sticky=W)
        Label(group_login, text="User:").grid(row=0, column=0, sticky=W, padx=10, pady=5)
        Label(group_login, text="Password:").grid(row=1, column=0, sticky=W, padx=10, pady=5)
        v = StringVar()
        self.e1 = Entry(group_login, text=v, validate="focusout", validatecommand=self.test_entry, width=31)  # 加了验证函数
        self.e2 = Entry(group_login, show="*", width=31)
        self.e1.grid(row=0, column=1, sticky=E, padx=10, pady=5)
        self.e2.grid(row=1, column=1, sticky=E, padx=10, pady=5)

        # 如果表格大于组件，那么可以使用sticky选项来设置组件的位置
        # 同样我们需要使用N,E,S,W以及他们的组合NE,SE,SW,NW来表示方位、
        Button(group_login, text="获取信息", width=10, command=self.show).grid(row=0, column=2, sticky=E, padx=10, pady=5)
        Button(group_login, text="退出程序", width=10, command=root.quit).grid(row=1, column=2, sticky=E, padx=10, pady=5)

        # LabelFrame组件
        group_code = LabelFrame(root, text="最好的脚本语言是？", padx=5, pady=5)
        group_code.grid(row=2, column=0, columnspan=3, sticky=W)
        LANGS = [("life is short, you need Python!", 1), ("Perl", 2), ("Ruby", 3), ("Lua", 4)]
        v = IntVar()
        v.set(1)
        for lang, num in LANGS:
            self.b = Radiobutton(group_code, text=lang, variable=v, value=num, indicatoron=False, width=60)
            # b = Radiobutton(group, text=lang, variable=v, value=num, width=60)
            self.b.pack(anchor=W)

        # CheckButton组件（多选框）
        group_girls = LabelFrame(root, text="选出下面谁是美女？？", padx=5, pady=5)
        group_girls.grid(row=3, column=0, columnspan=3, sticky=W)
        GIRLS = ["西施", "王昭君", "貂蝉", "杨玉环"]
        v = []
        for girl in GIRLS:
            v.append(IntVar())
            self.c = Checkbutton(group_girls, text=girl, variable=v[-1])
            self.c.pack(anchor=W)

        # Listbox组件
        # 创建一个空列表
        group_lb = LabelFrame(root, text="比较牛逼的互联网企业", padx=5, pady=5)
        group_lb.grid(row=4, column=0, columnspan=3, sticky=W)
        self.Listbox_info = Listbox(group_lb, width=60, height=8)
        self.Listbox_info.pack()
        # 往列表里添加数据
        for item in ["百度", "阿里巴巴", "腾讯", "网易", "新浪", "今日头条"]:
            self.Listbox_info.insert(END, item)

        # Scrollbar组件
        group_sb = LabelFrame(root, text="可以滚动的框", padx=5, pady=5)
        group_sb.grid(row=5, column=0, columnspan=3, sticky=W)
        sb = Scrollbar(group_sb)
        sb.pack(side=RIGHT, fill=Y)
        self.lb = Listbox(group_sb, yscrollcommand=sb.set, width=58, height=5)
        for i in range(1000, 10000):
            self.lb.insert(END, str(i))
        self.lb.pack(side=LEFT, fill=BOTH)
        sb.config(command=self.lb.yview)

        # Scale, 区域控制条组件
        group_scale = LabelFrame(root, text="区域控制条组件", padx=5, pady=5)
        group_scale.grid(row=6, column=0, columnspan=3, sticky=W)
        self.s1 = Scale(group_scale, from_=0, to=42, orient=HORIZONTAL)
        self.s1.pack()
        Button(group_scale, text='打开文件', command=tk.filedialog.askopenfilename).pack(fill=X)  # 文件打开对话框

        # 图像显示
        global photo_python
        global img_lable_python
        photo_python = tk.PhotoImage(file="./python.gif")
        img_lable_python = Label(group_girls, image=photo_python, width=420, height=100)
        img_lable_python.pack(anchor=W)

    def show(self):
        print("User:<< %s >>" % self.e1.get())
        print("Password:<< %s >>" % self.e2.get())
        self.e1.delete(0, END)
        # self.e1.insert(0, "请输入用户名…")
        self.e2.delete(0, END)
        print("区域控制条S1:%s" % self.s1.get())
        # print("可滚动的框lb:%s" % self.lb.get(self.lb.curselection()))

    def test_entry(self):
        if len(self.e1.get()) > 6:
            print("输入正确！")
            return True
        else:
            # print("输入长度不够，请重新输入！")
            tk.messagebox.showinfo("提示", "输入用户名长度不够，请重新输入！")
            self.e1.delete(0, END)
            return False


if __name__ == "__main__":
    # 创建一个top level的根窗口，并把他作为参数实例化APP对象
    # root = tk.Tk()
    root = ThemedTk(theme="arc")
    root.minsize(400, 870)  # 设置最小尺寸
    app = App(root)
    # 开始主事件循环
    root.mainloop()


