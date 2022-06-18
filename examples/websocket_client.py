import asyncio
import random
import time
from threading import Thread

import websocket
import websockets

ws = websocket.WebSocket()
ws.connect("ws://localhost:8080/position/nutrymaco")
wsapp = websocket.WebSocketApp("ws://localhost:8080/position/nutrymaco", on_message=print)
Thread(target=wsapp.run_forever).start()
while True:
    ws.send("hi + " + str(random.randint(1, 100)))
    time.sleep(1)