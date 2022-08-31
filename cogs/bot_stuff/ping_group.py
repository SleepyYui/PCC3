import discord
from discord.ext import commands
from discord.ui import Button, View

#command -> bot_group

"""@commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f'Pong\nLatency: **{self.client.latency*1000:,.0f}ms**')"""



async def ping_slash(ctx, client):
    await ctx.respond(f'Latency: **{client.latency*1000:,.0f}ms**')