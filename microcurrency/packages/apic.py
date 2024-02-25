# API Control
from microcurrency.core.db import Database
from discord import app_commands
from discord.ext import commands
from pathlib import Path
import discord, json

class APIC(commands.Cog):
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
		############################

		@bot.tree.command(name="create_token", description="Creates or regenerates an API token for you.")
		async def create_token(interaction: discord.Interaction):
			tok = db.createAPIToken(interaction.user.id)

			await interaction.response.send_message(f"Your new API token is: `{tok}`\nFor security purposes, API token can only be shown **once**.\nIf you lose it, you will have to regenerate it with the same command.", ephemeral=True)

async def setup(bot):
	await bot.add_cog(APIC(bot))