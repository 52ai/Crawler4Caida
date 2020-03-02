# coding:utf-8
"""
create on Mar 2, 2020 By Wenyan YU

Function:

尝试着用tkinter写一款简易图片浏览器
"""

import tkinter as tk
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        self.files = os.listdir(r'./GOOD')
        self.index = 0
        self.img = tk.PhotoImage(file=r'./GOOD' + '\\' + self.files[self.index])
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.lblImage = tk.Label(self, width=300, height=300)
        self.lblImage['image'] = self.img
        self.lblImage.pack()
        self.f = tk.Frame()
        self.f.pack()
        self.btnPrev = tk.Button(self.f, text='上一张', command=self.prev)
        self.btnPrev.pack(side=tk.LEFT)
        self.btnNext = tk.Button(self.f, text='下一张', command=self.next)
        self.btnNext.pack(side=tk.LEFT)

    def prev(self):
        self.showfile(-1)

    def next(self):
        self.showfile(1)

    def showfile(self, n):
        self.index += n
        if self.index < 0:
            self.index = len(self.files) - 1
        if self.index > (len(self.files) - 1):
            self.index = 0
        self.img = tk.PhotoImage(file=r'./GOOD' + '\\' + self.files[self.index])
        self.lblImage['image'] = self.img


root = tk.Tk()
root.title('简易图片浏览器')
app = Application(master=root)
app.mainloop()

