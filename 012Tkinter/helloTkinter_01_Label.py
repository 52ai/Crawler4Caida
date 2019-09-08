# coding:utf-8
"""
Create on 29 Aug,2019 by Wayne Yu
"""

from tkinter import *

root = Tk()
textLabel = Label(root, text="There is a potential safety hazard on this page.", justify=LEFT, padx=10)
textLabel.pack(side=LEFT)
# 创建一个图像Label对象，这里只支持gif格式的图片
photo = PhotoImage(file="./warning.gif")
imgLabel = Label(root, image=photo)
imgLabel.pack(side=RIGHT)

mainloop()