import json
from threading import Thread

import websocket
from sseclient import SSEClient

HOST = "212.193.49.161:8080"
# HOST = "localhost:8080"


class PositionHolder:
    def __init__(self, json):
        self.json = json

    def get_pos(self):
        return self.json


class PlayersPositionManager:
    def __init__(self, player_name):
        self.player_name = player_name
        self.player_pos_dict = dict()
        self.wsapp = websocket.WebSocketApp(f"ws://{HOST}/position/{player_name}", on_message=self._message_reader)
        self.ws = websocket.WebSocket()
        self.ws.connect(f"ws://{HOST}/position/{player_name}")
        self.thread = Thread(target=self.wsapp.run_forever)

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.join()

    def get_last_pos(self, player_name):
        return self.player_pos_dict.get(player_name, None)

    def get_all_players_name(self):
        return self.player_pos_dict.keys()

    def _message_reader(self, wsapp, message):
        position = json.loads(message)
        print("load pos : " + message + " for " + position["player_name"])
        self.player_pos_dict[position["player_name"]] = position

    def send_position(self, x, y):
        last_pos = self.get_last_pos(self.player_name)
        if last_pos is not None and last_pos["x"] == x and last_pos["y"] == y:
            return
        self.ws.send(format("{\"x\" : " + str(x) + ", \"y\" : " + str(y) + "}"))

