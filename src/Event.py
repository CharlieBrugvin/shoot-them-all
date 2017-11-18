import constant

#this class represent an event
#it is constructed from a string, which represent its type
#and, eventualy an assicated object, which is useful for the graphicEngine

class Event:

	def __init__(self, type, associatedObject = None):

		self.type = type
		self.remainingTime = constant.dictEvent[type]
		self.associatedObject = associatedObject
		self.songPlayed = False #this attribute is only necessary for events which triggers songs

	def __str__(self):
		return "type : " + self.type + ", remaining time : " + str(self.remainingTime )+ " "

	def updateTime(self, elapsedTime):
		self.remainingTime -= elapsedTime

	def isFinished(self):
		return self.remainingTime <= 0