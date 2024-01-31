from microcurrency.db import Database
from pathlib import Path
import json

PATH = Path(__file__).parents[2]
DB = PATH / "DATABASE.db"
CONFIG = PATH / "config.json"

db = Database(DB)
with open(str(CONFIG)) as f:
	config = json.loads(f.read())

print("Dev-Scriptz!!!")
print("Dev tools for devs.\n")

def print_currencies():
	global config

	for index, currency in enumerate(config["currencies"]):
		name = currency["name"] 
		print(f"{index}\t{name}")

def create_money():
	print_currencies()
	currency_id = int(input("Enter currnecy ID: "))
	receiver_id = input("Enter user ID of receiver: ")
	amount = float(input("Enter amount you want to create: "))

	code = db.createTransaction(currency_id, 0, receiver_id, amount)

	print(f"Exiting with code {code}")
