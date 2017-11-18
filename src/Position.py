class Position:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def copy(self):
		return Position(self.x, self.y)

	def __str__(self):
		return "(" + str(self.x) + "," + str(self.y) + ")"

	def __eq__(self, pos2):
		if self.x == pos2.x and self.y == pos2.y :
			return True
		else:
			return False
