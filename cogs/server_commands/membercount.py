import discord
from discord.ext import commands

class membercount(commands.Cog):

    def __init__(self, client):
        self.client = client

 
    """@commands.command()
    async def membercount(self, ctx):
        membercount = ctx.guild.member_count
        await ctx.send(f"**PC CREATOR** has **{membercount}** members")"""


    """@commands.slash_command(name="membercount", description="Sends how many members are on the server")
    async def membercount_slash(self, ctx):
        membercount = ctx.guild.member_count
        guildname = ctx.guild.name
        await ctx.respond(f"**{guildname}** has **{membercount}** members")  """  


def setup(client):
    client.add_cog(membercount(client)) 