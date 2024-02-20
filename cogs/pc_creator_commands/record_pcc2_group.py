import discord
from discord.ext import commands
import websockets
import json
from asyncio import create_task
from cogs.pc_creator_commands.importantfunctions import (format_msg, definitions, live_check, bool_emoji, decrypt_currency,
                                                         PUBLIC_PROMOCODE_LIST, WS_HEADERS, get_account, upload_account,
                                                         LEADERBOARDS, get_lb, LEADERBOARD_TITLES, LOADING, get_trader, get_userid) # the import is getting bigger and bigger
   
ICONS = {
    "Bitcoin": "<:Bitcoin:728463949892419624>",
    "Ethereum": "<:ethereum:932746985751076864>"
}

staff_ids = [1056941196196458507, 648546626637398046, 589435378147262464, 1058779237168992286, 697728131003580537, 697002610892341298, 1208540296527482890]

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
    embed.add_field(name="List of known promocodes", value="- " + "\n- ".join(PUBLIC_PROMOCODE_LIST), inline=False)
    embed.add_field(name="❗️How to use promocodes", value='1. Go to the Shop (right side of the screen)\n2. Scroll to the right and press "Restore Purchases"\n3. Enter the promocode and click "Restore"', inline=False)
    return await ctx.respond(embed=embed)


async def pcc2_leaderboard(ctx, category):
    msg = await ctx.respond(LOADING)
    category = category.strip()
    try:
        result = await get_lb(LEADERBOARDS[category], count=10)
        result = result["records"]
    except:
        return await msg.edit_original_message(content="", embed=discord.Embed(title="Something went wrong while retrieving leaderboard data"))
    embed = discord.Embed(title=category + " Leaderboard")
    for place in result:
        position = place["position"]
        value = place["score"]
        value = round(value, 3) if type(value) == float else value
        if str(value)[-2:] == ".0":
            value = int(value)
        embed.add_field(name=f"{LEADERBOARD_TITLES.get(position, str(position) + '.')} {discord.utils.escape_markdown(place['payload']['user']['userName'])}", value=f"{value} {ICONS.get(category, category)}", inline=False)
    return await msg.edit_original_message(content="", embed=embed)


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
            await msg.edit_original_message(content="", embed=embed)
        else:
            await msg.edit_original_message(content="", embed=discord.Embed(title="User not found", description=f"User with the ID {code} was not found!"))
    except:
        await msg.edit_original_message(embed=discord.Embed(title="Failed to get data", description="Something went wrong."))

def is_staff(user):
    for role in user.roles:
        if role.id in staff_ids:
            return True
    return False

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

    for currency in account["currency"]:
        value = decrypt_currency(account["currency"][currency])
        e.add_field(name=currency.upper(), value=value)

    e.add_field(name="Level", value=account["level"], inline=False)

    vip = account["accountInfo"]["hasSubscription"]
    e.add_field(name="VIP", value=bool_emoji(vip))
    e.add_field(name="No Ads", value=bool_emoji(account["adsRemoved"]))
    e.add_field(name="No Ads + X2", value=bool_emoji(account["adsRemovedUltimate"]))

    e.add_field(name="Inventory", value=f'{len(account["inventory"]["itemReferences"])}/{"5000" if vip else "500"}', inline=False)
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
        await self.msg.edit_original_message(embed=inspect_embed(self.account), view=inspect_view(self.msg, self.account, self.userid))

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
        return await msg.edit_original_message(content="Failed to get account ID")
    
    try:
        account = await get_account(id)
    except:
        return await msg.edit_original_message(content="Failed to get account data")
    
    await msg.edit_original_message(content="", embed=inspect_embed(account), view=inspect_view(msg, account, id))