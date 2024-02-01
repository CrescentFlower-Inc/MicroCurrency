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

	'''
	More codes!!!
		0 - Succesful exchange
		1 - exchanging standard for standard
		2 - End-User cant make that transaction
		3 - Bot cant afford, time to panic!
	'''

	def exchange(self, userid, rate, amount, recvcurr, sendcurr):
		if recvcurr == sendcurr:
			return 1, 0

		# standardRate, _ = exchange.getExchangeRates(currency)

		exchanged = rate*amount

		code = recvcurr.createTransaction(userid, self.id, amount)

		if not code == 0:
			return 2, 0

		code = sendcurr.createTransaction(self.id, userid, exchanged)

		if not code == 0:
			return 3, 0

		return 0, exchanged