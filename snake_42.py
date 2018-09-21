"""
## -------- ##
## SNAKE 42 ##
## -------- ##
"""

import sys
from random import randint
from pygame.locals import *
from pygame.mixer import *
import pygame as pg
import snake_data as data


def init():
    pg.init()
    pg.mixer.init()
    pg.mouse.set_cursor((8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0))


init()
SCREEN = pg.display.set_mode((600, 630))
STATUS_BAR = Rect(0, 600, 600, 30)

color = GREEN

back = pg.image.load('back.png')  # black 20x20 square, used for resetting
food = pg.image.load('food.png')

play_music = True
food_is_super = False
food_position = (300, 300)
name = 'Snakey'


class Game:
    """ Game class. WoW """

    def __init__(self):
        self.height = 600
        self.width = 600
        self.speed = 6
        self.score = 0
        self.walls = snake_data.levels[0]
        self.playing = True
        pg.mouse.set_visible(True)
        SCREEN.fill(BLACK)

    def main(self):
        """ Main menu loop etc. """

        start_box = Rect(250, 200, 100, 35)
        name_box = Rect(250, 300, 100, 40)
        green_snake_box = Rect(260, 400, 30, 30)
        orange_snake_box = Rect(310, 400, 30, 30)
        music_box = Rect(226, 470, 152, 35)
        active = False
        finished = False
        snake_color = GREEN_SNAKE
        global name, color, play_music

        SCREEN.fill(BLACK)
        draw_text_box('title:SNAKE 42', Rect(300, 70, 0, 0), RED)
        draw_text_box('Start', start_box, RED)
        draw_text_box('small:Enter name', Rect(300, 270, 0, 0), YELLOW)
        draw_text_box('small:Select color', Rect(300, 370, 0, 0), YELLOW)
        pg.draw.rect(SCREEN, LIGHTGREEN, green_snake_box)
        pg.draw.rect(SCREEN, ORANGE, orange_snake_box)

        if play_music:
            draw_text_box('MUSIC off', music_box, RED, GREEN)
        else:
            draw_text_box('MUSIC on', music_box, RED, GREEN)

        # logic and loop for name_box and color choosing
        while not finished:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    if wanna_quit():
                        sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if start_box.collidepoint(event.pos):
                        finished = True
                    elif music_box.collidepoint(event.pos):
                        play_music = not play_music
                        if play_music:
                            MUSIC.play(-1)
                            draw_text_box('MUSIC off', music_box, RED, GREEN)
                        else:
                            MUSIC.stop()
                            draw_text_box('MUSIC on', music_box, RED, GREEN)
                    if name_box.collidepoint(event.pos):
                        active = True
                        color = BLUE
                    else:
                        active = False
                        color = GREEN
                    if green_snake_box.collidepoint(event.pos):
                        snake_color = GREEN_SNAKE
                    elif orange_snake_box.collidepoint(event.pos):
                        snake_color = ORANGE_SNAKE
                if event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        if wanna_quit():
                            sys.exit()
                        else:
                            pg.mouse.set_visible(True)
                    elif active:
                        if event.key == pg.K_RETURN:
                            active = False
                            color = GREEN
                        elif event.key == pg.K_BACKSPACE:
                            name = name[:-1]
                        else:
                            name += event.unicode

            if snake_color == GREEN_SNAKE:
                pg.draw.rect(SCREEN, BLUE, green_snake_box, 2)
                pg.draw.rect(SCREEN, BLACK, orange_snake_box, 2)
            else:
                pg.draw.rect(SCREEN, BLACK, green_snake_box, 2)
                pg.draw.rect(SCREEN, BLUE, orange_snake_box, 2)

            name_width = FONT.size(name)[0]
            # set w and h larger to clear old borders and name
            name_box.w += 5
            name_box.h += 5
            draw_text_box('', name_box, BLACK, BLACK)
            name_box.h -= 5
            # set name_box width to match name_width
            name_box.w = max(100, name_width+15)
            name_box.x = 300 - name_box.w/2
            # draw name in name_box
            draw_text_box(name, name_box, RED, color, 2)

            pg.display.update()
            pg.time.delay(30)

        # animation of menu sliding up
        bottom = 600
        i = 1
        org_screen = SCREEN.copy()
        while bottom > 0:
            SCREEN.blit(org_screen, (0, bottom - 600))
            pg.display.update()
            pg.time.delay(17)
            bottom -= i*i / 2
            i += 1

        SCREEN.fill(BLACK)
        pg.draw.rect(SCREEN, GREY, STATUS_BAR)
        text_surface = SMALL_FONT.render(name, True, RED)
        SCREEN.blit(text_surface, (10, 605))
        draw_text_box('small:0', Rect(580, 600, 0, 0), RED, GREY)
        for wall in self.walls:
            SCREEN.blit(BRICK, wall)

        pg.mouse.set_visible(False)
        return name, snake_color

    def pause(self):
        """ Pauses game when p is pressed during play. Game continues when p is pressed again. """

        org_screen = SCREEN.copy()
        draw_text_box('title:PAUSED', Rect(300, 275, 0, 0), RED)
        pg.display.update()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    if wanna_quit():
                        game.playing = False
                        update_highscores()
                        return True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if wanna_quit():
                            game.playing = False
                            update_highscores()
                            return True
                    elif event.key == K_p:
                        pg.time.delay(100)
                        SCREEN.blit(org_screen, (0, 0))
                        pg.event.get()
                        return
            pg.time.delay(50)

    def place_food(self):
        """ places new food in a random free spot """

        global food_position, food_is_super
        food_is_super = False

        while True: # runs until the random spot is free of snake
            food_position = (randint(0, 29) * 20, randint(0, 29) * 20)
            if food_position not in player.snake + game.walls:
                # 1/20 chance for placed food to be SUPERFOOD
                # which speeds up snake when eaten
                if randint(0, 20) == 0:
                    SCREEN.blit(SUPERFOOD, food_position)
                    food_is_super = True
                else:
                    SCREEN.blit(food, food_position)
                break

    def change_level(self, level):
        """ clears SCREEN, cuts snake, moves it to start and draws new walls. """

        # clear SCREEN
        draw_text_box('', Rect(0, 0, self.width, self.height), YELLOW, BLACK)

        # move snake to start
        player.snake = [(140, 100), (160, 100), (180, 100), (200, 100)]
        for position in player.snake:
            SCREEN.blit(player.img, position)

        # new walls
        self.walls = snake_data.levels[level % len(snake_data.levels)]
        for wall in self.walls:
            SCREEN.blit(BRICK, wall)

        # replace food if it's on new walls or snake
        if food_position in player.snake:
            SCREEN.blit(player.img, food_position)
            self.place_food()
        elif food_position in self.walls:
            SCREEN.blit(BRICK, food_position)
            self.place_food()
        else:
            SCREEN.blit(food, food_position)

        # change level number and update SCREEN
        draw_text_box('small:' + str(player.lvl), Rect(560, 600, 40, 30), RED, GREY)
        pg.display.update()

        # reset snake direction and speed
        self.speed = 6
        player.vx = 20
        player.vy = 0
        pg.time.delay(1000)
        pg.event.get()


class Player:

    def __init__(self, name, snake_color):
        self.name = name
        self.snake = [(140, 100), (160, 100), (180, 100), (200, 100)]
        for position in self.snake:
            SCREEN.blit(snake_color, position)
        self.vx = 20
        self.vy = 0
        self.img = snake_color
        self.lvl = 0
        pg.display.update()

    def move(self):
        """ Processes players actions during game loop """

        score_box = Rect(SMALL_FONT.size(name)[0] + 20, 600, 100, 30)
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                if wanna_quit():
                    game.playing = False
                    update_highscores()
                    return
            if event.type != KEYDOWN:
                continue
            if event.key == K_ESCAPE:
                if wanna_quit():
                    game.playing = False
                    update_highscores()
                    return
            elif event.key == K_p:
                if game.pause():
                    return
            elif event.key == K_UP and self.vy != 20:
                self.vx = 0
                self.vy = -20
                break
            elif event.key == K_RIGHT and self.vx != -20:
                self.vx = 20
                self.vy = 0
                break
            elif event.key == K_DOWN and self.vy != -20:
                self.vx = 0
                self.vy = 20
                break
            elif event.key == K_LEFT and self.vx != 20:
                self.vx = -20
                self.vy = 0
                break

        # next position of snakes head with current direction
        head_position = ((self.snake[-1][0] + self.vx) % game.width,
                         (self.snake[-1][1] + self.vy) % game.height)

        if head_position == food_position:
            CHOMP.play()
            if food_is_super:
                game.speed = 8
            elif game.speed > 6:
                game.speed -= 1
            game.score += 20
            game.place_food()
        elif head_position in self.snake + game.walls:
            UGH.play()
            pg.time.delay(1500)
            game.playing = False
            update_highscores()
            return
        else:
            # removes tail if no food was eaten
            SCREEN.blit(back, player.snake.pop(0))
            if food_is_super:
                SCREEN.blit(SUPERFOOD, food_position)
            else:
                SCREEN.blit(food, food_position)

        self.snake.append(head_position)
        SCREEN.blit(self.img, head_position)

        # draws game.score on STATUS_BAR
        pg.draw.rect(SCREEN, GREY, score_box)
        text_surface = SMALL_FONT.render(str(game.score), True, RED)
        SCREEN.blit(text_surface, (score_box.x, 605))
        pg.display.update()

        if game.score >= (self.lvl + 1) * 200:
            draw_text_box('title:LVL UP!', Rect(300, 275, 0, 0), GREEN)
            pg.display.update()
            VICTORY.play()
            pg.time.delay(2000)
            self.lvl += 1
            game.change_level(self.lvl)


def draw_text_box(text, box, text_color=YELLOW, box_color=GREEN, border=0):
    """ Draws box with horizontally centered text. Top of text at box.y + 5 """

    if text[0:6] == 'title:':
        text_surface = TITLE_FONT.render(text[6:], True, text_color)
    elif text[0:6] == 'small:':
        text_surface = SMALL_FONT.render(text[6:], True, text_color)
    else:
        text_surface = FONT.render(text, True, text_color)

    if box.w > 0 and box.h > 0:
        pg.draw.rect(SCREEN, box_color, box, border)
    SCREEN.blit(text_surface, (box.x + box.w/2 - text_surface.get_width()/2, box.y + 4))


def wanna_quit():
    """ Runs when esc or pg.QUIT activated. """

    # draw quitting box in middle of screen
    pg.mouse.set_visible(True)
    org_screen = SCREEN.copy()
    back_box = Rect(200, 200, 200, 160)
    quit_box = Rect(250, 260, 100, 35)
    continue_box = Rect(250, 305, 100, 35)
    draw_text_box('Wanna quit?', back_box, YELLOW, BLUE)
    draw_text_box('Yes', quit_box)
    draw_text_box('No', continue_box)
    pg.display.update()

    # runs until player chooses Yes or No
    while True:
        for event in pg.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if quit_box.collidepoint(event.pos):
                    return True
                elif continue_box.collidepoint(event.pos):
                    SCREEN.blit(org_screen, (0, 0))
                    pg.display.update()
                    pg.mouse.set_visible(False)
                    return False
        pg.time.delay(25)


def update_highscores():
    """ Updates and keeps record of 10 highest scores. """

    with open('highscores.txt', 'r') as file:
        score_data = file.read().split('\n')
    for i in range(10):
        score_data[i] = score_data[i].split('- -')
    i = 0
    while game.score <= int(score_data[i][1]):
        i += 1
        if i == 10:
            break
    score_data.insert(i, [player.name, str(game.score)])
    with open('highscores.txt', 'w') as file:
        for line in score_data[:10]:
            file.write('- -'.join(line) + '\n')


if __name__ == '__main__':
    MUSIC.play(-1)
    while True:
        game = Game()
        player = Player(*game.main())
        pg.time.delay(500)
        while game.playing:
            player.move()
            # delay dictates game speed
            pg.time.delay(int(25 * (11 - game.speed)))
