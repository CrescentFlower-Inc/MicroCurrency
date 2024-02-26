from microcurrency.core.db import Database
from microcurrency.core.currency import Currency
from microcurrency.util import mround
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

@app.get('/api/balance')
async def balance(request: Request):
	# auth = request.headers.get("X-Auth-Token")
	body = await request.json()

	try:
		return {"success": True, "balance": mround(db.getBalance(body["currency"], body["user"]))}
	except json.decoder.JSONDecodeError:
		return {"success": False, "error": "No JSON provided!"}
	except KeyError as e:
		return {"success": False, "error": f"Missing {e} field."}

@app.post('/api/transaction')
async def transaction(request: Request):
	auth = request.headers.get("X-Auth-Token")
	body = await request.json()

	status, userid = db.authenticate(auth)
	if not status:
		return {"success": False, "error": "Authentication failed!"}

	try:
		curr = currencies[int(body["currency"])]
		resp = curr.createTransaction(int(userid), int(body["receiver"]), float(body["amount"]))
		if resp == 0:
			return {"success": True}

		return {"success": False, "error": resp}
	except json.decoder.JSONDecodeError:
		return {"success": False, "error": "No JSON provided!"}
	except KeyError as e:
		return {"success": False, "error": f"Missing {e} field."}

@app.get("/api/list_currencies")
async def list():
	return {"success": True, "currencies": config["currencies"]}

@app.get("/api")
async def root():
	return {"test_succesful": True}