import discord
from discord.ext import commands
import websockets
import json
from cogs.pc_creator_commands.importantfunctions import check_all
   

async def record_pcc2(ctx): 
    embed = discord.Embed(title="__PCC2 World Record__", description="This is the current PCC2 World Record PC", color=13565696)
    embed.add_field(name=f":small_blue_diamond: Achieved by", value="<@530725164703416340> Vinrellren#9894 (530725164703416340)", inline=False)
    embed.add_field(name=f":small_blue_diamond: Details", value="Max overclocks are needed to get the highest score \n• MX-4 45 Thermal Paste is required and needs to cover \n100% of the CPU \n• Max overclocking skill is required.", inline=False)
    embed.add_field(name=f":small_blue_diamond: Score achieved", value="`3.313.336`", inline=False)
    embed.set_image(url="https://media.discordapp.net/attachments/748122380383027210/959825115485470790/1648910536234.jpg")

    await ctx.respond(embed=embed)   

async def pcc2_status(ctx):
   status = await check_all()
   await ctx.respond(embed=discord.Embed(title="Status", description=f"{status}"))

async def pcc2_user(ctx, code):
    code = str(code)
    try:
        async with websockets.connect("ws://83.229.84.175:8082/TradingPlatform", max_size=99999999999) as ws:
            await ws.send('{"method":"getTrader","args":id}'.replace("id", code, 1))
            msg = json.loads(await ws.recv())
            if msg["response"] != None:
                totals = {"CPU": 0, "RAM": 0, "PCCase": 0, "PowerSupply": 0, "Drive": 0, "Cooler": 0, "Motherboard": 0, "Videocard": 0, "ThermalGrease": 0}
                stuff = msg["response"]
                user = stuff["user"]
                inventory = stuff["inventory"]
                for item in inventory:
                    totals[item["id"].split(".")[0]] += 1
                embed = discord.Embed(title=user['userName'])
                embed.add_field(name="ID", value=user['code'], inline=False)
                embed.add_field(name="Items", value=len(inventory), inline=False)
                embed.add_field(name="Cases", value=totals['PCCase'], inline=True)
                embed.add_field(name="Motherboards", value=totals['Motherboard'], inline=True)
                embed.add_field(name="CPUs", value=totals['CPU'], inline=True)
                embed.add_field(name="Coolers", value=totals['Cooler'], inline=True)
                embed.add_field(name="RAMs", value=totals['RAM'], inline=True)
                embed.add_field(name="Videocards", value=totals['Videocard'], inline=True)
                embed.add_field(name="Drives", value=totals['Drive'], inline=True)
                embed.add_field(name="Power Supplies", value=totals['PowerSupply'], inline=True)
                embed.add_field(name="Thermal Grease", value=totals['ThermalGrease'], inline=True)
                await ctx.respond(embed=embed)
            else:
                await ctx.respond(embed=discord.Embed(title="User Not Found", description=f"User with the ID {code} was not found!"))
            await ws.close()
    except:
        await ctx.respond(embed=discord.Embed(title="Failed To Get Data", description="The bot has failed to succesfully receive user data, most likely, the trading servers are offline."))
