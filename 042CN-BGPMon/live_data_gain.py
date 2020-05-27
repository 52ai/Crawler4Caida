# coding:utf-8
"""
create on May 27, 2020 By Wenyan YU
Function:

url: https://ris-live.ripe.net/
该程序主要实现对RIPE NCC BGP路由数据采集项目实时数据的获取
目前该项目共有25个采集器

rrc00、rrc01、……、rrc24

由于25个采集点合在一起峰值速率很大，暂不处理这么大规模的数据，后期真正实现的时候再行处理
暂只处理1-3个监测点的数据（当然可以任意采集器）
如果不要求实时，可以直接下载各采集的压缩包，5分钟切割，加上传输和处理时延，10分钟的延迟应该能够Hold住

BGP UPDATE报文样例如下：
ris_message {'timestamp': 1590569894.28, 'peer': '154.11.15.28', 'peer_asn': '852', 'id': '24-154-11-15-28-59041686',
'host': 'rrc24', 'type': 'UPDATE', 'path': [852, 3356, 2914, 20473, 9558], 'origin': 'igp',
'announcements': [{'next_hop': '154.11.15.28', 'prefixes': ['103.209.182.0/24']}]}

"""
import json
import websocket


def gain_rrc_update(aim_rrc):
    """
    根据传入的rrc，实时获取采集器更新的UPDATE报文，Add和withdraw报文
    :param rrc:
    :return:
    """
    ws = websocket.WebSocket()
    ws.connect("wss://ris-live.ripe.net/v1/ws/?client=py-example-1")

    params = {
        "moreSpecific": True,
        "host": aim_rrc,
        "socketOptions": {
            "includeRaw": False
        }
    }
    ws.send(json.dumps({
        "type": "ris_subscribe",
        "data": params
    }))

    message_info_withdraw = []  # 存储撤销的报文信息
    message_info_announcement = []  # 存储通告的报文信息

    for data in ws:
        parsed = json.loads(data)
        # print(parsed["type"], parsed["data"])
        timestamp = parsed["data"]["timestamp"]
        if parsed["data"]["type"] == "UPDATE":
            if "withdrawals" in parsed["data"].keys():
                print("withdraw")
                for item in parsed["data"]["withdrawals"]:
                    message_info_withdraw.append([timestamp, item])
                    print([timestamp, item])
            if "announcements" in parsed["data"].keys():
                print("announcements")
                as_path = parsed["data"]["path"]
                for item in parsed["data"]["announcements"]:
                    message_info_announcement.append([timestamp, item['prefixes'], as_path])
                    print([timestamp, item['prefixes'], as_path])
        else:
            pass


if __name__ == "__main__":
    aim_rrc = "rrc00"
    gain_rrc_update(aim_rrc)
