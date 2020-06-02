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

20200601
将AS与国家和地理位置信息结合起来

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


def gain_as_info():
    """
    获取AS的相关信息
    :return:
    """
    # as_info_file = '../000LocalData/as_map/as_core_map_data_new20200201.csv'
    as_info_file_gao = '../000LocalData/as_Gao/asn_info.txt'
    as_info_dict = {}  # 存储AS信息的字典
    file_read = open(as_info_file_gao, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        as_info_dict[line[0]] = line[-1].split(',')[-1]

    return as_info_dict


def gain_rib_info(rib_file):
    """
    根据传入的rib file<M>，进行相关的数据统计分析
    :param rib_file:
    :return rib_info_Prefix2AS:
    """
    print("- - - - - - - - - -RIB INFO- - - - - - - - - - - - - - - - ")
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


def gain_radb_info(radb_file):
    """
    根据传入的radb库的信息，按需求格式获取prefix2as以及其他可能需要的信息
    :param radb_file:
    :return radb_info_Prefix2AS:
    """
    print("- - - - - - - - - -RADB INFO- - - - - - - - - - - - - - - - ")
    print(radb_file)
    radb_info_Prefix2AS = {}  # 存储prefix2as的记录
    radb_records_cnt = 0  # 统计RADB中注册的有效记录的个数
    radb_as_list = []  # 存储radb库中存在的AS记录
    file_read = open(radb_file, 'rb')
    temp_route = ''
    temp_origin = ''
    for line in file_read.readlines():
        line = line.strip()
        if line:
            line = line.split()
            # print(line[0].decode('utf-8', 'ignore'), line[-1].decode('utf-8', 'ignore'))
            """"
            文件中存在多种编码的，可使用不严格解码的方式decode('utf-8', 'ignore')
            """
            if line[0].decode('utf-8', 'ignore') == 'route:':
                temp_route = line[-1].decode('utf-8', 'ignore').strip()
            elif line[0].decode('utf-8', 'ignore') == 'origin:':
                temp_origin = line[-1].decode('utf-8', 'ignore').strip().upper().strip("AS")
        else:
            if temp_route and temp_origin:
                # print(temp_route, temp_origin)
                radb_as_list.append(temp_origin)  # 记录出现的AS网络
                radb_records_cnt += 1
                # 判断前缀是否在字典中
                if temp_route not in radb_info_Prefix2AS.keys():
                    radb_info_Prefix2AS.setdefault(temp_route, []).append(temp_origin)
                else:
                    # 若前缀在字典中，则需要判断origin as是否存在该前缀对应的源AS中
                    if temp_origin not in radb_info_Prefix2AS[temp_route]:
                        radb_info_Prefix2AS.setdefault(temp_route, []).append(temp_origin)
                    else:
                        print("Duplicate Registration!", temp_route, temp_origin)
            temp_route = ''
            temp_origin = ''
    print("RADB All Records:", radb_records_cnt)
    print("Prefix All Records(Origin AS):", len(radb_info_Prefix2AS))
    print("AS Records:", len(set(radb_as_list)))

    return radb_info_Prefix2AS


def gain_message_info(message_file):
    """
    根据传入的message file<M>，进行相关数据统计分析
    :param message_file:
    :return message_info_Prefix2AS:
    """
    print("- - - - - - - - - -MESSAGE INFO- - - - - - - - - - - - - - - - ")
    print(message_file)
    message_info_withdraw = []  # 存储撤销的报文信息
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
            # print(line[2])
            pass
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
    print("- - - - - - - - - -Find Abnormal(RIB)- - - - - - - - - - - - - - - - ")
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


def find_abnormal_realtime(message_file, rib_prefix2as, radb_prefix2as, message_file_out):
    """
    根据每15分钟切割好的UPDATE报文，逐行读取并判断是否为异常事件
    :param message_file:
    :param rib_prefix2as:
    :param radb_prefix2as:
    :param message_file_out:
    :return:
    """
    message_file_out_list = []  # 存储输出的报文信息
    # 利用radb_prefix2as中的源AS数据扩充rib_prefix2as中的源AS数据
    for key in rib_prefix2as.keys():
        if key in radb_prefix2as.keys():
            rib_prefix2as.setdefault(key, []).extend(radb_prefix2as[key])
            rib_prefix2as[key] = list(set(rib_prefix2as[key]))  # 两个库合并，可能存在重复项，需去重

    print("- - - - - - - - - -Find Abnormal Realtime(RIB+RADB)- - - - - - - - - - - - - - - - ")
    new_prefix_cnt = 0
    new_prefix_list = []  # 存储新通告的前缀
    abnormal_event_cnt = 0
    abnormal_prefix_list = []  # 存储通告中存在异常的前缀
    file_read = open(message_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        flag = 0
        if line[2] == "A":
            origin_as = line[7].split(" ")[-1]
            if line[5] not in rib_prefix2as.keys():
                if line[5] not in new_prefix_list:
                    new_prefix_list.append(line[5])
                new_prefix_cnt += 1
            else:
                if origin_as not in rib_prefix2as[line[5]]:
                    flag = 1
                    if line[5] not in abnormal_prefix_list:
                        print("++++++++++++++++++++++++++++++++")
                        print("Event Type: Possible Hijack")
                        print("Abnormal Prefix:", line[5])
                        print("Expected Origin AS:", rib_prefix2as[line[5]])
                        print("Detect Origin AS:", origin_as)
                        print("Detect time(UTC):", line[1])
                        abnormal_prefix_list.append(line[5])

                    abnormal_event_cnt += 1
        line.append(flag)
        message_file_out_list.append(line)
        # print(line)
    write_to_csv(message_file_out_list, message_file_out)
    print("New Prefix Announce:", new_prefix_cnt, "Not Repeated:", len(new_prefix_list))
    print("Abnormal Event:", abnormal_event_cnt, "Not Repeated:", len(abnormal_prefix_list))


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    rib_file_in = '../000LocalData/BGPData/birdmrt_master_2020-05-08_00_45_09_M.txt'
    radb_file_in = '../000LocalData/BGPData/20200527radb.db.route'
    # message_file_in = '../000LocalData/BGPData/updates.20200526.1010_M_Bird.txt'
    # message_file_in = '../000LocalData/BGPData/birdmrt_messages_2020-05-26_18_22_57_M.txt'
    message_file_in = '../000LocalData/BGPData/birdmrt_messages_2020-06-01_12_30_08_M.txt'
    message_file_out = '../000LocalData/BGPData/birdmrt_messages_2020-06-01_12_30_08_M_out.txt'
    as_info_dict = gain_as_info()
    rib_prefix2as = gain_rib_info(rib_file_in)
    radb_prefix2as = gain_radb_info(radb_file_in)
    message_prefix2as = gain_message_info(message_file_in)
    find_abnormal(rib_prefix2as, message_prefix2as)
    find_abnormal_realtime(message_file_in, rib_prefix2as, radb_prefix2as, message_file_out)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")



