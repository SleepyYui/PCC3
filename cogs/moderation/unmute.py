import discord
from discord.ext import commands
from discord import Option
from discord.ext.commands import MissingPermissions
from discord.commands import permissions
from discord import default_permissions

class unmute(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.slash_command(name="unmute")
    @default_permissions(mute_members=True)
    async def unmute(self, ctx, member: Option(discord.Member, required=True)):
        user = ctx.author
        
        if True:
            await member.remove_timeout()
            await ctx.respond(f"<@{member.id}> has been untimed out by <@{ctx.author.id}>", delete_after=10)

    @unmute.error
    async def unmuteerror(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You can't do this! You need to have moderate members permissions!", delete_after=10)
        else:
            raise error


def setup(client):
    client.add_cog(unmute(client))