import discord
from discord.ext import commands
from discord import Option
import json
from discord.commands import permissions

class ping_support(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.slash_command(name="ping_support", description="DM Support for help")
    #@permissions.has_any_role(697728131003580537, 589435378147262464, 632674518317531137)
    async def ping_support_slash(self, ctx):
        embed = discord.Embed(title="Support", description="This is Support: <@550685810232524830>", color=13565696)
        await ctx.respond(embed=embed)
    


def setup(client):
    client.add_cog(ping_support(client))