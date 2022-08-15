from tabnanny import check
import discord
from discord.ext import commands
import json


 
async def get_restriction():
    with open("json_files/channel_restrictions.json", "r") as f:
        restriction = json.load(f)
    return restriction


async def check_server_restriction(ctx):
    restriction = await get_restriction()
    
    if restriction[str(ctx.channel.id)]["Server"] == 1:
        await ctx.send("This command is restricted. You can use it in the <#748122380383027210>")
        return True
    return False

async def new_restriction(ctx):

    #for guild in client.guilds:
        #for channel in guild.channels:
            #print(channel.id, channel.name)

            restriction = await get_restriction()

            if str(ctx.channel.id) in restriction:
                pass
            else:
                restriction[str(ctx.channel.id)] = {}
                restriction[str(ctx.channel.id)]["Moderation"] = 0
                restriction[str(ctx.channel.id)]["Scores"] = 0
                restriction[str(ctx.channel.id)]["PCC_Content"] = 0
                restriction[str(ctx.channel.id)]["Server"] = 0  

            with open("channel_restrictions.json", "w") as f:
                json.dump(restriction,f)
            #return True  

async def test_187():
    print("TEST412")            
