# I def gotta switch to an ORM later
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
		token = "".join([random.choice(CHARSET) for x in range(32)])
		hashed = sha512(token.encode('utf-8')).hexdigest()

		# print(self.curr.execute("SELECT userid FROM apitokens WHERE userid=?", (user,)).fetchone())
		if not self.curr.execute("SELECT userid FROM apitokens WHERE userid=?", (user,)).fetchone == None:
			self.curr.execute("DELETE FROM apitokens WHERE userid=?", (user,))
		self.curr.execute("INSERT INTO apitokens (userid, token) VALUES (?,?)", (user, hashed,))
		self.conn.commit()

		return token

	def getTransactionByID(self, tid):
		res = curr.execute("SELECT * FROM transactions WHERE tid=?").fetchall()
		if len(res) == 0: return False, None

		return True, res[0]

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

		if amt <= 0: return 1
		elif sid == rid: return 2
		elif self.getBalance(cid, sid) < amt and sid > 0: return 3

		self.curr.execute("INSERT INTO transactions (cid, sid, rid, amt) VALUES (?, ?, ?, ?)", (cid, sid, rid, amt,))
		self.conn.commit()

		return 0