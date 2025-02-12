from discord.ext import commands
from discord import app_commands
from sqlmodel import Session, select
import discord

from microcurrency.core.models import Currency

class Account(commands.Cog):
    def __init__(self, bot, config, session: Session, curchoices):
        self.bot = bot
        self.config = config
        self.session = session # db should be initialized by now
        self.curchoices = curchoices
        # self.currencies = currencies

        # aaaa i hate that i have to do this
        @app_commands.describe(currency="In which currency?", user="User you want to check the account of (default is self)")
        @app_commands.choices(currency=self.curchoices)
        @self.bot.tree.command(name="balance", description="Gets the balance of a user")
        async def balance(interaction: discord.Interaction, currency: app_commands.Choice[int], user: discord.Member=None):
            if user == None: user = interaction.user
            # currency = self.currencies[currency.value]
            currency = self.session.exec(select(Currency).where(Currency.id==currency.value)).fetchall()[0]
            balance = currency.get_balance(self.session, user.id)

            # embed = discord.Embed(description=f"{mround(balance)} {currency.symbol}", color=0x00ff00)
            embed = discord.Embed(description=f"{balance} {currency.symbol}", color=0x00ff00)
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url.split("?")[0])
            await interaction.response.send_message(embeds=[embed])


async def setup(bot):
    await bot.add_cog(Account(bot, bot.___CONFIG, bot.___SESSION, bot.___CURCHOICES))