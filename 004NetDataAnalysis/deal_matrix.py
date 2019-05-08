# coding:utf-8
"""
create on Jan 6,2019 by Wayne Yu
Fun:按薛雪要求处理对应的数据
输入为基础数据矩阵
输出为时延五张表（联通、电信、移动、最优、平均），以及丢包率五张表
"""
import csv
import time


def write_csv(file_list, file_name):
    """
    写CSV 文件
    :param file_list:
    :return: None
    """
    f = open(file_name, "w", newline='', encoding='GBK')
    writer = csv.writer(f)
    province_list = [" ", "北京", "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "山东", "河南", "上海", "江苏", "浙江",
                     "安徽", "福建", "江西", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海",
                     "宁夏", "新疆"]
    writer.writerow(province_list)
    line_cnt = 1
    for item in file_list:
        item.insert(0, province_list[line_cnt])
        writer.writerow(item)
        line_cnt += 1
    f.close()


def process_data(file_name_1, file_name_2):
    base_matrix = []  # 基础矩阵数据
    province_list = ["北京","天津","河北","山西","内蒙古","辽宁","吉林","黑龙江","山东","河南","上海","江苏","浙江",
                     "安徽","福建","江西","湖北","湖南","广东","广西","海南","重庆","四川","贵州","云南","西藏","陕西","甘肃","青海","宁夏","新疆"]
    # 打开基础矩阵数据文件，并读取，写进base_matrix 列表
    file_read = open(file_name_1, 'r', encoding='utf-8-sig')
    line_cnt = 0
    for line in file_read.readlines():
        line_cnt += 1
        # print(line_cnt, ":", line.strip())
        base_matrix.append(line.strip())
    # print(base_matrix)
    file_read.close()
    # 打开省会与省对应数据表，并处理base_matrix表（将省会名称替换为省名称）
    file_read = open(file_name_2, 'r', encoding='utf-8-sig')
    line_cnt = 0
    for line in file_read.readlines():
        line_cnt += 1
        city_name = line.strip().split(',')[0]
        province_name = line.strip().split(',')[1]
        # print(line_cnt, ":", city_name, province_name)
        # 搜索base_matrix，并进行替换
        base_matrix = [line_str.replace(city_name, province_name) for line_str in base_matrix]
        # province_name_split = "#"+province_name+"#"
        # base_matrix = [line_str.replace(province_name, province_name_split) for line_str in base_matrix]
    file_read.close()
    [print(item) for item in base_matrix]
    print(len(province_list))

    # ######################移动开始############################
    yidong_delay = [([0]*31) for i in range(31)]  # 生成31*31的各省移动_时延矩阵
    # 处理并生成移动时延矩阵
    # 遍历
    for i in range(31):
        for j in range(31):
            # print(i, j, province_list[i]+"移动,移动"+province_list[j])
            find_str = province_list[i]+"移动,移动"+province_list[j]
            aim_delay = 0
            for line_str in base_matrix:
                # 如果找到了指定字符串
                if line_str.find(find_str) == 0:
                    print(i, j, province_list[i], province_list[j], line_str.strip().split(',')[2])
                    aim_delay = line_str.strip().split(',')[2]
            yidong_delay[i][j] = aim_delay
    print(yidong_delay)
    # ################移动结束##################################

    # ################联通开始##################################
    liantong_delay = [([0]*31) for i in range(31)]  # 生成31*31的各省联通时延矩阵
    # 处理并生成联通时延矩阵
    # 遍历
    for i in range(31):
        for j in range(31):
            # print(i, j, province_list[i]+"联通,联通"+province_list[j])
            find_str = province_list[i]+"联通,联通"+province_list[j]
            aim_delay = 0
            for line_str in base_matrix:
                # 如果找到了指定字符串
                if line_str.find(find_str) == 0:
                    print(i, j, province_list[i], province_list[j], line_str.strip().split(',')[2])
                    aim_delay = line_str.strip().split(',')[2]
            liantong_delay[i][j] = aim_delay
    print(liantong_delay)
    # ################移动结束##################################

    # ################电信开始##################################
    dianxin_delay = [([0]*31) for i in range(31)]  # 生成31*31的各省电信时延矩阵
    # 处理并生成电信时延矩阵
    # 遍历
    for i in range(31):
        for j in range(31):
            find_str = province_list[i]+"电信,电信"+province_list[j]
            aim_delay = 0
            for line_str in base_matrix:
                # 如果找到了指定字符串
                if line_str.find(find_str) == 0:
                    print(i, j, province_list[i], province_list[j], line_str.strip().split(',')[2])
                    aim_delay = line_str.strip().split(',')[2]
            dianxin_delay[i][j] = aim_delay
    print(dianxin_delay)
    # ################移动结束#################################

    # ################求最优和平均#############################
    best_delay = [([0]*31) for i in range(31)]  # 生成31*31的各省运营商最优时延矩阵
    average_delay = [([0] * 31) for i in range(31)]  # 生成31*31的各省运营商平均时延矩阵
    nums = []
    for i in range(31):
        for j in range(31):
            if float(yidong_delay[i][j]) != 0:
                nums.append(float(yidong_delay[i][j]))
            if float(liantong_delay[i][j]) != 0:
                nums.append(float(liantong_delay[i][j]))
            if float(dianxin_delay[i][j]) != 0:
                nums.append(float(dianxin_delay[i][j]))
            min_delay = min(nums)
            best_delay[i][j] = min_delay
            average_delay[i][j] = max(nums) / len(nums)
            nums = []
    print(best_delay)
    print(average_delay)
    ###########################################################
    # 按要求输出yidong_delay
    write_csv(yidong_delay, "yidong_delay.csv")
    # 按要求输出dianxin_delay
    write_csv(dianxin_delay, "dianxin_delay.csv")
    # 按要求输出liantong_delay
    write_csv(liantong_delay, "liantong_delay.csv")
    # 按要求输出最优矩阵
    write_csv(best_delay, "best_delay.csv")
    # 按要求输出平均矩阵
    write_csv(average_delay, "average_delay.csv")


if __name__ == "__main__":
    # process_file = "分小时算平均-电信到移动_ywy.csv"
    process_file_1 = "base_matrix_data.csv"
    process_file_2 = "city_province.csv"
    process_data(process_file_1, process_file_2)
