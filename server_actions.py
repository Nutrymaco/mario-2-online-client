import json
import time
from threading import Thread

import websocket

from utils import cur_time_in_millis


class PositionHolder:
    def __init__(self, json):
        self.json = json

    def get_pos(self):
        return self.json


class ServerClient:
    def __init__(self, player_name, host):
        self.player_name = player_name
        self.player_pos_dict = dict()
        self.wsapp = websocket.WebSocketApp(f"ws://{host}/socket/{player_name}", on_message=self._message_reader)
        self.ws = websocket.WebSocket()
        self.ws.connect(f"ws://{host}/socket/{player_name}")
        self.thread = Thread(target=self.wsapp.run_forever)
        self.block_disable_start = 0
        self.block_disable_end = 0
        self.last_pos_x = None
        self.last_pos_y = None

    def start(self):
        self.thread.start()

    def stop(self):
        self.wsapp.close()
        self.ws.close()
        self.thread.join()

    def get_last_pos(self, player_name):
        return self.player_pos_dict.get(player_name, None)

    def get_all_players_name(self):
        return self.player_pos_dict.keys()

    def _message_reader(self, wsapp, raw_msg):
        print("get message " + raw_msg)
        msg = json.loads(raw_msg)
        if msg["type"] == "POSITION":
            position = msg["data"]
            print("load pos : " + raw_msg + " for " + msg["playerName"])
            self.player_pos_dict[msg["playerName"]] = position
        elif msg["type"] == "DISABLE_BLOCK":
            print("get disable action")
            print(msg)
            if msg["playerName"] != self.player_name:
                self.block_disable_start = msg["data"]["start"]
                self.block_disable_end = self.block_disable_start + msg["data"]["duration"]

    def send_position(self, x, y):
        if self.last_pos_x is not None and self.last_pos_x == x and self.last_pos_y == y:
            return
        self.last_pos_x = x
        self.last_pos_y = y
        self.ws.send(format("{\"type\": \"POSITION\", \"timestamp\": \"" + str(cur_time_in_millis()) + "\", \"data\": {\"x\" : " + str(x) + ", \"y\" : " + str(y) + "}}"))

    def send_disable_block_action(self):
        self.ws.send(json.dumps({
            "type": "DISABLE_BLOCK",
            "timestamp" : str(cur_time_in_millis()),
            "playerName": self.player_name
        }))
