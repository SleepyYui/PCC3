import discord
from discord.ext import commands
from discord import Option
import json
from bank_functions import set_things
from discord.commands import permissions

class manage_member_stats(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.slash_command(name="manage_stats", description="Bot dev only", guild_ids=[951463924279181322])#, guild_ids=[571031703661969430])#, guild_ids=[571031703661969430])
    #@permissions.has_any_role(951207540472029195, 951464246506565683)
    async def manage_member_slash(self, ctx, member : Option(discord.Member, required=True), mode: Option(str, 'Choose the mode', choices=["Coins", "Bank", "Messages", "xp"], required=True),  mode_2: Option(str, "Choose the mode", choices=["Setzero", "Give", "Set"], required=True), amount : Option(int, required=False)):
        if mode == "Coins":
            mode = "wallet"
          
        if mode == "Bank":
            mode = "bank"

        if mode == "Messages":
            mode = "messages"
            if ctx.author.id != 695229647021015040: 
                await ctx.respond("||https://www.youtube.com/watch?v=o-YBDTqX_ZU||\nTutorial to make it work the next time.", ephemeral=True)
                return
          
        if mode_2 == "Setzero":
            mode_2 = "set"
            amount = 0
        if mode_2 == "Give":
            mode_2 = "give"
        if mode_2 == "Set":
            mode_2 = "set"
            
        content = await set_things(member, mode, mode_2, amount)
        await ctx.respond(content)


def setup(client):
    client.add_cog(manage_member_stats(client)) 