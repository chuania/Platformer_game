import sys
import os
import pygame as pg
from pygame import sprite, rect, Rect, Color
import pyganim
from platforms import Island1, Island2, Island3, Brige, Bigisland
from player import Player
from mobs import Man

game_dir = os.path.dirname(os.path.abspath(__file__))
COLOR = "#888888"

# трали-вали

COMBAT = [
    (f"{game_dir}/png/combat1.png"),
    (f"{game_dir}/png/combat2.png"),
    (f"{game_dir}/png/combat3.png"),
    (f"{game_dir}/png/combat4.png"),
]


class Camera:
    """Класс "Камера". Это игровой экран(прямоугольник), в центре которого
    на протяжении игры будет персонаж"""

    def __init__(self, camera_func, width: int, height=400):
        """Высота равна высоте нашего игрового экрана всегда"""
        # функция конфигурирования прямоугольника камеры вокруг персонажа
        self.camera_func = camera_func
        # прямоугольник всего уровня
        self.state = Rect(0, 0, width, height)

    def apply(self, target: sprite):
        """Занимается пердвижением объектов уровня. Будет определяться
        положние прямоугольника камеры(update()),
        и только потом, относительно этого прямоугольника будут пердвигаться
        остальные предметы(target). x самих предметов не меняется,
        объект рисуется с измененными координатами"""
        return target.rect.move(self.state.topleft)

    def update(self, target: Player):
        """Функция конфигурирования(относительно главного героя)"""
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera: rect, target_rect: rect) -> rect:
    """Camera - прямоугольник уровня, target_rect - прямоугольник, по которому будет определяться
    положение камеры(это наш персонаж)."""
    # l это x координата персонажа, она влияет на положение камеры
    # - меняется она -> меняется положение камеры
    l, _, _, _ = target_rect
    t = 0  # y камеры = 0, так как смещений камеры по y у нас не будет
    _, _, w, h = camera  # ширину и высоту берем из прямоугольника всего уровня
    # координата x камеры равна -x персонажа + 600/2,
    # то есть когда персонаж на середине игрового экрана, камера двигается
    l = -l + 600 / 2

    l = min(0, l)  # не движемся дальше левой границы
    l = max(-(camera.width - 600), l)  # не движемся дальше правой границы
    return Rect(l, t, w, h)


class Combat(pg.sprite.Sprite):
    """Происходит при пересечении персонажа и моба"""

    def __init__(self, sprite_group):
        pg.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 230
        self.image = pg.image.load(f"{game_dir}/png/combat1.png").convert_alpha()
        self.image.set_colorkey(Color(COLOR))
        self.rect = Rect((self.x + 20, self.y, 100, 100))
        self.add(sprite_group)
        self.combat_number = 0  # номер картинки боя

        animation = []  # анимация
        for anim in COMBAT:
            animation.append((anim, 0.3))
            self.animation_combat = pyganim.PygAnimation(animation)
            self.animation_combat.play()

    def check_combat(self, player):
        if player.collision_man:
            player.loser = True

    def play_combat(self, player):
        """Вывод анимации"""
        if player.collision_man:
            self.image.fill(Color(COLOR))
            self.rect.x = player.rect.x  # координата х картинки боя = x персонажа
            if self.combat_number <= 59:  # бесконечная анимация
                self.animation_combat.blitFrameNum(
                    self.combat_number // 15, self.image, (0, 0)
                )
                self.combat_number += 1
            else:
                self.combat_number = 0
                self.animation_combat.blitFrameNum(
                    self.combat_number // 15, self.image, (0, 0)
                )


def main():
    """Начинаем игру"""
    pg.init()
    screen = pg.display.set_mode((600, 400))
    pg.display.set_caption("Woman")
    icon = pg.image.load(f"{game_dir}/png/icon.png")  # иконка
    pg.display.set_icon(icon)
    back = pg.image.load(f"{game_dir}/png/back1.png")  # задний фон

    # группа всех спратов для отрисовки уровня
    all_sprites = pg.sprite.Group()
    # список платформ для проверки позиции персонажа
    platforms = []
    # список парней, для проверки пересечения персонажа с мобом
    men_mobs = []

    # цифры - кол-во жизней персонажа
    digits = [
        pg.image.load(f"{game_dir}/png/digit1.png").convert_alpha(),
        pg.image.load(f"{game_dir}/png/digit2.png").convert_alpha(),
        pg.image.load(f"{game_dir}/png/digit3.png").convert_alpha(),
        pg.image.load(f"{game_dir}/png/digit4.png").convert_alpha(),
        pg.image.load(f"{game_dir}/png/digit4.png").convert_alpha(),
    ]

    # разбитое сердце при потере жизни
    heart = [
        pg.image.load(f"{game_dir}/png/heart1.png").convert_alpha(),
        pg.image.load(f"{game_dir}/png/heart2.png").convert_alpha(),
        pg.image.load(f"{game_dir}/png/heart3.png").convert_alpha(),
        pg.image.load(f"{game_dir}/png/heart4.png").convert_alpha(),
    ]
    count_heart = 0  # номер разбитого сердца

    # картинка проигрыша
    game_over_pic = pg.image.load(f"{game_dir}/png/game_over.png").convert_alpha()
    # картинка выигрыша
    win_pic = pg.image.load(f"{game_dir}/png/win.png").convert_alpha()
    win = False  # флаг выигрыша
    # finish_flag = pg.image.load(f"{game_dir}/png/flag.png").convert_alpha()

    clock = pg.time.Clock()
    platforms_map = "_ < _. < _  * , ' #_  <  .  _  _  _' "  # карта платформ уровня
    platforms_x = 0
    platforms_y = 330
    man_y = 241  # y моба-мужчины
    len_level = 0  # длина уровня

    # создание объектов игры, определенный знак - определенная платформа
    for symbol in platforms_map:
        if symbol == "_":
            platform = Island1(platforms_x, platforms_y, all_sprites, platforms)
            len_level += platform.rect.width + 70
            platforms_x += platform.rect.width + 70
        if symbol == ".":
            platform = Island2(platforms_x, platforms_y, all_sprites, platforms)
            len_level += platform.rect.width + 70
            platforms_x += platform.rect.width + 70
        if symbol == ",":
            platform = Island3(platforms_x, platforms_y, all_sprites, platforms)
            len_level += platform.rect.width + 70
            platforms_x += platform.rect.width + 70
        if symbol == "*":
            platform = Brige(platforms_x, platforms_y - 50, all_sprites, platforms)
            len_level += platform.rect.width + 70
            platforms_x += platform.rect.width + 70
        if symbol == "<":
            platform = Bigisland(platforms_x, platforms_y - 5, all_sprites, platforms)
            # на середине острова размещаем парня-моба
            Man(
                platform.rect.x + platform.rect.width // 2, man_y, all_sprites, men_mobs
            )
            len_level += platform.rect.width + 70
            platforms_x += platform.rect.width + 70

    player = Player(all_sprites)  # создаем персонажа
    camera = Camera(camera_configure, len_level)  # создаем камеру
    combat = Combat(all_sprites)  # создаем класс боя

    while True:

        clock.tick(100)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.flip()
        keys = pg.key.get_pressed()
        screen.blit(back, (0, 0))  # рисуем фон

        # функционал клавиш
        # ------------------------------------------------------
        # левая стрелка - персонаж идет влево
        if keys[pg.K_LEFT]:
            player.left = True
        else:
            player.left = False
        # правая стрелка - персонаж идет вправо
        if keys[pg.K_RIGHT]:
            player.right = True
        else:
            player.right = False
        # пробел или стрелка вверх - персонаж прыгает
        if keys[pg.K_SPACE] or keys[pg.K_UP]:
            player.up = True
        # ------------------------------------------------------

        # Проверка событий
        # ******************************************************
        camera.update(player)  # центрируем комеру вокруг персонажа

        # праверка на проигрыш и выигрыш
        if not (player.loser or win):
            player.update(platforms)  # обновляем движение персонажа
            player.collide_man(men_mobs)  # проверяем на столкновение с мобом
            player.dive()  # проверка на погружение
            player.on_ground = False  # провека положения персонажа всегда

        # обновляем движения парня-моба, его движение продолжается вне зависимости от статуса игры
        [mob.update() for mob in men_mobs]

        combat.check_combat(player)  # если есть пересечение с мобом, то вывод комбат
        combat.play_combat(player)

        # вывод на экран спрайтов
        # -------------------------------------------------
        for s in all_sprites:
            if not player.collision_man:
                if not isinstance(s, Combat):
                    screen.blit(
                        s.image, camera.apply(s)
                    )  # спрайт комбат нет выводим без пересечения с мобом
            else:
                if s not in men_mobs:
                    if not isinstance(s, Player):
                        screen.blit(
                            s.image, camera.apply(s)
                        )  # при пересечении выводим все, кроме персонажа и моба
        # error: если на экране два моба, то один из них пропадет при пересечении с другим
        # хочется, чтобы он остался
        # -------------------------------------------------

        # вывод жизней, проигрыша и выигрыша
        if player.lost_life:  # сердце разбивается при потери жизни
            if count_heart <= 59:
                screen.blit(heart[count_heart // 15], (560, 0))
                count_heart += 1
            elif player.loser:  # картинка проигрыша
                screen.blit(game_over_pic, (50, 50))
            else:  # продолжение игры после потери жизни
                player.lost_life = False
                player.stop_move = False
                count_heart = 0
        elif player.rect.x > platform.rect.x + 40:  # персонаж выиграл
            screen.blit(win_pic, (50, 50))
            win = True
        else:  # персонаж в процессе прохождения уровня
            screen.blit(heart[0], (560, 0))
            screen.blit(digits[player.lives - 1], (540, 7))

        # *************************************************

        pg.display.update()


if __name__ == "__main__":
    main()
