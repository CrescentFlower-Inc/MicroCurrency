# Import modules


from discord import app_commands
from discord.ext import commands
from datetime import datetime
import sqlite3 as sl
import discord, json
# Configure bot

PATH = "/".join(__file__.split("/")[:-2])+"/"
DBS = PATH+"dbs/"
CONFIG = PATH+"config.json"

f = open(str(CONFIG))
config = json.loads(f.read())
f.close()

conns = {}
currs = {}

for database in config['currencies']:
	conn = sl.connect(DBS+database+".db")
	curr = conn.cursor()
	curr.execute("CREATE TABLE IF NOT EXISTS user (aid INTEGER NOT NULL PRIMARY KEY, cid INTEGER, bal DOUBLE);")
	curr.execute("CREATE TABLE IF NOT EXISTS transactions (tid INTEGER NOT NULL PRIMARY KEY, sid INTEGER, rid INTEGER, amt DOUBLE);")
	conn.commit()
	conns[database] = conn
	currs[database] = curr


# Main code

bot = commands.Bot(command_prefix="cur!", intents = discord.Intents.default())

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord. Activity(type=discord.ActivityType.watching, name='exchanges | /help'))
    print("MicroCurrency [In-Development], version dev-b14")
    await bot.tree.sync(), print(f"All commands has been synced!")
    print("Ready!")

@bot.tree.command(name="test",description="A testing command for debugging bot.")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("[SUS](https://youtube.com/)")


@bot.tree.command(name="embtest",description="A command for testing embeds.")
async def embtest(interaction: discord.Interaction):
 embed=discord.Embed(title="Insert title here", description="It will be a testing embed.", color=0x6699ff)
 embed.add_field(name="Field1", value="No commands here", inline=True)
 embed.add_field(name="Field2", value="There's also no command", inline=True)
 embed.set_footer(text="Magest1ckkz")
 await interaction.response.send_message(embed=embed)

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
 
@bot.tree.command(name="exchangerates",description="View the current exchange rates.")
async def embtest(interaction: discord.Interaction):
 embed=discord.Embed(title="Exchange rates (" + datetime.today().strftime('%d.%m.%Y')+")", description="`1` Lunarian Spilling (Ł) • `0,475` Pur (Ᵽ)", color=0x6699ff)
 embed.set_footer(text="This bot is in the very early stage of development, so exchange rates will not change.")
 await interaction.response.send_message(embed=embed)

@bot.tree.command(name="strtest",description="A command for testing strings.")
@app_commands.describe(user = "The user where it will be targeted to.", amount = "Amount of currency you want to give.", currency = "What currency to give to the user.")
async def strtest(interaction: discord.Interaction, user: discord.Member, amount: int, currency: str):

    embed1=discord.Embed(description=":x: Hey man, you can't send a currency that is 0 or a negative value.", color=0xff0000)
    embed2=discord.Embed(description=":x: Hey man, sounds very stupid to send a currency to yourself!", color=0xff0000)

    if amount <= 0: await interaction.response.send_message(embed=embed1),
    elif user == interaction.user.mention: await interaction.response.send_message(embed=embed2),
    else: await interaction.response.send_message(f"This is a testing command, representing {interaction.user.name}, that wanted to give {amount} {currency} to {user.mention}.")

def start():
	bot.run(config["token"])
