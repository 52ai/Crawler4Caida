# coding:utf-8
"""
create on Feb 16, 2020 By Wenyan YU
Function:

该程序用于将李博士让大家人工提取关键词的数据和我程序爬取的数据进行整合
INPUT:
research_subject_clean.csv
院软科学研究课题与专报（2010-2019）-合稿.xlsx

目前暂只使用院软课题数据
整合后的数据项以李博士提供团课题数据项为基准，共计1690个。
数据以李博士整理的十年间院课题名称为key，整合其中领域、研究方向、关键词三项数据项

最终形成数据格式如下：
课题名称、课题编号、时间、负责人、负责单位、课题类型、课题领域、研究方向、关键词、课题内容、课题URL

共计1690个数据项，时间跨度为十年左右

最后将整合后的数据进行绘图，目前有两个想法
院软课题网络拓扑图（生成json数据）
院软课题关键词十年变化图（制作动态图，可借鉴各国人均寿面与GDP关系演变）。

"""
import openpyxl
import csv
import time
from urllib.request import urlopen
import json
from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.globals import ThemeType


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csvFile = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csvFile, delimiter="|")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def data_intergrate_draw(res_auto_file_path, res_manual_file_path, des_file_path):
    """
    对传入的原始数据进行数据整合，并绘图
    :param res_auto_file_path:
    :param res_manual_file_path:
    :param des_file_path:
    :return:
    """
    print("待处理的输入数据源:")
    print(res_auto_file_path)
    print(res_manual_file_path)
    workbook = openpyxl.load_workbook(res_manual_file)
    worksheet = workbook.worksheets[1]  # 读取软课题研究表
    """
    读取人工标注的信息
    """
    res_manual_list = []  # 存储人工标注的数据
    temp_list = []
    res_name_list = []  # 存储name_list 用于去重
    for row in worksheet.rows:
        # for cell in row:
        #     print(cell.value, end="")
        # print(row[0].value)
        if str(row[2].value) in res_name_list:
            continue
        temp_list.append(row[2].value)  # 添加题目
        temp_list.append(row[3].value)  # 添加领域
        temp_list.append(row[4].value)  # 添加研究方向
        key_words_str = ""
        for cell in row[5:]:
            if str(cell.value) != "None":
                key_words_str = key_words_str + str(cell.value).strip() + "、"
        key_words_str = key_words_str[0:-1]
        temp_list.append(key_words_str)
        res_manual_list.append(temp_list)
        res_name_list.append(str(row[2].value))
        temp_list = []
    res_manual_list = res_manual_list[1:]  # 去除头部的信息
    print("处理完成的人工标注信息记录数：", len(res_manual_list))
    # print(res_manual_list)
    """
    读取程序采集的数据生成key-value数据，key为标题，value 为相关字段
    """
    res_auto_file_read = open(res_auto_file_path, 'r', encoding='utf-8')
    res_auto_dict = {}
    res_auto_cnt = 0
    for line in res_auto_file_read.readlines():
        line = line.strip().split("|")
        # print(line)
        res_auto_dict[line[0]] = line[1:]
        res_auto_cnt += 1
    # print(res_auto_dict)
    print("处理完成的程序采集信息记录数：", res_auto_cnt)
    """
    开始做数据的整合
    """
    res_intergrate_list = []
    temp_list = []
    for item in res_manual_list:
        try:
            temp_list.append(item[0])
            temp_list.extend(res_auto_dict[item[0]][0:5])
            temp_list.extend(item[1:])
            temp_list.extend(res_auto_dict[item[0]][5:])
            res_intergrate_list.append(temp_list)
        except Exception as e:
            # print("ERROR:", e)
            pass
        finally:
            temp_list = []
    print("整合完成后的记录数：", len(res_intergrate_list))
    # print(res_intergrate_list)
    # 存储整合后的数据
    write_to_csv(res_intergrate_list, des_file_path)


def generate_json(res_file_path):
    """
    根据传入res_file_path数据，生成绘制院软课题网络拓扑图所需的json数据
    :param res_list:
    :return:
    """
    res_file_read = open(res_file_path, 'r', encoding='utf-8')
    res_list = []
    for line in res_file_read.readlines():
        line = line.strip().split("|")
        res_list.append(line)
    print("处理完成的程序采集信息记录数：", len(res_list))
    html = urlopen(r'https://www.echartsjs.com/examples/data/asset/data/webkit-dep.json')
    hjson = json.loads(html.read())
    hjson_web = hjson
    # print(hjson)
    # 生成tyepe
    type = "force"
    # 生成categories
    categories_list = [{'name': '无线移动', 'keyword': {}, 'base': '无线移动'},
                       {'name': '信息网络', 'keyword': {}, 'base': '信息网络'},
                       {'name': '大数据与人工智能', 'keyword': {}, 'base': '大数据与人工智能'},
                       {'name': '先进计算', 'keyword': {}, 'base': '先进计算'},
                       {'name': '数字经济与法律监管', 'keyword': {}, 'base': '数字经济与法律监管'},
                       {'name': '两化融合与产业互联网', 'keyword': {}, 'base': '两化融合与产业互联网'},
                       {'name': '网络安全与国际治理', 'keyword': {}, 'base': '网络安全与国际治理'},
                       {'name': 'ICT', 'keyword': {}, 'base': 'ICT'}]
    # 生成nodes
    categories_dict = {'无线移动': 0,
                       '信息网络': 1,
                       '大数据与人工智能': 2,
                       '先进计算': 3,
                       '数字经济与法律监管': 4,
                       '两化融合与产业互联网': 5,
                       '网络安全与国际治理': 6,
                       'ICT': 7
                       }
    """
     data: ['无线网络', '信息网络', '大数据与人工智能', '先进计算', '数字经济与法律监管', '两化融合与产业互联网', '网络安全与国际治理', 'ICT']
    """
    nodes_list = []
    temp_dict = {}
    iter_cnt = 0
    for item in res_list:
        temp_dict["name"] = item[0]
        temp_dict["value"] = 1
        temp_dict["category"] = categories_dict[str(item[6])]
        nodes_list.append(temp_dict)
        temp_dict = {}
        iter_cnt += 1
    # print(nodes_list)
    # 生成links
    links_list = []
    temp_dict = {}
    iter_cnt_out = 0
    for item_out in res_list:
        key_words_list_out = item_out[8].strip().split("、")
        iter_cnt_in = iter_cnt_out + 1
        for item_in in res_list[iter_cnt_in:]:
            key_words_list_in = item_in[8].strip().split("、")
            # 如果关键词存在重合，则存在连边
            if len(list(set(key_words_list_out) & set(key_words_list_in))) != 0:
                # print(key_words_list_out)
                # print(key_words_list_in)
                # print()
                temp_dict["source"] = iter_cnt_out
                temp_dict["target"] = iter_cnt_in
            else:
                # print("不存在关键词重合")
                pass
            links_list.append(temp_dict)
            iter_cnt_in += 1
        temp_dict = {}
        iter_cnt_out += 1
    # print(len(links_list))
    hjson['type'] = type
    hjson['categories'] = categories_list
    hjson['nodes'] = nodes_list
    hjson['links'] = links_list
    # print(hjson)

    # 生成json
    with open("..\\000LocalData\\caict_k\\research_subject_intergrate.json", "w") as f:
        json.dump(hjson, f)
        print("write json file complete!")

    # 绘制网络拓扑图
    # print("绘制网络拓扑图")
    # opts_title = "院软课题知识网络拓扑图绘制[2010-2019]"
    # graph_topology(hjson_web, opts_title).render("..\\000LocalData\\caict_k\\subject_graph.html")


def graph_topology(res_json, opts_title_name)->Graph:
    """
    绘制网络拓扑图
    :param res_json:
    :param opts_title_name:
    :return:
    """
    c = (
        Graph(init_opts=opts.InitOpts(width="1920px", height="960px", page_title=opts_title_name, theme=ThemeType.SHINE))
        .add(
            "",
            res_json["nodes"],
            res_json["links"],
            res_json["categories"],
            # layout="circular",
            is_rotate_label=True,
            gravity=0.2,
            repulsion=100000,
            linestyle_opts=opts.LineStyleOpts(width=0.1),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title=opts_title_name),
        )
    )
    return c


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    res_auto_file = "..\\000LocalData\\caict_k\\research_subject_clean.csv"
    res_manual_file = "..\\000LocalData\\caict_k\\院软科学研究课题与专报（2010-2019）-合稿.xlsx"
    des_file = "..\\000LocalData\\caict_k\\research_subject_intergrate.csv"
    data_intergrate_draw(res_auto_file, res_manual_file, des_file)
    # print("生成绘制院团课题网络拓扑图所需的json数据")
    # generate_json(des_file)
    time_end = time.time()  # 记录程序结束时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")