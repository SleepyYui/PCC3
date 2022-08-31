import discord
from discord.ext import commands
from discord.commands import permissions
import json
from discord import default_permissions
from discord import Option
from discord.ext.commands import MissingPermissions

#rolelist = [589435378147262464, 648546626637398046, 632674518317531137, 571032502181822506]

class kick(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    #@commands.has_permissions(ban_members=True)
    async def kick(self, ctx, member: discord.Member , *, reason = "No reason specified"):
        send = ctx.send
        await self.kick_function(ctx, member, reason, send)


    @kick.error
    async def kickerror(ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.respond("You can't do this! You need to have moderate members permissions!", delete_after=10)
        else:
            raise error

    
    @commands.slash_command(name="kick", description="Moderator only")
    @default_permissions(kick_members=True)
    #@default_permissions(manage_messages=True)
    async def kick_slash(self, ctx, member : Option(discord.Member, required=True), reason : Option(str, required=False)):
        send = ctx.respond
        if reason == None:
            reason = "No reason specified"
        await self.kick_function(ctx, member, reason, send)



    async def kick_function(self, ctx, member, reason, send):

        if send == ctx.send:
            await ctx.message.delete()

        if ctx.author.guild_permissions.manage_messages:
            await ctx.respond(f"Cannot ban a member with Moderator permissions.", delete_after=10)

        await self.new_warn_member(member)
        await member.kick(reason=reason)
        await send(f"Kicked {member.mention}", delete_after=10)

        try:
            await member.send(f"You were kicked from the PC Creater server for:\n" + reason)
        except:
            pass

        if ctx.guild.id == 571031703661969430:

            channel = self.client.get_channel(933768368970932254)

            embed = discord.Embed(title="Kicked", color=13565696)
            embed.add_field(name="Kicked:", value=f"{member.mention}")
            embed.add_field(name="Moderator", value=f"{ctx.author.mention}")
            embed.add_field(name="Reason:", value=reason, inline=False)
            await channel.send(embed=embed)

        await self.update_warns(member, reason)



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