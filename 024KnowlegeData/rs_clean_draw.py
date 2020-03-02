# coding:utf-8
"""
create on Feb 14, 2020 By Wenyan YU
Function:

对院知识工厂中爬取的软科学研究课题数据进行数据清洗

院知识工厂软科学研究课题，共有2461个课题，剔除页面信息不规范、链接错误等内容，共爬取2251条记录（8个数据项）
记录的格式为：rs_name、rs_number、rs_time、responsible_person、responsible_dept、rs_classification、rs_content、page_url

先需对其进行数据清洗
输入:research_subject_raw.csv
输出:research_subject_clean.csv


"""

import time
import csv
import re
from jieba.analyse import *
from pyecharts import options as opts
from pyecharts.charts import WordCloud, ThemeRiver, Bar, Line
from pyecharts.globals import SymbolType
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode


# caict_dept = ["泰尔数据研究中心", "信息通信安全研究所", "西部分院(重庆)", "电信与信息服务咨询中心",
#               "政策与经济研究所", "技术与标准研究所", "产业与规划研究所", "信息化与工业化融合研究所", "安全研究所",
#               "云计算与大数据研究所", "泰尔系统实验室", "泰尔终端实验室", "泰尔认证研究所",
#               "电信设备认证中心", "电信用户申诉受理中心", "电信与信息服务咨询中心", "通信工程定额质监中心",
#               "数据研究中心", "信息管理中心", "南方分院", "西部分院", "华东分院", "广州智慧城市研究所",
#               "工业互联网和物联网研究所", "无线电研究中心",
#               "人力资源部", "国际合作部",
#               "知识产权中心(原)", "规划设计研究所(原)",
#               "通信信息研究所(原)", "通信标准研究所", "泰尔实验室(原)", "泰尔管理研究所(原)", "泰尔规划研究所",
#               "电信研究院", "泰尔认证中心", "科技市场部(原)", "质监中心", "咨询中心", "NONE"]


caict_dept = ["泰尔数据研究中心", "信息通信安全研究所", "西部分院(重庆)", "电信与信息服务咨询中心",
              "政策与经济研究所", "技术与标准研究所", "产业与规划研究所", "信息化与工业化融合研究所", "安全研究所",
              "云计算与大数据研究所", "泰尔系统实验室", "泰尔终端实验室", "泰尔认证研究所",
              "电信设备认证中心", "电信用户申诉受理中心", "通信工程定额质监中心",
              "数据研究中心", "信息管理中心",
              "工业互联网和物联网研究所", "无线电研究中心",
              "人力资源部", "国际合作部",
              "知识产权中心(原)", "规划设计研究所(原)",
              "通信信息研究所(原)", "通信标准研究所", "泰尔实验室(原)", "泰尔管理研究所(原)", "泰尔规划研究所",
              "电信研究院", "泰尔认证中心", "科技市场部(原)", "质监中心", "咨询中心", "NONE"]

subject_type = ['A1课题', '重点滚动课题',  'A2课题', 'B类课题', '部软科学', '院软科学', '团队课题', '支撑类']


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
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def list2dict_count(res_list):
    """
    根据传入的list，统计各元素的频次，并返回频次字典
    :param res_list:
    :return des_dict:
    """
    des_dict = {}
    for item in set(res_list):
        des_dict[item] = 0
    for item in res_list:
        des_dict[item] += 1
    return des_dict


def dict2list_rank(res_dict):
    """
    根据传入的dict，将其转换为list，并按降序排名
    :param res_dict:
    :return des_list:
    """
    des_list = []
    temp_list = []
    for key in res_dict.keys():
        temp_list.append(key)
        temp_list.append(res_dict[key])
        des_list.append(temp_list)
        temp_list = []
    des_list.sort(reverse=True, key=lambda elem: int(elem[1]))
    return des_list


def list_rank2word_cloud(res_list_rank, opts_title_name)->WordCloud:
    """
    根据传入的list rank数据，利用pyecharts绘制词云图
    :param res_list_rank:
    :param opts_title_name:
    :return:
    """
    words_data = []
    for item in res_list_rank:
        words_data.append(item)
    print(words_data[0:100])
    words_data = words_data[1:100]
    save_path = "..\\000LocalData\\caict_k\\title_keywords_cloud.csv"
    write_to_csv(words_data, save_path)
    c = (
         WordCloud(init_opts=opts.InitOpts(width="1920px", height="1080px", page_title=opts_title_name, theme=ThemeType.SHINE))
         .add("", words_data, word_size_range=[10, 200], shape=SymbolType.ARROW)
         .set_global_opts(title_opts=opts.TitleOpts(title=opts_title_name))
         )
    return c


def list_2theme_river(res_list, opts_title_name)->ThemeRiver:
    """
    根据传入的list数据，利用pyecharts绘制主题河流图
    :param res_list:
    :param opts_title_name:
    :return:
    """
    c = (
         ThemeRiver(init_opts=opts.InitOpts(width="1920px", height="1080px", page_title=opts_title_name, theme=ThemeType.SHINE))
         .add(['A1课题', '重点滚动课题',  'A2课题', 'B类课题', '部软科学', '院软科学', '团队课题', '支撑类'],
              res_list,
              label_opts=opts.LabelOpts(is_show=False),
              singleaxis_opts=opts.SingleAxisOpts(type_="time", pos_bottom="10%"))
         .set_global_opts(title_opts=opts.TitleOpts(title=opts_title_name))
         )
    return c


def list_2bar(res_list, opts_title_name)->Bar:
    """
    根据传入的list数据，利用pyecharts绘制Bar图
    :param res_list:
    :param opts_title_name:
    :return:
    """
    c = (
         Bar(init_opts=opts.InitOpts(width="1920px", height="1080px", page_title=opts_title_name, theme=ThemeType.SHINE))
         .add_xaxis(res_list[0])
         .add_yaxis("A1课题", res_list[1])
         .add_yaxis("重点滚动课题", res_list[2])
         .add_yaxis("A2课题", res_list[3])
         .add_yaxis("B类课题", res_list[4])
         .add_yaxis("部软科学", res_list[5])
         .add_yaxis("院软科学", res_list[6])
         .add_yaxis("团队课题", res_list[7])
         .add_yaxis("支撑类", res_list[8])
         .set_series_opts(itemstyle_opts={
             "normal": {
                 "barBorderRadius": [30, 30, 30, 30]
             }})
         .set_global_opts(title_opts=opts.TitleOpts(title=opts_title_name))
         )
    return c


def list_2line_areastyle(res_list, opts_title_name)->Line:
    """
    根据传入的list数据，利用pyecharts绘制Line面积图
    :param res_list:
    :param opts_title_name:
    :return:
    """
    c = (
         Line(init_opts=opts.InitOpts(width="1920px", height="1080px", page_title=opts_title_name, theme=ThemeType.ROMA))
         .add_xaxis(res_list[0])
         .add_yaxis("A1课题", res_list[1], is_smooth=True)
         .add_yaxis("重点滚动课题", res_list[2], is_smooth=True)
         .add_yaxis("A2课题", res_list[3], is_smooth=True)
         .add_yaxis("B类课题", res_list[4], is_smooth=True)
         .add_yaxis("部软科学", res_list[5], is_smooth=True)
         .add_yaxis("院软科学", res_list[6], is_smooth=True)
         .add_yaxis("团队课题", res_list[7], is_smooth=True)
         .add_yaxis("支撑类", res_list[8], is_smooth=True)
         .set_series_opts(
             areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
             label_opts=opts.LabelOpts(is_show=False),
            )
         .set_global_opts(title_opts=opts.TitleOpts(title=opts_title_name),
                          xaxis_opts=opts.AxisOpts(
                              axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                              is_scale=False,
                              boundary_gap=False,
                          ),
                          )
         )
    return c


def data_clean(res_file_path, des_file_path):
    """
    根据传入的数据源路径和目标源路径，进行数据的清洗和存储
    :param res_file_path:
    :param des_file_path:
    :return:
    """
    res_file_read = open(res_file_path, 'r', encoding='utf-8')
    des_list = []
    line_cnt = 0
    subject_number_list = []  # 存储课题编号
    year_list = []  # 存储年份
    responsible_person_list = []  # 存储负责人
    dept_type_list = []  # 存储部门类型list
    subject_type_list = []  # 存储课题类型list
    title_keywords_list = []  # 存储课题标题关键词提取结果
    content_keywords_list = []  # 存储课题内容关键词提取结果
    subject_time_type_themeriver = []  # 存储主题河流图数据，时间（2005-2019）、计数、类型
    # 初始化主题河流图数据
    temp_themeriver_list = []
    for type_item in subject_type:
        for year_time in range(2005, 2020):
            temp_themeriver_list.append(str(year_time)+"/12/01")
            temp_themeriver_list.append(0)
            temp_themeriver_list.append(type_item)
            subject_time_type_themeriver.append(temp_themeriver_list)
            temp_themeriver_list = []
    # print(subject_time_type_themeriver)
    for line in res_file_read.readlines():
        line = line.strip().split('|')
        try:
            # 处理负责人信息开始
            line[3] = line[3].replace(' ', '、', 3)
            # print(line[3].split("、"))
            if line[3] == "None":
                line[3] = "佚名"
            # 处理负责人信息结束

            # 处理责任单位信息开始
            if len(line[4]) == 0:
                line[4] = "None"
            line[4] = line[4].replace("原", "(原)", 10)
            line[4] = line[4].replace("重庆", "(重庆)", 10)
            line_4_str = ""
            iter_cnt = 0
            for item in caict_dept:
                if str(line[4].find(item)) != "-1":
                    line_4_str = line_4_str + item + "、"
                    line[4] = line[4].replace(item, "", 10)
                    iter_cnt += 1
            line_4_str = line_4_str[:-1]
            line[4] = line_4_str
            # print(line[4].split("、"))
            # 处理责任单位信息结束
            # print(line[5])

            # 处理课题内容描述开始
            line_6_str = line[6]
            dr = re.compile(r'<[^>]+>', re.S)  # 去除html标签信息
            line_6_str = dr.sub('', line_6_str)
            # print(line_6_str)
            line[6] = line_6_str
            # 处理课题内容描述结束
            """
            开始JIEBA词，进行主题词提取
            """
            # print(line[0])
            # print(line[6])
            for keyword, weight in extract_tags(line[0], withWeight=True):
                # print('%s %s' % (keyword, weight))
                title_keywords_list.append(keyword)
           #  print("------------------line----------------------")
            for keyword, weight in extract_tags(line[6], withWeight=True):
                # print('%s %s' % (keyword, weight))
                content_keywords_list.append(keyword)
            # print("==================line======================")
            # print("")

            """
            结束JIEBA分词
            """
            """
            获取主题河流图信息开始
            """
            for item in subject_time_type_themeriver:
                if item[0].split("/")[0] == line[2] and item[2] == line[5]:
                    item[1] += 1
            """
            获取主题河流图信息结束
            """
            subject_number_list.append(line[1])
            if len(line[1]) == 0:
                print(line[0], line[5])
            year_list.append(line[2])
            responsible_person_list.extend(line[3].split("、"))
            dept_type_list.extend(line[4].split("、"))
            subject_type_list.append(line[5])

        except Exception as e:
            print("ERROR:", e, " line:", line_cnt)
        line_cnt += 1
        des_list.append(line)
    # print(subject_time_type_themeriver)
    print("=>编号统计:", len(set(subject_number_list)))
    # print(list2dict_count(subject_number_list))
    print("=>年份统计:", len(set(year_list)), list(set(year_list)))
    print(dict2list_rank(list2dict_count(year_list)))
    print("=>人员统计:", len(set(responsible_person_list)))
    # print(dict2list_rank(list2dict_count(responsible_person_list)))
    print("=>负责单位:", len(set(dept_type_list)))
    print(dict2list_rank(list2dict_count(dept_type_list)))
    print("=>课题类型:", len(set(subject_type_list)), list(set(subject_type_list)))
    print(dict2list_rank(list2dict_count(subject_type_list)))
    # 存储清洗之后的数据
    write_to_csv(des_list, des_file_path)
    print("=>TF-IDF算法关键词提取（课题名称）:", len(set(title_keywords_list)))
    # print(dict2list_rank(list2dict_count(title_keywords_list)))
    print("=>TF-IDF算法关键词提取（课题内容）:", len(set(content_keywords_list)))
    # print(dict2list_rank(list2dict_count(content_keywords_list)))
    # for keyword, weight in extract_tags(title_str, withWeight=True):
    #     print('%s %s' % (keyword, weight))
    # print("------------------line----------------------")
    # for keyword, weight in extract_tags(content_str, withWeight=True):
    #     print('%s %s' % (keyword, weight))
    print("=>绘制词云（课题名称关键词）:", len(set(title_keywords_list)))
    opts_title = "院软科学研究课题关键词词云（2005-2019）[课题标题]"
    title_list_rank = dict2list_rank(list2dict_count(title_keywords_list))
    list_rank2word_cloud(title_list_rank[0:], opts_title).render("..\\000LocalData\\caict_k\\title_keywords_cloud.html")

    # print("=>绘制词云（课题负责人）:", len(set(responsible_person_list)))
    # opts_title = "院软科学研究课题关键词词云（2005-2019）[课题负责人]"
    # title_list_rank = dict2list_rank(list2dict_count(responsible_person_list))
    # list_rank2word_cloud(title_list_rank[1:801], opts_title).render("..\\000LocalData\\caict_k\\responsible_person_cloud.html")
    #
    # print("=>绘制词云（负责单位）:", len(set(dept_type_list)))
    # opts_title = "院软科学研究课题关键词词云（2005-2019）[负责单位]"
    # title_list_rank = dict2list_rank(list2dict_count(dept_type_list))
    # list_rank2word_cloud(title_list_rank[0:], opts_title).render("..\\000LocalData\\caict_k\\dept_type_cloud.html")
    #
    # print("=>绘制词云（课题类型）:", len(set(subject_type_list)))
    # opts_title = "院软科学研究课题关键词词云（2005-2019）[课题类型]"
    # title_list_rank = dict2list_rank(list2dict_count(subject_type_list))
    # list_rank2word_cloud(title_list_rank[0:], opts_title).render("..\\000LocalData\\caict_k\\subject_type_cloud.html")

    print("=>绘制主题河流图（时间-统计-类型）:", len(subject_time_type_themeriver))
    opts_title = "院软科学研究课题主题河流图（2005-2019）"
    list_2theme_river(subject_time_type_themeriver, opts_title).render("..\\000LocalData\\caict_k\\subject_theme_river.html")
    print(subject_time_type_themeriver)


    """"
    处理subject_bar_list开始
    """
    subject_bar_list = []
    temp_list = []
    for time_year in range(2005, 2020):
        temp_list.append(str(time_year)+"/12/01")
    subject_bar_list.append(temp_list)

    for type_item in subject_type:
        temp_list = []
        for item in subject_time_type_themeriver:
            if item[2] == type_item:
                temp_list.append(item[1])
        subject_bar_list.append(temp_list)
    print(subject_bar_list)
    """
    处理subject_bar_list结束
    """
    print("=>绘制课题类型柱状图（课题类型）:", len(subject_bar_list))
    opts_title = "院软科学研究课题柱状图（2005-2019）[课题类型]"
    list_2bar(subject_bar_list, opts_title).render("..\\000LocalData\\caict_k\\subject_bar.html")

    print("=>绘制课题类型Line面积图（课题类型）:", len(subject_bar_list))
    opts_title = "院软科学研究课题Line面积图（2005-2019）[课题类型]"
    list_2line_areastyle(subject_bar_list, opts_title).render("..\\000LocalData\\caict_k\\subject_line_areastyle.html")
    save_path = "..\\000LocalData\\caict_k\\subject_line_areastyle.csv"
    write_to_csv(subject_time_type_themeriver, save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    res_file = "..\\000LocalData\\caict_k\\research_subject_raw.csv"
    des_file = "..\\000LocalData\\caict_k\\research_subject_clean.csv"
    data_clean(res_file, des_file)
    time_end = time.time()  # 记录程序结束时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")