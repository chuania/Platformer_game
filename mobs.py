"""Реализация моба. Характеристики и анимация"""

import os
import pygame as pg
from pygame import Color
import pyganim


game_dir = os.path.dirname(os.path.abspath(__file__))
ANIMATION_SPEED = 0.2
COLOR = "#888888"

MAN = [
    (f"{game_dir}/png/man1.png"),
    (f"{game_dir}/png/man2.png"),
    (f"{game_dir}/png/man3.png"),
]


class Man(pg.sprite.Sprite):
    """Класс мужчина"""

    def __init__(self, x, y, sprite_group, list_group):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pg.image.load(f"{game_dir}/png/man1.png").convert_alpha()
        self.rect = pg.Rect((self.x - 10, self.y, 15, 90))
        self.add(sprite_group)
        list_group.append(self)
        self.image.set_colorkey(Color(COLOR))

        animation_m = []
        for anim in MAN:
            animation_m.append((anim, ANIMATION_SPEED))
            self.animation_man = pyganim.PygAnimation(animation_m)
            self.animation_man.play()

    def update(self):
        """Показ анимации"""
        self.image.fill(Color(COLOR))
        self.animation_man.blit(self.image, (0, 0))
