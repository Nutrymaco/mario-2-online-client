import pygame

from blocks import *
from generator import get_random_level
from platformer import Camera, camera_configure
from player import *
from position import PlayersPositionManager

WIN_WIDTH = 900  #Ширина создаваемого окна
WIN_HEIGHT = 500  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"



player_name = input("Enter name : ")
pos_manager = PlayersPositionManager(player_name)
other_players = dict()


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Super Mario Boy")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом
    y = 4590
    hero = PlayerSprite(30, 4500)  # создаем героя по (x,y) координатам

    level = get_random_level(y // 32, width=40)

    boost = left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться

    entities.add(hero)

    timer = pygame.time.Clock()
    x = y = 0  # координаты

    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)
    pos_manager.start()
    print("ergerge")
    while True:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                flag = True
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                boost = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                boost = False

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, platforms, boost)  # передвижение
        pos_manager.send_position(hero.rect.x, hero.rect.y)
        update_other_players_info(entities)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()  # обновление и вывод всех изменений на экран


def update_other_players_info(entities):
    for other_player_name in list(pos_manager.get_all_players_name()):
        last_pos = pos_manager.get_last_pos(other_player_name)
        if other_player_name != player_name:
            if other_player_name not in other_players.keys():
                other_player_info = PlayerInfo(other_player_name, PlayerSprite(30, 4500))
                other_players[other_player_name] = other_player_info
                entities.add(other_player_info.sprite)
            other_players[other_player_name].sprite.rect.x = last_pos["x"]
            other_players[other_player_name].sprite.rect.y = last_pos["y"]


if __name__ == "__main__":
    main()
