# coding:utf-8
"""
create on Oct 15, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

根据海缆中间数据集，处理成AS Core Map图的数据输入，点&边，进行绘图
数据输入为子飞输出的Excel文件“cable_info.xlsx”


第一阶段，在原始阶段基础上，把C国所有在建海缆全部剔除，重新绘制极图

"bay-to-bay-express-btobe-cable-system",
"hong-kong-americas-hka",
"pacific-light-cable-network-plcn"


"""

import openpyxl
import time
import numpy as np
import matplotlib.pyplot as plt
import csv


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


def gain_format_data():
    """
    根据cable_info.xlsx
    :return:
    """

    """
    获取年份和容量对应的数据
    """
    capacity_file = "../000LocalData/CableMap/capacity.csv"
    capacity_dict = {}  # 存储年份与容量的对应数据
    capacity_file_in = open(capacity_file, 'r', encoding='utf-8')
    for line in capacity_file_in.readlines():
        line = line.strip().split(",")
        # print(line)
        capacity_dict[line[0]] = line[1]
    print(capacity_dict)
    cable_file = "../000LocalData/CableMap/cable_info.xlsx"
    print(cable_file)
    work_book = openpyxl.load_workbook(cable_file)
    cable_info_sheet = work_book.worksheets[0]
    cable_rel_sheet = work_book.worksheets[1]

    cable_1 = []  # 存储1阶段要断的缆
    landing_cn_list = []  # 存储中国所有的登陆点数据
    """"
    统计登陆点信息
    """
    landing_point_dict = dict()  # 存储登陆点，及其综合参数值（根据登陆海缆数量及海缆开通年份综合分析结果）
    rows_cnt = 1  # 行计数，初始化为1
    max_arg_value = 0  # 存储最大的映射容量值
    min_arg_value = 10000.0  # 存储最小的映射容量值
    for row in cable_info_sheet.rows:
        if rows_cnt == 1:
            rows_cnt += 1
            continue
        row_list = []
        for cell in row:
            # print(cell.value, end="")
            row_list.append(cell.value)

        if row_list[5] == "China":
            landing_cn_list.append(row_list[4])

        # print(row_list)
        # if row_list[2] != "n.a.":
        #     if row_list[2] >= 2020 and row_list[5] == "China":
        #         # 满足第一阶段条件，则不统计
        #         print(row_list[0], row_list[2], row_list[4],  row_list[3])
        #         cable_1.append(row_list[0])
        #         continue
        #
        #     if row_list[2] >= 2020 and row_list[5] == "China(HK)":
        #         # 满足第一阶段条件，则不统计
        #         print(row_list[0], row_list[2], row_list[4],  row_list[3])
        #         cable_1.append(row_list[0])
        #         continue
        cable_1 = ["bay-to-bay-express-btobe-cable-system",
                   "hong-kong-americas-hka",
                   "pacific-light-cable-network-plcn"]
        arg_value = float(capacity_dict[str(row_list[2])])
        if row_list[0] in cable_1:
            if row_list[5] == "China" or row_list[5] == "China(HK)":
                arg_value = 0.0
            if row_list[5] == "United States":
                arg_value = 0.5 * arg_value
        angle = 0.0
        lon = float(row_list[8])  # 存储当前登陆点的经度信息，用于计算极坐标图的角度
        if lon >= 0.0:
            angle = lon
        else:
            angle = lon + 360.0
        angle = (angle/360.0) * 2 * np.pi
        country = row_list[5]  # 存储当前登陆点的国别

        if row_list[4] not in landing_point_dict.keys():
            landing_point_dict[row_list[4]] = [arg_value, angle, country]
            if landing_point_dict[row_list[4]][0] > max_arg_value:
                max_arg_value = landing_point_dict[row_list[4]][0]
            if landing_point_dict[row_list[4]][0] < min_arg_value:
                min_arg_value = landing_point_dict[row_list[4]][0]
        else:
            landing_point_dict[row_list[4]][0] += arg_value
            if landing_point_dict[row_list[4]][0] > max_arg_value:
                max_arg_value = landing_point_dict[row_list[4]][0]
            if landing_point_dict[row_list[4]][0] < min_arg_value:
                min_arg_value = landing_point_dict[row_list[4]][0]

    print("第一阶段：", list(set(cable_1)))
    print("海缆登陆站数量统计:%s" % (len(landing_point_dict.keys())))
    print("登陆点中容量映射值最大值为:%s" % max_arg_value)
    print("登陆点中容量映射值最小值为:%s" % min_arg_value)
    # print(landing_point_dict)
    print("根据容量映射最大值，按照 radius = 1 - log((ARGS(Point)+1) / (MAX_ARGS + 1))，计算极径")
    for key in landing_point_dict.keys():
        landing_point_dict[key][0] = 1 - np.log((landing_point_dict[key][0] + 1)/(max_arg_value + 1))

    # print(landing_point_dict)
    """
    统计登陆点海缆互联信息
    """
    print(landing_cn_list)
    cable_rel_list = list()  # 统计登陆点之间海缆互联关系
    rows_cnt = 1  # 行计数，初始化为1
    for row in cable_rel_sheet.rows:
        if rows_cnt == 1:
            rows_cnt += 1
            continue
        row_list = []
        for cell in row:
            row_list.append(cell.value)
        if row_list[0] in cable_1:
            # if row_list[1] in landing_cn_list and row_list[2] not in landing_cn_list:
            #     print(row_list)
            #     continue
            # if row_list[2] in landing_cn_list and row_list[1] not in landing_cn_list:
            #     print(row_list)
            #     continue
            if row_list[1] in landing_cn_list or row_list[2] in landing_cn_list:
                print(row_list)
                continue

        cable_rel_list.append([row_list[1], row_list[2]])
    print("登陆点之间的互联关系数量:%s" % (len(cable_rel_list)))
    # print(cable_rel_list)
    return landing_point_dict, cable_rel_list


def draw_polar_map():
    """
    根据格式化信息，绘制海缆的极图
    :return:
    """
    landing_point, rel_info = gain_format_data()
    # print(landing_point)  # key: 极径,角度，国别

    # #############关键参数生成################
    max_radius = 0.0
    min_radius = 10000.0
    min_key = ""
    angle_list = []
    radius_list = []
    coordinate_dic =dict()
    item_cnt = 0
    for key in landing_point.keys():
        if landing_point[key][0] > max_radius:
            max_radius = landing_point[key][0]
        if landing_point[key][0] < min_radius:
            min_radius = landing_point[key][0]
            min_key = key
        angle_list.append(landing_point[key][1])
        radius_list.append(landing_point[key][0])
        coordinate_dic[key] = [landing_point[key][1], landing_point[key][0]]  # 点到极坐标的映射
        item_cnt += 1
    # print(coordinate_dic)
    # 准备绘图
    plt.figure(figsize=(9, 5))
    ax = plt.subplot(111, projection='polar')
    ax.set_ylim(0.0, max_radius + 2)  # 设置极坐标半径radius的最大刻度
    # ####绘图参数生成##########
    area_list = []
    lw_list = []
    c_color_list = []
    z_order_list = []
    max_key = []  # 记录全球TOP节点
    cn_key = []  # 记录中国TOP节点
    cn_all_as = []  # 存储所有中国的登陆点
    us_all_as = []  # 存储所有美国的登陆点
    hk_all_as = []  # 存储所有香港的登陆点
    global_all_as = []  # 所有世界所有的登陆点

    point_cnt = 0
    cn_index_list = []  # 存储在打点列表中cn的下标

    for key in landing_point.keys():
        if landing_point[key][0] < max_radius * 0.2:
            area_list.append(12)
            lw_list.append(0.1)
            c_color_list.append([float(200 / 256), float(100 / 256), float(100 / 256)])
            z_order_list.append(2)
            max_key.append(key)  # 记录最牛逼的几个点的坐标
            if landing_point[key][2] == "China":
                cn_key.append(key)
        elif landing_point[key][0] < max_radius * 0.4:
            area_list.append(8)
            lw_list.append(0.1)
            c_color_list.append([float(224.0 / 256), float(200.0 / 256), float(41.0 / 256)])
            z_order_list.append(2)
            if landing_point[key][2] == "China":
                cn_key.append(key)
        elif landing_point[key][0] < max_radius * 0.6:
            area_list.append(3)
            lw_list.append(0.1)
            c_color_list.append([float(100 / 256), float(100 / 256), float(200 / 256)])
            z_order_list.append(2)
            if landing_point[key][2] == "China":
                cn_key.append(key)
        else:
            area_list.append(2)
            lw_list.append(0.1)
            c_color_list.append([float(256 / 256), float(256 / 256), float(256 / 256)])
            z_order_list.append(1)
        # 如果该点为中国，则改变其填充颜色,改变其Marker，并存储
        if landing_point[key][2] == "China":
            cn_all_as.append([key, landing_point[key][0], landing_point[key][1], landing_point[key][2]])
            del c_color_list[-1]
            c_color_list.append([float(100.0 / 256), float(200.0 / 256), float(100.0 / 256)])
            # del area_list[-1]
            # area_list.append(12)
            cn_index_list.append(point_cnt)

        if landing_point[key][2] == "United States":
            us_all_as.append([key, landing_point[key][0], landing_point[key][1], landing_point[key][2]])
            del c_color_list[-1]
            c_color_list.append([float(255.0 / 256), float(0.0 / 256), float(255.0 / 256)])

        if landing_point[key][2] == "China(HK)":
            hk_all_as.append([key, landing_point[key][0], landing_point[key][1], landing_point[key][2]])
            del c_color_list[-1]
            c_color_list.append([float(29.0 / 256), float(113.0 / 256), float(244 / 256)])

        # 存储实世界所有AS号
        global_all_as.append([key, landing_point[key][0], landing_point[key][1], landing_point[key][2]])
        point_cnt += 1
    area = area_list
    print("CN All Landing Point Count:", len(cn_all_as))
    print("Global All Landing Point Count:", len(global_all_as))
    # ###########################画线################################
    edges_cnt = 0
    for item in rel_info:
        p1 = coordinate_dic.get(item[0])
        p2 = coordinate_dic.get(item[1])
        # print(p1, p2)

        z_order_value = 1
        line_width = 0.05
        alpha_value = 1
        if p1 is None or p2 is None:
            continue
        if p1[1] < max_radius * 0.2 and p2[1] < max_radius * 0.2:
            line_width = 0.4
            line_color = [float(110 / 256), float(32 / 256), float(142 / 256)]
            alpha_value = 1
            z_order_value = 6
        elif p1[1] < max_radius * 0.4 and p2[1] < max_radius * 0.4:
            line_width = 0.2
            line_color = [float(167 / 256), float(114 / 256), float(244 / 256)]
            alpha_value = 0.7
            z_order_value = 4
        elif p1[1] < max_radius * 0.6 and p2[1] < max_radius * 0.6:
            line_width = 0.1
            line_color = [float(145 / 256), float(102 / 256), float(210 / 256)]
            alpha_value = 0.5
            z_order_value = 2
        else:
            line_width = 0.02
            line_color = [float(62 / 256), float(132 / 256), float(132 / 256)]
            z_order_value = 1
        # print("computing:", p1, p2)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]],
                linewidth=line_width,
                alpha=alpha_value,
                color=line_color,
                zorder=z_order_value, )
        edges_cnt += 1
    # ######################## 打点######################################
    ax.scatter(angle_list, radius_list,
               c=c_color_list,
               edgecolors=[0, 0, 0],
               marker="s",
               lw=lw_list,
               s=area,
               cmap='hsv',
               alpha=0.9,
               zorder=7)

    angle_list_cn = []
    radius_list_cn = []
    c_color_list_cn = []
    lw_list_cn = []
    area_cn = []
    for index in cn_index_list:
        angle_list_cn.append(angle_list[index])
        radius_list_cn.append(radius_list[index])
        c_color_list_cn.append(c_color_list[index])
        lw_list_cn.append(lw_list[index])
        area_cn.append(area[index])

    ax.scatter(angle_list_cn, radius_list_cn,
               c=c_color_list_cn,
               edgecolors=[0, 0, 0],
               marker="s",
               lw=lw_list_cn,
               s=area_cn,
               cmap='hsv',
               alpha=0.9,
               zorder=7)
    # ########################绘制外围辅助性图标##########################
    # 画个内圆
    circle_theta = np.arange(0, 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.1] * len(circle_theta)
    # print(circle_theta)
    # print(circle_radius)
    ax.plot(circle_theta, circle_radius, color=[1, 1, 1], linewidth=0.2)
    # 画个外圆1
    circle_theta = np.arange(0, 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.3] * len(circle_theta)
    # print(circle_theta)
    # print(circle_radius)
    ax.plot(circle_theta, circle_radius, color=[1, 1, 1], linewidth=0.2)
    # 画外圆2
    circle_theta = np.arange(0, 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.5] * len(circle_theta)
    # print(circle_theta)
    # print(circle_radius)
    ax.plot(circle_theta, circle_radius, color=[1, 1, 1], linewidth=0.2)
    # 画外圆3
    circle_theta = np.arange(0, 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.6] * len(circle_theta)
    # print(circle_theta)
    # print(circle_radius)
    ax.plot(circle_theta, circle_radius, color=[1, 1, 1], linewidth=0.2)

    # 填充欧洲（Europe）颜色为#bd87bf，从西经14度至东经49度，即346-49
    circle_theta = np.arange(float(346.0 / 360) * 2 * np.pi, float(360 / 360) * 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.2] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#bd87bf", linewidth=3)

    circle_theta = np.arange(float(0.0 / 360) * 2 * np.pi, float(49 / 360) * 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.2] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#bd87bf", linewidth=3)

    # 填充亚洲（Asia）颜色为#00a895,从东经49度至西经175，即49-185
    circle_theta = np.arange(float(49.0 / 360) * 2 * np.pi, float(185 / 360) * 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.2] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#00a895", linewidth=3)

    # 填充北美洲（North American）颜色为#669ed8，从西经170度至西经20度，即190-340
    circle_theta = np.arange(float(190.0 / 360) * 2 * np.pi, float(340 / 360) * 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.2] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#669ed8", linewidth=3)

    # 填充非洲（Africa）颜色为#b680c3，从西经14度至东经52度，即346-52
    circle_theta = np.arange(float(346.0 / 360) * 2 * np.pi, float(360 / 360) * 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.4] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#f3c828", linewidth=3)

    circle_theta = np.arange(float(0.0 / 360) * 2 * np.pi, float(52 / 360) * 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.4] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#f3c828", linewidth=3)

    # 填充大洋洲(Oceana)，颜色为#fec273，从东经110度至东经180度，即110-180
    circle_theta = np.arange(float(110 / 360) * 2 * np.pi, float(180 / 360) * 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.4] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#fec273", linewidth=3)

    # 填充南美洲（South American），颜色为#f2c41d，从西经80度至西经40度，即280-320
    circle_theta = np.arange(float(280 / 360) * 2 * np.pi, float(320 / 360) * 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.4] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#f2c41d", linewidth=3)

    # 绘制圆心
    ax.scatter(0.0, 0.0, c="#ffffff", marker='+', lw=0.2, s=6)

    # 绘制经度刻度
    # circle_radius = np.arange(max_radius+0.5, max_radius+0.9, 0.01)
    # circle_theta = [0.0] * len(circle_radius)
    # ax.plot(circle_theta, circle_radius, color=[0, 0, 0], linewidth=0.8)
    # 每隔10度画一个
    for tap_zone in range(0, 36, 1):
        time_zone_angle = tap_zone * 10
        circle_radius = np.arange(max_radius + 0.55, max_radius + 0.8, 0.01)
        circle_theta = [float(time_zone_angle / 360) * 2 * np.pi] * len(circle_radius)
        ax.plot(circle_theta, circle_radius, color=[1, 1, 1], linewidth=0.3)
    # 每隔90度画一个
    for tap_zone in range(0, 4, 1):
        time_zone_angle = tap_zone * 90
        circle_radius = np.arange(max_radius + 0.55, max_radius + 0.9, 0.01)
        circle_theta = [float(time_zone_angle / 360) * 2 * np.pi] * len(circle_radius)
        ax.plot(circle_theta, circle_radius, color=[1, 1, 1], linewidth=1)

        # 添加关键城市和地区的文本信息
        # 一般字体统一用一个字典控制
        font = {'family': 'sans-serif',
                'style': 'italic',
                'weight': 'normal',
                'color': 'white',
                'size': 4
                }
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        text_theta = 0.0
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "伦敦, 英国", fontdict=font, ha='left', va='center', rotation=0)

        text_theta = float(5.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "巴黎, 法国", fontdict=font, ha='left', va='bottom', rotation=5)

        text_theta = float(9.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "法兰克福, 德国", fontdict=font, ha='left', va='bottom', rotation=9)

        text_theta = float(15.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "柏林, 德国", fontdict=font, ha='left', va='bottom', rotation=15)

        text_theta = float(27.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "赫尔辛基, 芬兰", fontdict=font, ha='left', va='bottom', rotation=27)

        text_theta = float(39.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "莫斯科, 俄罗斯", fontdict=font, ha='left', va='bottom', rotation=39)

        text_theta = float(75.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "孟买, 印度", fontdict=font, ha='left', va='bottom', rotation=75)

        text_theta = float(78.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "德里, 印度", fontdict=font, ha='left', va='bottom', rotation=78)

        text_theta = float(100.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "曼谷, 泰国", fontdict=font, ha='right', va='bottom', rotation=100)

        text_theta = float(102.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "新加坡, 新加坡", fontdict=font, ha='right', va='bottom', rotation=102)

        text_theta = float(116.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "北京, 中国", fontdict=font, ha='right', va='bottom', rotation=116)

        text_theta = float(121.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "台北, 中国", fontdict=font, ha='right', va='bottom', rotation=121)

        text_theta = float(139.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "东京, 日本", fontdict=font, ha='right', va='bottom', rotation=139)

        text_theta = float(151.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "悉尼, 澳大利亚", fontdict=font, ha='right', va='bottom', rotation=151)

        text_theta = float(201 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "火奴鲁鲁, 美国", fontdict=font, ha='right', va='top', rotation=201)

        text_theta = float(238.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "圣何塞, 美国", fontdict=font, ha='right', va='top', rotation=238)

        text_theta = float(242.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "圣迭戈, 美国", fontdict=font, ha='right', va='top', rotation=242)

        text_theta = float(248.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "菲尼克斯, 美国", fontdict=font, ha='right', va='top', rotation=248)

        text_theta = float(255.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "丹佛, 美国", fontdict=font, ha='right', va='top', rotation=255)

        text_theta = float(263.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "休斯顿, 美国", fontdict=font, ha='right', va='top', rotation=263)

        text_theta = float(272.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "芝加哥, 美国", fontdict=font, ha='center', va='top', rotation=272)

        text_theta = float(281.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "多伦多, 加拿大", fontdict=font, ha='left', va='top', rotation=281)

        text_theta = float(284.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "华盛顿, 美国", fontdict=font, ha='left', va='top', rotation=284)

        text_theta = float(286.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "渥太华, 加拿大", fontdict=font, ha='left', va='top', rotation=286)

        text_theta = float(289.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "波士顿, 美国", fontdict=font, ha='left', va='top', rotation=289)

        text_theta = float(302.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "布宜诺斯艾利斯, 阿根廷", fontdict=font, ha='left', va='top', rotation=302)

        text_theta = float(316.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "里约热内卢, 巴西", fontdict=font, ha='left', va='top', rotation=316)

        text_theta = float(351.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "阿尔吉斯, 葡萄牙", fontdict=font, ha='left', va='top', rotation=351)

        text_theta = float(354.0 / 360) * 2 * np.pi
        text_radius = max_radius + 1
        ax.text(text_theta, text_radius, "都柏林, 爱尔兰", fontdict=font, ha='left', va='top', rotation=354)

    # 添加TOP AS的文本信息
    # 一般字体统一用一个字典控制
    font = {'family': 'sans-serif',
            'style': 'italic',
            'weight': 'normal',
            'color': 'white',
            'size': 3
            }
    """
    全球TOP点
    """
    save_path = "../000LocalData/CableMap/TopLandingPoint20Global_new_1.csv"
    print("\nGlobal LandingPoint Rank(TOP20):")
    # 给全球TOP5的AS点做标记
    global_all_as.sort(reverse=False, key=lambda elem: elem[1])
    flag_cnt = 1
    for item_as in global_all_as[0:20]:
        print(item_as, coordinate_dic[item_as[0]])
        if flag_cnt <= 5:
            point_angle = coordinate_dic[item_as[0]][0]
            point_radius = coordinate_dic[item_as[0]][1]
            ax.text(point_angle, point_radius, str(flag_cnt), fontdict=font, ha='center', va='center', zorder=7)
        flag_cnt += 1
    write_to_csv(global_all_as[0:20], save_path)
    """
    中国TOP点
    """
    font = {'family': 'sans-serif',
            'style': 'italic',
            'weight': 'normal',
            'color': 'black',
            'size': 2
            }
    save_path = "../000LocalData/CableMap/TopLandingPoint20China_new_1.csv"
    print("\nChina LandingPoint Rank(TOP20):")
    # 给全国TOP5的AS点做标记
    cn_all_as.sort(reverse=False, key=lambda elem: elem[1])
    flag_cnt = 1
    for item_as in cn_all_as[0:20]:
        print(item_as, coordinate_dic[item_as[0]])
        if flag_cnt <= 5:
            point_angle = coordinate_dic[item_as[0]][0]
            point_radius = coordinate_dic[item_as[0]][1]
            ax.text(point_angle, point_radius, str(flag_cnt), fontdict=font, ha='center', va='center', zorder=7)
        flag_cnt += 1
    write_to_csv(cn_all_as[0:20], save_path)

    """
    美国TOP点
    """
    font = {'family': 'sans-serif',
            'style': 'italic',
            'weight': 'normal',
            'color': 'black',
            'size': 2
            }
    save_path = "../000LocalData/CableMap/TopLandingPoint20US_new_1.csv"
    print("\nUS LandingPoint Rank(TOP20):")
    # 给US TOP5的AS点做标记
    us_all_as.sort(reverse=False, key=lambda elem: elem[1])
    flag_cnt = 1
    for item_as in us_all_as[0:20]:
        print(item_as, coordinate_dic[item_as[0]])
        if flag_cnt <= 5:
            point_angle = coordinate_dic[item_as[0]][0]
            point_radius = coordinate_dic[item_as[0]][1]
            ax.text(point_angle, point_radius, str(flag_cnt), fontdict=font, ha='center', va='center', zorder=7)
        flag_cnt += 1
    write_to_csv(us_all_as[0:20], save_path)

    """
    香港TOP点
    """
    font = {'family': 'sans-serif',
            'style': 'italic',
            'weight': 'normal',
            'color': 'black',
            'size': 2
            }
    save_path = "../000LocalData/CableMap/TopLandingPoint20HK_new_1.csv"
    print("\nHK LandingPoint Rank(TOP20):")
    # 给HK TOP5的AS点做标记
    hk_all_as.sort(reverse=False, key=lambda elem: elem[1])
    flag_cnt = 1
    for item_as in hk_all_as[0:20]:
        print(item_as, coordinate_dic[item_as[0]])
        if flag_cnt <= 2:
            point_angle = coordinate_dic[item_as[0]][0]
            point_radius = coordinate_dic[item_as[0]][1]
            ax.text(point_angle, point_radius, str(flag_cnt), fontdict=font, ha='center', va='center', zorder=7)
        flag_cnt += 1
    write_to_csv(hk_all_as[0:20], save_path)

    print("连通度最高的AS号半径：", landing_point[min_key])

    plt.axis('off')
    save_fig_name = "../000LocalData/CableMap/as_core_map_scatter_cable_new_1.jpg"
    plt.savefig(save_fig_name, dpi=1080, facecolor='#202d62')
    # plt.savefig(save_fig_name, dpi=1080, transparent=True)  # 设置背景色为透明
    plt.close()
    return [item_cnt, edges_cnt]


if __name__ == "__main__":
    time_start = time.time()  # 记录程序启动的时间
    draw_polar_map()
    time_end = time.time()  # 记录程序结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")