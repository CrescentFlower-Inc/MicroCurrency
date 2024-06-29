# This is a tribute to the old testing commands

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
