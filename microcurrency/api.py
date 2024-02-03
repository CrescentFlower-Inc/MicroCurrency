from microcurrency.db import Database
from fastapi import FastAPI, Request
from pathlib import Path
import json

db_path = str(  Path(__file__).parents[1] / "DATABASE.db"  )
db = Database(db_path)

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

@app.get("/api")
async def root():
	return {"test_succesful": True}