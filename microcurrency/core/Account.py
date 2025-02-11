from discord.ext import commands
from discord import app_commands
from sqlmodel import Session
import discord

class Account(commands.Cog):
    def __init__(self, bot, config, session: Session):
        self.bot = bot
        self.config = config
        self.session = Session # db should be initialized by now

    # AAA THIS SUCKsm i ate working with this!!
    @app_commands.command(name="hello", description="test to see if cogs work")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("works")
        # await interaction.response.send_message(f"work, test value of config is: {self.config['test']}")

async def setup(bot):
    await bot.add_cog(Account(bot, bot.___CONFIG, bot.___SESSION))