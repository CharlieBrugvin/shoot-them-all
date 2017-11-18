from Ship import Ship
from Position import Position
import constant
import random
from Invader import Invader
from Event import Event

class Board:

	def __init__(self, width, height, nbColumn):

		#definition of the attributes
		self.width = width
		self.height = height
		self.nbColumn = nbColumn

		#when on invader is killed, 1 is generator, or maybe two, depending of a probability
		self.probability_of_second_invader_popping = constant.probability_of_second_invader_popping
		#if one invader go down and succed to go out of the screen, the user lose points
		self.penality_if_invader_succeed = constant.penality_if_invader_succeed
		self.score = 0
		self.gameOver = False

		# the ship
		x_ship = constant.window_width/2 - constant.ship_width/2
		y_ship = constant.window_height - constant.ship_height
		self.ship = Ship(Position(x_ship,y_ship), constant.ship_width, constant.ship_height)

		#the lists of the invader and the lasers on the screen
		self.listInvader = []
		self.listLaser = []

		#The list of events. When one event is
		self.events = []

		#we generate the first invader
		self.genereateInvader()


	#function used to update the board according to the input, which are the position of the mouse
	#and if the user clicked on a button to shoot
	def update(self, xPosMouse, clicked):

		#we delete all the events
		del self.events[:]

		# ship modification

		# 	deplacement
		self.ship.move(xPosMouse)
		# 	tir
		if clicked:
			self.listLaser.append(self.ship.shoot())
			self.events.append(Event("ship_shot"))

		#invader modification
		i = 0
		for invader in self.listInvader:

			#we move the invader
			invader.move()
			#maybe it shoots
			if random.random() <= invader.probShoot:
				self.listLaser.append(invader.shoot())
				self.events.append(Event("invader_shot"))
			#maybe it succed to pass the screen
			if invader.pos.y > self.height-20:
				self.invaderSucceed(i)
				self.events.append(Event("invader_succeed"))
			else:
				i += 1

		#laser modification
		i = 0 #indice of the current laser in in listLaser
		for laser in self.listLaser:
			#we move the laser
			self.listLaser[i].move()
			#if the laser is out of the screen, we delete it
			if laser.pos.y == -laser.height:
				del self.listLaser[i]
			else:
				i += 1


		#we find the colision of lasers
		l = 0 # counter of the indice of the laser in listLaser
		for laser in self.listLaser:
			#if the laser is in colision with the ship
			if laser.against == "ship" and laser.collision(self.ship):
				self.shipShooted(l)
				l -= 1

			#if it is in colision with an invader
			elif laser.against == "invader":
				i = 0 # counter of the indice of the invaders in listInvader
				for invader in self.listInvader:
					if laser.collision(invader):
						self.invaderShooted(i,l)
					else:
						i += 1
			l += 1


		#we update the gameOver value, according to the life of the ship
		if not self.ship.alive():
			self.gameOver = True


	#this function is called if the i-eme invader is touched by the l-eme laser
	def invaderShooted(self, i, l):

		#we dell the laser and update the invader life
		self.listInvader[i].shooted()
		del self.listLaser[l]

		#if the invader is dead
		if (self.listInvader[i].isDead()):
			# +1 point
			self.score += 1
			self.events.append(Event("invader_killed", self.listInvader[i]))
			#one invader less...
			del self.listInvader[i]
			#...but more are created
			self.genereateInvader()
			if random.random() < self.probability_of_second_invader_popping:
				self.genereateInvader()



	#this function is called if the ship is touched by the l-eme laser
	def shipShooted(self, l):
		self.ship.shooted()
		del self.listLaser[l]
		self.events.append(Event("ship_shooted"))


	#this function creates a new invader and put it in the board
	#on a random column
	def genereateInvader(self):
		pos = Position(random.randrange(self.nbColumn) * self.width / self.nbColumn, constant.invader_height*-1)
		self.listInvader.append( Invader( constant.invader_width, constant.invader_height, pos ) )

	#this function is called if one invader succed to pass the screen
	def invaderSucceed(self, i):
		del self.listInvader[i]
		self.genereateInvader()
		self.score -= self.penality_if_invader_succeed
		print "invader succeed"
