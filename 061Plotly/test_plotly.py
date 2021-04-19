# coding: utf-8
"""
create on Apr 19, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:
用过matplotlib、seaborn、pyecharts
据说plotly画图很不错，可以让数据绘图变得很愉悦，那就试试咯
让自己在数据科学和可视化方面变得更快、更强、更美
凡事追求简单和极致

"""
import plotly.graph_objects as go
import plotly.express as px
import random
import numpy as np

def first_figure():
    """

    :return None:
    """
    fig = go.Figure(data=go.Bar(x=["2018", "2019", "2020", "2021"], y=[611, 695, 834, 880]))
    fig.write_html('first_figure.html', auto_open=True)
    fig.write_image("first_figure.png", engine="kaleido")


def scatter_figure():
    """
    打点
    :return:
    """
    df = px.data.iris()
    print(df)

    x = []
    y = []

    for i in range(0, 10):
        x.append(random.uniform(-1, 1))
        y.append(random.uniform(-1, 1))

    fig = px.scatter(x, y)

    fig.write_html('scatter_figure.html', auto_open=True)
    fig.write_image("scatter_figure.png", engine="kaleido")


def line_figure():
    """
    画线
    :return:
    """
    t = []

    for i in range(0, 100):
        t.append(i/10)

    fig = px.line(x=t, y=np.cos(t), labels={'x': 't', 'y': 'cos(t)'})

    fig.write_html('line_figure.html', auto_open=True)
    fig.write_image("line_figure.png", engine="kaleido")


def bar_figure():
    """
    柱图
    :return:
    """
    years = ["2018", "2019", "2020", "2021"]
    nums = [611, 695, 834, 880]

    fig = px.bar(x=years, y=nums, labels={'x': 'years', 'y': 'nums'})
    fig.write_html('bar_figure.html', auto_open=True)
    fig.write_image("bar_figure.png", engine="kaleido")




if __name__ == "__main__":
    # first_figure()
    bar_figure()
