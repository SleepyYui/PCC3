import discord
from discord.ext import commands
from discord import Option
from discord import default_permissions

class unban(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.slash_command(name="unban", description="For Moderation")
    @default_permissions(ban_members=True)
    async def unban(self, ctx, member: Option(str, required = True)):
        user = ctx.author
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split('#')
        for banned_entry in banned_users:
            user = banned_entry.user

            if(user.name, user.discriminator)==(member_name, member_disc):

                await ctx.guild.unban(user)
                await ctx.respond(f"Unbanned {member_name}", delete_after=10)
                return
        await ctx.respond(f"Can't find {member}", delete_after=10)

def setup(client):
    client.add_cog(unban(client))