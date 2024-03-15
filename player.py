import os
import pygame as pg
from pygame import Rect, Color, sprite
import pyganim

COLOR = "#888888"
ANIMATION_SPEED = 0.2  # скорость смены кадров
game_dir = os.path.dirname(os.path.abspath(__file__))

# png игры ⬇

WALK = [
    (f"{game_dir}/png/person1.png"),  # персонаж идет
    (f"{game_dir}/png/person2.png"),
    (f"{game_dir}/png/person3.png"),
    (f"{game_dir}/png/person4.png"),
    (f"{game_dir}/png/person5.png"),
]

JUMP = [(f"{game_dir}/png/person1.png", ANIMATION_SPEED)]  # прыжок

STAY = [(f"{game_dir}/png/person1.png", ANIMATION_SPEED)]  # персонаж стоит

SINK = [
    (f"{game_dir}/png/Sprite_sink_0.png"),  # персонаж тонет
    (f"{game_dir}/png/Sprite_sink_1.png"),
    (f"{game_dir}/png/Sprite_sink_2.png"),
    (f"{game_dir}/png/Sprite_sink_3.png"),
    (f"{game_dir}/png/Sprite_sink_4.png"),
]


class Player(pg.sprite.Sprite):
    """Класс Игрок"""

    def __init__(self, sprite_group):
        pg.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 250
        self.speed = 1  # скорость персонажа
        self.add(sprite_group)  # добавление в группу спрайтов для отрисовки
        self.on_ground = False  # провека положения персонажа на платформе
        self.collision_man = False  # проверка пересечения с мобом
        self.image = pg.image.load(f"{game_dir}/png/person1.png").convert_alpha()
        self.rect = Rect(
            (self.x + 20, self.y, 30, 100)
        )  # прямоугольник персонажа, по которому определяется пересечение
        self.right = False  # идет вправо
        self.left = False  # идет влево
        self.up = False  # прыжок
        self.jump_power = 9  # высота прыжка
        self.right_jump = False  # прыжок вправо
        self.left_jump = False  # прыжок влево
        self.loser = False  # проигрыш
        self.lives = 3  # кол-во жизней
        self.stop_move = False  # остановка движения
        self.state = 0  # координата x сохранения персонажа
        self.lost_life = False  # потеря жизни
        self.image.set_colorkey(Color(COLOR))
        self.sink_num = 0  # номер картинки

        animation_w = []  # анимация хотьбы
        for anim in WALK:
            animation_w.append((anim, ANIMATION_SPEED))
            self.animation_walk = pyganim.PygAnimation(animation_w)
            self.animation_walk.play()

        self.animation_stay = pyganim.PygAnimation(STAY)  # анимация бездействия/стояния
        self.animation_stay.play()

        self.animation_jump = pyganim.PygAnimation(JUMP)  # анимация прыжка
        self.animation_jump.play()

        animation_s = []  # анимация погружения в воду
        for anim in SINK:
            animation_s.append((anim, ANIMATION_SPEED))
            self.animation_sink = pyganim.PygAnimation(animation_s)
            self.animation_sink.play()

    def collide_platform(self, platforms: list):
        """Проверка нахождения персонажа на платформе"""
        for platform in platforms:
            if sprite.collide_rect(self, platform):
                self.on_ground = True  # персонаж на платформе
                self.state = (
                    platform.rect.x
                )  # сохранение персонажа на x коорденате последнего пройденного острова

    def collide_man(self, men: list):
        """Проверка пересечения с мобом"""
        for man in men:
            if sprite.collide_rect(self, man):
                self.collision_man = True  # персонаж пересекает парня-моба
                self.stop_move = True  # персонаж останавливает движение

    def update(self, platforms):
        """Изменение персонажа в прсотранстве"""
        self.collide_platform(platforms)  # персонаж на платформе ?
        if not self.stop_move:  # если движение персонажа не приостановлено,
            # то он может изменять положение в пространстве

            if self.left and self.rect.x >= 20:  # джижение влево
                self.rect.x -= self.speed
                self.image.fill(Color(COLOR))
                self.animation_walk.blit(self.image, (0, 0))

            if self.right:  # движение вправо
                self.rect.x += self.speed
                self.image.fill(Color(COLOR))
                self.animation_walk.blit(self.image, (0, 0))

            if not (self.left or self.right):  # если не двигаемся, то стоим
                self.image.fill(Color(COLOR))
                self.animation_stay.blit(self.image, (0, 0))

            if self.up:  # реализация прыжка
                if self.jump_power >= -9:
                    if self.jump_power > 0:  # вверх
                        self.rect.y -= (self.jump_power**2) // 2
                        self.image.fill(Color(COLOR))
                        self.animation_jump.blit(self.image, (0, 0))
                        if self.right_jump:  # смещение при прыжке вправо
                            self.rect.x += 10
                        elif (
                            self.left_jump and self.rect.x >= 40
                        ):  # смещение при прыжке влево
                            self.rect.x -= 6
                    else:  # опускаем персонажа
                        self.rect.y += (self.jump_power**2) // 2
                        self.image.fill(Color(COLOR))
                        self.animation_jump.blit(self.image, (0, 0))
                    self.jump_power -= 1
                else:
                    self.up = self.left_jump = self.right_jump = False  # прыжок окончен
                    self.jump_power = 9
        if not self.on_ground and not self.up:
            # падение в воду
            if not self.loser:
                self.image.fill(Color(COLOR))
                if self.sink_num == 0:
                    self.rect.y += 20
                    self.stop_move = True
                if self.sink_num <= 59:
                    self.animation_sink.blitFrameNum(
                        self.sink_num // 15, self.image, (0, 0)
                    )
                    self.sink_num += 1
                else:
                    self.lives -= 1
                    self.sink_num = 0
                    self.lost_life = True
                    if self.lives == 0:
                        self.loser = True
                    else:
                        self.rect.x = self.state
                        self.rect.y = 250

        self.on_ground = False  # провека положения персонажа всегда
