# coding:utf-8
"""
create on Dec 11, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:测试Python绘制词云图

"""
import matplotlib.pyplot as plt
import jieba
import jieba.analyse
from wordcloud import wordcloud
from PIL import Image
import numpy as np
import re


def count_fre_dict(word_list):
    """
    根据传入的word list,统计其词频信息，以字典的形式返回
    :param word_list:
    :return re_dict:
    """
    re_dict = {}  # 存储统计词频的字典
    for item in word_list:
        if item not in re_dict.keys():
            re_dict[item] = 1
        else:
            re_dict[item] += 1

    return re_dict


def count_fre_list(word_list):
    """
    根据传入的word list,统计其词频信息，以列表的形式返回
    :param word_list:
    :return re_dict:
    """
    re_dict = {}  # 存储统计词频的字典
    for item in word_list:
        if item not in re_dict.keys():
            re_dict[item] = 1
        else:
            re_dict[item] += 1
    re_list = []  # 存储返回的列表
    for key in re_dict.keys():
        re_list.append([key, re_dict[key]])
    re_list.sort(reverse=True, key=lambda elem: int(elem[1]))
    return re_list


# 读词 D:\Code\Crawler4Caida\056WordCloud\test_project.txt
text = open("D:/Code/Crawler4Caida/056WordCloud/test_project.txt", 'r', encoding='utf-8').read()
# print(text)
text = text.strip("\n")
text = re.sub("[()（）\"，。、”.“〇！；]", "", text)

# 获取文本主题词
print(jieba.analyse.extract_tags(text, topK=20, withWeight=False, allowPOS=()))

# 分词
text = text.replace('\n', "")
cut_text = jieba.lcut(text)
# print(count_fre_list(cut_text))


# result = ' '.join(cut_text)
# print(result)


# 绘图
background = Image.open("D:/Code/Crawler4Caida/056WordCloud/fu.jpg")
graph = np.array(background)

stop_words = set(open('D:/Code/Crawler4Caida/056WordCloud/cn_stopwords.txt', encoding="utf-8").read().split("\n"))
# print(stop_words)

wc = wordcloud.WordCloud(
    font_path='C:/Windows/Fonts/simsun.ttc',  # 字体路径
    background_color='white',  # 背景颜色
    # width=1080,
    # height=960,
    # max_font_size=50,  # 字体大小
    # min_font_size=10,
    mask=graph,  # 指定词云形状
    # max_words=1000,
    mode='RGBA',
    stopwords=stop_words
)

# wc.generate(result)
wc.fit_words(count_fre_dict(cut_text))
wc.to_file('D:/Code/Crawler4Caida/056WordCloud/result_project.png')  # 图片显示的名字
plt.subplots(figsize=(12, 8))
plt.imshow(wc)
plt.axis('off')  # 关闭坐标
plt.savefig("D:/Code/Crawler4Caida/056WordCloud/result_project_2020.png", dpi=600, facecolor='white')
# plt.show()
