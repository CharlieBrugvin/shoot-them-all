import constant
import random

#a laser can be against an invader or against a ship
class Laser:

	def __init__(self, against, width, height, pos):

		self.width = width
		self.height = height
		self.against = against

		if against == "invader":
			self.step = constant.red_laser_speed
		elif against == "ship":
			self.step = random.uniform(constant.white_laser_speed_min, constant.white_laser_speed_max)

		if against == "invader":
			self.step *= -1

		self.pos = pos

		self.alive = True

	def move(self):
		self.pos.y += self.step

	def collision(self, object):

		if self.against == "ship":
			return object.pos.x <=  self.pos.x  <= object.pos.x + object.width and \
		 		   object.pos.y <=  self.pos.y+self.height <= object.pos.y + object.height

		else:
			return object.pos.x <=  self.pos.x  <= object.pos.x + object.width and \
		 		   object.pos.y <=  self.pos.y+20 <= object.pos.y + object.height
		 		