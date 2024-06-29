# I def gotta switch to an ORM later
from microcurrency.enum import *
from microcurrency.core.currency import Transaction, Currency
from hashlib import sha512
import sqlite3 as sl
import random

class Database:
	def __init__(self, db_url):
		self.conn = sl.connect(db_url)
		self.curr = self.conn.cursor()

		self.curr.execute("CREATE TABLE IF NOT EXISTS transactions (tid INTEGER NOT NULL PRIMARY KEY, cid INTEGER NOT NULL, sid INTEGER NOT NULL, rid INTEGER NOT NULL, amt DOUBLE NOT NULL);")
		self.curr.execute("CREATE TABLE IF NOT EXISTS apitokens (userid INTEGER NOT NULL, token CHAR(128) NOT NULL)")
		self.conn.commit()

	def createAPIToken(self, user):
		CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()"
		token = "".join([random.choice(CHARSET) for t in range(32)])
		hashed = sha512(token.encode('utf-8')).hexdigest()

		# print(self.curr.execute("SELECT userid FROM apitokens WHERE userid=?", (user,)).fetchone())
		if not self.curr.execute("SELECT userid FROM apitokens WHERE userid=?", (user,)).fetchone == None:
			self.curr.execute("DELETE FROM apitokens WHERE userid=?", (user,))
		self.curr.execute("INSERT INTO apitokens (userid, token) VALUES (?,?)", (user, hashed,))
		self.conn.commit()

		return token

	def authenticate(self, token):
		hashed = sha512(token.encode('utf-8')).hexdigest()
		dbresp = self.curr.execute("SELECT * FROM apitokens WHERE token=?",(hashed,)).fetchone()
		if dbresp == None:
			return False, 0

		return True, dbresp[0]

	def getTransactionByID(self, tid):
		res = self.curr.execute("SELECT * FROM transactions WHERE tid=?", (tid,)).fetchall()
		if len(res) == 0: return False, None

		return True, Transaction(res[0][0], res[0][1], res[0][2], res[0][3], res[0][4])

	def getTransactions(self, currency=None):
		if currency == None:
			return (Transaction(t[0], t[1], t[2], t[3], t[4]) for t in self.curr.execute("SELECT * FROM transactions").fetchall())
		else:
			rawhist = self.curr.execute("SELECT * FROM transactions WHERE cid=?", (int(currency),)).fetchall() # probably shuold also do this for the upper one, however that may break shit
			return len(rawhist), (Transaction(t[0], t[1], t[2], t[3], t[4]) for t in rawhist)

	def getTransactionsOfUser(self, user, currency=None):
		# # rawhist = self.curr.execute("SELECT * FROM ")
		# if currency == None:
		# 	rawhist = 
		# 	# return (Transaction(t[0], t[1], t[2], t[3], t[4]) for t in self.curr.execute("SELECT * FROM transactions WHERE (sid=? OR rid=?)", (user,user,)).fetchall())
		# else:
		# 	# return (Transaction(t[0], t[1], t[2], t[3], t[4]) for t in self.curr.execute("SELECT * FROM transactions WHERE cid=? AND (sid=? OR rid=?)", (currency, user, user)).fetchall())		
		rawhist = self.curr.execute("SELECT * FROM transactions WHERE (sid=? OR rid=?)", (user,user,)).fetchall() if currency == None else  self.curr.execute("SELECT * FROM transactions WHERE cid=? AND (sid=? OR rid=?)", (currency,user,user,)).fetchall()
		return len(rawhist), (Transaction(t[0], t[1], t[2], t[3], t[4]) for t in rawhist)

	def getBalance(self, cid, id):
		res = self.curr.execute("SELECT sid, rid, amt FROM transactions WHERE cid=? AND (sid=? OR rid=?);", (cid, id, id,)).fetchall()
		bal = 0
		for transaction in res:
			if transaction[0] == id:
				bal -= transaction[2]
			else:
				bal += transaction[2]

		return bal

	def createTransaction(self, cid, sid, rid, amt): # amazing names here

		'''
		Response codes.
		Do we need them? no
		Do I *want* them? yes

			0 = :white_check_mark: Succesfully transfered <amount> <symbol> to <target>!
			1 = :x: You cannot send no or negative money!
			2 = :x: You cannot send money to yourself!
			3 = :x: Insufficient funds

		'''


		print(cid)

		if amt <= 0: return TRANSACTION_RESPONSES.NEGATIVE_AMOUNT
		elif sid == rid: return TRANSACTION_RESPONSES.SELF_SEND
		elif self.getBalance(cid, sid) < amt and sid > 0: return TRANSACTION_RESPONSES.INSUFFICIENT_FUNDS

		self.curr.execute("INSERT INTO transactions (cid, sid, rid, amt) VALUES (?, ?, ?, ?)", (cid, sid, rid, amt,))
		self.conn.commit()

		return TRANSACTION_RESPONSES.SUCCESS