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
		self.role = raw["managing_role"]
		self.db = db

	def getBalance(self, userid):
		return self.db.getBalance(self.id, userid)

	def getTransaction(self, tid):
		status, rawt = self.db.getTransactionById(tid)
		if not status: return False, "Transaction doesn't exist"

		return True, Transaction(rawt[0], self, rawt[2], rawt[3], rawt[4])

	def getTransactions(self):
		return self.db.getTransactions(self.id)
	def getTransactionsOfUser(self, user):
		return self.db.getTransactionsOfUser(user, self.id)

	def createTransaction(self, sender, receiver, amount):
		return self.db.createTransaction(self.id, sender, receiver, amount)