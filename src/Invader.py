import constant
from Laser import Laser
from Position import Position
import random

class Invader:

	def __init__(self, width, height, pos):
		
		self.width = width
		self.height = height
		self.pos = pos
		self.speed = random.uniform(constant.invader_speed_min, constant.invader_speed_max)
		self.probShoot = constant.invader_probality_shooting
		self.life = 100
		self.laser_dammage_against_invader = constant.laser_dammage_against_invader

		self.alive = True

	def move(self):
		self.pos.y += self.speed

	def shoot(self):
		return (Laser("ship", constant.laser_width, constant.laser_height, Position(self.pos.x+self.width/2, self.pos.y)))

	def shooted(self):
		self.life -= self.laser_dammage_against_invader

	def isDead(self):
		return self.life <= 0



