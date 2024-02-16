import os
import pygame as pg
from pygame import *

"""Платформы"""

dir = os.path.dirname(os.path.abspath(__file__))


class Island_0(pg.sprite.Sprite):
    """Класс остров 1"""

    def __init__(self, x, y, sprite_group, list_group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"{dir}/png/Sprite_island0.png").convert_alpha()
        self.x = x
        self.y = y
        self.rect = Rect((self.x + 20, self.y, 80, 40))
        self.add(sprite_group)
        list_group.append(self)


class Island_1(pg.sprite.Sprite):
    """Класс остров 2"""

    def __init__(self, x, y, sprite_group, list_group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"{dir}/png/Sprite_island1.png").convert_alpha()
        self.x = x
        self.y = y
        self.rect = Rect(self.x + 15, self.y, 80, 40)
        self.add(sprite_group)
        list_group.append(self)


class Island_2(pg.sprite.Sprite):
    """Класс остров 3"""

    def __init__(self, x, y, sprite_group, list_group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"{dir}/png/Sprite_island2.png").convert_alpha()
        self.x = x
        self.y = y
        self.rect = Rect(self.x + 15, self.y, 80, 40)
        self.add(sprite_group)
        list_group.append(self)


class Brige(pg.sprite.Sprite):
    """Класс мост"""

    def __init__(self, x, y, sprite_group, list_group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"{dir}/png/Sprite_brige0.png").convert_alpha()
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x + 5, self.y, 350, 80)
        self.add(sprite_group)
        list_group.append(self)


class Big_island(pg.sprite.Sprite):
    """Класс большой остров"""

    def __init__(self, x, y, sprite_group, list_group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"{dir}/png/Sprite_big1.png").convert_alpha()
        self.x = x
        self.y = y
        self.rect = pg.Rect((self.x + 20, self.y, 220, 40))
        self.add(sprite_group)
        list_group.append(self)
