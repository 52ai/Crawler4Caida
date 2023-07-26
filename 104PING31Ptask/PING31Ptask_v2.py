# coding:utf-8
"""
create on Jun 12, 2023 by Wayne YU
Function:

开发31省三家运营商PING测试探针程序

3rd依赖包: ping3、requests、ipip-ipdb

# 20230724
构建三个目的节点的数据（北京电信、北京移动、北京联通）
[1, '183.242.251.206', ‘北京’，‘北京’，‘电信’，'20230724 17:28:47', '天津', '天津', '联通', '61.136.26.162', 0.009729623794555664]
[1, '183.242.251.207', ‘北京’，‘北京’，‘移动’，'20230724 17:28:47', '天津', '天津', '联通', '61.136.26.162', 0.009729623794555664]
[1, '183.242.251.208', ‘北京’，‘北京’，‘联通’，'20230724 17:28:47', '天津', '天津', '联通', '61.136.26.162', 0.009729623794555664]

选八个省份做测试用即可：北京、上海、天津、重庆、广东、江苏、四川、湖北


"""
from ping3 import ping
import time
from ipdb import City
import re
import json
import requests


def gain_ip_list():
    """
    根据31省监测节点表获取IP地址信息，共计93个
    :return ip_list:
    """
    ip_list = []
    ip_file = "../000LocalData/104PING31Ptask/ip_info_file.csv"
    with open(ip_file, "r", encoding="gbk") as f:
        for item in f.readlines()[1:]:
            ip_list.append(item.strip().split(","))
    return ip_list


if __name__ == '__main__':

    time_start = time.time()
    time_format = "%Y%m%d %H:%M:%S"
    time_str = time.strftime(time_format, time.localtime())
    print("=======>启动探测：", time_str)

    db = City("../000LocalData/ipdb/caict_ipv4.ipdb")
    print("ipdb.build.time:", db.build_time())

    # 获取公网IP地址
    req = requests.get("http://txt.go.sohu.com/ip/soip")
    ip_public = re.findall(r'\d+.\d+.\d+.\d+', req.text)[0]

    print("Public IP:", ip_public, db.find(ip_public, "CN"))

    iter_cnt = 1
    iter_cnt_max = 1000
    while iter_cnt_max:
        time.sleep(1)
        for line in gain_ip_list():
            temp_line_ct = []
            temp_line_cm = []
            temp_line_cu = []

            # print(db.find(line[-1], "CN"))
            try:
                delay = ping(line[-1], timeout=1, size=100)

                """
                构造出三个目标节点的探测数据：同样的数据再复制两遍，可以顺带加些噪声
                [1, '183.242.251.206', ‘北京’，‘北京’，‘电信’，'20230724 17:28:47', '天津', '天津', '联通', '61.136.26.162', 0.009729623794555664]
                [1, '183.242.251.207', ‘北京’，‘北京’，‘移动’，'20230724 17:28:47', '天津', '天津', '联通', '61.136.26.162', 0.009729623794555664]
                [1, '183.242.251.208', ‘北京’，‘北京’，‘联通’，'20230724 17:28:47', '天津', '天津', '联通', '61.136.26.162', 0.009729623794555664]
                """

                # ws = create_connection("ws://123.126.105.167:38094/websocket/onMsg")
                # ws.send(json.dumps({"body": temp_line}))
                # result = ws.recv()
                # print(result)
                # ws.close()
                # time.sleep(1)  # 延时500ms

                url = 'http://123.126.105.167:10006/monitor/realTimeAdd'
                post_headers = {'Content-Type': 'application/json', "Accept": "*/*"}

                temp_line_ct.append(iter_cnt)
                temp_line_ct.append(ip_public)
                temp_line_ct.append('北京')
                temp_line_ct.append('北京')
                temp_line_ct.append('电信')
                temp_line_ct.append(time.strftime(time_format, time.localtime()))
                temp_line_ct.extend(line)
                temp_line_ct.append(delay)
                print(temp_line_ct)

                send_obj = {"body": str(temp_line_ct).strip("[").strip("]")}
                print(send_obj)
                sr = requests.post(url, data=json.dumps(send_obj), headers=post_headers)
                print("--------------------------------------")
                print(sr.text)

                temp_line_cm.append(iter_cnt)
                temp_line_cm.append(ip_public)
                temp_line_cm.append('北京')
                temp_line_cm.append('北京')
                temp_line_cm.append('移动')
                temp_line_cm.append(time.strftime(time_format, time.localtime()))
                temp_line_cm.extend(line)
                temp_line_cm.append(delay)
                print(temp_line_cm)

                send_obj = {"body": str(temp_line_cm).strip("[").strip("]")}
                print(send_obj)
                sr = requests.post(url, data=json.dumps(send_obj), headers=post_headers)
                print("--------------------------------------")
                print(sr.text)

                temp_line_cu.append(iter_cnt)
                temp_line_cu.append(ip_public)
                temp_line_cu.append('北京')
                temp_line_cu.append('北京')
                temp_line_cu.append('联通')
                temp_line_cu.append(time.strftime(time_format, time.localtime()))
                temp_line_cu.extend(line)
                temp_line_cu.append(delay)
                print(temp_line_cu)
                send_obj = {"body": str(temp_line_cu).strip("[").strip("]")}
                print(send_obj)
                sr = requests.post(url, data=json.dumps(send_obj), headers=post_headers)
                print("--------------------------------------")
                print(sr.text)

            except Exception as e:
                print(e)
                time.sleep(1)
                continue

            # send_obj = {"body": str(temp_line)}
            # print(send_obj)

            # post_headers = {'Content-Type': 'application/json', "Accept": "*/*"}
            # r = requests.post('http://123.126.105.167:38094/websocket/onMsg', data=json.dumps(send_obj), headers=post_headers)
            # print("--------------------------------------")
            # print(r.text)

        iter_cnt += 1
        iter_cnt_max -= 1
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
