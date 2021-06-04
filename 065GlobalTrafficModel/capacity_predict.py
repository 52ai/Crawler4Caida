# coding:utf-8
"""
create on Jun 4, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

根据过去十年的历史数据，利用回归算法初步预测未来3-5年的数据

"""
import time
import csv


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


def capacity_predict():
    """
    对数据进行预测
    :return:
    """
    pass


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    capacity_predict()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
