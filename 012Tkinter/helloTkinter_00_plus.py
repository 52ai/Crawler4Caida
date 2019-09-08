# utf-8
"""
create on 28 Aug,2019 by Wayne Yu

采用类的思想来编写UI程序
"""

import tkinter as tk


class App:
    def __init__(self, root):
        frame = tk.Frame(root)  # 创建一个框架
        frame.pack()  # 框架一般适用于在复杂的布局中起到组件分组的作用
        self.hi_there = tk.Button(frame, text="Hello！", fg="blue", command=self.say_hi)
        self.hi_there.pack(side=tk.LEFT)

    def say_hi(self):
        print("This a event when you clicked the button!")


if __name__ == "__main__":
    # 创建一个top level的根窗口，并把他作为参数实例化APP对象
    root = tk.Tk()
    app = App(root)
    # 开始主事件循环
    root.mainloop()


