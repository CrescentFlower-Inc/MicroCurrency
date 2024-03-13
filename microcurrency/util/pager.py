import discord

# This class should never be instantiated, only inherited from!
class GeneralPager(discord.ui.View):
    def __init__(self, data, owner, timeout=180):
        super().__init__(timeout=timeout)

        self.data = data
        self.owner = owner
        self.title = "Pager"
        self.description = "More information"
        self.pages = 0 # This should be set by an inheriting class!
        self.page = 0

    ##################################################
    async def move_page(self, interaction, number):
        if not interaction.user.id == self.owner:
            await interaction.response.send_message(":x: You are not allowed to use this button!", ephemeral=True)
            return
        self.page = number
        if self.page < 0: self.page = 0
        if self.page > self.pages-1: self.page = self.pages - 1
        await interaction.response.edit_message(embeds=[self.getEmbed()], view=self)

    @discord.ui.button(label="<<<", style=discord.ButtonStyle.red)
    async def button_to_beginning(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.move_page(interaction, 0)

    # @discord.ui.button(label="-5", style=discord.ButtonStyle.gray)
    # async def button_back_five(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     await self.move_page(interaction, self.page-5)

    @discord.ui.button(label="-1", style=discord.ButtonStyle.green)
    async def button_back_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.move_page(interaction, self.page-1)

    @discord.ui.button(label="+1", style=discord.ButtonStyle.green)
    async def button_forward_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.move_page(interaction, self.page+1)

    # @discord.ui.button(label="+5", style=discord.ButtonStyle.gray)
    # async def button_(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     await self.move_page(interaction, self.page+5)


    @discord.ui.button(label=">>>", style=discord.ButtonStyle.red)
    async def button_to_end(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.move_page(interaction, self.pages-1)
    ##################################################


    def getEmbed(self):
        embed = discord.Embed(title=self.title, description=self.description, color=0x00ff00)
        embed.set_footer(text=f"Page {self.page+1}/{self.pages} Showing {self.page*self.getAmountInPage()+1}-{(self.page+1)*self.getAmountInPage()}")
        for field in self.getPage():
            embed.add_field(name=field["name"], value=field["value"], inline=field["inline"])

        return embed

    # The inheriting class should define this function!
    # The returned value should be a list of dictionaries that represents the fields of an embed
    # The structure of these dictionaries should be as the following: {"name": str, "value": str, "inline": bool}
    def getPage(self): 
        None

    # The inheriting class shuold define this function!
    # The returned value should be an integer that represents how many contents (eg. lines, transactions, accounts) are displayed in a single page
    def getAmountInPage(self):
        None


class TestPager(GeneralPager):
    def __init__(self, owner, timeout=180):
        super().__init__([f"test item number {x}" for x in range(1,50)], owner)
        self.pages = 5
        self.title = "Test pager"

    def getPage(self):
        startIndex = self.page*self.getAmountInPage()
        endIndex = (self.page+1)*self.getAmountInPage()
        focus = self.data[startIndex:endIndex]

        out = []
        for index, field in enumerate(focus):
            out.append({"name": f"Index {index}", "value": field, "inline": False})

        return out
    def getAmountInPage(self):
        return 10
