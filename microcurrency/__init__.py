# Import modules
from microcurrency.currency import Currency
from microcurrency.db import Database
from microcurrency.exchange import Exchange

from discord import app_commands
from discord.ext import commands
from datetime import datetime
from typing import List
from pathlib import Path
import discord, json, typing, uvicorn, threading, time, contextlib
# Configure bot and initialize database

PATH = Path(__file__).parents[1]
DB = PATH / "DATABASE.db"
CONFIG = PATH / "config.json"

with open(str(CONFIG)) as f:
	config = json.loads(f.read())

db = Database(DB)
exchange = Exchange(0, Currency(0, config["currencies"][0], db))

# Initialize discord.py values

currencies = []
for index, rawdata in enumerate(config["currencies"]):
	currencies.append(Currency(index, rawdata, db))

curchoices = []
for index, currency in enumerate(config["currencies"]):
	curchoices.append(app_commands.Choice(name=currency["name"], value=index))

# Main code

bot = commands.Bot(command_prefix="cur!", intents = discord.Intents.default())

@bot.event
async def on_ready():
	print("MicroCurrency [In-Development], version dev-b14")
	await bot.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name='the market | /help'))
	await bot.tree.sync()

	exchange.id = bot.user.id

	print("Ready!")

@bot.tree.command(name="help",description="List of all commands available on the bot.")
async def help(interaction: discord.Interaction):
 embed=discord.Embed(title="MicroCurrency [In-Development]", description="An economy bot that allows currency trades and exchanges within micronations.", color=0x6699ff)
 embed.add_field(name="/test", value="A testing command for debugging bot.")
 embed.add_field(name="/embtest", value="A command for testing embeds.")
 embed.add_field(name="/rules", value="Read the bot rules.")
 embed.set_footer(text="dev-b14 • Made by Magest1ckkz")
 await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rules",description="Read the rules before doing anything in the bot.")
async def embtest(interaction: discord.Interaction):
 embed=discord.Embed(title="MicroCurrency Rules", description="You must agree with the rules to use this bot. By using this bot, you agree with the rules.\n\n:one: • Do not use macros, other bots, or anything else for farming.\n:two: • No scamming\n:three: • No hacking", color=0x6699ff)
 embed.set_footer(text="Violating any of the rules might result to your bank account reset or terminated.")
 await interaction.response.send_message(embed=embed)

@app_commands.describe(currency = "In what currency would you like to view?", user = "Who's balance would you like to view?")
@app_commands.choices(currency = curchoices)
@bot.tree.command(name="balance", description="Gets the balance of your or somebody else's account")
async def balance(interaction: discord.Interaction, currency: app_commands.Choice[int], user: discord.Member=None):
	if user == None: user = interaction.user
	currency = currencies[currency.value]
	balance = currency.getBalance(int(user.id))

	embed = discord.Embed(description=f"{balance} {currency.symbol}", color=0x00ff00)
	embed.set_author(name=user.display_name, icon_url=user.avatar.url.split("?")[0])
	await interaction.response.send_message(embeds=[embed])

	# await interaction.response.send_message(f"{user.display_name}'s balance is: `{balance} {currency.symbol}`!")

@app_commands.describe(currency = "What currency", user = "The target user")
@app_commands.choices(currency = curchoices)
@bot.tree.command(name="transfer", description="Transfer money to another person")
async def transfer(interaction: discord.Interaction, currency: app_commands.Choice[int], amount: float, user: discord.Member): # gonna refactor this later
	currency = currencies[currency.value]
	status = currency.createTransaction(interaction.user.id, user.id, amount)
	# responses_title = [
	# 	f":white_check_mark: Succesfully transfered {amount} {currency.symbol} to {user.display_name}!",
	# 	":x: You cannot send no or negative money!",
	# 	":x: You cannot send money to yourself!",
	# 	":x: Insufficient funds"
	# ]

	responses = [
		f"Succesfully transfered {amount} {currency.symbol} to {user.display_name}",
		"You cannot send no or negative money!",
		"You cannot send money to yourself!",
		"You have insufficient funds!"
	]

	color = [0x00ff00, 0xff0000][status>0] # if status>0 is true, index "1" gets set into color (aka the red hex code), if it's false then index "0" gets set into color (aka green hex code)
	title = [":white_check_mark: Transaction completed", ":x: Transaction failed"][status>0] # same thing with color

	embed = discord.Embed(title=title, color=color, description=responses[status])
	await interaction.response.send_message(embeds=[embed])

	# await interaction.response.send_message(responses[status])

@app_commands.describe(currency = "What currency you want to see the exchange rates of")
@app_commands.choices(currency = curchoices)
@bot.tree.command(name="exchangerates", description="Get buy/sell rates for the standard currency.")
async def exchange_rates(interaction: discord.Interaction, currency: app_commands.Choice[int]):
	currency = currencies[currency.value]
	stcurrency = currencies[0]

	if currency == stcurrency:
		await interaction.response.send_message(f"`{currency.symbol} 1 = {currency.symbol} 1`, duck!")
		return

	standardRate, otherRate = exchange.getExchangeRates(currency)

	await interaction.response.send_message(f'''Exchange rates of `{currency.name}` and `{stcurrency.name}`

```{standardRate} {stcurrency.symbol} = 1 {currency.symbol}
1 {stcurrency.symbol} = {otherRate} {currency.symbol}```
	''')

@app_commands.describe(currency = "What currency do you want to sell", amount = "How much do you want to sell?")
@app_commands.choices(currency = curchoices)
@bot.tree.command(name="sell", description="Converts your currency of choice into the standard currency.") # , scope=1138412428036685864
async def sell(interaction: discord.Interaction, currency: app_commands.Choice[int], amount: float):
	currency = currencies[currency.value]
	stcurrency = currencies[0]
	standardRate, _ = exchange.getExchangeRates(currency)
	status, exchanged = exchange.exchange(interaction.user.id, standardRate, amount, currency, stcurrency)

	responses = [
		f":white_check_mark: Succesfully sold `{amount} {currency.symbol}` for `{exchanged} {stcurrency.symbol}`!",
		f":x: You cannot sell `{currency.name}` for `{currency.name}`",
		":x: You cannot afford the transaction or have entered in the wrong information!",
		f":x: Couldn't send `{exchanged} {stcurrency.symbol}`, contact a microcurrency dev immediately!"
	]

	await interaction.response.send_message(responses[status])


@app_commands.describe(currency = "What currency do you want to buy", amount = "How much currency do you want to buy?")
@app_commands.choices(currency = curchoices)
@bot.tree.command(name="buy", description="Converts the standard currency into your currency of choice.") # , scope=1138412428036685864
async def buy(interaction: discord.Interaction, currency: app_commands.Choice[int], amount: float):
	currency = currencies[currency.value]
	stcurrency = currencies[0]
	_, otherRate = exchange.getExchangeRates(currency)
	status, exchanged = exchange.exchange(interaction.user.id, otherRate, amount, stcurrency, currency)

	responses = [
		f":white_check_mark: Succesfully bought `{exchanged} {currency.symbol}` for `{amount} {stcurrency.symbol}`!",
		f":x: You cannot buy `{currency.name}` for `{currency.name}`",
		":x: You cannot afford the transaction or have entered in the wrong information!",
		f":x: Couldn't send `{exchanged} {currency.symbol}`, contact a microcurrency dev immediately!"
	]

	await interaction.response.send_message(responses[status])

@bot.tree.command(name="create_token", description="Creates or regenerates an API token for you.")
async def create_token(interaction: discord.Interaction):
	tok = db.createAPIToken(interaction.user.id)

	await interaction.response.send_message(f"Your new API token is: `{tok}`\nFor security purposes, API token can only be shown **once**.\nIf you lose it, you will have to regenerate it with the same command.", ephemeral=True)

####### uvicorn stuff

class Server(uvicorn.Server):
	def install_signal_handlers(self):
		pass

	@contextlib.contextmanager
	def run_in_thread(self):
		thread = threading.Thread(target=self.run)
		thread.start()
		try:
			while not self.started:
				time.sleep(1e-3)
			yield
		finally:
			self.should_exit = True
			thread.join()

uconfig = uvicorn.Config("microcurrency.api:app", host=config["api"]["host"], port=config["api"]["port"], reload=config["api"]["reload"])
server = Server(config=uconfig)

#######


def start():
	if config["api"]["enabled"]:
		with server.run_in_thread():
			bot.run(config["token"])
		# threading.Thread(daemon=True, target=bot.run, args=(config["token"],)).start()
		# uvicorn.run("microcurrency.api:app", host=config["api"]["host"], port=config["api"]["port"], reload=config["api"]["reload"])
	else:
		bot.run(config["token"])