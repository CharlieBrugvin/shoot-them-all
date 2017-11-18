import constant
import pygame
from pygame.locals import *
from Board import *
from Position import Position
from GraphicEngine import GraphicEngine
import time

pygame.init()

quit = False
while not quit:

	#creation of the board and the graphic engine
	board = Board( constant.window_width, constant.window_height, constant.nbColumn )
	graphicEngine = GraphicEngine(constant.window_width, constant.window_height,board)

	#creation of the window
	if constant.fullscreen:
		fenetre = pygame.display.set_mode((constant.window_width, constant.window_height), FULLSCREEN)
	else:
		fenetre = pygame.display.set_mode((constant.window_width, constant.window_height))

	#music initialisation
	pygame.mixer.music.load("../res/music.wav")
	pygame.mixer.music.play(-1)

	#loop of one game
	gameOver = False
	clicked = False
	while not gameOver:

		#we update the graphic engine
		graphicEngine.update(board)
		fenetre.blit(graphicEngine.surface, (0,0)) #on ajoute a la fenetre principale la surface renvoye par le mg

		pygame.display.flip()

		#we look at the input
		for event in pygame.event.get():
			#if the user wants to quit
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
				quit = True
				gameOver = True
			#if the user click on its mouse
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				clicked = True

		#we update the board
		board.update(pygame.mouse.get_pos()[0], clicked)
		clicked = False

		if board.gameOver:
			gameOver = True

	#----- AFTER A GAME OVER -----

	#we print the GAME OVER message
	police = pygame.font.SysFont(None, 60)
	game_over_text = police.render("GAME OVER !! You have a score of  {}.".format(board.score), True, (255,255,255))

	rect = game_over_text.get_rect()
	rect.centerx = constant.window_width/2
	rect.centery = constant.window_height/2

	fenetre.blit(game_over_text, (rect.x, rect.y))
	pygame.display.flip()

	#the game restart after few seconds
	time_beg = time.time()
	while not quit and time.time() - time_beg < 5:
		#we look at the input
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
				quit = True
