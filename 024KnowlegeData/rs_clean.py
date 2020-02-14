# coding:utf-8
"""
create on Feb 14, 2020 By Wenyan YU
Function:

对院知识工厂中爬取的软科学研究课题数据进行数据清洗

院知识工厂软科学研究课题，共有2461个课题，剔除页面信息不规范、链接错误等内容，共爬取2251条记录（8个数据项）
记录的格式为：rs_name、rs_number、rs_time、responsible_person、responsible_dept、rs_classification、rs_content、page_url

先需对其进行数据清洗
输入:research_subject_raw.csv
输出:research_subject_clean.csv


"""

import time
import csv
import re


# caict_dept = ["泰尔数据研究中心", "信息通信安全研究所", "西部分院(重庆)", "电信与信息服务咨询中心",
#               "政策与经济研究所", "技术与标准研究所", "产业与规划研究所", "信息化与工业化融合研究所", "安全研究所",
#               "云计算与大数据研究所", "泰尔系统实验室", "泰尔终端实验室", "泰尔认证研究所",
#               "电信设备认证中心", "电信用户申诉受理中心", "电信与信息服务咨询中心", "通信工程定额质监中心",
#               "数据研究中心", "信息管理中心", "南方分院", "西部分院", "华东分院", "广州智慧城市研究所",
#               "工业互联网和物联网研究所", "无线电研究中心",
#               "人力资源部", "国际合作部",
#               "知识产权中心(原)", "规划设计研究所(原)",
#               "通信信息研究所(原)", "通信标准研究所", "泰尔实验室(原)", "泰尔管理研究所(原)", "泰尔规划研究所",
#               "电信研究院", "泰尔认证中心", "科技市场部(原)", "质监中心", "咨询中心", "NONE"]


caict_dept = ["泰尔数据研究中心", "信息通信安全研究所", "西部分院(重庆)", "电信与信息服务咨询中心",
              "政策与经济研究所", "技术与标准研究所", "产业与规划研究所", "信息化与工业化融合研究所", "安全研究所",
              "云计算与大数据研究所", "泰尔系统实验室", "泰尔终端实验室", "泰尔认证研究所",
              "电信设备认证中心", "电信用户申诉受理中心", "通信工程定额质监中心",
              "数据研究中心", "信息管理中心",
              "工业互联网和物联网研究所", "无线电研究中心",
              "人力资源部", "国际合作部",
              "知识产权中心(原)", "规划设计研究所(原)",
              "通信信息研究所(原)", "通信标准研究所", "泰尔实验室(原)", "泰尔管理研究所(原)", "泰尔规划研究所",
              "电信研究院", "泰尔认证中心", "科技市场部(原)", "质监中心", "咨询中心", "NONE"]


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


def list2dict_count(res_list):
    """
    根据传入的list，统计各元素的频次，并返回频次字典
    :param res_list:
    :return des_dict:
    """
    des_dict = {}
    for item in set(res_list):
        des_dict[item] = 0
    for item in res_list:
        des_dict[item] += 1
    return des_dict


def dict2list_rank(res_dict):
    """
    根据传入的dict，将其转换为list，并按降序排名
    :param res_dict:
    :return des_list:
    """
    des_list = []
    temp_list = []
    for key in res_dict.keys():
        temp_list.append(key)
        temp_list.append(res_dict[key])
        des_list.append(temp_list)
        temp_list = []
    des_list.sort(reverse=True, key= lambda elem: int(elem[1]))
    return des_list


def data_clean(res_file_path, des_file_path):
    """
    根据传入的数据源路径和目标源路径，进行数据的清洗和存储
    :param res_file_path:
    :param des_file_path:
    :return:
    """
    res_file_read = open(res_file_path, 'r', encoding='utf-8')
    des_list = []
    line_cnt = 0
    subject_number_list = []  # 存储课题编号
    year_list = []  # 存储年份
    responsible_person_list = []  # 存储负责人
    dept_type_list = []  # 存储部门类型list
    subject_type_list = []  # 存储课题类型list
    for line in res_file_read.readlines():
        line = line.strip().split('|')
        try:
            # 处理负责人信息开始
            line[3] = line[3].replace(' ', '、', 3)
            # print(line[3].split("、"))
            # 处理负责人信息结束

            # 处理责任单位信息开始
            if len(line[4]) == 0:
                line[4] = "None"
            line[4] = line[4].replace("原", "(原)", 10)
            line[4] = line[4].replace("重庆", "(重庆)", 10)
            line_4_raw = line[4]
            # print(line[4])
            line_4_str = ""
            iter_cnt = 0
            for item in caict_dept:
                if str(line[4].find(item)) != "-1":
                    line_4_str = line_4_str + item + "、"
                    line[4] = line[4].replace(item, "", 10)
                    iter_cnt += 1
            line_4_str = line_4_str[:-1]
            line[4] = line_4_str
            # print(line[4].split("、"))
            # 处理责任单位信息结束
            # print(line[5])

            # 处理课题内容描述开始
            line_6_str = line[6]
            dr = re.compile(r'<[^>]+>', re.S)  # 去除html标签信息
            line_6_str = dr.sub('', line_6_str)
            # print(line_6_str)
            line[6] = line_6_str
            # 处理课题内容描述结束

            subject_number_list.append(line[1])
            if len(line[1]) == 0:
                print(line[0], line[5])
            year_list.append(line[2])
            responsible_person_list.extend(line[3].split("、"))
            dept_type_list.extend(line[4].split("、"))
            subject_type_list.append(line[5])

        except Exception as e:
            print("ERROR:", e, " line:", line_cnt)
        line_cnt += 1
        des_list.append(line)
    print("=>编号统计:", len(set(subject_number_list)), line_cnt)
    # print(list2dict_count(subject_number_list))
    print("=>年份统计:", len(set(year_list)), list(set(year_list)))
    print(dict2list_rank(list2dict_count(year_list)))
    print("=>人员统计:", len(set(responsible_person_list)))
    # print(dict2list_rank(list2dict_count(responsible_person_list)))
    print("=>负责单位:", len(set(dept_type_list)))
    print(dict2list_rank(list2dict_count(dept_type_list)))
    print("=>课题类型:", len(set(subject_type_list)), list(set(subject_type_list)))
    print(dict2list_rank(list2dict_count(subject_type_list)))
    # 存储清洗之后的数据
    write_to_csv(des_list, des_file_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    res_file = "..\\000LocalData\\caict_k\\research_subject_raw.csv"
    des_file = "..\\000LocalData\\caict_k\\research_subject_clean.csv"
    data_clean(res_file, des_file)
    time_end = time.time()  # 记录程序结束时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")