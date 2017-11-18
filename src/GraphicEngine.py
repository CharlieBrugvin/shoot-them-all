import time
import pygame
from pygame.locals import *
import constant
from Event import Event
import math

pygame.init()

class GraphicEngine:

	def __init__(self, width, height, board):

		#dimension of the board
		self.width = width
		self.height = height

		#we create the graphical elements from the files

		#the surface of the ship
		self.ship_surface = pygame.image.load("../res/ship.png")
		self.ship_bad_surface = pygame.image.load("../res/ship_bad.png")
		self.ship_very_bad_surface = pygame.image.load("../res/ship_very_bad.png")

		#the surfaces of the invaders
		self.invader_green_surface = pygame.image.load("../res/invader_green.png")
		self.invader_green_bad_surface = pygame.image.load("../res/invader_green_bad.png")
		self.invader_green_very_bad_surface = pygame.image.load("../res/invader_green_very_bad.png")

		#the surface of the lasers
		self.laser_red_surface = pygame.image.load("../res/laser_red.png")
		self.laser_green_surface = pygame.image.load("../res/laser_white.png")

		#the surface to print for some events
		self.event_ship_shooted_surface = pygame.image.load("../res/event_ship_shooted.png")
		self.event_invader_killed_surface = pygame.image.load("../res/event_invader_killed.png")

		#definition of the police of the texts

		#the police of the text of the score
		self.score_police = pygame.font.SysFont(None, constant.text_score_size)
		#the police of the life of the ship
		life_ship_police_size = int(board.ship.height / 2)
		self.life_ship_police = pygame.font.SysFont(None, life_ship_police_size)
		#the text if an invader succed to pass
		self.score_inv_succ = pygame.font.SysFont(None, 50)
		self.invader_succeed_text = self.score_inv_succ.render("One invader succeed to pass. You loose {} points !".format(constant.penality_if_invader_succeed), True, (255,255,255))
		
		#the songs

		self.ship_shot_song = pygame.mixer.Sound("../res/ship_shot.wav")
		self.invader_shot_song = pygame.mixer.Sound("../res/invader_shot.wav")
		self.invader_killed_song = pygame.mixer.Sound("../res/invader_killed.wav")
		self.ship_shooted_song = pygame.mixer.Sound("../res/ship_shooted.wav")
		self.invader_succeed_song = pygame.mixer.Sound("../res/invader_succed.wav")

		#we create the surface

		#this surface represent the board at a given time
		#it is updated after the call of the function update()
		self.surface = pygame.Surface((self.width, self.height))

		#we store the last time of the call of the update function
		self.lastCallOfUpdate = time.time()

		#contains the list of the events
		#each element is an object of type Event
		self.events = []


	def update(self,board):

		#we add the graphical element on the surface, such as the invaders, lasers, ship, ...
		self.updateSurface(board)

		#we add the audio/graphical elements which depends of events
		self.updateEvent(board)

		#time of the last call update
		self.lastCallOfUpdate = time.time()

	#this function update the surface according to the given board
	def updateSurface(self, board):
		#we add the elements to the main surface

		#we fill the background with black color
		self.surface.fill((0,0,0))

		#we draw the graphical elements
		
		#the laser
		for laser in board.listLaser:
			if laser.against == "ship":
				self.surface.blit(self.laser_green_surface, (laser.pos.x, laser.pos.y))
			else:
				self.surface.blit(self.laser_red_surface, (laser.pos.x, laser.pos.y))

		#the ship
		if 66 <= board.ship.life <= 100:
				self.surface.blit(self.ship_surface, (board.ship.pos.x, board.ship.pos.y))
		if 33 <= board.ship.life <= 66: 
				self.surface.blit(self.ship_bad_surface, (board.ship.pos.x, board.ship.pos.y))
		if 0 <= board.ship.life <= 33:
				self.surface.blit(self.ship_very_bad_surface, (board.ship.pos.x, board.ship.pos.y))

		#the invaders
		for invader in board.listInvader:
			#we choose the good surface according to the invader life
			if 66 <= invader.life <= 100:
				invader_surface_tmp = self.invader_green_surface
			if 33 <= invader.life <= 66: 
				invader_surface_tmp = self.invader_green_bad_surface
			if 0 <= invader.life <= 33:
				invader_surface_tmp = self.invader_green_very_bad_surface
			#we change the size of the surface to give an ilusion of movement
			coef = ((math.cos(invader.pos.y / 6 )) / 20)
			#the coeficient of this is a cosinus function depdening of the y coo of the invader
			#the cos modified to give a smoother movement
			#print coef
			invader_surface_tmp = pygame.transform.scale(invader_surface_tmp, ( int(invader.width*(coef+1)), int(invader.height*(coef+1)) ))
			invader_surface_tmp = pygame.transform.rotate(invader_surface_tmp, coef*50)

			self.surface.blit(invader_surface_tmp, (invader.pos.x, invader.pos.y))

		#the text with the life and the score
		score_text = self.score_police.render("SCORE : " + str(board.score), True, (255,255,255))
		life_text = self.life_ship_police.render(str(board.ship.life) + " %", True, (255,0,0))
		
		self.surface.blit(score_text, (10, board.height - score_text.get_rect().height - 10 ))
		self.surface.blit(life_text, (board.ship.pos.x + board.ship.width + 5, board.ship.pos.y + board.ship.height/3))


	def updateEvent(self, board):
		#events

		#we update the remaing time of the event and 
		#eventualy delete them if they are finished
		i = 0
		for event in self.events:
			event.updateTime(time.time() - self.lastCallOfUpdate)
			if event.isFinished():
				del self.events[i]
			else:
				i += 1

		#we add the new events to the list actual of event
		self.events += board.events

		#we add the graphical or audio elements according to the current events
		for event in self.events:

			#-----SHIP SHOOTED-----

			#if the ship is shooted, we add the surface on it and we play a song
			if event.type == "ship_shooted" :
				self.surface.blit(self.event_ship_shooted_surface, (board.ship.pos.x, board.ship.pos.y))
				if not event.songPlayed:
					self.ship_shooted_song.play()
					event.songPlayed = True

			#-----INVADER KILLED-----

			#if an invader is killed
			elif event.type == "invader_killed":

				#we add an explosion surface, with a size and a transparancy
				#which is changing according to the remaining time of the event

				#we determine the size of the explosion according to the remaining time
				coef = (constant.dictEvent["invader_killed"] - event.remainingTime) / constant.dictEvent["invader_killed"]
				#we create a new surface with the good size
				rectSurface = self.event_invader_killed_surface.get_rect()
				resized_surface = pygame.transform.scale(self.event_invader_killed_surface, (int(rectSurface.width*coef), int(rectSurface.height*coef)))
				#we change the transparancy
				resized_surface.fill((255, 255, 255, int(255*(1-coef)) % 255), None, pygame.BLEND_RGBA_MULT)
				
				#we center the explosion on the invader shooted
				rect_resized_surface = resized_surface.get_rect()
				rect_resized_surface.centerx = event.associatedObject.pos.x + event.associatedObject.width/2
				rect_resized_surface.centery =  event.associatedObject.pos.y + event.associatedObject.height/2
				
				#we blit surface
				self.surface.blit(resized_surface, (rect_resized_surface.x, rect_resized_surface.y))
				# we play the song
				if not event.songPlayed:
					self.ship_shot_song.play()
					self.invader_killed_song.play()
					event.songPlayed = True

			#-----INVADER SUCCEED-----

			#if an invader succeed, we print the message on the screen and we play the song
			elif event.type == "invader_succeed":
				rect = self.invader_succeed_text.get_rect()
				self.surface.blit(self.invader_succeed_text, ( (board.width - rect.width) / 2, (board.height - rect.height) / 3*2 ) )
				if not event.songPlayed:
					self.invader_succeed_song.play()
					event.songPlayed = True
					print "invader_succed_song"


			#-----SHIP SHOT-----

			#if the ship is shooted, we play the song
			elif event.type == "ship_shot":
				if not event.songPlayed:
					self.ship_shot_song.play()
					event.songPlayed = True

			#-----INVADER SHOT-----
			
			#if the invader shoot, we play the song
			elif event.type == "invader_shot":
				if not event.songPlayed:
					self.invader_shot_song.play()
					event.songPlayed = True