import discord
from discord.ext import commands
#from slash_commands_group import pcc1

class cost(commands.Cog):

    def __init__(self, client):
        self.client = client


    """@commands.command()
    async def cost(self, ctx):  
        embed = discord.Embed(title="PCC2", description="PC Creator 2 is a ~~paid game and costs **7,99€/7.99$**~~ **free to play** game", color=13565696)
        embed.set_image(url="https://cdn.discordapp.com/attachments/572536109754744839/935181436837830696/unknown.png")
        await ctx.send(embed=embed)"""


"""    @pcc1.command(name="cost", description="Sends a picture with information about the price of PCC2")
    async def cost_slash_pcc2(self, ctx):  
        embed = discord.Embed(title="PCC2", description="PC Creator 2 is a ~~paid game and costs **7,99€/7.99$**~~ **free to play** game", color=13565696)
        embed.set_image(url="https://cdn.discordapp.com/attachments/572536109754744839/935181436837830696/unknown.png")
        await ctx.respond(embed=embed)   """ 


def setup(client):
    client.add_cog(cost(client))