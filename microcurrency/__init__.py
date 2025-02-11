import asyncio
from microcurrency.core.db import create_db_and_tables, get_session
from microcurrency.core.config import get_config
from microcurrency.core.models import * # cluttering but who cares
from microcurrency.core.Account import Account
from discord import app_commands
from discord.ext import commands
import discord

config = get_config()
bot = commands.Bot(command_prefix="cur!", intents=discord.Intents.default())

@bot.event
async def on_ready():
	print("MicroCurrency, version 2.0")

	# sneak in our own data
	session = get_session()
	bot.___CONFIG = config
	bot.___SESSION = session

	await bot.load_extension("microcurrency.core.Account")

	await bot.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name='the market | /help'))
	await bot.tree.sync()

	print("Ready!")


def start():
	create_db_and_tables()
	bot.run(config["token"])