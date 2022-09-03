import discord
from discord.ext import commands
from discord.commands import permissions
from discord import Option
import json
from discord import default_permissions
from discord.ext.commands import MissingPermissions
from datetime import timedelta

class warns(commands.Cog):

    def __init__(self, client):
        self.client = client

 
    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason = None):
        await ctx.message.delete()
        if reason != None:
            moderator = ctx.author
            await self.new_warn_member(member)
            await self.update_warns(member, reason, moderator)
            await ctx.send(f"Warned {member.mention} for {reason}", delete_after=10)
        else:
            await ctx.send(f"You have to specify a reason -_-", delete_after=10)


    @commands.slash_command(name="warn", description="Moderator only")
    @default_permissions(manage_messages=True)
    async def warn_slash(self, ctx, member: Option(discord.Member, required=True), reason : Option(str, required=True)):
        moderator = ctx.author
        await self.new_warn_member(member)
        await self.update_warns(member, reason, moderator)
        await ctx.respond(f"Warned {member.mention} for {reason}", delete_after=10)



    @warn.error
    async def warnerror(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You can't do this! You need to have moderate members permissions!", delete_after=10)
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

    async def update_warns(self, member, reason, moderator):

        warns = await self.get_warns()

        warn_count_old = warns[str(member.id)]["warn_count"]
        warn_count_new = warn_count_old + 1
        warns[str(member.id)]["warn_count"] = warn_count_new
        warns[str(member.id)][f"warn {warn_count_new}"] = reason    

        with open("json_files/warns.json", "w") as f:
            json.dump(warns,f)   

        if warn_count_new > 0:

            the_other_logs = self.client.get_channel(989272480671739954)

            modlogs = self.client.get_channel(933768368970932254)

            if warn_count_new == 1:
                try:
                    await member.send(f"You were warned for the first time in the PC Creator server\nreason: {reason}")
                except:
                    pass
                await the_other_logs.send(f"{member.mention} has been warned for the first time by {moderator.mention} for **{reason}**")


            if warn_count_new == 2:
                try:
                    await member.send(f"You were warned for the second time in the PC Creator server. This leads to a 6 hour timeout\nreason: {reason}")
                except:
                    pass
                await the_other_logs.send(f"{member.mention} has been warned for the second time (mute 6 hours) by {moderator.mention} for **{reason}**")

                duration = timedelta(hours = 6)

                await member.timeout_for(duration)

                embed = discord.Embed(title="Timeout", color=13565696)
                embed.add_field(name="Muted", value=f"{member.mention}")
                embed.add_field(name="Moderator", value=f"{moderator.mention}")
                embed.add_field(name="Duration", value=f"**0** days, **6** hours,\n**0** minutes, and **0** seconds", inline=False)
                embed.add_field(name="Reason:", value=reason)

                await modlogs.send(embed=embed)

            if warn_count_new == 3:
                try:
                    await member.send(f"You were warned for the third time in the PC Creator server. This leads to a 24 hour timeout\nreason: {reason}")
                except:
                    pass
                await the_other_logs.send(f"{member.mention} has been warned for the third time (mute 24 hours) by {moderator.mention} for **{reason}**")

                duration = timedelta(hours = 24)

                await member.timeout_for(duration)

                embed = discord.Embed(title="Timeout", color=13565696)
                embed.add_field(name="Muted", value=f"{member.mention}")
                embed.add_field(name="Moderator", value=f"{moderator.mention}")
                embed.add_field(name="Duration", value=f"**0** days, **24** hours,\n**0** minutes, and **0** seconds", inline=False)
                embed.add_field(name="Reason:", value=reason)

                await modlogs.send(embed=embed)

            if warn_count_new == 4:
                try:
                    await member.send(f"You were warned for the fourth time in the PC Creator server. This leads to a softban\nreason: {reason}")
                except:
                    pass
                await the_other_logs.send(f"{member.mention} has been warned for the fourth time (softban) by {moderator.mention} for **{reason}**")

                if member.guild_permissions.manage_messages:
                    await the_other_logs.send(f"{moderator.mention} You can't ban a member with Moderator permissions.", delete_after=10)    

                await member.ban(reason=reason)
                await member.unban(reason=reason)

                embed = discord.Embed(title="Softbanned", color=13565696)
                embed.add_field(name="Softbanned:", value=f"{member.mention}")
                embed.add_field(name="Moderator", value=f"{moderator.mention}")
                embed.add_field(name="Reason:", value=reason, inline=False)
                await modlogs.send(embed=embed)

            if warn_count_new == 5:
                try:
                    await member.send(f"You were warned for the fifth time in the PC Creator server. This is your **last warning**. The next warn will lead to a permanent ban.\nreason: {reason}")
                except:
                    pass
                await the_other_logs.send(f"{member.mention} has been warned for the fifth time (last warning) by {moderator.mention} for **{reason}**")

            if warn_count_new == 6:
                try:
                    await member.send(f"You were warned for the sixth time in the PC Creator server. This leads to a **permanent ban**. If you think there is a mistake DM <@695229647021015040>\nreason: {reason}")
                except:
                    pass
                await the_other_logs.send(f"{member.mention} has been warned for the sixth time (permanent ban) by {moderator.mention} for **{reason}**")

                if member.guild_permissions.manage_messages:
                    await the_other_logs.send(f"{moderator.mention} You can't ban a member with Moderator permissions.", delete_after=10)    

                await member.ban(reason=reason)

                embed = discord.Embed(title="Banned", color=13565696)
                embed.add_field(name="Banned:", value=f"{member.mention}")
                embed.add_field(name="Moderator", value=f"{moderator.mention}")
                embed.add_field(name="Reason:", value=reason, inline=False)
                await modlogs.send(embed=embed)


def setup(client):
    client.add_cog(warns(client)) 