import json
import websocket

ws = websocket.WebSocket()
ws.connect("wss://ris-live.ripe.net/v1/ws/?client=py-manual-example")
ws.send(json.dumps({"type": "ris_subscribe", "data": {"host": "rrc21", "path": 3356}}))
for data in ws:
    parsed = json.loads(data)
    print(parsed["type"], parsed["data"])
