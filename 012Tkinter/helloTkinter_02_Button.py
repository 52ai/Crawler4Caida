# coding:utf-8
"""
Create on 30 Aug,2019 by Wayne Yu
"""

from tkinter import *


def callback():
    var.set("吹吧你，我才不信嘞！")

root = Tk()
frame1 = Frame(root)
frame2 = Frame(root)
# 创建一个文本Label对象
var = StringVar()
var.set("您所下载的影片含有未成年人限制内容，\n请满18岁后再点击观看！")
textLabel = Label(frame1, textvariable=var, justify=LEFT)
textLabel.pack(side=LEFT)
# 创建一个图形Label对象
# 用PhotoImage实例化一个图片对象(支持gif格式文件哦)
photo = PhotoImage(file="./warning.gif")
imgLabel = Label(frame1, image=photo)
imgLabel.pack(side=RIGHT)
# 加一个按钮
theButton = Button(frame2, text="已满18周岁", command=callback)
theButton.pack()
frame1.pack(padx=10, pady=10)
frame2.pack(padx=10, pady=10)

mainloop()
