# Import modules
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

# Main code

bot = commands.Bot(command_prefix="cur!", intents = discord.Intents.default())

async def load_packages():
	PACKAGES = ["account", "exchange", "apic"]
	for package in PACKAGES:
		await bot.load_extension(f"microcurrency.packages.{package}")
		print(f"Loaded '{package}'")

@bot.event
async def on_ready():
	print("MicroCurrency [In-Development], version dev-b14")

	await load_packages()

	await bot.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name='the market | /help'))
	await bot.tree.sync()

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