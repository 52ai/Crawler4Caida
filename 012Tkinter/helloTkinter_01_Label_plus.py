# coding:utf-8
"""
Create on 30 Aug,2019 by Wayne Yu
"""

from tkinter import *

root = Tk()
photo = PhotoImage(file="./bg.gif")
theLabel = Label(root, text="Hello, Python!Hello, Tkinter!\n--By Wayne Yu", justify=LEFT, image=photo,
                 compound=CENTER, font=("幼圆", 20), fg="white")
theLabel.pack()
mainloop()
