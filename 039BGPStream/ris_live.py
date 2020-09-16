# coding:utf-8
"""
create on Apr 10, 2020 By Wenyan YU
Function:

Using the RIS Live WebSocket interface

Require 'websocket-client'

"""
import json
import websocket
import time


def gain_live_data():
    """
    获取实时数据
    :return:
    """
    ws = websocket.WebSocket()
    ws.connect("wss://ris-live.ripe.net/v1/ws/?client=py-example-1")

    params = {
        "moreSpecific": True,
        "host": "rrc03",
        "socketOptions": {
            "includeRaw": True
        }
    }

    ws.send(json.dumps({
        "type": "ris_subscribe",
        "data": params
    }))

    for data in ws:
        parsed = json.loads(data)
        print(parsed["type"], parsed["data"])


if __name__ == "__main__":
    time_start = time.time()
    while True:
        try:
            gain_live_data()
        except Exception as e:
            print(e)
        time_end = time.time()
        print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
