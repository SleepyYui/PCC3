import discord
from discord.ext import commands
from discord.commands import permissions

rolelist = [589435378147262464, 648546626637398046, 632674518317531137, 571032502181822506]

class softban(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(name="softban")
    async def softban(self, ctx, member: discord.Member, *, reason = "No reason specified"):
        user = ctx.author
        if any(role.id in rolelist for role in user.roles):
            if not any(role.id in rolelist for role in member.roles):
                await ctx.message.delete()
                channel = self.client.get_channel(933768368970932254)
                try:
                    await member.send(f"You were banned from the PC Creater server for:\n" + reason)

                    await member.ban(reason=reason)
                    await member.unban(reason=reason)
                    await ctx.send(f"Softbanned {member.mention}", delete_after=10)

                    embed = discord.Embed(title="Softbanned", color=13565696)
                    embed.add_field(name="Softbanned:", value=f"{member.mention}")
                    embed.add_field(name="Moderator", value=f"{ctx.author.mention}")
                    embed.add_field(name="Reason:", value=reason, inline=False)
                    await channel.send(embed=embed)
                except:
                    await member.ban(reason=reason)
                    await member.unban(reason=reason)
                    await ctx.send(f"Softbanned {member.mention}", delete_after=10)

                    embed = discord.Embed(title="Softbanned", color=13565696)
                    embed.add_field(name="Softbanned:", value=f"{member.mention}")
                    embed.add_field(name="Moderator", value=f"{ctx.author.mention}")
                    embed.add_field(name="Reason:", value=reason, inline=False)
                    await channel.send(embed=embed)
            else:
                await ctx.send(f"Cannot ban a member with Moderator permissions.", delete_after=10)
        else:
            return

def setup(client):
    client.add_cog(softban(client))