# coding:utf-8
"""
create on Jun 4, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

根据过去十年的历史数据，利用回归算法初步预测未来3-5年的数据

"""
import time
import csv
import matplotlib.pyplot as plt
import numpy as np

capacity_file = "../000LocalData/global_traffic_model/gig_cap_countries.csv"


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    # print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='gbk')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    # print("write finish!")


def poly_fitting_predict(x, y):
    """
    利用多项式拟合进行预测
    :param x:
    :param y:
    :return:
    """
    for i in range(0, len(x)):
        x[i] = int(x[i])
    for i in range(0, len(y)):
        y[i] = float(y[i])/1000000

    print(x), print(y)
    res = np.polyfit(x, y, 2)  # 使用多项式进行拟合
    p = np.poly1d(res)  # 获取多项式表达式
    print("多项式:", p)
    x1 = x
    res_y = p(x1)
    x2 = []  # 存储时间
    for i in range(2021, 2025):
        x2.append(int(i))
    predict_y = p(x2)
    print("x2:", x2)
    print("predict_y:", predict_y)

    plt.figure(figsize=(12, 8))
    # 设置刻度字体大小
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plot1 = plt.plot(x, y, '*', label='original values', color='black')
    plot2 = plt.plot(x1, res_y, '--', label='polyfit values', color='black')
    plot3 = plt.plot(x2, predict_y, '-', label='predict values', color='black')
    # 设置坐标标签字体大小
    plt.ylabel('Bandwidth(Tbps)', fontsize=24)
    plt.xlabel('Time(Year)', fontsize=24)
    # 设置图例字体大小
    plt.legend(loc=4, fontsize=20)
    plt.title('Country Bandwidth Predict', fontsize=24)
    plt.savefig('Poply_fitting.png')
    plt.show()
    return x2, predict_y


def capacity_predict():
    """
    对数据进行预测
    :return:
    """
    file_read = open(capacity_file, 'r', encoding="utf-8")
    country_capacity_dict = {}  # 存储各个国家的国际互联带宽
    for line in file_read.readlines():
        if line.find("国家") != -1:
            line = line.strip().split(",")
            country_capacity_dict["时间"] = line[1:]
            continue
        line = line.strip().split(",")
        # print(line)
        country_capacity_dict[line[0]] = line[1:]
    # print(country_capacity_dict["时间"])
    # print(country_capacity_dict["China"])
    print(poly_fitting_predict(country_capacity_dict["时间"], country_capacity_dict["China"]))


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    capacity_predict()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
