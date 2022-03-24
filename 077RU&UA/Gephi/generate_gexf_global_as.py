# coding:utf-8
"""
create on Mar 24, 2022 By Wayne YU
Email: ieeflsyu@outlook.com

Function:
因Echarts难以发现一些实质上的问题，计划通过Gephi去先构建一个全局的AS可视化图
然后在此图上做相应的研究
甚至可以结合经纬度，做地理位置方面的可视化，（数据质量可以不用那么好，先做出来看看效果再说）
本程序主要用于构建Gephi的输入文件
包含node和edges

输入： asns_geo_all.csv、20220301.as-rel.txt
输出：global_as.gexf

"""
import time
import csv

asn_file = "asn_geo_all.csv"
as_rel_file = "20220301.as-rel.txt"


def write_to_csv(res_list, des_path, title):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :param title:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(title)
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def generate_gephi_file():
    """
    根据两个文件生成gephi文件
    :return:
    """
    pass


if __name__ == "__main__":
    time_start = time.time()
    generate_gephi_file()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
