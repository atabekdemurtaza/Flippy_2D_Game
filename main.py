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

#Количество места по бокам доски до края окна
#используется несколько раз, поэтому рассчитайте его здесь один раз и сохраните в переменных.
XMARGIN = int((WINDOWWIDTH - GEMIMAGESIZE * BOARDWIDTH)/2)
YMARGIN = int((WINDOWHEIGHT - GEMIMAGESIZE * BOARDHEIGHT)/2)

#Констатны значение направлений
UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'

EMPTY_SPACE = -1 #произвольное неположительное значение
ROWABOVEBOARD = 'row above board' #произвольное, нецелое значение

def main(): #Главная функция
	
	global FPSCLOCK, DISPLAYSURF, GEMIMAGES, GAMESOUNDS, BASICFONT, BOARDRECTS
	#Установка
	pygame.init() #Инициализация
	FPSCLOCK = pygame.time.Clock() #Счетчик
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('GemGem')
	BASICFONT = pygame.font.Font('freesansbold.ttf',36)

	#Загрузка картинок
	GEMIMAGES = []
	for i in range(1, NUMGEMIMAGES + 1):
		gemImage = pygame.image.load('gem%s.png' % i) #Загружаем картинки в примере gem1.png, gem2.png
		if gemImage.get_size() != (GEMIMAGESIZE, GEMIMAGESIZE):
			gemImage = pygame.transform.smoothscale(gemImage, GEMIMAGESIZE, GEMIMAGESIZE)
		GEMIMAGES.append(gemImage)
	
	#Загрузка звуков
	GAMESOUNDS = {}
	GAMESOUNDS['bad_swap'] = pygame.mixer.Sound('badswap.wav')
	GAMESOUNDS['match'] = []
	for i in range(NUMMATCHSOUNDS):
		GAMESOUNDS['match'].append(pygame.mixer.Sound('match%s.wav' % i))
	
	#Создайте объекты pygame.Rect для каждого места на доске, чтобы
	#преобразование координат платы в координаты пикселей.
	BOARDRECTS = []
	for x in range(BOARDWIDTH):
		BOARDRECTS.append([])
		for y in range(BOARDHEIGHT):
			r = pygame.Rect(
				(XMARGIN + (x * GEMIMAGESIZE),
				 YMARGIN + (y * GEMIMAGESIZE),
				 GEMIMAGESIZE,
				 GEMIMAGESIZE)
			)
			BOARDRECTS[x].append(r)
	
	while True:
		runGame()

def runGame():
	#Можно играть как одиночную игру. Когда игрок проигрывает
	#вернется этот функция 

	#Установка границы
	gameBoard = getBlankBoard()
	score = 0
	fillBoardAndAnimate(gameBoard, [], score) #Бросьте начальные драгоценные камни. 
	
	#Начальные переменные для старта новый игры
	firstSelectedGem = None
	lastMouseDownX = None 
	lastMouseDownY = None 
	gameIsOver = False 
	lastScoreDeduction = time.time()
	clickContinueTextSurf = None 

	while True: #Главный цикл игры
		clickedSpace = None 
		for event in pygame.event.get(): #цикл обработки событий
			if event.type == QUIT or (event.type==KEYUP and event.key==K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == KEYUP and event.key == K_BACKSPACE:
				return #Новая игра
			elif event.type == MOUSEBUTTONUP:
				if gameIsOver:
					return #После завершение игры, нажать на кнопку "Новая игра"
				if event.pos == (lastMouseDownX, lastMouseDownY):
					#Это событие является щелчком мыши, а не концом мыши
					clickedSpace = checkFormGemClick(event.pos)
				else:
					#это конец перетаскивания мышью
					firstSelectedGem = checkFormGemClick(lastMouseDownX, lastMouseDownY)
					clickedSpace = checkFormGemClick(event.pos)
					if not firstSelectedGem or not clickedSpace:
						#если не является частью допустимого перетаскивания, отмените выбор обоих
						firstSelectedGem = None 
						clickedSpace = None 
			elif event.type == MOUSEBUTTONDOWN:
				#это начало кликание мышью или перетаскивание ею
				lastMouseDownX, lastMouseDownY = event.pos
		if clickedSpace and not firstSelectedGem:
			#Это выбранное первый гем
			firstSelectedGem = clickedSpace
		elif clickedSpace and firstSelectedGem:
			#Выбрано сразу два гема. Поменяем их местами
			firstSwappingGem, secondSwappingGem = getSwappingGems(gameBoard, firstSelectedGem, clickedSpace)
			if firstSwappingGem == None and secondSwappingGem == None:
				#Если оба являются пустым, то гемы не будут прилагащими
				firstSelectedGem = None #Не выбрали первый гем
				continue 
			#Показать анимацию в экран как гемы меняются с друг другом
			boardCopy = getBoardCopyMinusGems(gameBoard, (firstSwappingGem, secondSwappingGem))
			animateMovingGems(boardCopy, [firstSwappingGem, secondSwappingGem], [], score)

			#Поменяйте гемы в их структуре
			



def getSwappingGems():
	pass 

def getBlankBoard():
	pass 

def canMakeMove():
	pass 

def drawMovingGem():
	pass 

def pullDownAllGems():
	pass 

def getGemAt():
	pass 

def getDropSlots():
	pass 

def findMatchingGems():
	pass 

def highlightSpace():
	pass 

def getDroppingGems():
	pass 

def animateMovingGems():
	pass 

def moveGems():
	pass 

def fillBoardAndAnimate():
	pass 

def checkFormGemClick():
	pass 

def drawBoard():
	pass 

def getBoardCopyMinusGems():
	pass 

def drawScore():
	pass 



if __name__ == '__main__':
	main()