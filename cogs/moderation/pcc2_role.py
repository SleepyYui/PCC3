import discord
from discord.ext import commands

rolelist = [589435378147262464, 632674518317531137]

class pcc2_role(commands.Cog):

    def __init__(self, client):
        self.client = client

 
    @commands.command(name="pcc2r")
    async def pcc2role(self, ctx, member:discord.Member):
        user = ctx.author
        if any(role.id in rolelist for role in user.roles):
            await ctx.message.delete()
            role = ctx.guild.get_role(934902778764091413)
            await ctx.send(f"Added the **PCC2** role to **{member}**", delete_after=30)
            await member.add_roles(role)
        else:
            return


def setup(client):
    client.add_cog(pcc2_role(client)) 
