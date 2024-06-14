from microcurrency.api.account import app as accountApp
from microcurrency.api.exchange import app as exchangeApp
from microcurrency.core.currency import Currency
from microcurrency.core.db import Database
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import json

PATH = Path(__file__).parents[2]
STATIC = PATH / "static"
DB = PATH / "DATABASE.db"
CONFIG = PATH / "config.json"

db = Database(DB)

with open(str(CONFIG)) as f:
	config = json.loads(f.read())

currencies = []
for index, rawdata in enumerate(config["currencies"]):
	currencies.append(Currency(index, rawdata, db))

app = FastAPI()

@app.get("/api/list_currencies")
async def list():
	return {"success": True, "currencies": config["currencies"]}


app.mount("/api/exchange", exchangeApp)
app.mount("/api/account", accountAp)
app.mount("/", StaticFiles(directory=str(STATIC)))