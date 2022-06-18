import json

from sseclient import SSEClient


def main():
    messages = SSEClient('http://localhost:8080/position-messages?room_name=test_room')
    for msg in messages:
        if len(str(msg)) > 0:
            print("start")
            position = json.loads(msg.data)
            print(position)
            print(position['roomName'])
            print("end")


if __name__ == '__main__':
    main()
