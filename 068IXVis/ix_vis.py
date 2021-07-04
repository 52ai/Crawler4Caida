# coding:utf-8
"""
create on July 2, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

分两部走：
一、通过ix的接入网络数量以及地理位置信息，可以画极图的点图
二、结合IX间的关系，可以绘制极图的点线图
"""

import time
import csv
import numpy as np
import matplotlib.pyplot as plt


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter="|")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def ix_geo_develop():
    """
    处理ix_geo_develop.csv
    id,
    org_id,
    name,
    city,
    country,
    region_continent,
    net_count,
    fac_count,
    ixf_net_count,
    cn_country_name,
    longitude,
    latitude,
    ROWID,
    cname
    :return:
    """
    ix_geo_develop_file = "ix_geo_develop.csv"
    file_read = open(ix_geo_develop_file, 'r', encoding="utf-8")
    ix_geo_develop_done = []  # 存储最终处理的结果
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        ix_id = line[0]
        ix_name = line[2]
        ix_city = line[3]
        ix_country = line[4]
        ix_net_count = line[6]
        ix_longitude = line[10]
        ix_latitude = line[11]
        temp_list = [ix_id, ix_name, ix_city, ix_country, ix_net_count, ix_longitude, ix_latitude]
        # print(temp_list)
        ix_geo_develop_done.append(temp_list)
    save_path = "ix_geo_develop_done.csv"
    write_to_csv(ix_geo_develop_done, save_path)
    return ix_geo_develop_done


def compute_polar_args(ix_info):
    """
    根据传入的ix_info，计算每个ix的参数angle、radius
    angle = longitude of the IX's orgs
    radius = 1 - log((NC(ix) + 1) / (maximum_NC + 1))
    :param ix_info:
    :return new_ix_info:
    """
    new_ix_info = []
    max_nc = 0  # 存储最大网络接入数量
    for item in ix_info:
        if int(item[4]) > max_nc:
            max_nc = int(item[4])
    print("Max Net Cnt:", max_nc)

    for item in ix_info:
        angle = 0.0
        radius = 0.0
        if float(item[5]) >= 0.0:
            angle = float(item[5])
        else:
            angle = float(item[5]) + 360.0
        radius = 1 - np.log((int(item[4]) + 1) / (max_nc + 1))
        item.append(angle)
        item.append(radius)
        new_ix_info.append(item)
        print(item)
    return new_ix_info


def draw_polar_map(ix_info):
    """
    根据传入的ix_info进行绘图
    :param ix_info:
    :return:
    """
    """
    关键参数生成
    """
    max_radius = 0.0
    min_radius = 10000.0
    min_index = 0
    angle_list = []
    radius_list = []
    coordinate_dic = {}
    item_cnt = 0
    for item in ix_info:
        if float(item[-1]) > max_radius:
            max_radius = float(item[-1])
        if float(item[-1]) < min_radius:
            min_radius = float(item[-1])
            min_index = item_cnt
        angle = (float(item[-2]) / 360.0) * 2 * np.pi
        radius = float(item[-1])
        temp_list = [angle, radius]
        angle_list.append(angle)
        radius_list.append(radius)
        coordinate_dic[item[0]] = temp_list
        item_cnt += 1
    # print(coordinate_dic)

    """
    准备绘图
    """
    plt.figure(figsize=(9, 5))
    ax = plt.subplot(111, projection='polar')
    ax.set_ylim(0.0, max_radius + 2)  # 设置极坐标半径radius的最大刻度
    """
    绘制参数生成
    """
    area_list = []
    lw_list = []
    c_color_list = []
    z_order_list = []
    max_index = []
    cn_index = []
    cn_all_ix = []  # 存储所有中国IX
    global_all_ix = []  # 存储全球所有IX
    index_cnt = 0
    for item in radius_list:
        if item < max_radius * 0.2:
            area_list.append(20)
            lw_list.append(0.1)
            c_color_list.append([float(200 / 256), float(100 / 256), float(100 / 256)])
            z_order_list.append(2)
            max_index.append(index_cnt)  # 记录最牛的几个点的坐标
            if ix_info[index_cnt][3] == "CN":
                cn_index.append(index_cnt)
        elif item < max_radius * 0.4:
            area_list.append(8)
            lw_list.append(0.1)
            c_color_list.append([float(224.0/256), float(200.0/256), float(41.0/256)])
            z_order_list.append(2)
            if ix_info[index_cnt][3] == "CN":
                cn_index.append(index_cnt)
        else:
            area_list.append(2)
            lw_list.append(0.1)
            c_color_list.append([float(256/256), float(256/256), float(256/256)])
            z_order_list.append(1)

        # 若该点为中国，则改变其填充颜色，改变其Marker，并存储
        if ix_info[index_cnt][3] == "CN":
            cn_all_ix.append(ix_info[index_cnt])  # 存储中国所有的ix
            del c_color_list[-1]
            c_color_list.append([float(100.0 / 256), float(200.0 / 256), float(100.0 / 256)])
        # 存储全球所有的ix
        global_all_ix.append(ix_info[index_cnt])
        index_cnt += 1
    area = area_list
    print("CN all IX:", len(cn_all_ix))
    cn_all_ix.sort(reverse=True, key=lambda elem: int(elem[4]))
    print("Global all IX:", len(global_all_ix))
    global_all_ix.sort(reverse=True, key=lambda elem: int(elem[4]))
    """
    画线
    """
    pass
    """
    打点
    """
    ax.scatter(angle_list, radius_list, c=c_color_list, edgecolors=[0, 0, 0], marker="s", lw=lw_list, s=area, cmap='hsv', alpha=0.9, zorder=7)
    """
    绘制外围辅助性图标
    """
    # 画个内圆
    circle_theta = np.arange(0, 2*np.pi, 0.01)
    circle_radius = [max_radius + 0.1] * len(circle_theta)
    # print(circle_theta)
    # print(circle_radius)
    ax.plot(circle_theta, circle_radius, color=[1, 1, 1], linewidth=0.2)
    # 画个外圆1
    circle_theta = np.arange(0, 2*np.pi, 0.01)
    circle_radius = [max_radius + 0.3] * len(circle_theta)
    # print(circle_theta)
    # print(circle_radius)
    ax.plot(circle_theta, circle_radius, color=[1, 1, 1], linewidth=0.2)
    # 画外圆2
    circle_theta = np.arange(0, 2*np.pi, 0.01)
    circle_radius = [max_radius + 0.5] * len(circle_theta)
    # print(circle_theta)
    # print(circle_radius)
    ax.plot(circle_theta, circle_radius, color=[1, 1, 1], linewidth=0.2)
    # 画外圆3
    circle_theta = np.arange(0, 2*np.pi, 0.01)
    circle_radius = [max_radius + 0.6] * len(circle_theta)
    # print(circle_theta)
    # print(circle_radius)
    ax.plot(circle_theta, circle_radius, color=[1, 1, 1], linewidth=0.2)

    # 填充欧洲（Europe）颜色为#bd87bf，从西经14度至东经49度，即346-49
    circle_theta = np.arange(float(346.0/360)*2*np.pi, float(360/360)*2*np.pi, 0.01)
    circle_radius = [max_radius + 0.2] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#bd87bf", linewidth=3)

    circle_theta = np.arange(float(0.0/360)*2*np.pi, float(49/360)*2*np.pi, 0.01)
    circle_radius = [max_radius + 0.2] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#bd87bf", linewidth=3)

    # 填充亚洲（Asia）颜色为#00a895,从东经49度至西经175，即49-185
    circle_theta = np.arange(float(49.0/360)*2*np.pi, float(185/360)*2*np.pi, 0.01)
    circle_radius = [max_radius + 0.2] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#00a895", linewidth=3)

    # 填充北美洲（North American）颜色为#669ed8，从西经170度至西经20度，即190-340
    circle_theta = np.arange(float(190.0/360) * 2 * np.pi, float(340/360) * 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.2] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#669ed8", linewidth=3)

    # 填充非洲（Africa）颜色为#b680c3，从西经14度至东经52度，即346-52
    circle_theta = np.arange(float(346.0/360) * 2 * np.pi, float(360/360) * 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.4] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#f3c828", linewidth=3)

    circle_theta = np.arange(float(0.0/360) * 2 * np.pi, float(52/360) * 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.4] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#f3c828", linewidth=3)

    # 填充大洋洲(Oceana)，颜色为#fec273，从东经110度至东经180度，即110-180
    circle_theta = np.arange(float(110/360) * 2 * np.pi, float(180/360) * 2 * np.pi, 0.01)
    circle_radius = [max_radius + 0.4] * len(circle_theta)
    ax.plot(circle_theta, circle_radius, color="#fec273", linewidth=3)

    # 填充南美洲（South American），颜色为#f2c41d，从西经80度至西经40度，即280-320
    circle_theta = np.arange(float(280/360) * 2 * np.pi, float(320/360) * 2 * np.pi, 0.01)
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
        circle_theta = [float(time_zone_angle / 360)*2*np.pi] * len(circle_radius)
        ax.plot(circle_theta, circle_radius, color=[1, 1, 1], linewidth=0.3)
    # 每隔90度画一个
    for tap_zone in range(0, 4, 1):
        time_zone_angle = tap_zone * 90
        circle_radius = np.arange(max_radius + 0.55, max_radius + 0.9, 0.01)
        circle_theta = [float(time_zone_angle / 360)*2*np.pi] * len(circle_radius)
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

    # 添加TOP IX的文本信息
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
    save_path = "topIX20Global.csv"
    print("Global IX Rank(TOP20):")
    # 给全球TOP5的IX点做标记
    flag_cnt = 1
    for item_ix in global_all_ix[0:20]:
        print(flag_cnt, ":", item_ix[1:])
        if flag_cnt <= 5:
            point_angle = coordinate_dic[item_ix[0]][0]
            point_radius = coordinate_dic[item_ix[0]][1]
            ax.text(point_angle, point_radius, str(flag_cnt), fontdict=font, ha='center', va='center', zorder=7)
        flag_cnt += 1
    write_to_csv(global_all_ix[0:20], save_path)
    """
    中国TOP点
    """
    font = {'family': 'sans-serif',
            'style': 'italic',
            'weight': 'normal',
            'color': 'black',
            'size': 2
            }
    save_path = "topIX20CN.csv"
    print("China IX Rank(TOP20):")
    # 给全球TOP5的IX点做标记
    flag_cnt = 1
    for item_ix in cn_all_ix[0:20]:
        print(flag_cnt, ":", item_ix[1:])
        if flag_cnt <= 5:
            point_angle = coordinate_dic[item_ix[0]][0]
            point_radius = coordinate_dic[item_ix[0]][1]
            ax.text(point_angle, point_radius, str(flag_cnt), fontdict=font, ha='center', va='center', zorder=7)
        flag_cnt += 1
    write_to_csv(cn_all_ix[0:20], save_path)

    print("连通度最高的IX半径：", radius_list[min_index], "IX info:", ix_info[min_index])
    plt.axis('off')
    save_fig_name = "ix_scatter.jpg"
    plt.savefig(save_fig_name, dpi=1080, facecolor='#202d62')
    # plt.savefig(save_fig_name, dpi=1080, transparent=True)  # 设置背景色为透明
    plt.close()


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    ix_list = ix_geo_develop()
    new_info = compute_polar_args(ix_list)
    draw_polar_map(new_info)

    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
