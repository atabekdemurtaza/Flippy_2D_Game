import random, time, pygame, sys, copy
from pygame.locals import *

FPS = 30 # кадры каждый секунд
WINDOWWIDTH = 600 # 600 пикселов на ширину
WINDOWHEIGHT = 600 #600 пикселов на высоту

BOARDWIDTH = 8 #Сколько столбцов внутри Плитки
BOARDHEIGHT = 8 #Сколько строк внутри Плитки
GEMIMAGESIZE = 64 #Длина и ширина в каждом пространстве в пикселе

#NUMGEMIMAGES -> количество гем типы. То есть нужно картинки с форматами .png
NUMGEMIMAGES = 7 
assert NUMGEMIMAGES >= 5 #Игра требует не меньше 5 типов гемов

#NUMMATCHSOUNDS -> количество звук чтобы выбрать из чего сделан.
#Форматы .wav файлы названы match0.wav, match1.wav 
NUMMATCHSOUNDS = 6 

MOVERATE = 25 #От 1 до 100, большее число означает более быструю анимацию.
DEDUCTSPEED = 0.8 #снижает счет на 1 очко каждые DEDUCTSPEED секунды.

#              R    G    B
PURPLE    = (255,   0, 255)
LIGHTBLUE = (170, 190, 255)
BLUE      = (  0,   0, 255)
RED       = (255, 100, 100)
BLACK     = (  0,   0,   0)
BROWN     = ( 85,  65,   0)

HIGHLIGHTCOLOR = PURPLE #Цвет выбранного гема
BGCOLOR = LIGHTBLUE #Цвет заднего фона
GRIDCOLOR = BLUE #Цвет рамки игры
GAMEOVERCOLOR = RED #Цвет текста "Вы проиграли"
GAMEOVERBGCOLOR = BLACK #Цвет заднего фона текста "Вы проиграли"
SCORECOLOR = BROWN #Цвет текста очки игрока

#Констатны значение направлений
UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'

EMPTY_SPACE = -1 #произвольное неположительное значение
ROWABOVEBOARD = 'row above board' #произвольное, нецелое значение

def main():
	pass 

if __name__ == '__main__':
	main()