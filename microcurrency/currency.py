class Transaction:
	def __init__(self, id, currency, sender, receiver, amount): # This is what we call in the industry: shit code
		self.id = id
		self.currency = currency
		self.sender = sender
		self.receiver = receiver
		self.amount = amount


class Currency:
	def __init__(self, id, raw, db):
		self.id = id
		self.standard = id == 0
		self.name = raw["name"]
		self.symbol = raw["symbol"]
		self.managers = raw["managers"]
		self.db = db

	def checkBalance(self, userid):
		return self.db.checkBalance(self.id, userid)

	def getTransaction(self, tid):
		status, rawt = self.db.getTransactionById(tid)
		if not status: return False, "Transaction doesn't exist"

		return True, Transaction(rawt[0], self, rawt[2], rawt[3], rat[4])

	def createTransaction(self, sender, receiver, amount):
		return self.db.createTransaction(self.id, sender, receiver, amount)


