import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from datetime import datetime
from datetime import timedelta
from datetime import date
from discord import Option
from discord.commands import permissions
import json

rolelist = [589435378147262464, 648546626637398046, 632674518317531137, 571032502181822506, 697002610892341298]

class timeout(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.slash_command(name = 'timeout', description = "mutes/timeouts a member")
    async def timeout(self, ctx, member: Option(discord.Member, required = True), reason: Option(str, required = False), days: Option(int, max_value = 27, required = False), hours: Option(int, required = False), minutes: Option(int, required = False), seconds: Option(int, required = False)):
        user = ctx.author
        if any(role.id in rolelist for role in user.roles):
            await self.new_warn_member(member)
            channel = self.client.get_channel(933768368970932254)
            if member.id == ctx.author.id:
                await ctx.respond("You can't timeout yourself!", ephemeral=True)
                return
            if any(role.id in rolelist for role in member.roles):
                await ctx.respond(f"Cannot ban a member with Moderator permissions.", delete_after=10)
                return
            if days == None:
                days = 0
            if hours == None:
                hours = 0
            if minutes == None:
                minutes = 0
            if seconds == None:
                seconds = 0
            duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
            if duration >= timedelta(days = 28):
                await ctx.respond("You can't mute someone for more than 27 days, 23 hours, 59 minutes and 59 seconds!", ephemeral=True)
                return
            if reason == None:
                await member.timeout_for(duration)
                embed = discord.Embed(title="Timeout", color=13565696)
                embed.add_field(name="Muted:", value=f"{member.mention}")
                embed.add_field(name="Moderator:", value=f"{ctx.author.mention}")
                embed.add_field(name="Duration:", value=f"**{days}** days, **{hours}** hours,\n**{minutes}** minutes, and **{seconds}** second",inline=False)
                embed.add_field(name="Reason:", value="No reason ...")
                await ctx.respond(f"Muted <@{member.id}> for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}>.", delete_after=10)
                await channel.send(embed=embed)
            else:
                await member.timeout_for(duration, reason = reason)
                embed = discord.Embed(title="Timeout", color=13565696)
                embed.add_field(name="Muted:", value=f"{member.mention}")
                embed.add_field(name="Moderator:", value=f"{ctx.author.mention}")
                embed.add_field(name="Duration:", value=f"**{days}** days, **{hours}** hours,\n**{minutes}** minutes, and **{seconds}** second",inline=False)
                embed.add_field(name="Reason:", value=reason)
                await channel.send(embed=embed)
                await ctx.respond(f"Muted <@{member.id}> for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds by <@{ctx.author.id}> for '{reason}'.", delete_after=10)
            await self.update_warns(member, reason)
        else:
            return
          
    @timeout.error
    async def timeouterror(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You can't do this! You need to have moderate members permissions!", ephemeral=True)
        else:
            raise error

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

        warn_count_old = warns[str(member.id)]["mute_count"]
        warn_count_new = warn_count_old + 1
        warns[str(member.id)]["mute_count"] = warn_count_new
        warns[str(member.id)][f"mute {warn_count_new}"] = reason    

        with open("json_files/warns.json", "w") as f:
            json.dump(warns,f) 

def setup(client):
    client.add_cog(timeout(client))