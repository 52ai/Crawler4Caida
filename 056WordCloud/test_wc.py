# coding:utf-8
"""
create on Dec 11, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:测试Python绘制词云图

"""
import matplotlib.pyplot as plt
import jieba
from wordcloud import wordcloud
from PIL import Image
import numpy as np

# 读词
text = open("wp.txt", 'r', encoding='utf-8').read()
print(text)

# 分词
text = text.replace('\n', "")
cut_text = jieba.lcut(text)
result = ' '.join(cut_text)
print(result)

# 绘图
background = Image.open("fu.jpg")
graph = np.array(background)

wc = wordcloud.WordCloud(
    font_path='C:/Windows/Fonts/simsun.ttc',  # 字体路径
    background_color='white',  # 背景颜色
    # width=1080,
    # height=960,
    # max_font_size=50,  # 字体大小
    # min_font_size=10,
    mask=graph,  # 指定词云形状
    max_words=1000,
    mode='RGBA'
)
wc.generate(result)
wc.to_file('result.png')  # 图片显示的名字
plt.subplots(figsize=(12, 8))
plt.imshow(wc)
plt.axis('off')  # 关闭坐标
plt.savefig("result_plt.png", dpi=600, facecolor='white')
plt.show()

