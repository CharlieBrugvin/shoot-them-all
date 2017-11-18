from Position import Position
from Laser import Laser
import constant

class Ship:

	def __init__(self, initialPos, width, height):
		self.pos = initialPos
		self.lastPos = initialPos
		self.width = width
		self.height = height
		self.laser_dammage = constant.laser_dammage_against_ship
		self.life = 100


	def __str__(self):
		return "pos : " + str(self.pos)

	def move(self, xPosMouse):
		self.pos.x = xPosMouse-self.width/2

	def shoot(self):
		return (Laser("invader", constant.laser_width, constant.laser_height, Position( self.pos.x+self.width/2, self.pos.y)))

	def shooted(self):
		self.life -= self.laser_dammage

	def alive(self):
		return self.life > 0
