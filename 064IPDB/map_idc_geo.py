# utf-8
"""
create on July 7, 2022 By Wayne YU
Email:ieeflsyu@outlook.com

Function:

根据提取的开放80、43端口IP地址Geo信息，统计其在国内地域分布

"""
import time
import csv


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
        writer = csv.writer(csv_file, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def deal():
    """
    处理并保存
    :return:
    """
    file_in = "../000LocalData/IPPorts/map_idc_v1.csv"
    file_read = open(file_in, 'r', encoding='gbk')
    line_cnt = 0
    province_dict = {}  # 存储每个省的开放WEB端口IP数量
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        province = line[1]
        if province is None:
            province = "ZZ"
        if province not in province_dict.keys():
            province_dict[province] = 1
        else:
            province_dict[province] += 1
        line_cnt += 1

    # 将字典转换为列表
    province_rank_list = []
    temp_list = []
    for item in province_dict.keys():
        temp_list.append(item)
        temp_list.append(province_dict[item])
        province_rank_list.append(temp_list)
        temp_list = []
    province_rank_list.sort(reverse=True, key=lambda elem: int(elem[1]))

    print("我国开放WEB端口IP地址数量(80+443)：", line_cnt)
    print("我国开放WEB端口IP地址数量分省排名：")
    print(province_rank_list)

    save_path = "map_idc_geo_result.csv"
    write_to_csv(province_rank_list, save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    deal()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
