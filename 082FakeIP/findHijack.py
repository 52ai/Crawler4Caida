# coding:utf-8
"""
create on May 12, 2022 By Wayne YU

Function:

找到Fake IP

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


def gain_as2country_caida():
    """
    根据Caida asn info获取as对应的国家信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_country = line[-1]
        as2country[as_number] = as_country
    return as2country


def find_fake_ip():
    """
    find fake ip
    :return:
    """
    as2country_dic = gain_as2country_caida()
    result_list = []
    file_read = open("./announce.csv", 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        country_list = []
        country = "CN"
        except_list = []  # 存储异常信息
        for item in line:
            # print(item)
            try:
                country = as2country_dic[str(item)]
            except Exception as e:
                except_list.append(e)
            country_list.append(country)
        print(country_list)
        result_list.append(country_list)
    write_to_csv(result_list, "as2country_result.csv")


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    find_fake_ip()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
