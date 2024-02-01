# This file handles exchanges

class Exchange:
	def __init__(self, id, standard):
		self.standard = standard # Currency standard
		self.id = id # ID of bot

	def getExchangeRates(self, other): # returns buy and sell prices: (? standard = 1 other, 1 standard = ? other)
		standardVol = self.standard.getBalance(self.id)
		otherVol = other.getBalance(self.id)

		try:
			return (standardVol/otherVol, otherVol/standardVol,)
		except ZeroDivisionError:
			return (0, 0,)
