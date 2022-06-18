import random

import requests
from time import sleep

if __name__ == '__main__':
    x = 30
    y = 4512
    while True:
        ans = requests.post("http://localhost:8080/position-messages",
                            data="{"
                                 "  \"x\": " + str(4000 % x) + ","
                                 "  \"y\": " + str(y) + ","
                                 "  \"room_name\": \"test_room\","
                                 "  \"player_name\": \"test_player\""
                                 "}",
                            headers={'Content-Type': 'application/json'}
                            )
        x += 1
        print(ans)
