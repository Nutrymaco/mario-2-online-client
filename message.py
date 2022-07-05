from threading import Thread

from utils import cur_time_in_millis


class MessageRepository:
    def __init__(self):
        self.messages = []
        self.clearing_thread = Thread(target=self._clear)

    def push(self, msg):
        self.messages.append(msg)

    def pop_last_message(self):
        if len(self.messages) == 1:
            return self.messages[-1]
        else:
            return self.messages.pop()

    def start_clear_thread(self):
        self.clearing_thread.start()

    def stop(self):
        self.clearing_thread.join()

    def _clear(self):
        for msg in self.messages:
            if cur_time_in_millis() - msg["timestamp"] > 20_000:
                self.messages.remove(msg)
