'''Собственно реализация игры, где персонаж прыгает по оставкам 
    и прыгает через парней-мобов в надежде добраться до финала'''
import pygame as pg
from pygame import sprite, rect, Rect, Color
import sys
import os
import pyganim
from platforms import Island_0, Island_1, Island_2, Brige, Big_island
from player import Player
from mobs import Man

game_dir = os.path.dirname(os.path.abspath(__file__))
COLOR = "#888888"

# анимация боя
COMBAT = [(f'{game_dir}\\png\\Sprite_combat1.png'),
            (f'{game_dir}\\png\\Sprite_combat2.png'),
            (f'{game_dir}\\png\\Sprite_combat3.png'),
            (f'{game_dir}\\png\\Sprite_combat4.png')]


# class Camera():
#     '''Класс "Камера". Это игровой экран(прямоугольник), в центре которого
#         на протяжении игры будет персонаж.'''
#     def __init__(self, camera_func, width: int, height = 400):
#         '''Высота равна высоте нашего игрового экрана всегда'''
#         # функция конфигурирования прямоугольника камеры вокруг персонажа
#         self.camera_func = camera_func
#         # прямоугольник всего уровня, уровень гораздо больше чем игровой экран
#         self.state = Rect(0, 0, width, height)

#     def apply(self, target: sprite):
#         '''Занимается пердвижением объектов уровня. Будет определяться 
#             положние прямоугольника камеры(этим занимается функция update()),
#             и только потом, относительно этого прямоугольника будут пердвигаться
#             остальные предметы(target). x самих предметов не меняется,
#             просто объект рисуется с измененными координатами'''
#         return target.rect.move(self.state.topleft)

#     def update(self, target: Player):
#         '''Та самая функция конфигурирования. Конфигурируется относительно главного героя.'''
#         self.state = self.camera_func(self.state, target.rect)



# def camera_configure(camera: rect, target_rect: rect) -> rect:
#     '''Camera - прямоугольник уровня, target_rect - прямоугольник, по которому будет определяться
#         положение камеры(это наш персонаж).'''
#     # l это x координата персонажа, она влияет на положение камеры
#     # - меняется она -> меняется положение камеры
#     l, _, _, _ = target_rect
#     t = 0 # y камеры = 0, так как смещений камеры по y у нас не будет
#     _, _, w, h = camera # ширину и высоту берем из прямоугольника всего уровня
#     # координата x камеры равна -x персонажа + 600/2,
#     # то есть когда персонаж на середине игрового экрана, камера двигается
#     l = -l +600/2

#     l = min(0, l)# не движемся дальше левой границы
#     l = max(-(camera.width-600), l)# не движемся дальше правой границы
#     return Rect(l, t, w, h)

class Game():
    def __init__(self):
        self.all_sprites = pg.sprite.Group()
        self.platforms = []
        self.men_mobs = []
        self.GAME_OVER = pg.image.load(f'{game_dir}\\png\\Sprite_game_over.png').convert_alpha()
        self.game_over = False # флаг проигрыша
        self.WIN = pg.image.load(f'{game_dir}\\png\\Sprite_win1.png').convert_alpha()
        self.win = False # флаг выигрыша

    class Combat(pg.sprite.Sprite):
        '''Класс бой, который происходит при пересечении персонажа и парня-моба'''
        def __init__(self, sprite_group):
            pg.sprite.Sprite.__init__(self)
            self.x = 0
            self.y = 230
            self.image = pg.image.load(f'{game_dir}\\png\\Sprite_combat1.png').convert_alpha()
            self.image.set_colorkey(Color(COLOR))
            self.rect = Rect((self.x+20, self.y, 100, 100))
            self.add(sprite_group)
            self.combat_number = 0 # номер картинки боя
            self.num = 0 # число флаг для выпонения условия один раз

            animation = [] #реализация анимации с помощью pyganim
            for anim in COMBAT:
                animation.append((anim, 0.3))
                self.animation_combat = pyganim.PygAnimation(animation)
                self.animation_combat.play()

        def play_combat(self, player):
            '''Вывод анимации боя'''
            if player.collision_man: # выводим анимацию боя с помощью pyganim
                self.image.fill(Color(COLOR))
                if self.num == 0:# условие выолняется один раз
                    self.rect.x = player.rect.x # координата х картинки боя = x персонажа
                    self.num += 1
                    player.loss = True # персонаж проиграл
                if self.combat_number <= 59: #бесконечная анимации боя
                    self.animation_combat.blitFrameNum(self.combat_number//15, self.image, (0, 0))
                    self.combat_number += 1
                else:
                    self.combat_number = 0
                    self.animation_combat.blitFrameNum(self.combat_number//15, self.image, (0, 0))
    class Camera():
        '''Класс "Камера". Это игровой экран(прямоугольник), в центре которого
            на протяжении игры будет персонаж.'''
        def __init__(self, camera_func, width: int, height = 400):
            '''Высота равна высоте нашего игрового экрана всегда'''
            # функция конфигурирования прямоугольника камеры вокруг персонажа
            self.camera_func = camera_func
            # прямоугольник всего уровня, уровень гораздо больше чем игровой экран
            self.state = Rect(0, 0, width, height)

        def apply(self, target: sprite):
            '''Занимается пердвижением объектов уровня. Будет определяться 
                положние прямоугольника камеры(этим занимается функция update()),
                и только потом, относительно этого прямоугольника будут пердвигаться
                остальные предметы(target). x самих предметов не меняется,
                просто объект рисуется с измененными координатами'''
            return target.rect.move(self.state.topleft)

        def update(self, target: Player):
            '''Та самая функция конфигурирования. Конфигурируется относительно главного героя.'''
            self.state = self.camera_func(self.state, target.rect)
    def camera_configure(camera: rect, target_rect: rect) -> rect:
        '''Camera - прямоугольник уровня, target_rect - прямоугольник, по которому будет определяться
            положение камеры(это наш персонаж).'''
        # l это x координата персонажа, она влияет на положение камеры
        # - меняется она -> меняется положение камеры
        l, _, _, _ = target_rect
        t = 0 # y камеры = 0, так как смещений камеры по y у нас не будет
        _, _, w, h = camera # ширину и высоту берем из прямоугольника всего уровня
        # координата x камеры равна -x персонажа + 600/2,
        # то есть когда персонаж на середине игрового экрана, камера двигается
        l = -l +600/2

        l = min(0, l)# не движемся дальше левой границы
        l = max(-(camera.width-600), l)# не движемся дальше правой границы
        return Rect(l, t, w, h)
def main():
    '''Функция реализует игру'''
    pg.init()
    screen = pg.display.set_mode((600, 400))
    pg.display.set_caption('Woman')
    icon = pg.image.load(f'{game_dir}\\png\\icon.png.png') # иконка нашей игры
    pg.display.set_icon(icon)
    back = pg.image.load(f'{game_dir}\\png\\Sprite_back22.png') # задний фон нашей игры
    game = Game()

    # группа всех спратов игры, нужны для отрисовки уровня игры
    # all_sprites = pg.sprite.Group()
    # список спрайтов-платформ, нужен для проверки позиции персонажа на платформе
    # platforms = []
    # список спрайтов-парней, нужен для проверки пересечения персонажа с парнем-мобом
    # men_mobs = []

    # цифры, показывающие кол-во жизней персонажа на экране
    DIGITS = [pg.image.load(f'{game_dir}\\png\\Sprite_digit1.png').convert_alpha(),
            pg.image.load(f'{game_dir}\\png\\Sprite_digit2.png').convert_alpha(),
            pg.image.load(f'{game_dir}\\png\\Sprite_digit3.png').convert_alpha(),
            pg.image.load(f'{game_dir}\\png\\Sprite_digit4.png').convert_alpha(),
            pg.image.load(f'{game_dir}\\png\\Sprite_digit4.png').convert_alpha()]

    # анимация разбитого сердца при потере жизни
    HEART = [ pg.image.load(f'{game_dir}\\png\\Sprite_heart11.png').convert_alpha(),
            pg.image.load(f'{game_dir}\\png\\Sprite_heart12.png').convert_alpha(),
            pg.image.load(f'{game_dir}\\png\\Sprite_heart13.png').convert_alpha(),
            pg.image.load(f'{game_dir}\\png\\Sprite_heart14.png').convert_alpha()]
    count_heart = 0 # номер картинки разбитого сердца

    # картинка проигрыша
    # GAME_OVER = pg.image.load(f'{game_dir}\\png\\Sprite_game_over.png').convert_alpha()
    # game_over = False # флаг проигрыша
    # картинка выигрыша
    # WIN = pg.image.load(f'{game_dir}\\png\\Sprite_win1.png').convert_alpha()
    # win = False # флаг выигрыша

    clock = pg.time.Clock()
    platforms_map = '_ < _. < _  * , _  <  .  _  _  _' # карта платформ уровня
    platforms_x = 0
    platforms_y = 330
    man_y = 241 # y моба-мужчины
    len_level = 0 # длина уровня

    # создание объектов игры, определенный знак - определенная платформа
    for symbol in platforms_map:
        if symbol == '_':
            platform = Island_0(platforms_x,platforms_y,game.all_sprites,game.platforms)
            len_level += platform.rect.width + 70
            platforms_x += platform.rect.width + 70
        if symbol == '.':
            platform = Island_1(platforms_x,platforms_y,game.all_sprites,game.platforms)
            len_level += platform.rect.width + 70
            platforms_x += platform.rect.width + 70
        if symbol == ',':
            platform = Island_2(platforms_x,platforms_y,game.all_sprites,game.platforms)
            len_level += platform.rect.width + 70
            platforms_x += platform.rect.width + 70
        if symbol == '*':
            platform = Brige(platforms_x,platforms_y-50,game.all_sprites,game.platforms)
            len_level += platform.rect.width + 70
            platforms_x += platform.rect.width + 70
        if symbol == '<':
            platform = Big_island(platforms_x,platforms_y-5,game.all_sprites,game.platforms)
            # на середине острова размещаем парня-моба
            man = Man(platform.rect.x + platform.rect.width//2, man_y, game.all_sprites, game.men_mobs)
            len_level += platform.rect.width + 70
            platforms_x += platform.rect.width + 70

    player = Player(game.all_sprites) # создаем персонажа
    camera = Game.Camera(Game.camera_configure, len_level) # создаем камеру
    combat = Game.Combat(game.all_sprites) # создаем класс боя
    while True:

        clock.tick(100)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.flip()
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]: # если нажимаем клавишу левая стрелка, то персонаж идет влево
            player.left = True
        else:
            player.left =False # если клавиша не нажата, то нет движения

        if keys[pg.K_RIGHT]: # если нажимаем клавишу правая стрелка, то персонаж идет вправо
            player.right = True
        else:
            player.right =False # если клавиша не нажата, то нет движения

        # если нажимаем клавишу пробел или стрелка вверх, то персонаж прыгает
        if keys[pg.K_SPACE] or keys[pg.K_UP]:
            player.up = True
            if keys[pg.K_RIGHT]:
                # если еще нажата клавиша вправо, то персонаж прыгает вправо
                player.right_jump = True
            elif keys[pg.K_LEFT]:
                #если еще нажата клавиша влево, то персонаж прыгает влево
                player.left_jump = True

        screen.blit(back, (0,0)) # рисуем фон

        camera.update(player) # центрируем комеру вокруг персонажа

        # если нет проигрыша или выигрыша, игра для персонажа продолжается
        if not (game.game_over or game.win):
            player.update(game.platforms, len_level) # обновляем движение персонажа
            player.collide_man(game.men_mobs) # проверяем на столкновение с мужчиной

        # обновляем движения парня-моба, его движение продолжается вне зависимости от статуса игры
        [mob.update() for mob in game.men_mobs]

        combat.play_combat(player)

        for s in game.all_sprites: #выводим на экран все спрайты игры если:
            if not player.collision_man: #если нет пересечения с парнем-мобом
                if type(s) != Game.Combat: #спрайт боя не выводим
                    screen.blit(s.image, camera.apply(s))
            else: # если произошло пересечение с парнем-мобом, выводим все, кроме
                # кроме парней-мобов, т.к. их анимация меняется на анимацию боя
                if s not in game.men_mobs:
                    # кроме анимации самого персонажа по уже вышеуказанной причине
                    if type(s) != Player:
                        screen.blit(s.image, camera.apply(s))

        # когда пересекам парня-моба или теряем жизнь
        if player.collision_man or player.loss_live:
            if count_heart <= 59: # показывается анимация разбитого сердца
                screen.blit(HEART[count_heart//15], (560, 0))
                count_heart += 1
            elif player.loss: # если проигрыш, то выводим соответствующую картинку
                game_over = True
                screen.blit(game.GAME_OVER, (50,50))
            else: # если у персонажа еще есть жизни, то игра продолжается
                player.loss_live = False
                count_heart = 0
                player.stop_move = False # игрок продолжает движение

        # если персонаж дошел до конца, то он выиграл, выводится соответствующая картинка
        elif player.rect.x > platform.rect.x + 40:
            screen.blit(game.WIN, (50,50))
            win = True
        else: # если нет коллизий с водой или мобом, то на экране выведены сердце и число жизней
            screen.blit(HEART[0], (560, 0))
            screen.blit(DIGITS[player.lives - 1], (540, 7))

        pg.display.update()

if __name__ =='__main__':
    main()
