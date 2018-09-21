
## ----------------------- ##
## LEVEL DATA FOR SNAKE 42 ##
## ----------------------- ##

from random import randint

levels = []

def random_level(n):
	'''creates a level with n randomly placed walls'''
	level = []
	while len(level) < n:
		wall = (randint(0,14) * 40, randint(0,29) * 20)
		if wall in [(140,100),(160,100),(180,100),(200,100),(220,100),(240,100)]:
			continue
		else:
			level.append(wall)
	return level

_0 = []
levels.append(_0)

_1 = 	[(i, 200) for i in range(100, 520, 20)] + [(i, 400) for i in range(100, 520, 20)]
levels.append(_1)

# walls around field
_2 =  [(i, 0) for i in range(0, 600, 20)] + [(i, 580) for i in range(0, 600, 20)]
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