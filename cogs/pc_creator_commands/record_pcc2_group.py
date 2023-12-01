import discord
from discord.ext import commands
import websockets
import json
from asyncio import create_task
from cogs.pc_creator_commands.importantfunctions import (format_msg, definitions, live_check, get_promocode, ITEM_DB, PROMOCODE_DB, 
                                                         FIELD_NAMES, PUBLIC_PROMOCODE_LIST, WS_HEADERS, get_power_lb, 
                                                         CURRENCIES, get_crypto_lb, LEADERBOARD_TITLES) # the import is getting bigger and bigger
   

async def record_pcc2(ctx): 
    embed = discord.Embed(title="__PCC2 World Record__", description="This is the current PCC2 World Record PC", color=13565696)
    embed.add_field(name=f":small_blue_diamond: Achieved by", value="<@530725164703416340> Vinrellren#9894 (530725164703416340)", inline=False)
    embed.add_field(name=f":small_blue_diamond: Details", value="Max overclocks are needed to get the highest score \n• MX-4 45 Thermal Paste is required and needs to cover \n100% of the CPU \n• Max overclocking skill is required.", inline=False)
    embed.add_field(name=f":small_blue_diamond: Score achieved", value="`3.313.336`", inline=False)
    embed.set_image(url="https://media.discordapp.net/attachments/748122380383027210/959825115485470790/1648910536234.jpg")

    await ctx.respond(embed=embed)   

async def pcc2_status(ctx):
    checks = list(map(lambda item: format_msg(item, "loading"), definitions.keys()))
    response = await ctx.respond(embed=discord.Embed(title="Status", description=''.join(checks).strip()))
    for index, item in enumerate(definitions):
        create_task(live_check(index, item, checks, response))

async def pcc2_promo(ctx, code_name):
    if code_name:
        try:
            code = await get_promocode(code_name)
        except:
            return await ctx.respond(embed=discord.Embed(title="Failed to retrieve promocode code")) 
        if not code:
            return await ctx.respond(embed=discord.Embed(title="Promocode not found!"))
        embed = discord.Embed(title=code_name)
        for item in code:
            if item in FIELD_NAMES:
                value = code[item]
                if type(value) == list:
                    combined = []
                    for thing in value:
                        if thing != "":
                            combined.append(ITEM_DB[thing]) 
                    if len(combined) > 0:
                        embed.add_field(name=FIELD_NAMES[item], value=", ".join(combined))
                elif value:
                    result = ""
                    if type(value) == bool:
                        result = "✅" if value else "❌"
                    else:
                        result = value
                    embed.add_field(name=FIELD_NAMES[item], value=result)
        return await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(title="Promocodes")
        embed.add_field(name="List of known promocodes", value="- " + "\n- ".join(PUBLIC_PROMOCODE_LIST), inline=False)
        embed.add_field(name="❗️How to use promocodes", value='1. Go to the Shop (right side of the screen)\n2. Scroll to the right and press "Restore Purchases"\n3. Enter the promocode and click "Restore"', inline=False)
        return await ctx.respond(embed=embed)


async def pcc2_leaderboard(ctx, category):
    category = category.strip()
    try:
        if category == "PC Score":
            result = await get_power_lb()
        elif category in CURRENCIES:
            result = await get_crypto_lb(CURRENCIES[category])
        else:
            raise NameError
    except:
        return await ctx.respond(embed=discord.Embed(title="Something went wrong while retrieving leaderboard data"))
    embed = discord.Embed(title=category + " Leaderboard")
    for place in result:
        position = place['UserPosition']
        value = place['Value']
        value = round(value, 3) if type(value) == float else value
        embed.add_field(name=f"{LEADERBOARD_TITLES.get(position, str(position) + '.')} {discord.utils.escape_markdown(place['NickName'])}", value=f"{value} {category}", inline=False)
    return await ctx.respond(embed=embed)


async def pcc2_user(ctx, code):
    code = str(code)
    try:
        async with websockets.connect("ws://83.229.84.175:8082/TradingPlatform", max_size=99999999999, extra_headers=WS_HEADERS) as ws:
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
                embed.add_field(name="Cases", value=totals['PCCase'])
                embed.add_field(name="Motherboards", value=totals['Motherboard'])
                embed.add_field(name="CPUs", value=totals['CPU'])
                embed.add_field(name="Coolers", value=totals['Cooler'])
                embed.add_field(name="RAMs", value=totals['RAM'])
                embed.add_field(name="Videocards", value=totals['Videocard'])
                embed.add_field(name="Drives", value=totals['Drive'], inline=True)
                embed.add_field(name="Power Supplies", value=totals['PowerSupply'])
                embed.add_field(name="Thermal Grease", value=totals['ThermalGrease'])
                await ctx.respond(embed=embed)
            else:
                await ctx.respond(embed=discord.Embed(title="User Not Found", description=f"User with the ID {code} was not found!"))
            await ws.close()
    except:
        await ctx.respond(embed=discord.Embed(title="Failed To Get code", description="The bot has failed to succesfully receive user data, most likely, the trading servers are offline."))
