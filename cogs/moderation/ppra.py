import discord
from discord.ext import commands
from discord.commands import permissions
from discord import Option

#rolelist = [589435378147262464, 632674518317531137]

class ppra(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="ppra", description="Moderator only", guild_ids=[571031703661969430, 708218806928932896])
    async def ppra(self, ctx, member: Option(discord.Member, required=True)):
        role = ctx.guild.get_role(775736993018806322)
        await ctx.respond(f"Added the **PRO PLAYER** role to **{member}**", delete_after=10)
        await member.add_roles(role)
       


def setup(client):
    client.add_cog(ppra(client)) 
