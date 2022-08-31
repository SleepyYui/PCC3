from optparse import Option
from discord import SlashCommandGroup
from discord.ext import commands
import discord
from cogs.bot_stuff.botinfo_group import info
from cogs.bot_stuff.credit_group import credit
from cogs.bot_stuff.ping_bot_problem_group import ping_bot_problem
from cogs.bot_stuff.ping_group import ping_slash
import json
from discord import Option


class bot_group(commands.Cog):

    def __init__(self, client):
        self.client = client


    group_bot = SlashCommandGroup("bot", "Bot related stuff")


    @group_bot.command(name="info", description="Shows some infromation about the bot")
    async def info_group_command(self, ctx):
        client1 = self.client
        await info(ctx, client1)

    @group_bot.command(name="credits", description="Just credits")
    async def credit(self, ctx):
        await credit(ctx)

    @group_bot.command(name="problem", description="Only if the Bot has major problems")
    async def bot_problem(self, ctx, reason: Option(str, required = True)):
        await ping_bot_problem(ctx, reason)

    @group_bot.command(name="ping", description="Returns the ping of the bot")   
    async def bot_ping(self, ctx):
        client = self.client
        await ping_slash(ctx, client) 

def setup(client):
    client.add_cog(bot_group(client))




