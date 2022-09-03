import discord
from discord.ext import commands
from discord.commands import permissions
from discord import default_permissions
from discord import Option
from discord.ext.commands import MissingPermissions


class softban(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(name="softban")
    @commands.has_permissions(kick_members=True)
    async def softban(self, ctx, member: discord.Member, * ,reason = "No reason specified"):
        send = ctx.send
        await self.softban_function(ctx, member, reason, send)


    @softban.error
    async def softbanerror(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You can't do this! You need to have moderate members permissions!", delete_after=10)
        else:
            raise error


    @commands.slash_command(name="softban", description="Moderator only")
    @default_permissions(kick_members=True)
    async def softban_slash(self, ctx, member : Option(discord.Member, required=True), reason : Option(str, required=False)):
        send = ctx.respond
        if reason == None:
            reason = "No reason specified"
        await self.softban_function(ctx, member, reason, send)


    async def softban_function(self, ctx, member, reason, send):

        if send == ctx.send:
            await ctx.message.delete()

        if member.guild_permissions.manage_messages:
            await ctx.respond(f"Cannot ban a member with Moderator permissions.", delete_after=10)    

        await member.ban(reason=reason)
        await member.unban(reason=reason)
        await send(f"Softbanned {member.mention}", delete_after=10)

        try:
            await member.send(f"You were banned from the PC Creater server for:\n" + reason)
        except:
            pass
        
        if ctx.guild.id == 571031703661969430:

            channel = self.client.get_channel(933768368970932254)

            embed = discord.Embed(title="Softbanned", color=13565696)
            embed.add_field(name="Softbanned:", value=f"{member.mention}")
            embed.add_field(name="Moderator", value=f"{ctx.author.mention}")
            embed.add_field(name="Reason:", value=reason, inline=False)
            await channel.send(embed=embed)

def setup(client):
    client.add_cog(softban(client))