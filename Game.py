
## -------- ##
## SNAKE 42 ##
## -------- ##

import pygame as pg, time, math, sys, snake_data
from pygame.locals import *
from pygame.mixer import *
from random import randint

pg.init()
pg.mixer.init()
pg.mouse.set_cursor(
	(8, 8), (4, 4), (24, 24, 24, 231, 231, 24, 24, 24), (0, 0, 0, 0, 0, 0, 0, 0)
					   )
screen = pg.display.set_mode((600, 630))
status_bar = Rect(0, 600, 600, 30)

green = 	(13, 	89, 	28)
lightgreen =(34,	177,	76)
orange =	(255,	127,	39)
grey = 		(160, 	163, 	165)
yellow = 	(229, 	212, 	57)
red = 		(239, 	14, 	14)
blue = 		(72, 	92, 	242)
black =		(0,		0,		0)
color = green

back = 			pg.image.load('back.png') # black 20x20 square, used for resetting
food = 			pg.image.load('food.png')
superfood = 	pg.image.load('superfood.png')
green_snake = 	pg.image.load('snake1.png')
orange_snake = 	pg.image.load('snake2.png')
brick = 		pg.image.load('brick.png')
small_font = 	pg.font.Font('kindergarten.ttf', 20)
font =			pg.font.Font('kindergarten.ttf', 32)
title_font = 	pg.font.Font('kindergarten.ttf', 50)
chomp = 		pg.mixer.Sound('chomp.wav')
victory = 		pg.mixer.Sound('victory.wav')
#music = 		pg.mixer.Sound('music.wav')
ugh = 			pg.mixer.Sound('ugh.wav')
#music.set_volume(0.45)
food_is_super = False
play_music = True
food_position = (300,300)
name = 'Snakey'

class Game():

	def __init__(self):
		self.height = 600
		self.width = 600
		self.speed = 6
		self.score = 0
		self.walls = snake_data.levels[0]
		self.playing = True
		screen.fill((0,0,0))

	def main(self):
		start_box = Rect(250, 200, 100, 35)
		name_box = Rect(250, 300, 100, 40)
		green_snake_box = Rect(260,400,30,30)
		orange_snake_box = Rect(310,400,30,30)
		music_box = Rect(226, 470, 148, 35)
		active = False
		finished = False
		snake_color = green_snake
		global name, color, play_music

		screen.fill((0,0,0))
		draw_text_box('title:SNAKE 42', Rect(300,70,0,0), red)
		draw_text_box('Start', start_box, red)
		draw_text_box('small:Enter name', Rect(300,270,0,0), yellow)
		draw_text_box('small:Select color', Rect(300,370,0,0), yellow)
		pg.draw.rect(screen, lightgreen, green_snake_box)
		pg.draw.rect(screen, orange, orange_snake_box)
		if play_music:
			draw_text_box('Music off', music_box, red, green)
		else:
			draw_text_box('Music on', music_box, red, green)

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
						#play_music = not play_music
						if play_music:
							#music.play(-1)
							draw_text_box('Music off', music_box, red, green)
						else:
							#music.stop()
							draw_text_box('Music on', music_box, red, green)
					if name_box.collidepoint(event.pos):
						active = True
						color = blue
					else:
						active = False
						color = green
					if green_snake_box.collidepoint(event.pos):
						snake_color = green_snake
					elif orange_snake_box.collidepoint(event.pos):
						snake_color = orange_snake
				if event.type == pg.KEYDOWN:
					if event.key == K_ESCAPE:
						if wanna_quit():
							sys.exit()
					elif active:
						if event.key == pg.K_RETURN:
							active = False
							color = green
						elif event.key == pg.K_BACKSPACE:
							name = name[:-1]
						else:
							name += event.unicode

			if snake_color == green_snake:
				pg.draw.rect(screen, blue, green_snake_box, 2)
				pg.draw.rect(screen, black, orange_snake_box, 2)
			else:
				pg.draw.rect(screen, black, green_snake_box, 2)
				pg.draw.rect(screen, blue, orange_snake_box, 2)

			name_width = font.size(name)[0]
			# set w and h larger to clear old borders and name
			name_box.w += 5
			name_box.h += 5
			draw_text_box('', name_box, (0,0,0), (0,0,0))
			name_box.h -= 5
			# set name_box width to match name_width
			name_box.w = max(100, name_width+15)
			name_box.x = 300 - name_box.w/2
			#draw name in name_box
			draw_text_box(name, name_box, red, color, 2)
			
			pg.display.update()
			pg.time.delay(30)

		# animation of menu sliding up
		bottom = 600
		i = 1
		org_screen = screen.copy()
		while bottom > 0:
			screen.blit(org_screen, (0, bottom - 600))
			pg.display.update()
			pg.time.delay(17)
			bottom -= i*i / 2
			i += 1

		screen.fill((0,0,0))
		pg.draw.rect(screen, grey, status_bar)
		text_surface = small_font.render(name, True, red)
		screen.blit(text_surface, (10, 605))
		draw_text_box('small:0', Rect(580,600,0,0), red, grey)
		for wall in self.walls:
			screen.blit(brick, wall)

		return name, snake_color

	def pause(self):
		org_screen = screen.copy()
		draw_text_box('title:PAUSED', Rect(300,275,0,0), red)
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
						screen.blit(org_screen, (0,0))
						pg.event.get()
						return
			pg.time.delay(50)

	def place_food(self):
		global food_position, food_is_super
		food_is_super = False

		while True: # runs until the random spot is free of snake
			food_position = (randint(0,29) * 20, randint(0,29) * 20)
			if food_position not in player.snake + game.walls:
				# 1/20 chance for placed food to be superfood
				# which speeds up snake when eaten
				if randint(0,20) == 0:
					screen.blit(superfood, food_position)
					food_is_super = True
				else:
					screen.blit(food, food_position)
				break

	def change_level(self, level):
		# clear screen
		draw_text_box('', Rect(0,0,self.width,self.height), yellow, black)

		# move snake to start
		player.snake = [(140,100),(160,100),(180,100),(200,100)]
		for position in player.snake:
			screen.blit(player.img, position)

		# new walls
		self.walls = snake_data.levels[level % len(snake_data.levels)]
		for wall in self.walls:
			screen.blit(brick, wall)

		# replace food if it's on walls or snake
		if food_position in player.snake:
			screen.blit(player.img, food_position)
			self.place_food()
		elif food_position in self.walls:
			screen.blit(brick, food_position)
			self.place_food()
		else:
			screen.blit(food, food_position)

		# change level number and update screen
		draw_text_box('small:' + str(player.lvl), Rect(560,600,40,30), red, grey)
		pg.display.update()
		
		#reset snake direction and speed
		self.speed = 6
		player.vx = 20
		player.vy = 0
		pg.time.delay(1000)
		pg.event.get()

class Player():

	def __init__(self,name,snake_color):
		self.name = name
		self.snake = [(140,100),(160,100),(180,100),(200,100)]
		for position in self.snake:
			screen.blit(snake_color, position)
		self.vx = 20
		self.vy = 0
		self.img = snake_color
		self.lvl = 0
		pg.display.update()

	def move(self):

		score_box = Rect(small_font.size(name)[0] + 20, 600, 100, 30)
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
				self.vx = 0; self.vy = -20
				break
			elif event.key == K_RIGHT and self.vx != -20:
				self.vx = 20; self.vy = 0
				break
			elif event.key == K_DOWN and self.vy != -20:
				self.vx = 0; self.vy = 20
				break
			elif event.key == K_LEFT and self.vx != 20:
				self.vx = -20; self.vy = 0
				break
			# elif event.key == 270 and game.speed < 9:
			# 	game.speed += 1
			# elif event.key == 269 and game.speed >= 3:
			# 	game.speed -= 1

		# next position of snakes head with current direction
		head_position = ((self.snake[-1][0] + self.vx) % game.width,
						 (self.snake[-1][1] + self.vy) % game.height)

		if head_position == food_position:
			chomp.play()
			if food_is_super:
				game.speed = 8
			elif game.speed > 6:
				game.speed -= 1
			game.score += 40
			game.place_food()
		elif head_position in self.snake + game.walls:
			ugh.play()
			pg.time.delay(1500)
			game.playing = False
			update_highscores()
			return
		else:
			# removes tail if no food was eaten
			screen.blit(back, player.snake.pop(0))
			if food_is_super:
				screen.blit(superfood, food_position)
			else:
				screen.blit(food, food_position)

		self.snake.append(head_position)
		screen.blit(self.img, head_position)

		# draws game.score on status_bar
		pg.draw.rect(screen, grey, score_box)
		text_surface = small_font.render(str(game.score), True, red)
		screen.blit(text_surface, (score_box.x, 605))
		pg.display.update()
		
		# if score is high enough, changes lvl
		if game.score >= (self.lvl + 1) * 200:
			draw_text_box('title:LVL UP!', Rect(300,275,0,0), green)
			pg.display.update()
			victory.play()
			pg.time.delay(2000)
			self.lvl += 1
			game.change_level(self.lvl)

def draw_text_box(text, box, text_color=yellow, box_color=green, border=0):
	'''draws box with horizontally centered text. top of text at box.y + 5'''
	if text[0:6] == 'title:':
		text_surface = title_font.render(text[6:], True, text_color)
	elif text[0:6] == 'small:':
		text_surface = small_font.render(text[6:], True, text_color)
	else:
		text_surface = font.render(text, True, text_color)

	if box.w > 0 and box.h > 0:
		pg.draw.rect(screen, box_color, box, border)
	screen.blit(text_surface, (box.x + box.w/2 - text_surface.get_width()/2, box.y + 4))

def wanna_quit():
	org_screen = screen.copy()
	x = 200
	y = 200
	back_box = 		Rect(x,		y,		200,	160)
	quit_box = 		Rect(x+50,	y+60,	100,	35)
	continue_box = 	Rect(x+50,	y+105,	100,	35)
	draw_text_box('Wanna quit?', back_box, yellow, blue)
	draw_text_box('Yes', quit_box)
	draw_text_box('No', continue_box)
	pg.display.update()

	done = False
	while True:
		for event in pg.event.get():
			if event.type == MOUSEBUTTONDOWN:
				if quit_box.collidepoint(event.pos):
					return True
				elif continue_box.collidepoint(event.pos):
					screen.blit(org_screen, (0,0))
					pg.display.update()
					return False
		pg.time.delay(25)

def update_highscores():
	with open('highscores.txt', 'r') as f:
		data = f.read().split('\n')
	for i in range(10):
		data[i] = data[i].split('- -')
	i = 0
	while game.score <= int(data[i][1]):
		i += 1
		if i == 10:
			break
	data.insert(i, [player.name, str(game.score)])
	with open('highscores.txt', 'w') as f:
		for line in data[:10]:
			f.write('- -'.join(line) + '\n')

if __name__ == '__main__':
	#music.play(-1)
	while True:
		game = Game()
		n, s = game.main()
		player = Player(n,s)
		pg.time.delay(500)
		while game.playing:
			player.move()
			# delay dictates game speed
			pg.time.delay(int(25 * (11 - game.speed)))
