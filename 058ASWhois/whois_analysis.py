# coding: utf-8
"""
create on Jan 15, 2021 By Wenyan YU
Email: ieeflsyu@outlook

Function:

对抓取的AS Whois原始信息进行分析，依托Google地图的功能，获取所有AS网络的画像
尤其是更细粒度的经纬度信息
"""
import csv
import time


def write_to_csv(res_list, des_path, title_list):
    """
    把给定的List，写到指定路径文件中
    :param res_list:
    :param des_path:
    :param title_list:
    :return None
    """
    print("write file <%s>.." % des_path)
    csv_file = open(des_path, "w", newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        writer.writerow(title_list)
        for i in res_list:
            writer.writerow(i)
    except Exception as e_csv:
        print(e_csv)
    finally:
        csv_file.close()
    print("write finish!")


def whois_analysis():
    """
    根据as whois原始信息，提取AS有效数据，尤其是机构地址
    并将其与Google地图结合
    """
    aswhois_file = "d:/code/Crawler4Caida/000LocalData/ASWhois/aswhois.txt"
    file_read = open(aswhois_file, 'r', encoding='utf-8')
    block_flag = True  # 标记每一个AS请求块
    block_cnt = 0  # AS请求块计数
    for line in file_read.readlines():
        line = line.strip()
        if line.startswith("======="):
            print("-------Block Counter:%d---------" %(block_cnt + 1 ))
            block_flag = True
            block_cnt += 1 # 块计数自加1       
        
        if line.startswith("ASNumber:") \
        or line.startswith("ASName:") \
        or line.startswith("as-block:") \
        or line.startswith("descr:") \
        or line.startswith("OrgName:") \
        or line.startswith("org-name:") \
        or line.startswith("aut-num:") \
        or line.startswith("as-name:"):
            print(line)
            block_flag = False

        if block_flag == False and (not line.startswith("========")):
            continue

        if block_cnt > 2000:
            break


if __name__ == "__main__":
    time_start = time.time()
    whois_analysis()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")

