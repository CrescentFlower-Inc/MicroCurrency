# API Control
from microcurrency.core.db import Database
from microcurrency.core.currency import Currency
from microcurrency.packages.account import TransactionHistoryPager
from discord import app_commands
from discord.ext import commands
from pathlib import Path
import discord, json
class Manager(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None


		############################
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

		@app_commands.guilds(discord.Object(config["dev_server"]["server"]))
		@app_commands.choices(currency = curchoices)
		@app_commands.describe(currency = "In what currency?", amount="How much do you wish to create?", receiver="To whom would you like to gift this new money?")
		@bot.tree.command(name="create_money", description="(Manager only) Adds more money in circulation. WARNING: THIS CAN MESS UP YOUR ECONOMY IF ABUSED.")
		async def create_money(interaction: discord.Interaction, currency: app_commands.Choice[int], amount: float, receiver: discord.Member):
			currency = currencies[currency.value]
			role = discord.utils.find(lambda r: r.id == currency.role, interaction.guild.roles)
			if not role in interaction.user.roles:
				print(f"Unauthorized attempt at using /create_money by {interaction.user.display_name} ({interaction.user.id})!")
				embed = discord.Embed(title="Access denied", description="You are not authorized to use this command!", color=0xff0000)
				await interaction.response.send_message(embeds=[embed], ephemeral=True)
				return

			code = currency.createTransaction(0, receiver.id, amount)
			print(f"{interaction.user.id} attempted to create {amount} money of {currency.name}, status code: {code}")


			responses = [
				f"The operation is succesfull",
				"You cannot send no or negative money!",
				"You cannot send money to yourself!",
				"You have insufficient funds!"
			]

			color = [0x00ff00, 0xff0000][code>0]
			title = [":white_check_mark: Operation completed", ":x: Operation failed"][code>0]

			embed = discord.Embed(title=title, color=color, description=responses[code])
			await interaction.response.send_message(embeds=[embed], ephemeral=True)

		@app_commands.guilds(discord.Object(config["dev_server"]["server"]))
		@app_commands.choices(currency = curchoices)
		@app_commands.describe(currency = "Of what currency?")
		@bot.tree.command(name="list_transactions", description="(Manager only) Lists all transactions of a currency")
		async def list_transactions(interaction: discord.Interaction, currency: app_commands.Choice[int]):
			currency = currencies[currency.value]
			role = discord.utils.find(lambda r: r.id == currency.role, interaction.guild.roles)
			if not role in interaction.user.roles:
				print(f"Unauthorized attempt at using /list_transactions by {interaction.user.display_name} ({interaction.user.id})!")
				embed = discord.Embed(title="Access denied", description="You are not authorized to use this command!", color=0xff0000)
				await interaction.response.send_message(embeds=[embed], ephemeral=True)
				return

			transaction_len, transactions = currency.getTransactions()
			pager = TransactionHistoryPager(transaction_len, transactions, currency.symbol, interaction.user.id)
			await interaction.response.send_message(embeds=[pager.getEmbed()], view=pager, ephemeral=True)
			

        # @reload_command.error
        # async def reload_command_error(interaction: discord.Interaction, error):
        #     print(f"Unauthorized attempt at using /reload_packages by {interaction.user.display_name} or {interaction.user.id}!")
        #     embed = discord.Embed(title="Access denied", description="You are not authorized to use this command!", color=0xff0000)
        #     # print(error)
        #     await interaction.response.send_message(embeds=[embed], ephemeral=True)

		# @bot.tree.command(name="create_token", description="Creates or regenerates an API token for you.")
		# async def create_token(interaction: discord.Interaction):
		# 	tok = db.createAPIToken(interaction.user.id)

		# 	await interaction.response.send_message(f"Your new API token is: `{tok}`\nFor security purposes, API token can only be shown **once**.\nIf you lose it, you will have to regenerate it with the same command.", ephemeral=True)

async def setup(bot):
	await bot.add_cog(Manager(bot))