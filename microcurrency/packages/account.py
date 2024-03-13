from microcurrency.core.currency import Currency
from microcurrency.core.db import Database
from microcurrency.util import mround, TestPager
from discord import app_commands
from discord.ext import commands
from pathlib import Path
import discord, json

class Account(commands.Cog):
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

		@app_commands.describe(currency = "In what currency would you like to view?", user = "Who's balance would you like to view?")
		@app_commands.choices(currency = curchoices)
		@self.bot.tree.command(name="balance", description="Gets the balance of your or somebody else's account")
		async def balance(interaction: discord.Interaction, currency: app_commands.Choice[int], user: discord.Member=None):
			if user == None: user = interaction.user
			currency = currencies[currency.value]
			balance = currency.getBalance(int(user.id))

			embed = discord.Embed(description=f"{mround(balance)} {currency.symbol}", color=0x00ff00)
			embed.set_author(name=user.display_name, icon_url=user.display_avatar.url.split("?")[0])
			await interaction.response.send_message(embeds=[embed])

		@app_commands.describe(currency = "In what currency?", user = "Who will receive the money?")
		@app_commands.choices(currency = curchoices)
		@self.bot.tree.command(name="transfer", description="Transfer money to another person")
		async def transfer(interaction: discord.Interaction, currency: app_commands.Choice[int], amount: float, user: discord.Member): # gonna refactor this later
			currency = currencies[currency.value]
			status = currency.createTransaction(interaction.user.id, user.id, amount)

			responses = [
				f"Succesfully transfered {mround(amount)} {currency.symbol} to {user.display_name}",
				"You cannot send no or negative money!",
				"You cannot send money to yourself!",
				"You have insufficient funds!"
			]

			color = [0x00ff00, 0xff0000][status>0] # if status>0 is true, index "1" gets set into color (aka the red hex code), if it's false then index "0" gets set into color (aka green hex code)
			title = [":white_check_mark: Transaction completed", ":x: Transaction failed"][status>0] # same thing with color

			embed = discord.Embed(title=title, color=color, description=responses[status])
			await interaction.response.send_message(embeds=[embed])

		@app_commands.describe(currency = "In what currency?", user = "Who do you want to inspect the transaction history of?")
		@app_commands.choices(currency = curchoices)
		@self.bot.tree.command(name="history", description="View transaction histories")
		async def history(interaction: discord.Interaction, currency: app_commands.Choice[int], user: discord.Member=None):
			if user == None: user = interaction.user
			pager = TestPager(interaction.user.id)
			await interaction.response.send_message(embeds=[pager.getEmbed()], view=pager)
			# await interaction.response.send_message("This command is under construction duck!!")

async def setup(bot):
	await bot.add_cog(Account(bot))