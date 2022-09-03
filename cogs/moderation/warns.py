import discord
from discord.ext import commands
from discord.commands import permissions
from discord import Option
import json
from discord import default_permissions
from discord.ext.commands import MissingPermissions
from datetime import timedelta

rolelist = [589435378147262464, 648546626637398046, 632674518317531137, 571032502181822506, 697002610892341298]

class warns(commands.Cog):

    def __init__(self, client):
        self.client = client

 
    @commands.command(name="warn")
    #@commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason = None):
        user = ctx.author
        if any(role.id in rolelist for role in user.roles):
            await ctx.message.delete()
            if reason != None:
                moderator = ctx.author
                await self.new_warn_member(member)
                await self.update_warns(member, reason, moderator)
                await ctx.send(f"Warned {member.mention} for {reason}", delete_after=10)
            else:
                await ctx.send(f"You have to specify a reason -_-", delete_after=10)
        else:
            return


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
            await ctx.respond("You can't do this! You have to have moderate members permissions!", delete_after=10)
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
                json.dump(warns,f, indent=4)
            return True     

    async def update_warns(self, member, reason, moderator):

        warns = await self.get_warns()

        warn_count_old = warns[str(member.id)]["warn_count"]
        warn_count_new = warn_count_old + 1

        warns[str(member.id)]["warn_count"] = warn_count_new

        mute_count_old = warns[str(member.id)]["mute_count"]
        mute_count_new = mute_count_old + 1

        kick_count_old = warns[str(member.id)]["kick_count"]
        kick_count_new = kick_count_old + 1

        ban_count_old = warns[str(member.id)]["ban_count"]
        ban_count_new = ban_count_old + 1
   

        if warn_count_new > 0:

            the_other_logs = self.client.get_channel(989272480671739954)

            modlogs = self.client.get_channel(933768368970932254)

            if warn_count_new == 1:

                warns[str(member.id)][f"warn {warn_count_new}"] = f"{reason} (1st warn)"

                try:
                    await member.send(f"You have been warned on **PC CREATOR** for `{reason}`")
                    await the_other_logs.send(f"{member.mention} has been warned for the first time by {moderator.mention} for `{reason}`")
                except:
                    await the_other_logs.send(f"{member.mention} has been warned for the first time by {moderator.mention} for `{reason}`\n**DM NOT SENT**")
                


            elif warn_count_new == 2:

                warns[str(member.id)][f"mute_count"] = mute_count_new
                warns[str(member.id)][f"mute {mute_count_new}"] = f"{reason} (2nd warn)"

                try:
                    await member.send(f"You have been warned on **PC CREATOR** for `{reason}`\nThis is your second warn, that's why you have been muted for 6 hours.")
                    await the_other_logs.send(f"{member.mention} has been warned for the second time (mute 6h) by {moderator.mention} for `{reason}`")
                except:
                    await the_other_logs.send(f"{member.mention} has been warned for the second time (mute 6h) by {moderator.mention} for `{reason}`\n**DM NOT SENT**")

                duration = timedelta(hours = 6)

                await member.timeout_for(duration)

                embed = discord.Embed(title="Timeout", color=13565696)
                embed.add_field(name="Muted", value=f"{member.mention}")
                embed.add_field(name="Moderator", value=f"{moderator.mention}")
                embed.add_field(name="Duration", value=f"**0** days, **6** hours,\n**0** minutes, and **0** seconds", inline=False)
                embed.add_field(name="Reason:", value=reason)

                await modlogs.send(embed=embed)

            elif warn_count_new == 3:

                warns[str(member.id)][f"mute_count"] = mute_count_new
                warns[str(member.id)][f"mute {mute_count_new}"] = f"{reason} (3rd warn)"

                try:
                    await member.send(f"You have been warned on **PC CREATOR** for `{reason}`\nThis is your third warn, that's why you have been muted for 24 hours.")
                    await the_other_logs.send(f"{member.mention} has been warned for the third time (mute 6h) by {moderator.mention} for `{reason}`")
                except:
                    await the_other_logs.send(f"{member.mention} has been warned for the third time (mute 6h) by {moderator.mention} for `{reason}`\n**DM NOT SENT**")

                duration = timedelta(hours = 24)

                await member.timeout_for(duration)

                embed = discord.Embed(title="Timeout", color=13565696)
                embed.add_field(name="Muted", value=f"{member.mention}")
                embed.add_field(name="Moderator", value=f"{moderator.mention}")
                embed.add_field(name="Duration", value=f"**0** days, **24** hours,\n**0** minutes, and **0** seconds", inline=False)
                embed.add_field(name="Reason:", value=reason)

                await modlogs.send(embed=embed)

            elif warn_count_new == 4:

                warns[str(member.id)][f"kick_count"] = kick_count_new
                warns[str(member.id)][f"kick {kick_count_new}"] = f"{reason} (4th warn)"

                try:
                    await member.send(f"You have been warned on **PC CREATOR** for `{reason}`\nThis is your fourth warn, that's why you have been soft-banned.")
                    await the_other_logs.send(f"{member.mention} has been warned for the fourth time (softban) by {moderator.mention} for `{reason}`")
                except:
                    await the_other_logs.send(f"{member.mention} has been warned for the fourth time (softban) by {moderator.mention} for `{reason}`\n**DM NOT SENT**")

                if member.guild_permissions.manage_messages:
                    await the_other_logs.send(f"{moderator.mention}\nYou can't ban a member with Moderator permissions.")    

                await member.ban(reason=reason)
                await member.unban(reason=reason)

                embed = discord.Embed(title="Softbanned", color=13565696)
                embed.add_field(name="Softbanned:", value=f"{member.mention}")
                embed.add_field(name="Moderator", value=f"{moderator.mention}")
                embed.add_field(name="Reason:", value=reason, inline=False)
                await modlogs.send(embed=embed)

            elif warn_count_new == 5:

                warns[str(member.id)][f"warn_count"] = warn_count_new
                warns[str(member.id)][f"warn {warn_count_new}"] = f"{reason} (5th warn)"

                try:
                    await member.send(f"You have been warned on **PC CREATOR** for `{reason}`\nThis is your last warning, please behave or you may get banned.")
                    await the_other_logs.send(f"{member.mention} has been warned for the fifth time (last warn) by {moderator.mention} for `{reason}`")
                except:
                    await the_other_logs.send(f"{member.mention} has been warned for the fifth time (last warn) by {moderator.mention} for `{reason}`\n**DM NOT SENT**")

            elif warn_count_new == 6:

                warns[str(member.id)][f"ban_count"] = ban_count_new
                warns[str(member.id)][f"ban {ban_count_new}"] = f"{reason} (6th warn)"

                try:
                    await member.send(f"You have been banned from **PC CREATOR** for `{reason}`")
                    await the_other_logs.send(f"{member.mention} has been warned for the sixth time (ban) by {moderator.mention} for `{reason}`")
                except:
                    await the_other_logs.send(f"{member.mention} has been warned for the sixth time (ban) by {moderator.mention} for `{reason}`\n**DM NOT SENT**")

                if member.guild_permissions.manage_messages:
                    await the_other_logs.send(f"{moderator.mention} You can't ban a member with Moderator permissions.")    

                await member.ban(reason=reason)

                embed = discord.Embed(title="Banned", color=13565696)
                embed.add_field(name="Banned:", value=f"{member.mention}")
                embed.add_field(name="Moderator", value=f"{moderator.mention}")
                embed.add_field(name="Reason:", value=reason, inline=False)
                await modlogs.send(embed=embed)
       
            else:
                try:
                    await member.send(f"You have been warned on **PC CREATOR** for `{reason}`")
                    await the_other_logs.send(f"{member.mention} has been warned for the {warn_count_new}th time by {moderator.mention} for `{reason}`")
                except:
                    await the_other_logs.send(f"{member.mention} has been warned for the {warn_count_new}th time by {moderator.mention} for `{reason}`\n**DM NOT SENT**")

        with open("json_files/warns.json", "w") as f:
            json.dump(warns,f, indent=4)


def setup(client):
    client.add_cog(warns(client)) 
