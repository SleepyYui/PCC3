import discord
from discord.ext import commands
from discord.commands import permissions
from discord import Option
import json
from discord import default_permissions
from discord.ext.commands import MissingPermissions

class warns(commands.Cog):

    def __init__(self, client):
        self.client = client

 
    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason = None):
        await ctx.message.delete()
        if reason != None:
            await self.new_warn_member(member)
            await self.update_warns(member, reason)
            await ctx.send(f"Warned {member.mention} for {reason}", delete_after=10)
        else:
            await ctx.send(f"You have to specify a reason -_-", delete_after=10)


    @commands.slash_command(name="warn", description="Moderator only")
    @default_permissions(manage_messages=True)
    async def warn_slash(self, ctx, member: Option(discord.Member, required=True), reason : Option(str, required=True)):
        await self.new_warn_member(member)
        await self.update_warns(member, reason)
        await ctx.send(f"Warned {member.mention} for {reason}", delete_after=10)



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

    async def update_warns(self, member, reason):

        warns = await self.get_warns()

        warn_count_old = warns[str(member.id)]["warn_count"]
        warn_count_new = warn_count_old + 1
        warns[str(member.id)]["warn_count"] = warn_count_new
        warns[str(member.id)][f"warn {warn_count_new}"] = reason    

        with open("json_files/warns.json", "w") as f:
            json.dump(warns,f)      

def setup(client):
    client.add_cog(warns(client)) 