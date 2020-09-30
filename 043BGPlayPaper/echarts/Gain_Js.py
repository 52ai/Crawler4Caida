# coding: utf-8
"""
create on Sep 29, 2020 By Wenyan YU
FUnction:

获取echarts的JS文件

"""
import wget

if __name__ == "__main__":
    url_list = ['http://static.popodv.com/dvlibs/echarts/echarts.v4.min.js',
                'http://static.popodv.com/dvlibs/echarts/echarts-gl.v1.min.js',
                'http://static.popodv.com/dvlibs/data/graph-modularity.js',
                'http://static.popodv.com/dvlibs/tool/jquery.min.js']

    for url in url_list:
        wget.download(url, url.strip().split("/")[-1])
