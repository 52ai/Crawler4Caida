# coding:utf-8
"""
create on Apr 10, 2020 By Wenyan YU
Function:

Using the RIS Live WebSocket interface


"""
import json
import websocket

ws = websocket.WebSocket()
ws.connect("wss://ris-live.ripe.net/v1/ws/?client=py-example-1")

params = {
    "moreSpecific": True,
    "host": "rrc21",
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
