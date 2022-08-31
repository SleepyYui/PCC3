import discord
from discord.ext import commands
from discord.commands import permissions
from discord import default_permissions

class botnews_command(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="botnews")
    #@default_permissions()
    async def botnews(self, ctx):
        if ctx.author.id == 695229647021015040 or ctx.author.id == 713696771188195368 or ctx.author.id == 443769343138856961:
            await ctx.message.delete()
            embed=discord.Embed(title="Update 1.10.2", description="What is new?", color=13565696)
            embed.set_author(name=f"{ctx.author.name}", url=f"https://discordapp.com/users/{ctx.author.id}", icon_url=f"{ctx.author.avatar.url}")
            embed.add_field(name="Commands", value="Due to issues with the '/' commands, we have reverted the commands to mostly be ',' again.", inline=False)
            embed.add_field(name="Bug fixes", value="We fixed many few bugs, like, MANY bugs. We really thank to those who reported those bugs. Thank You!", inline=False)
            embed.set_footer(text="Stay tuned for the next update. 😉")
            await ctx.send(embed=embed)
        else:
            return

def setup(client):
    client.add_cog(botnews_command(client))