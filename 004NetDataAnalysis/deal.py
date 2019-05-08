# coding:utf-8
"""
create on Nov 15,2018 by Wayne Yu
Fun:按薛雪要求处理对应的测速数据，每小时的数据求以此平均
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
    for item in file_list:
        writer.writerow(item)
    f.close()


def process_data(file_name):
    out_file_list = []  # 规定格式存储的数据列表
    file_read = open(file_name, 'r', encoding='utf-8')
    line_cnt = 0
    pre_hour = 0  # 记录当前小时（初始化为0），如果发生变化则翻转，重新计数
    sum_delay = 0.0  # 记录当前小时时间内时延数据的和
    sum_loss = 0.0  # 记录当前小时内丢包率数据的和
    hour_cnt = 0  # 记录当前小时内记录的个数
    tmp_list = []
    for line in file_read.readlines():
        line_cnt += 1
        line = line.strip().split(',')
        date_str = line[2]  # 提取当前时间字符串
        print(date_str)
        date_str = time.strptime(date_str, "%Y-%m-%d %H:%M")
        # print(date_str.tm_hour)
        if int(date_str.tm_hour) != pre_hour:
            # 如果小时发生变化
            print("翻转！")
            # 如果发生翻转，则需要在更新数据之前求上一小时的平均，并保存数据
            avg_delay = sum_delay / hour_cnt
            avg_loss = sum_loss / hour_cnt
            print(avg_delay, avg_loss)
            tmp_list.append(line[0])
            tmp_list.append(line[1])
            tmp_list.append(time.strftime("%Y-%m-%d %H", date_str))
            tmp_list.append(str(round(avg_delay, 2)))
            tmp_list.append(str(round(avg_loss, 2)))
            out_file_list.append(tmp_list)
            tmp_list = []
            # 处理完毕后，开始更新参数，进行新一轮的计算
            pre_hour = int(date_str.tm_hour)  # 更新当前小时
            sum_delay = float(line[3])  # 记录当前小时时间内时延数据的和
            sum_loss = float(line[4])  # 记录当前小时内丢包率数据的和
            hour_cnt = 1  # 记录当前小时内记录的个数
        else:
            # 否则执行小时组内计算
            sum_delay += float(line[3])
            sum_loss += float(line[4])
            hour_cnt += 1
    # print(line_cnt)
    print(out_file_list)
    write_csv(out_file_list, "处理完成_"+file_name)


if __name__ == "__main__":
    # process_file = "分小时算平均-电信到移动_ywy.csv"
    process_file = "分小时算平均-联通到移动_ywy.csv"
    process_data(process_file)
