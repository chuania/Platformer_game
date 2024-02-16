import pygame as pg
import os
from pygame import *
import pyganim

COLOR = "#888888"
ANIMATION_SPEED = 0.2  # скорость смены кадров
dir = os.path.dirname(os.path.abspath(__file__))

WALK = [
    (f"{dir}/png/Sprite_me1.png"),  # анимация хотьбы
    (f"{dir}/png/Sprite_me2.png"),
    (f"{dir}/png/Sprite_me3.png"),
    (f"{dir}/png/Sprite_me4.png"),
    (f"{dir}/png/Sprite_me5.png"),
]

JUMP = [(f"{dir}/png/Sprite_me1.png", ANIMATION_SPEED)]  # анимация прыжка

STAY = [(f"{dir}/png/Sprite_me1.png", ANIMATION_SPEED)]  # анимация персонаж стоит

SINK = [
    (f"{dir}/png/Sprite_sink_0.png"),  # анимация персонаж тонет
    (f"{dir}/png/Sprite_sink_1.png"),
    (f"{dir}/png/Sprite_sink_2.png"),
    (f"{dir}/png/Sprite_sink_3.png"),
    (f"{dir}/png/Sprite_sink_4.png"),
]
sink_number = 0  # номер картинки


class Player(pg.sprite.Sprite):
    """Класс игрок"""

    def __init__(self, sprite_group):
        pg.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 250
        self.speed = 1  # скорость персонажа
        self.add(sprite_group)  # добавление в группу спрайтов для отрисовки
        self.on_ground = False  # флаг провеки положения персонажа: на платформе или нет
        self.collision_man = False  # флаг проверки пересечения с мобом
        self.image = pg.image.load(f"{dir}/png/Sprite_me1.png").convert_alpha()
        self.rect = Rect(
            (self.x + 20, self.y, 30, 100)
        )  # прямоугольник персонажа, по которому определяется столкновение с другими предметами
        self.right = False
        self.left = False
        self.up = False  # флаг прыжка
        self.jump_power = 9  # высота прыжка
        self.right_jump = False  # флаг прыжка вправо
        self.left_jump = False  # флаг прыжка вправо
        self.loss = False  # флаг проигрыша
        self.lives = 3  # кол-во жизней
        self.stop_move = False  # флаг остановки движения
        self.state = 0  # координата x сохранения персонажа
        self.loss_live = False  # флаг потери жизни
        self.image.set_colorkey(Color(COLOR))

        animation = []  # реализации анимации хотьбы с помощью pyganim
        for anim in WALK:
            animation.append((anim, ANIMATION_SPEED))
            self.animation_walk = pyganim.PygAnimation(animation)
            self.animation_walk.play()

        self.animation_stay = pyganim.PygAnimation(
            STAY
        )  # реализация анимации персонаж стоит pyganim
        self.animation_stay.play()

        self.animation_jump = pyganim.PygAnimation(
            JUMP
        )  # реализация анимации прыжка pyganim
        self.animation_jump.play()

        animation_s = []  # реализация анимации персонаж тонет pyganim
        for anim in SINK:
            animation_s.append((anim, 0.3))
            self.animation_sink = pyganim.PygAnimation(animation_s)
            self.animation_sink.play()

    def collide_platform(self, platforms: list):
        """Проверка, находится ли персонаж на платформе"""
        for platform in platforms:
            if sprite.collide_rect(self, platform):
                self.on_ground = True  # персонаж на платформе
                self.state = (
                    platform.rect.x
                )  # сохранение персонажа на x коорденате последнего пройденного островка

    def collide_man(self, men: list):
        """Проверка, пересекается ли персонаж с парнем-мобом"""
        for man in men:
            if sprite.collide_rect(self, man):
                self.collision_man = True  # персонаж пересекает парня-моба
                self.stop_move = True  # персонаж останавливает движение

    def update(self, platforms, len_level):  # метод изменения персонажа в пространстве
        self.collide_platform(platforms)  # проверка нахождения персонажа на платформе
        global sink_number
        if (
            not self.stop_move
        ):  # если движение персонажа не приостановлено, то он может изменять положение в пространстве
            if self.left:  # реализация движения влево
                if self.rect.x >= 20:  # не может уйти влево меньше 20
                    self.rect.x -= self.speed
                    self.image.fill(Color(COLOR))
                    self.animation_walk.blit(self.image, (0, 0))
            if self.right:  # реализация движения вправо
                if (
                    self.rect.x <= len_level - 70
                ):  # до абсолютного конца экране не доходит
                    self.rect.x += self.speed
                    self.image.fill(Color(COLOR))
                    self.animation_walk.blit(self.image, (0, 0))

            if not (self.left or self.right):  # если не двигаемся, то стоим
                self.image.fill(Color(COLOR))
                self.animation_stay.blit(self.image, (0, 0))

            if self.up:  # реализация прыжка
                if self.rect.x <= len_level - 70:
                    if self.jump_power >= -9:
                        if self.jump_power > 0:  # поднимает персонажа
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
                        self.up = self.left_jump = self.right_jump = (
                            False  # прыжок окончен
                        )
                        self.jump_power = 9
        if not self.on_ground and not self.up:
            if not self.loss:
                self.image.fill(Color(COLOR))
                if sink_number == 0:
                    self.rect.y += 20
                    self.stop_move = True
                if sink_number <= 59:
                    self.animation_sink.blitFrameNum(
                        sink_number // 15, self.image, (0, 0)
                    )
                    sink_number += 1
                else:
                    self.lives -= 1
                    sink_number = 0
                    self.loss_live = True
                    if self.lives == 0:
                        self.loss = True
                    else:
                        self.rect.x = self.state
                        self.rect.y = 250

        self.on_ground = False  # мы не знаем, когда наш персонаж на платформе, для этого нужна постоянная проверка
