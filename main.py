
#pip install -r requirements.txt
#
import discord
from discord.ext import commands
import asyncio
from discord.ext import tasks
from datetime import datetime
from datetime import date
import json
from discord.ext.commands import CommandNotFound
import os
from discord.utils import get
from collections import Counter
import collections
import schedule
from discord.ext.commands import MemberNotFound
from discord.ext.commands import MissingPermissions
import sys
import subprocess
from decouple import config
import backup
from discord import SlashCommandGroup

with open("json_files/mainconfig.json", encoding="utf-8-sig") as f:
    mainconfig = json.load(f)

client = commands.Bot(command_prefix=mainconfig["prefix"], intents=discord.Intents.all(), case_insensitive=True) #debug_guilds=[708218806928932896])
client.remove_command('help')



@client.event
async def on_ready():
    schedule.every().day.at("00:00").do(backup.backthisup, "json_files", "../pcc3_backups")
    print("Bot is online")
    print(" _____   _____    _____                _               ___  ")                                               
    print("|  __ \ / ____|  / ____|              | |             |__ \ ")                                        
    print("| |__) | |      | |     _ __ ___  __ _| |_ ___  _ __     ) |")                                               
    print("|  ___/| |      | |    | '__/ _ \/ _` | __/ _ \| '__|   / / ")                                               
    print("| |    | |____  | |____| | |  __/ (_| | || (_) | |     / /_ ")                                              
    print("|_|     \_____|  \_____|_|  \___|\__,_|\__\___/|_|    |____|")
    print("  ____                               __   __    ___   _    _  _  ______ __    __   ___  ")
    print(" / __ \                          _   \ \ / /   / ,_\ | | _| || ||____  / /   / /  / _ \ ")
    print("| |  | |_      ___ __   ___ _ __(_)  _\ V /_ _| |_  / __)_  __  _|  / / /_  / /_ | | | |")
    print("| |  | \ \ /\ / / '_ \ / _ \ '__|   |___ ___|__ __| \__ \_| || |_  / / '_ \| '_ \| | | |")
    print("| |__| |\ V  V /| | | |  __/ |   _  |___ ___| | |___(   /_  __  _|/ /| (_) | (_) | |_| |")
    print(" \____/  \_/\_/ |_| |_|\___|_|  (_)    |_|   (_,_____|_|  |_||_| /_/  \___/ \___/ \___/ ")
    print(" _____                 _                              __     __    _   _  _    ___   ___   ___ ______                     ")
    print("|  __ \               | |                          _  \ \   / /   (_)_| || |_ / _ \ / _ \ / _ \____  |                    ")
    print("| |  | | _____   _____| | ___  _ __   ___ _ __ ___(_)  \ \_/ /   _ _|_  __  _| (_) | | | | (_) |  / /                     ")
    print("| |  | |/ _ \ \ / / _ \ |/ _ \| '_ \ / _ \ '__/ __|     \   / | | | |_| || |_ \__, | | | |\__, | / /                      ")
    print("| |__| |  __/\ V /  __/ | (_) | |_) |  __/ |  \__ \_     | || |_| | |_  __  _|  / /| |_| |  / / / /                       ")
    print("|_____/ \___| \_/ \___|_|\___/| .__/ \___|_|  |___(_)    |_| \__,_|_| |_||_|   /_/  \___/  /_/ /_/                        ")
    print("                              | |                               __  __ _______          __ _  _   _____  ___   ___  _____ ")                                                                                                                                                        
    print("                              |_|                         /\   |  \/  |  __ \ \        / /| || |_| ____|/ _ \ / _ \| ____|")                                                              
    print("                                                         /  \  | \  / | |__) \ \  /\  / /_  __  _| |__ | | | | (_) | |__  ")
    print("                                                        / /\ \ | |\/| |  ___/ \ \/  \/ / _| || |_|___ \| | | |\__, |___ \ ")
    print("                                                       / ____ \| |  | | |      \  /\  / |_  __  _|___) | |_| |  / / ___) |")
    print("                                                      /_/    \_\_|  |_|_|       \/  \/    |_||_| |____/ \___/  /_/ |____/ ")  
    print("                                                                                                                          ")  
    print("__      __           _                 __  __ ___    ___  ")          
    print("\ \    / /          (_)            _  /_ |/_ |__ \  / _ \ ")   
    print(" \ \  / /__ _ __ ___ _  ___  _ __ (_)  | | | |  ) || | | |")        
    print("  \ \/ / _ \ '__/ __| |/ _ \| '_ \     | | | | / / | | | |")    
    print("   \  /  __/ |  \__ \ | (_) | | | |_   | |_| |/ /_ | |_| |")    
    print("    \/ \___|_|  |___/_|\___/|_| |_(_)  |_(_)_|____(_)___/ ")                                                                                                                                                                                                                                                                    

    await client.change_presence(activity=discord.Streaming(name="Playing PC Creator 2", url="https://www.youtube.com/watch?v=o9qoiH0Am7o"))
    client.start_time = datetime.now()
    #client.get_restriction = await get_restriction()
    #await new_restriction()
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

@client.command(name="rsb")
async def rsb(ctx):
    if ctx.author.id == 443769343138856961 or ctx.author.id == 713696771188195368 or ctx.author.id == 695229647021015040:
        await ctx.send("Do you really want to do that? This can take up to 1 minute and could potentially break the bot. Reply with your user-ID to confirm.")
        ans = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        #print(ans.content)
        #print(ctx.author.id)
        if int(ans.content) == int(ctx.author.id):
            await ctx.send("Restarting...")
            subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
        else:
            await ctx.send("Canceled")
    else:
        await ctx.send("HOW DARE YOU")
        
  
@client.command(name="sdb")
async def sdb(ctx):
    if ctx.author.id == 443769343138856961 or ctx.author.id == 713696771188195368 or ctx.author.id == 695229647021015040:
        await ctx.send("Do you really want to do that? This will stop the bot")
        ans = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        #print(ans.content)
        #print(ctx.author.id)
        if int(ans.content) == int(ctx.author.id):
            await ctx.send("Shutting down...")
            sys.exit()
        else:
            await ctx.send("Canceled")
    else:
        await ctx.send("HOW DARE YOU")

@client.command(name="bub")
async def bub(ctx):
    if ctx.author.id == 443769343138856961 or ctx.author.id == 713696771188195368 or ctx.author.id == 695229647021015040:
        await ctx.send("Do you really want to do that? This will backup the User-Files")
        ans = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        if int(ans.content) == int(ctx.author.id):
            backup.backthisup("json_files", "../pcc3_backups")
            await ctx.send("Backup successful...\nMaybe")
        else:
            await ctx.send("Canceled")
    else:
        await ctx.send("HOW DARE YOU")


   

@client.event
async def on_command_error(ctx, error):
    
    send_help = (commands.MissingRequiredArgument, commands.BadArgument, commands.TooManyArguments, commands.UserInputError)
    
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown, you can use it in {round(error.retry_after, 2)}')     
    elif isinstance(error, CommandNotFound):
        return
    elif isinstance(error, MemberNotFound):
        await ctx.send("Can't find this member")
        return
    elif isinstance(error, send_help):
        await ctx.send(f"Hey! You made a mistake.\n{error}", delete_after=10)
        return
    else:
        try:
            channel = client.get_channel(933813622952562718)
        except:
            channel = client.get_channel(951562519217065984)
        await channel.send(f"A command_error occured:\n{error}")
        return


"""@client.event
async def on_application_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(error)
        return
    else:
        try:
            channel = client.get_channel(933813622952562718)
        except:
            channel = client.get_channel(951562519217065984)
        await channel.send(f"A application_command_error occured:\n{error}")
        return"""

initial_extensions = []
for directory in os.listdir('./cogs'):
    if directory != '__pycache__' and directory != 'testing':
        for filename in os.listdir('./cogs/' + directory):
                #print(filename)
                if filename.endswith("group.py") and directory != 'command_groups':
                    pass
                else:
                    if filename.endswith(".py"):
                        if filename != 'importantfunctions.py':
                                initial_extensions.append("cogs." + directory + '.' + filename[:-3])
                                print(directory + "/" + filename[:-3] + ".py was loaded successfully")

if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)    

client.run(config('TOKEN_NYAN'))
