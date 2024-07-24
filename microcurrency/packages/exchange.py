from microcurrency.core.currency import Currency
from microcurrency.core.db import Database
from microcurrency.util import mround
from microcurrency.enum import *
from discord import app_commands
from discord.ext import commands
from pathlib import Path
import discord, json

# TODO: Refactor these functions to be better

def getExchangeRates(currencyA, currencyB): # returns buy and sell prices: (? currencyA = 1 currencyB, 1 currencyA = ? currencyB)
	CurrencyAVol = currencyA.getBalance(1)
	CurrencyBVol = currencyB.getBalance(1)

	try:
		return (CurrencyAVol/CurrencyBVol, CurrencyBVol/CurrencyAVol,)
	except ZeroDivisionError:
		return (0, 0,)


def createExchangeTransaction(userid, rate, amount, sendcurr, recvcurr):
	'''
	More codes!!!
		0 - Succesful exchange
		1 - currencyA == currencyB
		2 - End-User cant make that transaction
		3 - Bot cant afford, time to panic!
	'''
	if recvcurr == sendcurr:
		return EXCHANGE_RESPONSES.CURRENCYA_IS_CURRENCYB, 0

	exchanged = rate*amount
	code = recvcurr.createTransaction(userid, 1, amount)

	if not code == 0:
		print(f"{userid} tried exchanging {amount} {recvcurr.symbol} to {sendcurr.symbol} with code {code}")
		return EXCHANGE_TRANSACTION_MAP[code], 0

	code = sendcurr.createTransaction(1, userid, exchanged)

	if not code == 0:
		recvcurr.createTransaction(1, userid, amount) # refund
		return EXCHANGE_RESPONSES.TRANSACTION_FAILED_ON_BOTS_END, 0

	return EXCHANGE_RESPONSES.SUCCESS, exchanged

class Exchange(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

		############################   TODO: Make it so that this doesn't have to be copy pasted inside every god damn package
		PATH = Path(__file__).parents[2]
		DB = PATH / "DATABASE.db"
		CONFIG = PATH / "config.json"

		with open(str(CONFIG)) as f:
			config = json.loads(f.read())

		db = Database(DB)

		currencies = []
		for index, rawdata in enumerate(config["currencies"]):
			currencies.append(Currency(index, rawdata, db))

		curchoices = []
		for index, currency in enumerate(config["currencies"]):
			curchoices.append(app_commands.Choice(name=currency["name"], value=index))

		############################


		@app_commands.describe(currency1 = "What currency you want to see the value of", currency2 = "The currency in which the value is portrayed")
		@app_commands.choices(currency1 = curchoices, currency2 = curchoices)
		@bot.tree.command(name="exchangerates", description="Get the exchange rates of two currencies")
		async def exchange_rates(interaction: discord.Interaction, currency1: app_commands.Choice[int], currency2: app_commands.Choice[int]):

			currencyA = currencies[currency1.value]
			currencyB = currencies[currency2.value]

			rate_AB, rate_BA = getExchangeRates(currencyA, currencyB)
			toolow = lambda rate: ["","<"][rate<0.01]

			embed = discord.Embed(title="Exchange Rates", description=f"Here are the buy and sell rates of `{currencyA.name}` and `{currencyB.name}`", color=0x00ff00)
			embed.add_field(name="Buy rate", value=f"1.00 {currencyA.symbol} = {toolow(rate_BA)}{mround(rate_BA)} {currencyB.symbol}", inline=True)
			embed.add_field(name="Sell rate", value=f"{toolow(rate_AB)}{mround(rate_AB)} {currencyA.symbol} = 1.00 {currencyB.symbol}", inline=True)

			await interaction.response.send_message(embeds=[embed])

		@app_commands.describe(currency1 = "The currency you want to exchange", currency2 = "The currency that you want to receive", amount = "The amount of currency1 you want to exchange")
		@app_commands.choices(currency1 = curchoices, currency2 = curchoices)
		@bot.tree.command(name="exchange", description="Exchange two currencies")
		async def exchange(interaction: discord.Interaction, currency1: app_commands.Choice[int], currency2: app_commands.Choice[int], amount: float):
			currencyA = currencies[currency1.value]
			currencyB = currencies[currency2.value]

			_, rate_BA = getExchangeRates(currencyA, currencyB)
			status, exchangedamt = createExchangeTransaction(interaction.user.id, rate_BA, amount, currencyB, currencyA)

			responses = [
				f"Succesfully exchanged `{mround(amount)} {currencyA.symbol}` for `{mround(exchangedamt)} {currencyB.symbol}`",
				f"You cannot exchange `{currencyB.name}` for `{currencyA.name}`!",
				f"The bot has insufficient funds, contact an administrator immediatley!",
				f"The amount you are trying to exchange is negative or zero!",
				f"You have insufficient funds!"
			]
			color = [0x00ff00, 0xff0000][status>0] # another ugly hack
			title = [":white_check_mark: Transaction succesful", ":x: Transaction failed"][status>0]

			embed = discord.Embed(title=title, description=responses[status], color=color)
			await interaction.response.send_message(embeds=[embed])

async def setup(bot):
	await bot.add_cog(Exchange(bot))