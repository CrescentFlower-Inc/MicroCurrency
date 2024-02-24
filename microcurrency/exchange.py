# This file handles exchanges
from microcurrency.enum import *


class Exchange:
	def __init__(self, id, standard):
		self.standard = standard # Currency standard
		self.id = id # ID of bot

	def getExchangeRates(self, currencyA, currencyB): # returns buy and sell prices: (? currencyA = 1 currencyB, 1 currencyA = ? currencyB)
		CurrencyAVol = currencyA.getBalance(self.id)
		CurrencyBVol = currencyB.getBalance(self.id)

		try:
			return (CurrencyAVol/CurrencyBVol, CurrencyBVol/CurrencyAVol,)
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
			return EXCHANGE_RESPONSES.EXCHANGING_STANDARD_FOR_STANDARD, 0

		# standardRate, _ = exchange.getExchangeRates(currency)

		exchanged = rate*amount

		code = recvcurr.createTransaction(userid, self.id, amount)

		if not code == 0:
			return EXCHANGE_RESPONSES.TRANSACTION_FAILED_ON_USERS_END, 0

		code = sendcurr.createTransaction(self.id, userid, exchanged)

		if not code == 0:
			return EXCHANGE_RESPONSES.TRANSACTION_FAILED_ON_BOTS_END, 0

		return EXCHANGE_RESPONSES.SUCCESS, exchanged