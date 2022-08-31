import discord
from discord.ext import commands
from discord import Option
import json
from discord.commands import permissions
from discord import Option


class twarn(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.slash_command(name="ticket_warn", description="For Moderation", guild_ids=[571031703661969430])
    async def twarn(self, ctx, member: Option(discord.Member, required=True)):
        user = ctx.author
        #if any(role.id in rolelist for role in user.roles):

        category = discord.utils.get(ctx.author.guild.categories, name="TICKETS")
        role = discord.utils.get(ctx.guild.roles, name="Helper")

        if ctx.channel.category == category:

            if role in ctx.author.roles:
            
                reason = "Useless ticket"

                await self.new_warn_member(member)
                await self.update_warns(member, reason)

                await ctx.respond(f"Warned {member.mention} for {reason}", delete_after=10)   

            else:
                await ctx.respond("You don't have the permissions to use this command", delete_after=10)    

        else:
            await ctx.respond("You can't use this command here", delete_after=10)

    

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
    client.add_cog(twarn(client)) 