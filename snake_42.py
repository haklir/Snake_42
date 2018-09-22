"""
## -------- ##
## SNAKE 42 ##
## -------- ##
"""
import sys
from random import randint
from pygame.locals import *
import pygame as pg
import snake_data as data


class Game:
    """
    Game class. Contains methods:
     - main(self) -> name, snake_color
     - pause(self) -> Boolean
     - place_food(self) -> None
     - change_level(self, level) -> None
    """

    food_is_super = False
    food_position = (300, 300)
    play_music = True

    def __init__(self):
        self.height = 600
        self.width = 600
        self.speed = 6
        self.score = 0
        self.walls = data.levels[0]
        self.playing = True
        pg.mouse.set_visible(True)
        data.SCREEN.fill(data.BLACK)

    def main(self):
        """ Main menu loop etc. This method is way too large... """

        name = 'Snakey'  # default name
        name_input_color = data.GREEN
        name_input_active = False
        finished = False
        snake_color = data.GREEN_SNAKE

        data.SCREEN.fill(data.BLACK)
        draw_text_box('title:SNAKE 42', Rect(300, 70, 0, 0), data.RED)
        draw_text_box('Start', data.START_BOX, data.RED)
        draw_text_box('small:Enter name', Rect(300, 270, 0, 0))
        draw_text_box('small:Select color', Rect(300, 370, 0, 0))
        pg.draw.rect(data.SCREEN, data.LIGHTGREEN, data.GREEN_SNAKE_BOX)
        pg.draw.rect(data.SCREEN, data.ORANGE, data.ORANGE_SNAKE_BOX)

        music_text = "Music off" if self.play_music else "Music on"
        draw_text_box(music_text, data.MUSIC_BOX, text_color=data.RED)

        # Logic and loop for data.NAME_BOX and color choosing.
        while not finished:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    if wanna_quit():
                        sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if data.START_BOX.collidepoint(event.pos):
                        finished = True
                    elif data.MUSIC_BOX.collidepoint(event.pos):
                        self.play_music = not self.play_music
                        if self.play_music:
                            data.MUSIC.play(-1)
                        else:
                            data.MUSIC.stop()
                        music_text = "Music off" if self.play_music else "Music on"
                        draw_text_box(music_text, data.MUSIC_BOX, text_color=data.RED)
                    if data.NAME_BOX.collidepoint(event.pos):
                        name_input_active = True
                        name_input_color = data.BLUE
                    else:
                        name_input_active = False
                        name_input_color = data.GREEN
                    if data.GREEN_SNAKE_BOX.collidepoint(event.pos):
                        snake_color = data.GREEN_SNAKE
                    elif data.ORANGE_SNAKE_BOX.collidepoint(event.pos):
                        snake_color = data.ORANGE_SNAKE
                if event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        if wanna_quit():
                            sys.exit()
                        else:
                            pg.mouse.set_visible(True)
                    elif name_input_active:
                        if event.key == pg.K_RETURN:
                            name_input_active = False
                            name_input_color = data.GREEN
                        elif event.key == pg.K_BACKSPACE:
                            name = name[:-1]
                        else:
                            name += event.unicode

            # Draw data.BLUE border around chosen snake_color box.
            if snake_color == data.GREEN_SNAKE:
                pg.draw.rect(data.SCREEN, data.BLUE, data.GREEN_SNAKE_BOX, 2)
                pg.draw.rect(data.SCREEN, data.BLACK, data.ORANGE_SNAKE_BOX, 2)
            else:
                pg.draw.rect(data.SCREEN, data.BLACK, data.GREEN_SNAKE_BOX, 2)
                pg.draw.rect(data.SCREEN, data.BLUE, data.ORANGE_SNAKE_BOX, 2)

            name_width = data.FONT.size(name)[0]
            # Set w and h larger to clear old borders and name.
            data.NAME_BOX.w += 5
            data.NAME_BOX.h += 5
            draw_text_box('', data.NAME_BOX, data.BLACK, data.BLACK)
            data.NAME_BOX.h -= 5
            # Set data.NAME_BOX width to match name_width.
            data.NAME_BOX.w = max(100, name_width+15)
            data.NAME_BOX.x = 300 - data.NAME_BOX.w/2
            # Draw name in data.NAME_BOX.
            draw_text_box(name, data.NAME_BOX, data.RED, name_input_color, 2)

            pg.display.update()
            pg.time.delay(30)

        # Animation of menu sliding up.
        bottom = 600
        i = 1
        org_screen = data.SCREEN.copy()
        while bottom > 0:
            data.SCREEN.blit(org_screen, (0, bottom - 600))
            pg.display.update()
            pg.time.delay(17)
            bottom -= i*i / 2
            i += 1

        # Init game field graphics.
        data.SCREEN.fill(data.BLACK)
        pg.draw.rect(data.SCREEN, data.GREY, data.STATUS_BAR)
        text_surface = data.SMALL_FONT.render(name, True, data.RED)
        data.SCREEN.blit(text_surface, (10, 605))
        draw_text_box('small:0', Rect(580, 600, 0, 0), data.RED, data.GREY)
        for wall in self.walls:
            data.SCREEN.blit(data.BRICK, wall)

        pg.mouse.set_visible(False)
        return name, snake_color

    def pause(self):
        """ Pauses game when p is pressed during play. Game continues when p is pressed again. """

        org_screen = data.SCREEN.copy()
        draw_text_box('title:PAUSED', Rect(300, 275, 0, 0), data.RED)
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
                        data.SCREEN.blit(org_screen, (0, 0))
                        pg.event.get()
                        return
            pg.time.delay(50)

    def place_food(self):
        """ Places new food in a random free spot. """

        Game.food_is_super = False

        while True:  # Runs until the random spot is free of snake and wall.
            Game.food_position = (randint(0, 29) * 20, randint(0, 29) * 20)
            if Game.food_position not in player.snake + game.walls:
                # 1/20 chance for placed food to be data.SUPERFOOD
                # which speeds up snake when eaten.
                if randint(0, 20) == 0:
                    data.SCREEN.blit(data.SUPERFOOD, Game.food_position)
                    Game.food_is_super = True
                else:
                    data.SCREEN.blit(data.FOOD, Game.food_position)
                break

    def change_level(self, level):
        """ Clears data.SCREEN, cuts snake, moves it to start and draws new walls. """

        # Clear data.SCREEN by covering it in black.
        draw_text_box('', Rect(0, 0, self.width, self.height), box_color=data.BLACK)

        # Move snake to start.
        player.snake = [(140, 100), (160, 100), (180, 100), (200, 100)]
        for position in player.snake:
            data.SCREEN.blit(player.img, position)

        # Draw new walls.
        self.walls = data.levels[level % len(data.levels)]
        for wall in self.walls:
            data.SCREEN.blit(data.BRICK, wall)

        # Replace food if it's on new walls or snake.
        if Game.food_position in player.snake:
            data.SCREEN.blit(player.img, Game.food_position)
            self.place_food()
        elif Game.food_position in self.walls:
            data.SCREEN.blit(data.BRICK, Game.food_position)
            self.place_food()
        else:
            data.SCREEN.blit(data.FOOD, Game.food_position)

        # Change level number and update data.SCREEN.
        draw_text_box('small:' + str(player.lvl), Rect(560, 600, 40, 30), data.RED, data.GREY)
        pg.display.update()

        # Reset snake direction and speed.
        self.speed = 6
        player.vx = 20
        player.vy = 0
        pg.time.delay(1000)
        pg.event.get()


class Player:
    """ Class for creating a player. Contains only move method."""

    def __init__(self, name, snake_color):
        self.name = name
        self.snake = [(140, 100), (160, 100), (180, 100), (200, 100)]
        for position in self.snake:
            data.SCREEN.blit(snake_color, position)
        self.vx = 20
        self.vy = 0
        self.img = snake_color
        self.lvl = 0
        pg.display.update()

    def move(self):
        """ Processes players actions during game loop. """

        score_box = Rect(data.SMALL_FONT.size(self.name)[0] + 20, 600, 100, 30)
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

        # Next position of snakes head with current direction.
        head_position = ((self.snake[-1][0] + self.vx) % game.width,
                         (self.snake[-1][1] + self.vy) % game.height)

        if head_position == Game.food_position:
            data.CHOMP.play()
            if Game.food_is_super:
                game.speed = 8
            elif game.speed > 6:
                game.speed -= 1
            game.score += 20
            game.place_food()
        elif head_position in self.snake + game.walls:
            data.UGH.play()
            pg.time.delay(1500)
            game.playing = False
            update_highscores()
            return
        else:
            # Removes tail if no food was eaten.
            data.SCREEN.blit(data.BACK, player.snake.pop(0))
            if Game.food_is_super:
                data.SCREEN.blit(data.SUPERFOOD, Game.food_position)
            else:
                data.SCREEN.blit(data.FOOD, Game.food_position)

        self.snake.append(head_position)
        data.SCREEN.blit(self.img, head_position)

        # Draws game.score on STATUS_BAR.
        pg.draw.rect(data.SCREEN, data.GREY, score_box)
        text_surface = data.SMALL_FONT.render(str(game.score), True, data.RED)
        data.SCREEN.blit(text_surface, (score_box.x, 605))
        pg.display.update()

        if game.score >= (self.lvl + 1) * 200:
            draw_text_box('title:LVL UP!', Rect(300, 275, 0, 0), data.GREEN)
            pg.display.update()
            data.VICTORY.play()
            pg.time.delay(2000)
            self.lvl += 1
            game.change_level(self.lvl)


def draw_text_box(text, box, text_color=data.YELLOW, box_color=data.GREEN, border=0):
    """
    Draws box with horizontally centered text. Top of text at box.y + 5.
    To draw with TITLE_FONT pass text parameter as "title:<your text>".
    To draw with FONT pass text parameter as "<your text>".
    To draw with SMALL_FONT pass text parameter as "small:<your text>".
    """

    if text[0:6] == 'title:':
        text_surface = data.TITLE_FONT.render(text[6:], True, text_color)
    elif text[0:6] == 'small:':
        text_surface = data.SMALL_FONT.render(text[6:], True, text_color)
    else:
        text_surface = data.FONT.render(text, True, text_color)

    if box.w > 0 and box.h > 0:
        pg.draw.rect(data.SCREEN, box_color, box, border)
    data.SCREEN.blit(text_surface, (box.x + box.w/2 - text_surface.get_width()/2, box.y + 4))


def wanna_quit():
    """ Runs when esc or pg.QUIT activated. """

    # Draw quitting dialog box in middle of screen.
    pg.mouse.set_visible(True)
    org_screen = data.SCREEN.copy()
    back_box = Rect(200, 200, 200, 160)
    quit_box = Rect(250, 260, 100, 35)
    continue_box = Rect(250, 305, 100, 35)
    draw_text_box('Wanna quit?', back_box, box_color=data.BLUE)
    draw_text_box('Yes', quit_box)
    draw_text_box('No', continue_box)
    pg.display.update()

    # Runs until player chooses Yes or No.
    while True:
        for event in pg.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if quit_box.collidepoint(event.pos):
                    return True
                elif continue_box.collidepoint(event.pos):
                    data.SCREEN.blit(org_screen, (0, 0))
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
    pg.mixer.init()
    pg.mouse.set_cursor((8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0))
    data.MUSIC.play(-1)
    while True:
        game = Game()
        player = Player(*game.main())
        pg.time.delay(500)
        while game.playing:
            player.move()
            # Delay dictates game speed.
            pg.time.delay(int(25 * (11 - game.speed)))
