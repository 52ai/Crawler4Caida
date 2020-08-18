# coding:utf-8
"""
create on Aug 15, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

按照Chinanet rib的分析思路，分析Chinaunicom rib
chinaunicom rib的数据格式相对简单些(在实际处理的时候，发现大量的不规范现象)

V2:

按照chinanet rib v2版本的分析思路，分析chinaunicom rib

V3:
分阶段统计AS中IP规模

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
    csvFile = open(des_path, 'w', newline='', encoding='gbk')
    try:
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def extract_as_info():
    """
    根据asn_info文件，提取as info 信息
    :return:
    """
    file_in = "../000LocalData/as_Gao/asn_info.txt"
    file_in_read = open(file_in, 'r', encoding='utf-8')
    as2country_dict = {}  # 存储as号和国家对应关系的字典
    for line in file_in_read.readlines():
        line = line.strip().split("\t")
        as2country_dict[line[0]] = line[1].split(",")[-1].strip()
    return as2country_dict


def chinaunicom_rib_analysis(rib_file, u_as_group):
    """
    根据转入的rib txt信息，统计其最优路由第一跳为U国的占比
    :param rib_file:
    :param u_as_group:
    :return:
    """
    as2country = extract_as_info()
    # print(as2country)
    rib_file_read = open(rib_file, 'r')
    line_cnt = 0  # 记录行数
    invalid_cnt = 0  # 记录无效记录数
    valid_cnt = 0  # 记录有效记录数
    ip_num_cnt = 0  # 根据前缀统计IP规模，用32减去网络号的长度，大约为2的N次方个地址
    prefix_u_cnt = 0  # 记录最优路由第一跳为U国的前缀数量
    ip_num_u_cnt = 0  # 记录最优路由第一跳为U国的IP地址数量
    prefix_u_cnt_anywhere = 0  # 记录最优路由任意一跳含U国的前缀数量
    ip_num_u_cnt_anywhere = 0  # 记录最优路由任意一跳含U过的IP地址数量
    direct_networks_list = []  # 存储该ISP直联网络的列表
    direct_networks_u_list = []  # 存储该ISP直联属于U国的网络列表
    direct_networks_c_list = []  # 存储该ISP直联属于C国的网络列表

    global_reachable_as_list = []  # 存储总的全球可达网络的AS列表
    reachable_as_list_first = []  # 存储第一层次可达的AS列表
    reachable_as_list_second = []  # 存储第二层次可达的AS列表
    for line in rib_file_read.readlines():
        line = line.strip()
        line_cnt += 1
        if line.find("/") != -1:
            line = line.strip("*").strip(">").strip("i").strip("?").strip("e").strip()
            line = line.split(" 219")
            if len(line) == 1:
                line = line[0].split(" 202")
            if len(line) == 1:
                line = line[0].split(" 218")
            if len(line) == 1:
                line = line[0].split(" 10")
            if len(line) == 1:
                line = line[0].split(" 220")
            # print(line)
            as_path = []
            ip_prefix = []
            try:
                ip_prefix = line[0].strip().split("/")
                # print(ip_prefix)
                as_path = line[1].strip().split("   ")[-1].split(" ")
            except Exception as e:
                # print(e)
                pass

            if len(as_path) == 1:
                invalid_cnt += 1
                continue
            # print(ip_prefix[-1], as_path[1])
            valid_cnt += 1
            net_len = int(ip_prefix[-1])
            ip_num_cnt += pow(2, (32-net_len))
            first_hop_as = as_path[1]
            last_hop_as = as_path[-1]
            last_hop_as = last_hop_as.strip("{").strip("}")

            if last_hop_as.find(",") != -1:
                # print(last_hop_as)
                last_hop_as = last_hop_as.split(",")[0]
            if last_hop_as.find(".") != -1:
                # print(as_path)
                # print(last_hop_as)
                left_point = last_hop_as.split(".")[0]
                right_point = last_hop_as.split(".")[1]
                last_hop_as = str(int(left_point) * 65536 + int(right_point))
                # print(last_hop_as)

            if first_hop_as in u_as_group:
                prefix_u_cnt += 1
                ip_num_u_cnt += pow(2, (32-net_len))

            if first_hop_as not in u_as_group:
                # 如果某AS网有一个前缀可达，则该AS网可达
                reachable_as_list_first.append(last_hop_as)

            # intersection_hop_set = set(as_path).intersection(set(u_as_group))

            u_flag = 0  # 是否路径是否含U国AS
            for item in as_path[1:]:
                try:
                    item = item.strip("{").strip("}")
                    if item.find(",") != -1:
                        # print(last_hop_as)
                        item = item.split(",")[0]
                    if item.find(".") != -1:
                        # print(as_path)
                        left_point = item.split(".")[0]
                        right_point = item.split(".")[1]
                        item = str(int(left_point) * 65536 + int(right_point))
                        # print(item)
                    if item == "0":
                        continue
                    if as2country[item] == "US":
                        u_flag = 1
                        break
                except Exception as e:
                    print(as_path[1:])
                    print(item)
                    pass

            # print(intersection_hop_set)
            if u_flag == 1:
                # print(intersection_hop_set)
                prefix_u_cnt_anywhere += 1
                ip_num_u_cnt_anywhere += pow(2, (32 - net_len))
            if u_flag == 0:
                # 如果某AS网有一个前缀可达，则该AS网可达
                reachable_as_list_second.append(last_hop_as)
            direct_networks_list.append(first_hop_as)  # 存储直联网络AS
            global_reachable_as_list.append(last_hop_as)  # 存储该条可达前缀所属的AS网络
            try:
                if as2country[first_hop_as] == "US":
                    # print(as2country[first_hop_as])
                    direct_networks_u_list.append(first_hop_as)  # 存储直联网络为U国的网络
                elif as2country[first_hop_as] == "CN":
                    direct_networks_c_list.append(first_hop_as)  # 存储直联网络为C国的网络
            except Exception as e:
                # print(e)
                pass
        else:
            invalid_cnt += 1

        # if line_cnt > 10:
        #     break
    direct_networks_list = list(set(direct_networks_list))
    direct_networks_u_list = list(set(direct_networks_u_list))
    direct_networks_c_list = list(set(direct_networks_c_list))

    global_reachable_as_list = list(set(global_reachable_as_list))
    reachable_as_list_first = list(set(reachable_as_list_first))
    reachable_as_list_second = list(set(reachable_as_list_second))

    temp_list = list()
    for item in global_reachable_as_list:
        temp_list.append([item])
    save_path = "../000LocalData/as_simulate/可达（联通）_0.txt"
    write_to_csv(temp_list, save_path)
    temp_list.clear()
    for item in reachable_as_list_first:
        temp_list.append([item])
    save_path = "../000LocalData/as_simulate/可达（联通）_1.txt"
    write_to_csv(temp_list, save_path)
    temp_list.clear()
    for item in reachable_as_list_second:
        temp_list.append([item])
        try:
            if as2country[item] == "US":
                print(item)
                pass
        except Exception as e:
            pass
    save_path = "../000LocalData/as_simulate/可达（联通）_2.txt"
    write_to_csv(temp_list, save_path)

    print("RIB文件总的行数:", line_cnt)
    print("无效记录数:", invalid_cnt)
    print("有效记录数:", valid_cnt)
    print("总的IP规模(v4):", ip_num_cnt)
    print("最优路由第一跳为U国的前缀数量:%s, 占比(%.6f)" % (prefix_u_cnt, prefix_u_cnt / valid_cnt))
    print("最优路由第一跳为U国的IP地址数量(V4):%s, 占比(%.6f)" % (ip_num_u_cnt, ip_num_u_cnt / ip_num_cnt))
    print("最优路由任意一跳含U国的前缀数量:%s, 占比(%.6f)" % (prefix_u_cnt_anywhere, prefix_u_cnt_anywhere / valid_cnt))
    print("最优路由任意一跳含U国的IP地址数量(V4):%s, 占比(%.6f)" % (ip_num_u_cnt_anywhere, ip_num_u_cnt_anywhere / ip_num_cnt))

    all_reach = len(global_reachable_as_list)
    reach_first = len(reachable_as_list_first)
    reach_second = len(reachable_as_list_second)
    print("\n该ISP可达的全球AS网络数量:", all_reach)
    print("第一层次操作后，该ISP全球可达的AS网络数量:%s, 占比(%.6f)" % (reach_first, reach_first/all_reach))
    print("第二层次操作后，该ISP全球可达的AS网络数量:%s, 占比(%.6f)" % (reach_second, reach_second/all_reach))
    print("注：某AS网络只要有一个前缀可达，则该AS网络可达")

    print("\n该ISP直联网络的数量:", len(direct_networks_list))
    print("该ISP直联网络中为U国的数量:", len(direct_networks_u_list))
    print("该ISP直联网络中为C国的数量:", len(direct_networks_c_list))


def gain_u_as_group():
    """
    根据All AS CSV文件，获取u as group
    :return re_list:
    """
    re_list = []  # 存储返回的list
    all_as_file = "../000LocalData/as_simulate/联通-所有企业.CSV"
    all_as_file_read = open(all_as_file, 'r')
    for line in all_as_file_read.readlines():
        line = line.strip().split(",")
        as_item = line[-1].strip("AS")
        # print(as_item)
        re_list.append(as_item)
    # print(len(re_list))
    return re_list


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    # us_as_group = ["9265", "8110", "8109", "8108", "8107", "8106", "7882", "7421", "7308", "7210",
    #                "6637", "6449", "6242", "6211", "6187", "6177", "6176", "6175", "6174", "6158",
    #                "6157", "6156", "6155", "6154", "6153", "5732", "56875", "56514", "5084", "5079",
    #                "4999", "4951", "4950", "4938", "4910", "43235", "42451", "41106", "4005", "4004",
    #                "4003", "4002", "4001", "4000", "3992", "3991", "3990", "3989", "3988", "3987",
    #                "3986", "3985", "3984", "3983", "3982", "3981", "3980", "3979", "3978", "3977",
    #                "3973", "3972", "3652", "3651", "3650", "3649", "3648", "3647", "3646", "3645",
    #                "3644", "3643", "3483", "33884", "3041", "3040", "3039", "3038", "3037", "3036",
    #                "3035", "3034", "3033", "3032", "3031", "3030", "3029", "3028", "3027", "3026",
    #                "3025", "3024", "3023", "3022", "3021", "3020", "3019", "3018", "3017", "3016",
    #                "3015", "3014", "3013", "3012", "3011", "3010", "3009", "3008", "3007", "3006",
    #                "3005", "3004", "3003", "3002", "3001", "3000", "2999", "2998", "2997", "2996",
    #                "2995", "2994", "2993", "2992", "2991", "2990", "2989", "2988", "2987", "2986",
    #                "2985", "2984", "2983", "2982", "2981", "2980", "2979", "2978", "2977", "2976",
    #                "2975", "2974", "2973", "2972", "2971", "2970", "2969", "2968", "2967", "2966",
    #                "2965", "2964", "2963", "2962", "2961", "2960", "2959", "2958", "2957", "2956",
    #                "2955", "2954", "2953", "2952", "2951", "2950", "2949", "2948", "2947", "2946",
    #                "2945", "2944", "2943", "2942", "2938", "270261", "24787", "23044", "21288", "2053",
    #                "2050", "197226", "1808", "1807", "1806", "1805", "1804", "1803", "1802", "1801",
    #                "1800", "1799", "1795", "1794", "1793", "1792", "1791", "1790", "1789", "17133",
    #                "137463", "131786", "1240", "1239", "1238", "11461", "10507",
    #                "7922", "7853", "7757", "7725", "7016", "7015", "6161", "53297", "396415", "396021",
    #                "396019", "396017", "395980", "395976", "395974", "395848", "393232", "36733", "36732", "36377",
    #                "36196", "33668", "33667", "33666", "33665", "33664", "33663", "33662", "33661", "33660",
    #                "33659", "33658", "33657", "33656", "33655", "33654", "33653", "33652", "33651", "33650",
    #                "33542", "33491", "33490", "33489", "33351", "33287", "269002", "264821", "23266", "23253",
    #                "22909", "22258", "21508", "202149", "20214", "16748", "14668", "14042", "13385", "13367",
    #                "132401", "11025",
    #                "7982", "7458", "7061", "6496", "6494", "6299", "6259", "4550", "22099", "2149", "19164", "174",
    #                "16631", "140664", "13129", "12207", "11526", "11220", "11024", "10768",
    #                "58682", "138951",
    #                "6431", "23143", "140237", "140235", "140234", "140233", "140232", "134537", "134536", "134535",
    #                "134534", "134533", "134532", "134531", "134530",
    #                "9555", "9194", "9062", "9055", "8768", "8671", "8385", "8243", "817", "816",
    #                "815", "814", "813", "8115", "8114", "8113", "8112", "8017", "8016", "7836",
    #                "7193", "7192", "705", "7046", "704", "703", "7021", "702", "7014", "701",
    #                "6995", "6984", "6976", "6811", "6541", "6350", "6256", "6167", "6113", "6066",
    #                "5725", "5621", "5614", "5599", "5586", "50146", "4981", "4908", "4860", "4313",
    #                "4239", "4183", "4017", "3966", "3965", "3964", "3963", "394260", "3707", "3493",
    #                "33052", "32471", "28625", "284", "2830", "2828", "28122", "2634", "2548", "23626",
    #                "23148", "22521", "22394", "21910", "2125", "19973", "19699", "19698", "19262", "19028",
    #                "19027", "19026", "19025", "1890", "18654", "18653", "18652", "18573", "1849", "18461",
    #                "17106", "16224", "15572", "15429", "15308", "15133", "15060", "15058", "15057", "15056",
    #                "14551", "14407", "14406", "14405", "14311", "14210", "14153", "14040", "13671", "13670",
    #                "13669", "13668", "13667", "13666", "13665", "13664", "13663", "13662", "13661", "13562",
    #                "12702", "12585", "12367", "12234", "12199", "12079", "11486", "11371", "11303", "11149",
    #                "11148", "11147", "11146", "11145", "11113", "10805", "10784", "10720", "10719", "10027 ",
    #                "6939", "6427", "393338", "20341",
    #                "97", "93", "7019", "6944", "685", "62609", "53550", "46108", "396071", "3949", "3948",
    #                "3947", "3946", "3945", "3942", "3941", "3940", "3939", "3938", "3937", "3936", "393536",
    #                "3934", "3844", "37923", "37900", "3745", "35953", "3150", "2914", "280", "275", "27023",
    #                "263", "262", "253", "23461", "21576", "20110", "19810", "19809", "19808", "19807", "19806",
    #                "19805", "19804", "19803", "18491", "18490", "18489", "18488", "18487", "18486", "18485",
    #                "18484", "17307", "13500", "1294", "1225", "114", "11158", "11018", "10848", "10743",
    #                "6453", "6421",
    #                "8218", "6461", "4997", "36841", "33321", "32327", "31993", "31933", "31932", "31555",
    #                "31367", "27540", "22969", "19158", "19092", "17025", "16503", "13555", "11359",
    #                "9057", "7991", "7990", "7989", "7988", "7987", "7986", "7776", "7359", "7191", "7161",
    #                "6745", "6640", "6367", "6347", "6227", "6226", "6225", "6224", "6223", "6222", "6100",
    #                "5778", "5737", "5668", "4911", "4298", "4297", "4296", "4295", "4294", "4293", "4292",
    #                "4291", "4290", "4289", "4288", "4287", "4285", "4284", "4283", "4282", "4281", "4212",
    #                "4048", "4015", "3951", "394190", "394179", "394125", "394120", "393789", "393645", "3910",
    #                "3909", "3908", "3561", "3447", "32855", "27497", "2379", "23126", "22561", "22186", "209",
    #                "202818", "18494", "17402", "17047", "16941", "16835", "16718", "14921", "14910", "14905", "13787",
    #                "11538", "11530", "11415", "11412", "11398", "11226", "11225", "11104", "10960", "10833", "10832",
    #                "10831", "10830", "10829", "10828", "10827", "10826", "10825", "10424", "10383",
    #                "7262", "6279", "3491", "26957", "25178",
    #                "3356", "3549", "7018",
    #                "11537", "7843", "46887", "7029", "11164", "22773", "13786", "20115", "23520", "6128", "32787",
    #                "20473", "54004",
    #                "11404", "10796", "1820", "33491", "3908", "7385", "7015", "32098", "5650", "29791", "3561",
    #                "33651", "3910", "23005",
    #                "11427", "13536", "33667", "13789", "2381", "721", "20001", "33132", "33287", "33657", "13649",
    #                "2686", "55002", "26554",
    #                "7016", "46786", "22822", "62", "27064", "19551", "33668", "11426", "33659", "6079", "18747",
    #                "11351", "33660", "15164",
    #                "13760", "10913", "12182", "33363", "7795", "12129", "15305", "40676", "25899", "19024", "2711",
    #                "2687", "19108", "33597",
    #                "27552", "19151", "7342", "13876", "22911", "6181", "10912", "19271", "11317", "4181", "36236",
    #                "36086", "5056", "7725",
    #                "12179", "600", "11796", "16905", "14265", "12042", "306"]
    # us_as_group = ["3356", "1239", "701", "174", "6939",
    #                "6453", "2914", "6461", "7018", "7922",
    #                "3491", "3549", "2828", "703"]
    us_as_group = gain_u_as_group()
    my_rib_file = "../000LocalData/as_simulate/Chinaunicom RIB.txt"
    chinaunicom_rib_analysis(my_rib_file, us_as_group)
    time_end = time.time()  # 记录结束时间
    print("\nScripts Finish, Time Consuming:", (time_end - time_start), "S")


