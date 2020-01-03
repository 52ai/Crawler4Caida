# codding:utf-8
"""
create on Jan 2,2020 By Wayne Yu

Function: 五分钟快速开始pyecharts

"""

import pyecharts
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.render import make_snapshot

# 使用snapshot-selenium渲染图片
from snapshot_selenium import snapshot

# 内置类型可查看 pyecharts.globals.ThemeType
from pyecharts.globals import ThemeType

print(pyecharts.__version__)
print(pyecharts.__author__)

bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
bar.add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
bar.add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
bar.add_yaxis("商家B", [15, 6, 20, 30, 35, 66])

# 使用options配置项，在pyecharts中，一切皆Options
bar.set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))

# pycharts 所有方法均支持链式调用
# bar = (
#     Bar()
#     .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
#     .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
# )

make_snapshot(snapshot, bar.render(), "bar.png")
