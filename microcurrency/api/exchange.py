from microcurrency.packages.exchange import getExchangeRates, createExchangeTransaction
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

@app.get("/rates")
async def rates(request: Request):
    try:
        body = await request.json()
        currency1 = currencies[body["currency1"]]
        currency2 = currencies[body["currency2"]]

        rates = getExchangeRates(currency1, currency2)

        return {"success": True, "rates": {
            "buy": rates[1],
            "sell": rates[0]
        }}
    except json.decoder.JSONDecodeError:
        return {"success": False, "error": "No JSON provided!"}
    except KeyError as e:
        return {"success": False, "error": f"Missing {e} field."}

@app.post("/exchange")
async def exchange(request: Request):
	auth = request.headers.get("X-Auth-Token")

	status, userid = db.authenticate(auth)
	if not status:
		return {"success": False, "error": "Authentication failed!"}

	try:
		body = await request.json()
		currency1 = currencies[body["currency1"]]
		currency2 = currencies[body["currency2"]]
		amount = int(body["amount"])
		_, rate_BA = getExchangeRates(currency1, currency2)
		status, exchangedamt = createExchangeTransaction(userid, rate_BA, amount, currency2, currency1)

		responses = [
			"what the sigma",
			f"Invalid currency options",
			f"Something has gone terribly wrong with the bot!",
			f"The amount you are trying to exchange is negative or zero!",
			f"You have insufficient funds!"
		]

		if status > 0:
			return {"success": False, "error": responses[status]}
		else:
			return {"success": True}
	except json.decoder.JSONDecodeError:
		return {"success": False, "error": "No JSON provided!"}
	except KeyError as e:
		return {"success": False, "error": f"Missing {e} field."}