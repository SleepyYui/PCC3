import discord
from discord.ext import commands
import websockets
import orjson
from asyncio import create_task
from cogs.pc_creator_commands.importantfunctions import (format_msg, definitions, live_check, bool_emoji, decrypt_currency, WS_HEADERS, get_account, upload_account, items, Rarity,
                                                         LEADERBOARDS, get_lb, LEADERBOARD_TITLES, LOADING, get_trader, get_userid) # the import is getting bigger and bigger
   
ICONS = {
    "Bitcoin": "<:Bitcoin:728463949892419624>",
    "Ethereum": "<:ethereum:932746985751076864>"
}
inv_skill = [0, 25, 55, 100, 150, 200, 300] # increase of inventory space with the skill level (skill level 6 -> +300 space and etc)
pc_item_keys = ["PcCases", "MotherBoards", "CPUs", "Videocards", "Drives", "PowerSuppllies", "Coolers"]
staff_ids = [1056941196196458507, 648546626637398046, 589435378147262464, 1058779237168992286, 697728131003580537, 697002610892341298, 1208540296527482890]

with open("json_files/promocodes.json", "rb") as file:
    promocodes = orjson.loads(file.read())

def format_time(s):
    res = ""
    mins = s // 60
    hrs = mins // 60
    
    if hrs > 0:
        res += f"{hrs}h"
    
    if mins > 0:
        mins -= hrs * 60
        res += f"{mins}m"
    
    if s > 0:
        s -= hrs * 3600 + mins * 60
        res += f"{s}s"

    return res

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

async def pcc2_promo(ctx):
    embed = discord.Embed(title="Promocodes")
    embed.add_field(name="List of known promocodes", value="- " + "\n- ".join(promocodes), inline=False)
    embed.add_field(name="❗️How to use promocodes", value='1. Go to the Shop (right side of the screen)\n2. Scroll to the right and press "Restore Purchases"\n3. Enter the promocode and click "Restore"', inline=False)
    return await ctx.respond(embed=embed)


async def pcc2_leaderboard(ctx, category):
    msg = await ctx.respond(LOADING)
    category = category.strip()
    try:
        result = await get_lb(LEADERBOARDS[category], count=10)
        result = result["records"]
    except:
        return await msg.edit_original_response(content="", embed=discord.Embed(title="Something went wrong while retrieving leaderboard data"))
    embed = discord.Embed(title=category + " Leaderboard")
    for place in result:
        position = place["position"]
        value = place["score"]
        value = round(value, 3) if type(value) == float else value
        if str(value)[-2:] == ".0":
            value = int(value)
        embed.add_field(name=f"{LEADERBOARD_TITLES.get(position, str(position) + '.')} {discord.utils.escape_markdown(place['payload']['user']['userName'])}", value=f"{value} {ICONS.get(category, category)}", inline=False)
    return await msg.edit_original_response(content="", embed=embed)


async def pcc2_user(ctx, code):
    msg = await ctx.respond(LOADING)
    code = str(code)    
    try:
        trader = await get_trader(code=code)
        if trader != None:
            totals = {"CPU": 0, "RAM": 0, "PCCase": 0, "PowerSupply": 0, "Drive": 0, "Cooler": 0, "Motherboard": 0, "Videocard": 0, "ThermalGrease": 0}
            for item in trader["inventory"]:
                totals[item["id"].split(".")[0]] += 1
            embed = discord.Embed(title=trader["payload"]["user"]["name"])
            embed.add_field(name="ID", value=trader["code"], inline=False)
            embed.add_field(name="Items", value=len(trader["inventory"]), inline=False)
            embed.add_field(name="Cases", value=totals['PCCase'])
            embed.add_field(name="Motherboards", value=totals['Motherboard'])
            embed.add_field(name="CPUs", value=totals['CPU'])
            embed.add_field(name="Coolers", value=totals['Cooler'])
            embed.add_field(name="RAMs", value=totals['RAM'])
            embed.add_field(name="Videocards", value=totals['Videocard'])
            embed.add_field(name="Drives", value=totals['Drive'], inline=True)
            embed.add_field(name="Power Supplies", value=totals['PowerSupply'])
            embed.add_field(name="Thermal Grease", value=totals['ThermalGrease'])
            await msg.edit_original_response(content="", embed=embed)
        else:
            await msg.edit_original_response(content="", embed=discord.Embed(title="User not found", description=f"User with the ID {code} was not found!"))
    except:
        await msg.edit_original_response(embed=discord.Embed(title="Failed to get data", description="Something went wrong."))

def is_staff(user):
    for role in user.roles:
        if role.id in staff_ids:
            return True
    return False

def is_rarity(item, rarity):
    return items.get(item["id"]) == rarity.value

def is_rarity_filter(rarity):
    def f(item):
        return is_rarity(item, rarity)
    return f

def process_pc(f, pc):
    in_pc = []

    for key in pc_item_keys:
        if key not in pc:
            continue
                
        for i in pc[key]:
            if f(i):
                in_pc.append(i)
        
    return in_pc

def of_rarity(rarity, account):
    inv = account["inventory"]
    f = is_rarity_filter(rarity)

    all_items = list(filter(f, inv["itemReferences"]))

    for pc in inv["PCs"]:
        all_items += process_pc(f, pc)

    building = account["BuildingStatus"]
    all_items += process_pc(f, building["ActiveBuildingPC"])
    all_items += process_pc(f, building["ActiveEditingPC"])
    return all_items 

def inspect_embed(account):
    e = discord.Embed(title=account["userName"])
    email = account["email"]
    if email == "":
        email = "❌"
    e.add_field(name="Email", value=email, inline=False)
    userhash = account["userHash"]
    userid = account["userId"]
    if userid == "":
        userid = f"guest.{userhash}"
    e.add_field(name="UserID", value=userid, inline=False)
    e.add_field(name="UserHash", value=userhash, inline=False)
    e.add_field(name="Suspect", value=bool_emoji(account["suspect"]), inline=False)
    e.add_field(name="Platform", value=account["platform"], inline=False)

    currencies = {}
    for currency in account["currency"]:
        value = decrypt_currency(account["currency"][currency])
        currencies[currency] = value
        e.add_field(name=currency.upper(), value=value)

    vip = account["accountInfo"]["hasSubscription"]
    visual_inventory = list(filter(lambda a: items.get(a["id"], Rarity.Gold.value) != Rarity.Gold.value, account["inventory"]["itemReferences"]))
    item_limit = 100 if account.get("hasNewInventorySystem") else 500
    invskill = account["userSkills"].get("InventoryCapacity", 0)
    if invskill > 6:
        invskill = 6
    
    item_limit += inv_skill[invskill]
    if vip:
        item_limit *= 10
    
    e.add_field(name="Level", value=account["level"], inline=False)
    e.add_field(name="Playtime", value=f'{format_time(account["playTime"])} ({account["playTime"]})', inline=False)

    e.add_field(name="VIP", value=bool_emoji(vip))
    e.add_field(name="No Ads", value=bool_emoji(account["adsRemoved"]))
    e.add_field(name="No Ads + X2", value=bool_emoji(account["adsRemovedUltimate"]))

    e.add_field(name="Actual Inventory", value=f'{len(account["inventory"]["itemReferences"])}', inline=False)
    e.add_field(name="Visual Inventory", value=f'{len(visual_inventory)}/{item_limit}', inline=False)
    e.add_field(name="Epic Items", value=len(of_rarity(Rarity.Epic, account)))
    e.add_field(name="Season Items", value=len(of_rarity(Rarity.Season, account)))
    e.add_field(name="Relict Items", value=len(of_rarity(Rarity.Relict, account)))
    return e

def inspect_view(msg, account, id):
    view = discord.ui.View(timeout=3600)
    view.add_item(SuspectButton(msg, account, id))
    return view

class SuspectButton(discord.ui.Button):
    def __init__(self, msg, account, userid):
        self.msg = msg
        self.account = account
        self.userid = userid

        super().__init__(label=f'{"Remove" if account["suspect"] else "Set"} Suspect')
    
    async def callback(self, interaction):
        if not is_staff(interaction.user):
            return interaction.response.send_message("This button is only available to staff members!")
        
        self.account["suspect"] = not self.account["suspect"]
        self.account["playTime"] += 500
        try:
            result = await upload_account(self.userid, self.account)
            assert result.status < 400
        except:
            await interaction.response.send_message("Failed to upload account", ephemeral=True)
        
        await interaction.response.send_message(f"{interaction.user} changed suspect status of the account")
        await self.msg.edit_original_response(embed=inspect_embed(self.account), view=inspect_view(self.msg, self.account, self.userid))

async def pcc2_inspect(ctx, method, data):
    msg = await ctx.respond(LOADING)
    id = data

    try:
        if method == "Email":
            id = await get_userid(data)
        elif method == "Trading ID":
            id = (await get_trader(code=data))["ID"]
        elif method == "UserHash":
            id = f"guest.{id}"
        
        assert id is not None
        assert id != ""
    except:
        return await msg.edit_original_response(content="Failed to get account ID")
    
    try:
        account = await get_account(id)
    except:
        return await msg.edit_original_response(content="Failed to get account data")
    
    await msg.edit_original_response(content="", embed=inspect_embed(account), view=inspect_view(msg, account, id))

async def pcc2_promocode_edit(ctx, promo):
    if promo in promocodes:
        promocodes.remove(promo)
        await ctx.respond(f"{promo} removed!", ephemeral=True)
    else:
        promocodes.append(promo)
        await ctx.respond(f"{promo} added!", ephemeral=True)
    with open("json_files/promocodes.json", "wb") as file:
        file.write(orjson.dumps(promocodes))