# coding:utf-8
"""
create on May 26, 2020 By Wenyan YU
Function:

该程序主要实现对Bird系统中的RIB（M）和MESSAGE(M)数据进行分析
RIB数据可以构建Prefix2AS, AS_PATH 2元组和AS_PATH 3元组
MESSAGE数据可以构建通告数据的Prefix2AS，AS_PATH 2元组和AS_PATH 3元组。

此外二者还可以分析相关的统计信息
RIB(M)，PVR五元组，AS集、地址前缀集（再结合国家信息可出很多统计数据）
MESSAGE(M)，通告前缀的记录数（新增通道和撤销通告的统计）等
"""
import csv
import time


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


def gain_rib_info(rib_file):
    """
    根据传入的rib file<M>，进行相关的数据统计分析
    :param rib_file:
    :return rib_info_Prefix2AS:
    """
    print(rib_file)
    rib_info_Prefix2ASPath = {}  # 存储Prefix: AS_PATH
    rib_info_Prefix2AS = {}  # 存储Prefix2AS的记录
    rib_records_cnt = 0
    file_read = open(rib_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        origin_as = line[7].split(" ")[-1]
        # print(line)
        # 判断key（前缀）是否在字典中
        if line[5] not in rib_info_Prefix2ASPath.keys():
            # 若前缀不在字典中，则新建记录
            rib_info_Prefix2ASPath.setdefault(line[5], []).append(line[7])
        else:
            # 若前缀在字典中，则需要判断AS PATH是否已存在
            if line[7] not in rib_info_Prefix2ASPath[line[5]]:
                # 若该AS PATH记录不存在，则新增记录
                rib_info_Prefix2ASPath.setdefault(line[5], []).append(line[7])

        # 判断key（前缀）是否在字典中
        if line[5] not in rib_info_Prefix2AS.keys():
            # 若前缀不在字典中，则新建记录
            rib_info_Prefix2AS.setdefault(line[5], []).append(origin_as)
        else:
            # 若前缀在字典中，则需要判断Origin AS是否存在
            if origin_as not in rib_info_Prefix2AS[line[5]]:
                # 若该Origin AS记录不存在，则新增记录
                rib_info_Prefix2AS.setdefault(line[5], []).append(origin_as)

        rib_records_cnt += 1
        if rib_records_cnt >= 10:
            pass
    print("RIB All Records:", rib_records_cnt)
    print("Prefix All Records(AS_PATH):", len(rib_info_Prefix2ASPath.keys()))
    print("Prefix All Records(Origin AS):", len(rib_info_Prefix2AS.keys()))
    return rib_info_Prefix2AS


def gain_message_info(message_file):
    """
    根据传入的message file<M>，进行相关数据统计分析
    :param message_file:
    :return message_info_Prefix2AS:
    """
    print(message_file)
    message_info_withdraw = []  # 存储撤销的报文信息、
    message_info_Prefix2ASPath = {}  # 新增通告，存储Prefix: AS_PATH
    message_info_Prefix2AS = {}  # 新增通告，存储Prefix2AS的记录
    message_records_cnt = 0

    file_read = open(message_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        if line[2] == "W":
            message_info_withdraw.append([line[1], line[5]])
        elif line[2] == "A":
            origin_as = line[7].split(" ")[-1]
            # 判断key（前缀）是否在字典中
            if line[5] not in message_info_Prefix2ASPath.keys():
                # 若前缀不在字典中，则新建记录
                message_info_Prefix2ASPath.setdefault(line[5], []).append(line[7])
            else:
                # 若前缀在字典中，则需要判断AS PATH是否已存在
                if line[7] not in message_info_Prefix2ASPath[line[5]]:
                    # 若该AS PATH记录不存在，则新增记录
                    message_info_Prefix2ASPath.setdefault(line[5], []).append(line[7])

            # 判断key（前缀）是否在字典中
            if line[5] not in message_info_Prefix2AS.keys():
                # 若前缀不在字典中，则新建记录
                message_info_Prefix2AS.setdefault(line[5], []).append(origin_as)
            else:
                # 若前缀在字典中，则需要判断Origin AS是否存在
                if origin_as not in message_info_Prefix2AS[line[5]]:
                    # 若该Origin AS记录不存在，则新增记录
                    message_info_Prefix2AS.setdefault(line[5], []).append(origin_as)
        else:
            print(line[2])
        message_records_cnt += 1
        if message_records_cnt >= 10000000:
            pass
    print("Message All Records:", message_records_cnt)
    print("Message Withdraw(Prefix):", len(message_info_withdraw))
    print("Prefix All Records(AS_PATH):", len(message_info_Prefix2ASPath.keys()))
    print("Prefix All Records(Origin AS):", len(message_info_Prefix2AS.keys()))
    return message_info_Prefix2AS


def find_abnormal(rib_prefix2as, message_prefix2as):
    """
    根据传入的rib prefix2as和 message add报文 prefix2as进行比对发现异常事件
    :param rib_prefix2as:
    :param message_prefix2as:
    :return:
    """
    new_prefix_cnt = 0
    abnormal_event_cnt = 0
    for key in message_prefix2as.keys():
        if key not in rib_prefix2as.keys():
            # print("New Prefix: %s(%s)" % (key, message_prefix2as[key]))
            new_prefix_cnt += 1
        else:
            if not set(message_prefix2as[key]).issubset(set(rib_prefix2as[key])):
                # 判断message中origin as 是否为rib中的真子集，若不是则为异常
                # print("Prefix %s, Message(%s), RIB(%s)" % (key, message_prefix2as[key], rib_prefix2as[key]))
                abnormal_event_cnt += 1
    print("New Prefix Announce:", new_prefix_cnt)
    print("Abnormal Event:", abnormal_event_cnt)


def find_abnormal_realtime(message_file, rib_prefix2as):
    """
    根据每15分钟切割好的UPDATE报文，逐行读取并判断是否为异常事件
    :param message_file:
    :param rib_prefix2as:
    :return:
    """
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    new_prefix_cnt = 0
    new_prefix_list = []  # 存储新通告的前缀
    abnormal_event_cnt = 0
    abnormal_prefix_list = []  # 存储通告中存在异常的前缀
    file_read = open(message_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        if line[2] == "A":
            origin_as = line[7].split(" ")[-1]
            if line[5] not in rib_prefix2as.keys():
                if line[5] not in new_prefix_list:
                    new_prefix_list.append(line[5])
                new_prefix_cnt += 1
            else:
                if origin_as not in rib_prefix2as[line[5]]:
                    if line[5] not in abnormal_prefix_list:
                        print("++++++++++++++++++++++++++++++++")
                        print("Event Type: Possible Hijack")
                        print("Abnormal Prefix:", line[5])
                        print("Expected Origin AS:", rib_prefix2as[line[5]])
                        print("Detect Origin AS:", origin_as)
                        print("Detect time(UTC):", line[1])
                        abnormal_prefix_list.append(line[5])
                    abnormal_event_cnt += 1

    print("New Prefix Announce:", new_prefix_cnt, "Not Repeated:", len(new_prefix_list))
    print("Abnormal Event:", abnormal_event_cnt, "Not Repeated:", len(abnormal_prefix_list))


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    rib_file_in = '../000LocalData/BGPData/birdmrt_master_2020-05-08_00_45_09_M.txt'
    message_file_in = '../000LocalData/BGPData/birdmrt_messages_2020-05-26_15_37_56_M.txt'
    rib_prefix2as = gain_rib_info(rib_file_in)
    message_prefix2as = gain_message_info(message_file_in)
    find_abnormal(rib_prefix2as, message_prefix2as)
    find_abnormal_realtime(message_file_in, rib_prefix2as)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")




