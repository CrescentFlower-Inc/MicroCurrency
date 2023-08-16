from sqlite3 import sl

PATH = "/".join(__file__.split("/")[:-2])+"/"
DBS = PATH+"dbs/"

def start():
	print("WARNING: ONLY USE THIS WHEN YOU ARE STARTING A NEW CURRENCY")
	print("ABUSE OF THIS TOOL **WILL** LEAD TO THE ECONOMY CRASHING")
	print("Also please make sure that the account is created")
	print("This should be done automatically when running /account, /bal or any other command")

	db = input("Economy: ")

	conn = sqlite3.connect(DBS+db)
	curr = sqlite3.cursor()

	target = int(input("Target UID: "))
	amount = float(input("Amount: "))
	curr.execute("UPDATE users SET bal=? WHERE uid=?",(amount,target,))
	conn.commit()

	print("all done!")
