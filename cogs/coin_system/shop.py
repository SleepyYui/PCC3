import discord
from discord.ext import commands
from discord.ui import Button, View
import json
from discord import Option
from discord.commands import permissions


class Shop_Select(discord.ui.View):

    with open("json_files/shop.json", "r") as f:
            items = json.load(f)

    options = []

    for item_list in items:
        name = item_list["item_name"]
        price = item_list["price"]
        emoji = item_list["emoji"]

        options.append(discord.SelectOption(label=name, description=f"Price: {price}"))

    async def get_coins(self):
            with open("json_files/usercoins.json", "r") as f:
                users_coins = json.load(f)
            return users_coins

    async def get_useritems(self):
                with open("json_files/useritems.json", "r") as f:
                    users_items = json.load(f)
                return users_items

    async def sub_coins(self, user, subprice):

        with open("json_files/usercoins.json", "r") as f:
                users_coins = json.load(f)
        user = str(user)
        if user in users_coins:
            purse = users_coins[user]
            if purse >= subprice:
                successpurchase = 'successpurchase'
                return successpurchase
            else:
                failpurchase = 'failpurchase'
                return failpurchase
        else:
            users_coins[str(user)] = {}
            users_coins[str(user)] = 0
            nocoins = 'nocoins'
        return nocoins

    @discord.ui.select(placeholder="Choose the item you want to buy", min_values=1, max_values=1, options=options)
    async def callback(self, select, interaction : discord.Interaction):

        global shop_context
        if interaction.user != shop_context:
            await interaction.response.send_message("Use /shop to use the shop", ephemeral=True)


        with open("json_files/shop.json", "r") as f:
            items = json.load(f)
        responder = str(interaction.user.id)
        item_name = select.values[0]
        for item in items:
            if item["item_name"] == item_name:
                subprice = item["price"]
        status = await self.sub_coins(responder, subprice)
        with open("json_files/usercoins.json", "r") as f:
                users_coins = json.load(f)
        if responder in users_coins:
            purse = users_coins[str(responder)]
            if status == 'successpurchase':
                with open("json_files/useritems.json", "r") as f:
                        users_items = json.load(f)
                twoitem = False
                if responder in users_items:
                    for testitem in users_items[str(responder)]:
                        if testitem == item_name:
                            twoitem = True

                async def newuseritem_member(self):
                    with open("json_files/useritems.json", "r") as f:
                        users_items = json.load(f)
                    if str(responder) in users_items:
                        currentitem = users_items[str(responder)]
                        currentitem = currentitem + [item_name]
                        users_items[str(responder)] = currentitem
                        with open("json_files/useritems.json", "w") as f:
                            json.dump(users_items, f)
                        return True
                    else:
                        users_items[str(responder)] = [f"{item_name}"]
                        with open("json_files/useritems.json", "w") as f:
                            json.dump(users_items, f)
                    return False

                if True: #twoitem != #Double items enabled due to the Update
                    subcoins = int(subprice)
                    purse -= subcoins
                    users_coins[str(responder)] = purse
                    with open("json_files/usercoins.json", "w") as f:
                        json.dump(users_coins,f)
                    await newuseritem_member(self)
                    await interaction.message.edit(content=f"You bought a {item_name} for **{subprice}**<:bot_icon:951868023503986699> and have **{purse}**<:bot_icon:951868023503986699> remaining.", view=None)
                #else:
                    #await interaction.message.edit(content=f"You can't buy a {item_name} for **{subprice}**<:bot_icon:951868023503986699> because you already have it", view=None)
            elif status == 'failpurchase':
                await interaction.message.edit(content=f"You do not have enough money for **{item_name}**. It costs **{subprice}**<:bot_icon:951868023503986699> and you only have **{purse}**<:bot_icon:951868023503986699>", view=None)
            elif status == 'nocoins':
                await interaction.message.edit(content=f"Something went completely wrong and the Bot is now broken and has probably crashed, or all of the coin-data has been lost", view=None)
        else:
            await interaction.message.edit(content=f"You somehow don't have any coins yet.", view=None)



class shop(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def get_items(self):
        with open("json_files/shop.json", "r") as f:
            items = json.load(f)
        return items

    async def get_coins(self):
            with open("json_files/usercoins.json", "r") as f:
                users_coins = json.load(f)
            return users_coins

    async def get_useritems(self):
                with open("json_files/useritems.json", "r") as f:
                    users_items = json.load(f)
                return users_items

    @commands.slash_command(name='shop', description='Buy items')
    async def shop(self, ctx):
        global shop_context
        shop_context = ctx.author
        view = Shop_Select()
        await ctx.respond("Choose the item you want to buy", view=view)

    


    """@commands.slash_command(name="new_item")
    @permissions.has_any_role(951207540472029195, 951464246506565683)
    async def new_item(self, ctx, item_name : Option(str, 'Item Name', required=True), price: Option(int, 'Price (only numbers)', required=True), emoji: Option(str, required=False)):
        shopjson = open("json_files/shop.json", "r")
        items = json.load(shopjson)
        if type(items) is dict:
            items = [items]

        for itemname in items:
            if item_name.lower() == itemname["item_name"].lower():
                await ctx.respond(f"Could not add " + item_name + "since it is already added.")
                return False

        if len(items) < 25:
            items.append({
            'item_name': item_name,
            'price': price,
            'emoji': emoji
            })
            with open("json_files/shop.json", "w") as outshopjson:
                json.dump(items,outshopjson)
            await ctx.respond(f"Added {item_name} \nprice: {price} \nemoji: {emoji}\n\nIt will be added to /shop on the next restart.")
        else:
            await ctx.respond(f"Could not add " + item_name + "since there are already 25(Max. amount)")
                

            

    @commands.slash_command(name="rem_item")
    @permissions.has_any_role(951207540472029195, 951464246506565683)
    async def rem_item(self, ctx, item_name : Option(str, 'Item Name', required=True)):
        shopjson = open("json_files/shop.json", "r")
        items = json.load(shopjson)
        if type(items) is dict:
            items = [items]
        value = False
        lira = 0
        for item in items:
            if item["item_name"] == item_name:
                items.pop(lira)
                await ctx.respond(f"Removed {item_name}")
                value = True
                break
            lira += 1
        if value == False:
            await ctx.respond(f"Could not remove {item_name}")


        with open("shop.json", "w") as outshopjson:
            json.dump(items,outshopjson)

    @commands.slash_command(name="list_item")
    @permissions.has_any_role(951207540472029195, 951464246506565683)
    async def list_item(self, ctx):
        shopjson = open("json_files/shop.json", "r")
        items = json.load(shopjson)
        itemprint = []
        if type(items) is dict:
            items = [items]

        for item_name in items:
            itemprint.append(item_name)
        await ctx.respond(f"```json\n{itemprint}\n```")"""




def setup(client):
    client.add_cog(shop(client))