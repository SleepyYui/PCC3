import discord
from discord.ext import commands
from discord.commands import permissions
import json

rolelist = [589435378147262464, 648546626637398046, 632674518317531137, 571032502181822506]

class kick(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(name="kick")
    async def kick(self, ctx, member: discord.Member, *, reason = "No reason specified"):
        user = ctx.author
        if any(role.id in rolelist for role in user.roles):
            if not any(role.id in rolelist for role in member.roles):
                await ctx.message.delete()
                await self.new_warn_member(member)
                channel = self.client.get_channel(933768368970932254)
                try:
                    await member.send(f"You were kicked from the PC Creater server for:\n" + reason)

                    await member.kick(reason=reason)
                    await ctx.send(f"Kicked {member.mention}", delete_after=10)

                    embed = discord.Embed(title="Kicked", color=13565696)
                    embed.add_field(name="Kicked:", value=f"{member.mention}")
                    embed.add_field(name="Moderator", value=f"{ctx.author.mention}")
                    embed.add_field(name="Reason:", value=reason, inline=False)
                    await channel.send(embed=embed)
                except:
                    await member.kick(reason=reason)
                    await ctx.send(f"Kicked {member.mention}", delete_after=10)

                    embed = discord.Embed(title="Kicked", color=13565696)
                    embed.add_field(name="Kicked:", value=f"{member.mention}")
                    embed.add_field(name="Moderator", value=f"{ctx.author.mention}")
                    embed.add_field(name="Reason:", value=reason, inline=False)
                    await channel.send(embed=embed)
                await self.update_warns(member, reason)
            else:
                await ctx.send(f"Cannot ban a member with Moderator permissions.", delete_after=10)
        else:
            return


    async def get_warns(self):
        with open("json_files/warns.json", "r") as f:
                warns = json.load(f)
        return warns

    async def new_warn_member(self, member):

            warns = await self.get_warns()

            if str(member.id) in warns:
                return False
            else:
                warns[str(member.id)] = {}
                warns[str(member.id)]["warn_count"] = 0
                warns[str(member.id)]["mute_count"] = 0
                warns[str(member.id)]["ban_count"] = 0
                warns[str(member.id)]["kick_count"] = 0

            with open("json_files/warns.json", "w") as f:
                json.dump(warns,f)
            return True     

    async def update_warns(self, member, reason):

        warns = await self.get_warns()

        warn_count_old = warns[str(member.id)]["kick_count"]
        warn_count_new = warn_count_old + 1
        warns[str(member.id)]["kick_count"] = warn_count_new
        warns[str(member.id)][f"kick {warn_count_new}"] = reason    

        with open("json_files/warns.json", "w") as f:
            json.dump(warns,f) 

def setup(client):
    client.add_cog(kick(client))