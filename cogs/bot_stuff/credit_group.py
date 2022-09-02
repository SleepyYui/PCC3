import discord
from discord.ext import commands
from discord import SlashCommandGroup
import json

#command -> bot_group

async def credit(ctx):
    embed = discord.Embed(title="Credits", color=13565696)
    embed.add_field(name="Bot Owner/Developer", value="<@695229647021015040>", inline=False)
    embed.add_field(name="Bot Developer", value="<@713696771188195368>\n<@443769343138856961>", inline=False)
    embed.add_field(name="Bot host", value="<@443769343138856961>", inline=False)
    embed.add_field(name="Scores sheets", value="<@695229647021015040>\n<@713696771188195368>", inline=False)
    embed.add_field(name="Ticket system, message filter etc.", value="<@443769343138856961>", inline=False)
    #embed.add_field(name="Coin system", value="<@443769343138856961>\n<@695229647021015040>\n<@713696771188195368>", inline=False)

    await ctx.respond(embed=embed)


