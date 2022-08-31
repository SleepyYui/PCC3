import discord
from discord.ext import commands
from discord import Option

#command -> bot_group

async def ping_bot_problem(ctx, reason):
    embed = discord.Embed(title=None, description=reason, color=13565696)
    await ctx.respond(f"<@&951207540472029195>")
    await ctx.send(embed=embed)
    