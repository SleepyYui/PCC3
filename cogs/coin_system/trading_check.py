
import json
import discord
from bank_functions import get_trading, get_trading_list, update_bank2, get_coins
from discord.ext import commands
from discord.ui import Button, View


class trading_check(commands.Cog):

    def __init__(self, client):
        self.client = client

    """@commands.slash_command(name="check_trades", description="Check your trades")
    async def check_trades_slash(self, ctx):
        trading_member = await get_trading()
        trading_list = await get_trading_list()
        open_trades = trading_member[str(ctx.author.id)]
        global length
        length = len(open_trades)
        #await ctx.send(open_trades)
        if len(open_trades) == 0:
            await ctx.respond("You have no trade offers")
            return
        else:
            global i
            i = 1
            send = "send"
            global button_next
            button_next = Button(emoji="➡", style=discord.ButtonStyle.primary)
            global button_back
            button_back = Button(emoji="⬅", style=discord.ButtonStyle.primary)
            global button_accept
            button_accept = Button(label="Accept", style=discord.ButtonStyle.success)
            global button_decline
            button_decline = Button(label="Decline", style=discord.ButtonStyle.danger)

            button_back.disabled = True
            if length == 1:
                button_next.disabled = True
            
            global view
            view1 = View()
            view1.add_item(button_back)
            view1.add_item(button_decline)
            view1.add_item(button_accept)
            view1.add_item(button_next)
            await ctx.respond("Use `/trading` if you want to trade your stuff.", ephemeral=True)
            await self.check_trade(ctx, i, send, view1)


    @commands.command(name="checktrades")
    async def ctrade(self, ctx):
        trading_member = await get_trading()
        trading_list = await get_trading_list()
        open_trades = trading_member[str(ctx.author.id)]
        global length
        length = len(open_trades)
        #await ctx.send(open_trades)
        if len(open_trades) == 0:
            await ctx.send("You have no trade offers.")
            return
        else:
            global i
            i = 1
            send = "send"
            global button_next
            button_next = Button(emoji="➡", style=discord.ButtonStyle.primary)
            global button_back
            button_back = Button(emoji="⬅", style=discord.ButtonStyle.primary)
            global button_accept
            button_accept = Button(label="Accept", style=discord.ButtonStyle.success)
            global button_decline
            button_decline = Button(label="Decline", style=discord.ButtonStyle.danger)

            button_back.disabled = True
            if length == 1:
                button_next.disabled = True
            
            global view
            view1 = View()
            view1.add_item(button_back)
            view1.add_item(button_decline)
            view1.add_item(button_accept)
            view1.add_item(button_next)
            await self.check_trade(ctx, i, send, view1)
            



    async def check_trade(self, ctx, i, send, view1):
        trading_member = await get_trading()
        trading_list = await get_trading_list()
        open_trades = trading_member[str(ctx.author.id)]
        global length
        length = len(open_trades)
        #print(length)
        #print(i)
        trade_id = i - 1
        
        #global trades_list
        trades_list = trading_member[str(ctx.author.id)]
        #global actual_trade_id
        actual_trade_id = trades_list[trade_id]
        trade_guy_1 = trading_list[f"trade_{actual_trade_id}"]["trade_guy_1"]
        
        if str(ctx.author.id) == trade_guy_1:
            trading_partner = trading_list[f"trade_{actual_trade_id}"]["trade_guy_2"]
        
        else:
            trading_partner = trading_list[f"trade_{actual_trade_id}"]["trade_guy_1"]   

        trades_list_partner = trading_member[str(trading_partner)]    

        give_type = trading_list[f"trade_{actual_trade_id}"]["give_type"]
        want_type = trading_list[f"trade_{actual_trade_id}"]["want_type"]

        if give_type == "parts":   
            give_parts = trading_list[f"trade_{actual_trade_id}"]["give_item"]
            give_parts_shown = ",\n".join(give_parts)

            if want_type == "parts":
                want_parts = trading_list[f"trade_{actual_trade_id}"]["want_item"]
                want_parts_shown = ",\n".join(want_parts)
                embed = discord.Embed(title=f"Trade {i}", description=f"**Trading partner**\n<@{trading_partner}>\n\n**What you give**\n{give_parts_shown}\n\n**What you receive**\n{want_parts_shown}", color=13565696)

            if want_type == "coins":
                want_money = trading_list[f"trade_{actual_trade_id}"]["want_coins_amount"]
                embed = discord.Embed(title=f"Trade {i}", description=f"**Trading partner**\n<@{trading_partner}>\n\n**What you give**\n{give_parts_shown}\n\n**What you receive**\n{want_money}<:bot_icon:951868023503986699>", color=13565696)    
       
        if give_type == "coins":
            give_money = trading_list[f"trade_{actual_trade_id}"]["give_coins_amt"]

            if want_type == "parts":
                want_parts = trading_list[f"trade_{actual_trade_id}"]["want_item"]
                want_parts_shown = ", ".join(want_parts)
                embed = discord.Embed(title=f"Trade {i}", description=f"**Trading partner**\n<@{trading_partner}>\n\n**What you give**\n{give_money}<:bot_icon:951868023503986699>\n\n**What you receive**\n{want_parts_shown}", color=13565696)

            if want_type == "coins":
                want_money = trading_list[f"trade_{actual_trade_id}"]["want_coins_amount"]
                embed = discord.Embed(title=f"Trade {i}", description=f"**Trading partner**\n<@{trading_partner}>\n\n**What you give**\n{give_money}<:bot_icon:951868023503986699>\n\n**What you receive**\n{want_money}<:bot_icon:951868023503986699>", color=13565696)    

        member = await self.client.fetch_user(trading_partner)
        embed.set_thumbnail(url=member.avatar.url)
        if send == "send":
            global msg
            msg = await ctx.send(embed=embed, view=view1)
        if send == "edit":
            await msg.edit(embed=embed, view=view1)    

        async def button_next_callback(interaction):
            if interaction.user != ctx.author:
                return   

            button_back.disabled = False
            j = i + 1
            send = "edit"
            if j == length:
                button_next.disabled = True
            await self.check_trade(ctx, j, send, view1)    

        async def button_back_callback(interaction):
            if interaction.user != ctx.author:
                return   

            button_next.disabled = False
            j = i - 1
            send = "edit"
            if j == 1:
                button_back.disabled = True
            await self.check_trade(ctx, j, send, view1)   

        async def button_decline_callback(interaction):
            if interaction.user != ctx.author:
                return        

            trades_list1 = trades_list[trade_id]
            trades_list2 = trading_member[str(ctx.author.id)]
            trades_list3 = trading_member[str(trading_partner)]

            trades_list2.remove(trades_list1)
            trades_list3.remove(trades_list1)
            #if i == 1:
            #    j = i + 1
            #    button_back.disabled = True
            #    button_next.disabled = False
            if length == 1:
                await msg.delete()
                return True
            if i == length:
                j = i - 1
                if length == 2:
                    button_back.disabled = True
                    button_next.disabled = True
                else:
                    button_back.disabled = False
                    button_next.disabled = True
            else:
                j = i
                if i == 1:
                    button_back.disabled = True
                    button_next.disabled = False 
                else:
                    button_back.disabled = False
                    button_next.disabled = False        

            with open("json_files/trading_member.json", "w") as f:
                json.dump(trading_member,f)     

            send = "edit"    

            await self.check_trade(ctx, j, send, view1)               


        async def button_accept_callback(interaction):
            if interaction.user != ctx.author:
                return        

            with open("json_files/useritems.json", "r") as f:
                    useritems = json.load(f)

            trading_member = await get_trading()
            trading_list = await get_trading_list()    

            #trades_list = trading_member[str(ctx.author.id)]
            give_type = trading_list[f"trade_{actual_trade_id}"]["give_type"]
            want_type = trading_list[f"trade_{actual_trade_id}"]["want_type"]

            if give_type == "parts":

                give_parts = trading_list[f"trade_{actual_trade_id}"]["give_item"]

                items = useritems[str(ctx.author.id)]     

                x = 0

                missing_parts = []

                while x<len(give_parts):
                    if give_parts[x] in items:
                        pass
                    else:
                        missing_parts.append(give_parts[x])
                    x += 1

                if len(missing_parts) != 0:
                    missing_parts_shown = ", ".join(missing_parts)
                    await interaction.message.channel.send(f"You don't have the following items: **{missing_parts_shown}**.")    
                    return True    

                #print("weird")    

                if want_type == "parts": 
                    
                    want_parts = trading_list[f"trade_{actual_trade_id}"]["want_item"]

                    items_partner = useritems[str(trading_partner)] 

                    y = 0

                    missing_parts_partner = []

                    while y<len(want_parts):
                        if want_parts[y] in items_partner:
                            pass
                        else:
                            missing_parts_partner.append(want_parts[y])
                        y += 1
                        
                    if len(missing_parts_partner) != 0:
                        missing_parts_partner_shown = ", ".join(missing_parts_partner)
                        await interaction.message.channel.send(f"Your partner doesn't own the following items: **{missing_parts_partner_shown}**")    
                        return True     

                    z = 0

                    while z<len(give_parts):
                        items.remove(give_parts[z])
                        items_partner.append(give_parts[z])
                        z += 1

                    w = 0

                    while w<len(want_parts):
                        items_partner.remove(want_parts[w])
                        items.append(want_parts[w])
                        w += 1   

                    with open("json_files/useritems.json", "w") as f:
                        json.dump(useritems,f)   
                    #await interaction.message.channel.send("SUCCESS")   


                if want_type == "coins":

                    want_money = trading_list[f"trade_{actual_trade_id}"]["want_coins_amount"]

                    users_coins = await get_coins()

                    wallet_money_amount_partner = users_coins[str(trading_partner)]

                    items_partner = useritems[str(trading_partner)] 

                    if want_money > wallet_money_amount_partner:
                        await interaction.message.channel.send("Your trading partner does not have enough money in their wallet")
                        return True

                    z = 0

                    while z<len(give_parts):
                        items.remove(give_parts[z])
                        items_partner.append(give_parts[z])
                        z += 1

                    mode = "wallet"    

                    error = await update_bank2(ctx.author, want_money, mode)

                    if error == "error":
                            await interaction.message.channel.send
                            return True

                    error = await update_bank2(trading_partner, -1*want_money, mode)

                    if error == "error":
                            await interaction.message.channel.send
                            return True

                    with open("json_files/useritems.json", "w") as f:
                        json.dump(useritems,f)   
                    #await interaction.message.channel.send("SUCCESS")   

            if give_type == "coins":

                give_money = trading_list[f"trade_{actual_trade_id}"]["give_coins_amt"]    

                users_coins = await get_coins()

                wallet_money_amount = users_coins[str(ctx.author.id)]

                if give_money > wallet_money_amount:
                    await interaction.message.channel.send("Your don't have enough money in your wallet.")
                    return True



                if want_type == "parts":
                    
                    want_parts = trading_list[f"trade_{actual_trade_id}"]["want_item"]

                    items = useritems[str(ctx.author.id)] 

                    items_partner = useritems[str(trading_partner)] 

                    y = 0

                    missing_parts_partner = []

                    while y<len(want_parts):
                        if want_parts[y] in items_partner:
                            pass
                        else:
                            missing_parts_partner.append(want_parts[y])
                        y += 1

                    if len(missing_parts_partner) != 0:
                        missing_parts_partner_shown = ", ".join(missing_parts_partner)
                        await interaction.message.channel.send(f"Your partner doesn't own the following items: **{missing_parts_partner_shown}**.")    
                        return True     

                    w = 0

                    while w<len(want_parts):
                        items_partner.remove(want_parts[w])
                        items.append(want_parts[w])
                        w += 1   

                    mode = "wallet"    

                    error = await update_bank2(ctx.author, -1*give_money, mode)

                    if error == "error":
                            await interaction.message.channel.send
                            return True

                    error = await update_bank2(trading_partner, give_money, mode)

                    if error == "error":
                            await interaction.message.channel.send
                            return True

                    with open("json_files/useritems.json", "w") as f:
                        json.dump(useritems,f)   
                    #await interaction.message.channel.send("SUCCESS")   


                    if want_type == "coins":

                        give_money = trading_list[f"trade_{actual_trade_id}"]["give_coins_amt"]    

                        users_coins = await get_coins()

                        wallet_money_amount = users_coins[str(ctx.author.id)]

                        if give_money > wallet_money_amount:
                            await interaction.message.channel.send("Your dont have enough money in your wallet.")
                            return True

                        want_money = trading_list[f"trade_{actual_trade_id}"]["want_coins_amount"]

                        wallet_money_amount_partner = users_coins[str(trading_partner)]

                        if want_money > wallet_money_amount_partner:
                            await interaction.message.channel.send("Your trading partner does not have enough money in their wallet.")
                            return True

                        mode = "wallet"    

                        error = await update_bank2(ctx.author, -1*give_money, mode)

                        if error == "error":
                            await interaction.message.channel.send
                            return True

                        error = await update_bank2(trading_partner, -1*want_money, mode)

                        if error == "error":
                            await interaction.message.channel.send
                            return True

                        error = await update_bank2(ctx.author, want_money, mode)

                        if error == "error":
                            await interaction.message.channel.send
                            return True

                        error = await update_bank2(trading_partner, give_money, mode)

                        if error == "error":
                            await interaction.message.channel.send
                            return True


                        with open("json_files/useritems.json", "w") as f:
                            json.dump(useritems,f)   
                        #wait interaction.message.channel.send("SUCCESS")               


            #print("GEHT")
            trades_list1 = trades_list[trade_id]
            trades_list2 = trading_member[str(ctx.author.id)]
            trades_list3 = trading_member[str(trading_partner)]

            trades_list2.remove(trades_list1)
            trades_list3.remove(trades_list1)

            if length == 1:
                await msg.delete()
                return True
            if i == length:
                j = i - 1
                if length == 2:
                    button_back.disabled = True
                    button_next.disabled = True
                else:
                    button_back.disabled = False
                    button_next.disabled = True
            else:
                j = i
                if i == 1:
                    button_back.disabled = True
                    button_next.disabled = False 
                else:
                    button_back.disabled = False
                    button_next.disabled = False        

            with open("json_files/trading_member.json", "w") as f:
                json.dump(trading_member,f)     

            send = "edit"    

            await self.check_trade(ctx, j, send, view1)

        button_next.callback = button_next_callback     
        button_back.callback = button_back_callback   
        button_decline.callback = button_decline_callback
        button_accept.callback = button_accept_callback
"""


def setup(client):
    client.add_cog(trading_check(client))
