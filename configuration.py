import os

WIN_WIDTH = 900  #Ширина создаваемого окна
WIN_HEIGHT = 500  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"

MOVE_SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35 # Сила, которая будет тянуть нас вниз
ANIMATION_DELAY = 0.001 # скорость смены кадров
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

REMOTE_HOST = "212.193.49.161:8080"
LOCAL_HOST = "localhost:8080"