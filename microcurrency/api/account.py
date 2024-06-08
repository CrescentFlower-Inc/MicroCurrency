from microcurrency.core.db import Database
from microcurrency.core.currency import Currency
from fastapi import FastAPI, Request
from pathlib import Path
import json

PATH = Path(__file__).parents[2]
DB = PATH / "DATABASE.db"
CONFIG = PATH / "config.json"

db = Database(DB)

with open(str(CONFIG)) as f:
	config = json.loads(f.read())

currencies = []
for index, rawdata in enumerate(config["currencies"]):
	currencies.append(Currency(index, rawdata, db))


app = FastAPI()

@app.get('/balance')
async def balance(request: Request):
	# auth = request.headers.get("X-Auth-Token")

	try:
		body = await request.json()

		return {"success": True, "balance": db.getBalance(body["currency"], body["user"])}
	except json.decoder.JSONDecodeError:
		return {"success": False, "error": "No JSON provided!"}
	except KeyError as e:
		return {"success": False, "error": f"Missing {e} field."}


@app.get("/history/page")
async def history(request: Request):
	try:
		body = await request.json()

		user = body["user"]
		currency = currencies[body["currency"]]
		begin = body["begin"] if "begin" in body else 0
		end = body["end"] if "end" in body else -1
		transactions_count, _transactions = currency.getTransactionsOfUser(user)

		#TODO: this sucks aswell, exterminate later
		transactions = [t for t in _transactions]
		subset = transactions[begin:end]
		resp = {"success": True, "history": []}
		for transaction in subset:
			resp["history"].append({
				"id": transaction.id,
				"sender": transaction.sender,
				"receiver": transaction.receiver,
				"amount": transaction.amount
			})

		return resp
	except json.decoder.JSONDecodeError:
		return {"success": False, "error": "No JSON provided!"}
	except KeyError as e:
		return {"success": False, "error": f"Missing {e} field."}

@app.get("/history/count")
async def history(request: Request):

	try:
		body = await request.json()
		user = body["user"]
		currency = currencies[body["currency"]]
		transactions_count, _ = currency.getTransactionsOfUser(user)
		return {"success": False, "count": int(transactions_count)}
	except json.decoder.JSONDecodeError:
		return {"success": False, "error": "No JSON provided!"}
	except KeyError as e:
		return {"success": False, "error": f"Missing {e} field."}

@app.get("/transaction")
async def transaction_get(request: Request):
	try:
		body = await request.json()
		ID = int(body["id"])

		status, transaction = db.getTransactionByID(ID)
		if not status:
			return {"success": False, "error": "Transaction not found!"}

		return {"success": True, "transaction": {
			"id": transaction.id,
			"currency": transaction.currency,
			"sender": transaction.sender,
			"receiver": transaction.receiver,
			"amount": transaction.amount
		}}
	except json.decoder.JSONDecodeError:
		return {"success": False, "error": "No JSON provided!"}
	except KeyError as e:
		return {"success": False, "error": f"Missing {e} field."}
@app.post('/transaction')
async def transaction_post(request: Request):
	auth = request.headers.get("X-Auth-Token")

	status, userid = db.authenticate(auth)
	if not status:
		return {"success": False, "error": "Authentication failed!"}

	try:
		body = await request.json()
		curr = currencies[int(body["currency"])]
		resp = curr.createTransaction(int(userid), int(body["receiver"]), float(body["amount"]))
		if resp == 0:
			return {"success": True}

		return {"success": False, "error": resp}
	except json.decoder.JSONDecodeError:
		return {"success": False, "error": "No JSON provided!"}
	except KeyError as e:
		return {"success": False, "error": f"Missing {e} field."}