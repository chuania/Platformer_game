"""Реализация платформ, по которым ходит персонаж"""

import os
import pygame as pg
from pygame import Rect


game_dir = os.path.dirname(os.path.abspath(__file__))


class Island1(pg.sprite.Sprite):
    """Первый остров"""

    def __init__(self, x, y, sprite_group, list_group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"{game_dir}/png/island1.png").convert_alpha()
        self.x = x
        self.y = y
        self.rect = Rect((self.x + 20, self.y, 80, 40))
        self.add(sprite_group)
        list_group.append(self)


class Island2(pg.sprite.Sprite):
    """Второй остров"""

    def __init__(self, x, y, sprite_group, list_group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"{game_dir}/png/island2.png").convert_alpha()
        self.x = x
        self.y = y
        self.rect = Rect(self.x + 15, self.y, 80, 40)
        self.add(sprite_group)
        list_group.append(self)


class Island3(pg.sprite.Sprite):
    """Третий остров"""

    def __init__(self, x, y, sprite_group, list_group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"{game_dir}/png/island3.png").convert_alpha()
        self.x = x
        self.y = y
        self.rect = Rect(self.x + 15, self.y, 80, 40)
        self.add(sprite_group)
        list_group.append(self)


class Brige(pg.sprite.Sprite):
    """Мост"""

    def __init__(self, x, y, sprite_group, list_group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"{game_dir}/png/brige.png").convert_alpha()
        self.x = x
        self.y = y
        self.rect = pg.Rect(self.x + 5, self.y, 350, 80)
        self.add(sprite_group)
        list_group.append(self)


class Bigisland(pg.sprite.Sprite):
    """Большой остров"""

    def __init__(self, x, y, sprite_group, list_group):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(f"{game_dir}/png/big_island.png").convert_alpha()
        self.x = x
        self.y = y
        self.rect = pg.Rect((self.x + 20, self.y, 220, 40))
        self.add(sprite_group)
        list_group.append(self)
