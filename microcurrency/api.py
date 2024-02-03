from microcurrency.db import Database
from fastapi import FastAPI, Request
from pathlib import Path
import json

db_path = str(  Path(__file__).parents[1] / "DATABASE.db"  )
db = Database(db_path)

with open(Path(__file__).parents[1] / "config.json"):
	config = json.loads(f.read())

app = FastAPI()

@app.get('/api/balance')
async def balance(request: Request):
	# auth = request.headers.get("X-Auth-Token")
	body = await request.json()

	try:
		return {"success": True, "balance": db.getBalance(body["currency"], body["user"])}
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
		resp = db.createTransaction(int(body["currency"]), int(userid), int(body["receiver"]), float(body["amount"]))
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