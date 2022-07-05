#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from time import time as py_time

import pygame
import requests

from blocks import Platform
from message import MessageRepository
from player import *
from server_actions import ServerClient
from utils import cur_time_in_millis


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

    
def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


class Game:
    def __init__(self):
        self.player_name = None
        self.room_name = None
        self.level = None
        self.server_client = None
        self.host = None
        self.hero = PlayerSprite(30, 4500)
        self.platforms = []  # то, во что мы будем врезаться или опираться
        self.other_players = dict()
        self.last_disable_block_activating = 0
        self.in_rewind = False
        self.rewind_start = 0
        self.message_repository = MessageRepository()

    def start(self):
        self._get_info_from_user()
        self._register_on_server()
        self._init_graphics()
        self._init_external_resources()
        self._start_graphic()

    def _get_info_from_user(self):
        self.player_name = input("Enter name: ")
        self.room_name = input("Enter room name: ")
        connect_to_server = input("Connect to remote server? (Yes/No) ").lower()
        if connect_to_server == "yes":
            self.host = REMOTE_HOST
        else:
            self.host = LOCAL_HOST

    def _register_on_server(self):
        resp = requests.patch(
            f"http://{self.host}/rooms/{self.room_name}",
            data="{\"name\": \"" + self.player_name + "\"}",
            headers={"Content-Type": "application/json"})\
            .content
        room = json.loads(resp)
        self.level = room["level"]["value"]

    def _init_graphics(self):
        self._init_window()
        # создаем героя по (x,y) координатам
        self.entities = pygame.sprite.Group()  # Все объекты
        self.entities.add(self.hero)
        self._init_level()

        self.timer = pygame.time.Clock()

        self.camera = Camera(camera_configure, self.total_level_width, self.total_level_height)

    def _init_window(self):
        pygame.init()  # Инициация PyGame, обязательная строчка
        self.screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
        pygame.display.set_caption("Super Mario Boy - 2")  # Пишем в шапку
        self.bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
        # будем использовать как фон
        self.bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    def _start_graphic(self):
        boost = left = right = up = False
        is_blocks_transparent = False
        while True:
            self.timer.tick(60)

            if self.server_client.block_disable_start < py_time() * 1000 < self.server_client.block_disable_end:
                self.hero.ignore_blocks = True
                if not is_blocks_transparent:
                    for p in self.platforms:
                        if p.is_switchable:
                            p.image.set_alpha(140)
                    is_blocks_transparent = True
            else:
                self.hero.ignore_blocks = False
                if is_blocks_transparent:
                    for p in self.platforms:
                        if p.is_switchable:
                            p.image.set_alpha(255)
                    is_blocks_transparent = False

            if cur_time_in_millis() - self.rewind_start > 3_000:
                self.in_rewind = False

            for e in pygame.event.get():
                if e.type == QUIT:
                    flag = True
                    self.server_client.stop()
                    self.message_repository.stop()
                    raise SystemExit
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
                if e.type == KEYDOWN and e.key == K_LSHIFT:
                    boost = True
                if e.type == KEYDOWN and e.key == K_RSHIFT and cur_time_in_millis() - self.last_disable_block_activating > 20_000:
                    self.last_disable_block_activating = cur_time_in_millis()
                    self.server_client.send_disable_block_action()
                if e.type == KEYUP and e.key == K_r:
                    self.in_rewind = False
                if e.type == KEYDOWN and e.key == K_r:
                    self.in_rewind = True
                    self.rewind_start = cur_time_in_millis()
                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
                if e.type == KEYUP and e.key == K_LSHIFT:
                    boost = False
                if e.type == KEYUP and e.key == K_BACKSPACE:
                    self.hero.rect.x = 40
                    self.hero.rect.y = 4500

            self.screen.blit(self.bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

            self.camera.update(self.hero)  # центризируем камеру относительно персонажа
            if not self.in_rewind:
                self.hero.update(left, right, up, self.platforms, boost)  # передвижение
                self.message_repository.push({
                    "x": self.hero.rect.x,
                    "y": self.hero.rect.y,
                    "action_type": self.hero.cur_action_type
                })
            else:
                last_pos = self.message_repository.pop_last_message()
                self.hero.rect.x = last_pos["x"]
                self.hero.rect.y = last_pos["y"]
                self.hero.update_by_action_type(last_pos["action_type"])

            self.server_client.send_position(self.hero.rect.x, self.hero.rect.y)
            self._update_other_players_info()
            for e in self.entities:
                self.screen.blit(e.image, self.camera.apply(e))
            pygame.display.update()  # обновление и вывод всех изменений на экран

    def _init_external_resources(self):
        self.server_client = ServerClient(self.player_name, self.host)
        self.server_client.start()
        self.message_repository.start_clear_thread()

    def _init_level(self):
        x = y = 0  # координаты
        for row in self.level:  # вся строка
            for col in row:  # каждый символ
                if col == "-":
                    if y == 4800:
                        pf = Platform(x, y, is_switchable=False)
                    else:
                        pf = Platform(x, y, is_switchable=True)
                    self.entities.add(pf)
                    self.platforms.append(pf)

                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

        self.total_level_width = len(self.level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
        self.total_level_height = len(self.level) * PLATFORM_HEIGHT  # высоту

    def _update_other_players_info(self):
        for other_player_name in list(self.server_client.get_all_players_name()):
            last_pos = self.server_client.get_last_pos(other_player_name)
            if other_player_name != self.player_name:
                if other_player_name not in self.other_players.keys():
                    print("add new player")
                    other_player_info = PlayerInfo(other_player_name, PlayerSprite(30, 4500))
                    self.other_players[other_player_name] = other_player_info
                    self.entities.add(other_player_info.sprite)
                self.other_players[other_player_name].sprite.rect.x = last_pos["x"]
                self.other_players[other_player_name].sprite.rect.y = last_pos["y"]
