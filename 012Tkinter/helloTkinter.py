# coding:utf-8
"""
Create on 20 Aug,2019 by Wayne Yu

Less is more! Using Tkinter.

"""

import tkinter as tk

root = tk.Tk()  # 创建一个主窗口，用于容纳整个GUI程序
root.title("NEW")  # 设置主窗口对象的标题栏

the_lable = tk.Label(root, text="Hello，Python GUI---Tkinter!")  # 添加一个Label组件，Label可以显示文本、图标或图片
the_lable.pack()  # 调用Label组件的pack()方法，用于自动调节组件自身尺寸
root.mainloop()
