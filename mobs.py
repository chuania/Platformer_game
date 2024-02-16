import pygame as pg
import os
from pygame import *
import pyganim

"""Препятствия"""

dir = os.path.dirname(os.path.abspath(__file__))
ANIMATION_SPEED = 0.2
COLOR = "#888888"

MAN = [(f"{dir}/png/Sprite_man_back1", ANIMATION_SPEED)]

MAN_BACK = [
    (f"{dir}/png/Sprite_man_back1.png"),
    (f"{dir}/png/Sprite_man_back2.png"),
    (f"{dir}/png/Sprite_man_back3.png"),
    (f"{dir}/png/Sprite_man_back1.png"),
]

MAN_SIDE = [
    (f"{dir}/png/Sprite_man1.png"),
    (f"{dir}/png/Sprite_man2.png"),
    (f"{dir}/png/Sprite_man3.png"),
]


class Man(pg.sprite.Sprite):
    """Класс мужчина"""

    def __init__(self, x, y, sprite_group, list_group):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pg.image.load(f"{dir}/png/Sprite_man1.png").convert_alpha()
        self.rect = pg.Rect((self.x - 10, self.y, 15, 90))
        self.add(sprite_group)
        list_group.append(self)
        self.image.set_colorkey(Color(COLOR))

        animation_b = []
        for anim in MAN_BACK:
            animation_b.append((anim, ANIMATION_SPEED))
            self.animation_back = pyganim.PygAnimation(animation_b)
            self.animation_back.play()

        animation_s = []
        for anim in MAN_SIDE:
            animation_s.append((anim, ANIMATION_SPEED))
            self.animation_side = pyganim.PygAnimation(animation_s)
            self.animation_side.play()

    def update(self):
        self.image.fill(Color(COLOR))
        self.animation_side.blit(self.image, (0, 0))
