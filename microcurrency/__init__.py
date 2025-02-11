from microcurrency.core.config import get_config
from microcurrency.core.models import *
from discord import app_commands
from discord.ext import commands
import discord

from microcurrency.core.db import create_db_and_tables

config = get_config()
bot = commands.Bot(command_prefix="cur!", intents=discord.Intents.default())

@bot.event
async def on_ready():
	print("MicroCurrency, version 2.0")

	await bot.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name='the market | /help'))
	await bot.tree.sync()

	print("Ready!")
	
def start():
	create_db_and_tables()
	bot.run(config["token"])