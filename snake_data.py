# ------------------------------------ #
# LEVEL AND CONSTANT DATA FOR SNAKE 42 #
# ------------------------------------ #
# field is
#
#
#
#

import os
import pygame as pg
from random import randint
from pygame.locals import *

# Colors
GREEN = (13, 89, 28)
LIGHTGREEN = (34, 177, 76)
ORANGE = (255, 127, 39)
GREY = (160, 163, 165)
YELLOW = (229, 212, 57)
RED = (239, 14, 14)
BLUE = (72, 92, 242)
BLACK = (0, 0, 0)

pg.init()

# Images and sounds
os.chdir("media")
BACK = pg.image.load('back.png')  # black 20x20 square, used for resetting
FOOD = pg.image.load('food.png')
SUPERFOOD = pg.image.load('SUPERFOOD.png')
GREEN_SNAKE = pg.image.load('snake1.png')
ORANGE_SNAKE = pg.image.load('snake2.png')
BRICK = pg.image.load('BRICK.png')
SMALL_FONT = pg.font.Font('kindergarten.ttf', 20)
FONT = pg.font.Font('kindergarten.ttf', 32)
TITLE_FONT = pg.font.Font('kindergarten.ttf', 50)
CHOMP = pg.mixer.Sound('CHOMP.wav')
VICTORY = pg.mixer.Sound('VICTORY.wav')
MUSIC = pg.mixer.Sound('MUSIC.wav')
UGH = pg.mixer.Sound('UGH.wav')
MUSIC.set_volume(0.45)
os.chdir("..")

# Rects
START_BOX = Rect(250, 200, 100, 35)
NAME_BOX = Rect(250, 300, 100, 40)
GREEN_SNAKE_BOX = Rect(260, 400, 30, 30)
ORANGE_SNAKE_BOX = Rect(310, 400, 30, 30)
MUSIC_BOX = Rect(226, 470, 152, 35)

levels = []


def random_level(n):
    """ Creates a level with n randomly placed walls """
    level = []
    while len(level) < n:
        wall = (randint(0, 14) * 40, randint(0, 29) * 20)
        if wall in [(140, 100), (160, 100), (180, 100), (200, 100), (220, 100), (240, 100)]:
            continue
        else:
            level.append(wall)
    return level


# empty field
_0 = []
levels.append(_0)

# horizontal bars in middle
_1 = [(i, 200) for i in range(100, 520, 20)] + [(i, 400) for i in range(100, 520, 20)]
levels.append(_1)

# walls around field
_2 = [(i, 0) for i in range(0, 600, 20)] + [(i, 580) for i in range(0, 600, 20)]
_2 += [(0, i) for i in range(0, 600, 20)] + [(580, i) for i in range(0, 600, 20)]
levels.append(_2)

_3 = random_level(20)
levels.append(_3)

_4 = _2 + [(i, 60) for i in range(60, 521, 20)] + [(i, 520) for i in range(60, 521, 20)]
levels.append(_4)

_5 = _4 + [(100, i) for i in range(100, 481, 20)] + [(480, i) for i in range(100, 481, 20)]
levels.append(_5)

_6 = random_level(40)
levels.append(_6)

_7 = []

if __name__ == '__main__':
    for lvl in levels:
        # print(lvl)
        pass
