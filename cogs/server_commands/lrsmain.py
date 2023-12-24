import discord
from discord.ext import commands
from datetime import datetime
import json
from datetime import timedelta
from datetime import date
from discord.utils import get
import schedule
import time
from PIL import Image, ImageDraw, ImageFont
import asyncio
from discord.ext import tasks
from discord import Option
from discord.commands import permissions
import random


class levelroles(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        schedule.every().day.at("00:00").do(self.lrs_stats) 
        
     
    @commands.command(aliases=["levelroles", "lrs", "rank"])
    async def lrs_normal_command(self, ctx, member:discord.Member = None):
        #if not ctx.author.id == 695229647021015040:
        #    return
        send = ctx.send
        await self.lrs(ctx , send, member)


    @commands.slash_command(name="lrs", description="Sends your current levelroles progress")
    async def lrs_slash_command(self, ctx, member: Option(discord.Member, required = False)):
        #if not ctx.author.id == 695229647021015040:
        #    return
        send = ctx.respond
        await self.lrs(ctx , send, member)    
            
    async def lrs(self, ctx, send, member):
        if member == None:
            await self.new_member(ctx.author)
        else:
            await self.new_member(member)    

        if member == None:
            member = ctx.author
            you = "You"
            your = "Your"
            your2 = "your"
            have = "have"
            dont = "don't"

        else:
            you = "He/She"   
            your = "His/Her"
            your2 = "his/her"
            have = "has"
            dont = "doesn't"

        user = member

        users = await self.get_messages()



        messages_amt_str = users[str(user.id)]
        messages_amt = int(messages_amt_str)
    

        if member in ctx.guild.members: # checks if the provided member is in the current server
            date_now = date.today()
            join_date = member.joined_at.date()
            delta = date_now - join_date
            delta_int = int(delta.days)
            reached_level_1 = False
            reached_level_2 = False
            reached_level_3 = False
            reached_level_4 = False
            reached_level_5 = False
            member = ctx.guild.get_member(member.id) # Get the member object of the user

            if member == self.client.user:
                level = discord.Embed(title=f"{member.display_name}'s Levels", description=f"{you} {dont} {have} any level roles yet \n{your} next level role is **Level 1** and here's {your2} progress:", color=13565696)
                message_field = int(1000)
                date_field = int(60)
                if messages_amt >= message_field and not get(member.roles, name="Level 1"):
                    emoji = ":white_check_mark:"
                else:
                    emoji = ":x:"
                if delta_int >= date_field and not get(member.roles, name="Level 1"):
                    date_emoji = ":white_check_mark:"
                else:
                    date_emoji = ":x:"    
                    
            if get(member.roles, name="Level 1"): # Check if this role is in the member's roles
                level = discord.Embed(title=f"{member.display_name}'s Level", description=f"{you} already {have} the **Level 1** role \n{your} next level role is **Level 2** and here's {your2} progress:", colour=13565696)
                message_field = int(2000)
                date_field = int(90)
                if messages_amt >= message_field and not get(member.roles, name="Level 2"):
                    emoji = ":white_check_mark:"
                else:
                    emoji = ":x:" 
                if delta_int >= date_field and not get(member.roles, name="Level 2"):
                    date_emoji = ":white_check_mark:"
                else:
                   date_emoji = ":x:"    
                if messages_amt >= message_field and delta_int >= date_field and not get(member.roles, name="Level 2"):
                    reached_level_2 = True    
                if get(member.roles, name="Level 2"):
                    level = discord.Embed(title=f"{member.display_name}'s Levels", description=f"{you} already {have} the **Level 1** and **Level 2** roles \n{your} next level role is **Level 3** and here's {your2} progress:", colour=13565696)
                    message_field = int(4000)
                    date_field = int(120)
                    if messages_amt >= message_field and not get(member.roles, name="Level 3"):
                        emoji = ":white_check_mark:"
                    else:
                        emoji = ":x:"
                    if delta_int >= date_field and not get(member.roles, name="Level 3"):
                        date_emoji = ":white_check_mark:"
                    else:
                        date_emoji = ":x:"    
                    if messages_amt >= message_field and delta_int >= date_field and not get(member.roles, name="Level 3"):
                        reached_level_3 = True
                    if get(member.roles, name="Level 3"):
                        level = discord.Embed(title=f"{member.display_name}'s Levels", description=f"{you} already {have} the **Level 1**, **Level 2** and **Level 3** roles \n{your} next level role is **Level 4** and here's {your2} progress:", colour=13565696)
                        message_field = int(8000)
                        date_field = int(150)
                        if messages_amt >= message_field and not get(member.roles, name="Level 4"):
                            emoji = ":white_check_mark:"
                        else:
                            emoji = ":x:"
                        if delta_int >= date_field and not get(member.roles, name="Level 4"):
                            date_emoji = ":white_check_mark:"
                        else:
                            date_emoji = ":x:"    
                        if messages_amt >= message_field and delta_int >= date_field and not get(member.roles, name="Level 4"):
                            reached_level_4 = True
                        if get(member.roles, name="Level 4"):
                            level = discord.Embed(title=f"{member.display_name}'s Levels", description=f"{you} already {have} the **Level 1**, **Level 2**, **Level 3** and **Level 4** roles \n{your} next level role is **Level 5** and here's {your2} progress:", colour=13565696)    
                            message_field = int(16000)
                            date_field = int(180)
                            if messages_amt >= message_field and not get(member.roles, name="Level 5"):
                                emoji = ":white_check_mark:"
                            else:
                                emoji = ":x:"
                            if delta_int >= date_field and not get(member.roles, name="Level 5"):
                                date_emoji = ":white_check_mark:"
                            else:
                               date_emoji = ":x:"    
                            if messages_amt >= message_field and delta_int >= date_field and not get(member.roles, name="Level 5"):
                                reached_level_5 = True    
                            if get(member.roles, name="Level 5"):
                                level = discord.Embed(title=f"{member.display_name}'s Levels", description=f"{you} already {have} **all** of the level **roles**. Here's {your2} progress:", colour=13565696)  
                                emoji = ":gem:"
                                date_emoji = ":gem:"
            else:
                level = discord.Embed(title=f"{member.display_name}'s Levels", description=f"{you} {dont} {have} any level roles yet \n{your} next level role is **Level 1** and here's {your2} progress:", color=13565696)
                message_field = int(1000)
                date_field = int(60)
                if messages_amt >= message_field and not get(member.roles, name="Level 1"):
                    emoji = ":white_check_mark:"
                else:
                    emoji = ":x:"
                if delta_int >= date_field and not get(member.roles, name="Level 1"):
                    date_emoji = ":white_check_mark:"
                else:
                    date_emoji = ":x:"    
                if messages_amt >= message_field and delta_int >= date_field and not get(member.roles, name="Level 1"):
                    reached_level_1 = True    
            

        else:
           await send("Can't find this user")

        embed = level
        embed.add_field(name="Messages", value=f"{emoji} {messages_amt}/{message_field}")
        embed.add_field(name="Days", value=f"{date_emoji} {delta_int}/{date_field}")
        try:    
            embed.set_thumbnail(url=member.avatar.url)
        except:
            pass    
        await send(embed=embed)

        if reached_level_1 == True:
            role = discord.utils.get(ctx.guild.roles, name="Level 1")  
            await ctx.send(f"{you} received the **Level 1** role")
            await member.add_roles(role)   

        if reached_level_2 == True:
            role = discord.utils.get(ctx.guild.roles, name="Level 2")
            await ctx.send(f"{you} received the **Level 2** role")
            await member.add_roles(role)

        if reached_level_3 == True:
            role = discord.utils.get(ctx.guild.roles, name="Level 3")
            await ctx.send(f"{you} received the **Level 3** role")
            await member.add_roles(role)  

        if reached_level_4 == True:
            role = discord.utils.get(ctx.guild.roles, name="Level 4")  
            await ctx.send(f"{you} received the **Level 4** role")
            await member.add_roles(role)   

        if reached_level_5 == True:
            role = discord.utils.get(ctx.guild.roles, name="Level 5")  
            await ctx.send(f"{you} received the **Level 5** role")
            await member.add_roles(role)       


    async def get_messages(self):
        with open("json_files/userLevels.json", "r") as f:
            users = json.load(f)
        return users   

    async def new_member(self, user):

        users = await self.get_messages()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)] = 0        

        with open("json_files/userLevels.json", "w") as f:
            json.dump(users,f)
        return True


    @commands.slash_command(name="lead", description="Shows the lrs leaderboard")
    async def lead_command(self, ctx):
        send = ctx.respond
        await self.lead(ctx, send)

    async def lead(self, ctx, send):
        #self.lrs_stats()
        with open("json_files/userLevels.json", "r") as f:
            data = json.load(f)
            f = discord.File("dailymsgs.png")

            leaderboard = sorted(data.items(), key= lambda x: x[1], reverse=True)[:5]
            user_id_1st, msg_count_1st = leaderboard[0]
            user_id_2nd, msg_count_2nd = leaderboard[1]
            user_id_3rd, msg_count_3rd = leaderboard[2]
            user_id_4th, msg_count_4th = leaderboard[3]
            user_id_5th, msg_count_5th = leaderboard[4]
            embed= discord.Embed(title="Leaderboard", color=13565696)
            embed.add_field(name="Top users by messages sent", value=f"`1.` <@{user_id_1st}>: {msg_count_1st} \n`2.` <@{user_id_2nd}>: {msg_count_2nd} \n`3.` <@{user_id_3rd}>: {msg_count_3rd} \n`4.` <@{user_id_4th}>: {msg_count_4th} \n`5.` <@{user_id_5th}>: {msg_count_5th}")
            embed.set_image(url="attachment://dailymsgs.png")
            await send(file=f,embed=embed)   

    @commands.command(name="refreshlrsstats", guild_ids=[951463924279181322])
    #@permissions.has_any_role(951207540472029195, 951464246506565683)
    async def refreshlrsstats(self, ctx):
        if ctx.author.id in [695229647021015040, 443769343138856961, 713696771188195368]:
            await ctx.send("Do you really want to do that? This can take up to 1 minute, **will set the leaderboard 1 day ahead** and could potentially break the leaderboard. **ONLY USE WHEN IT IS HAS NOT REFRESHED AT 1am CET!!!** Reply with your user-ID to confirm.")
            ans = await self.client.wait_for('message', check=lambda message: message.author == ctx.author)
            if str(ans.content) == str(ctx.author.id):
                await self.awaitable_lrs_stats()
                await ctx.send("done")
            else:
                await ctx.send("Wrong ID")
        else:
            await ctx.send("F*** you")

    def lrs_stats(self):

        output_path = "dailymsgs.png"

        with open ("json_files/counter-file.txt", "r") as d_m:
            data = d_m.readlines()
            d_m.close
        new_amt = data[64]
        data[0] = f"{new_amt}\n{data[0]}"
        data[59] = ""
        data[64] = "0"
        with open ("json_files/counter-file.txt", "w") as cf:
            cf.writelines(data)
            cf.close
        with open ("json_files/counter-file.txt", "r") as d_m:
            data = d_m.read().splitlines()
            d_m.close
        data = [string for string in data if string != ""]

        data_2 = list(int(x) for x in data)

        lines = round(max(data_2)/1000)
        #print(lines)
        if lines > 2:
            lines_2 = 1000

        if lines == 2:
            lines_2 = 500
            lines = 4

        if lines == 1:
            if int(round(max(data_2)/100)) >= 12 <= 15:
                lines_2 = 500
                lines = 3
            else:
                lines_2 = 250
                lines = 4

        max_1 = int(round(max(data_2)/10))
        if lines == 0:
            if max_1 <= 10:
                lines_2 = 25
                lines = 4
            if max_1 > 10 <=20:
                lines_2 = 50
                lines = 4
            if max_1 > 20 <= 30:
                lines_2 = 100
                lines = 3
            if max_1 > 30:
                lines_2 = 100
                lines = 5



        image = Image.new("RGB", (4000, 2000), (49, 51, 56))
        image.save(output_path)
        image = Image.open("dailymsgs.png")
        draw = ImageDraw.Draw(image)
        draw.fontmode = "L"
        myFont = ImageFont.truetype('ARIAL.TTF', 35)

        x1 = 3800
        lines_distance = int(1500/lines) #auf 1200 ändern um oben platz zu haben
        y = int(1900-lines_distance)

        
        for n in range(1, lines+1):
            draw.line((4000, y, 0, y), fill=(244,249,255), width=2)
            draw.text((10, y-50), f"{n*lines_2} msgs",font=myFont, fill=(244,249,255))
            y = y-lines_distance

        image.save(output_path)


        image = Image.open("dailymsgs.png")
        draw = ImageDraw.Draw(image)

        for i in range(1, 61):

            maximum = lines*lines_2
            number = data_2[i-1]
            number_2 = float(number/maximum)
            number_3 = int(round(1500*number_2)) #auch 1200 hier
            
            dark_colour = random.randint(int(number_3/10), int(number_3/100*40))
            medium_colour = random.randint(int(number_3/100*20), int(number_3/100*40))
            light_colour = number_3-(dark_colour+medium_colour)
     
            x1 = x1 - 60
            x2 = x1 + 40
    
            draw.rectangle((x2, 1900, x1, 1900-dark_colour), fill=(20,66,49))
            draw.rectangle((x2, 1900-dark_colour, x1, 1900-dark_colour-medium_colour), fill=(34,152,108))
            draw.rectangle((x2, 1900-dark_colour-medium_colour, x1, 1900-dark_colour-medium_colour-light_colour), fill=(46,206,150)) 

        image.save(output_path)


        image = Image.open("dailymsgs.png")
        draw = ImageDraw.Draw(image)

        today = date.today()
        date_today = today.strftime("%b %d")
        days_delta = 15
        draw.line((3760, 1900, 3760, 1930), fill=(244,249,255), width=2)
        date_lines_x = 3760
        yesterday = 1
        delta_yesterday = today - timedelta(days = yesterday)
        yesterday_format = delta_yesterday.strftime("%b %d")
        draw.text((3700, 1935), f"{yesterday_format}",font=myFont, fill=(244,249,255))
    
    
        for n in range(1,5):
            date_lines_x = date_lines_x - 15*60
            if date_lines_x == 160:
                date_lines_x = date_lines_x + 60
                days_delta = days_delta - 1
            draw.line((date_lines_x, 1900, date_lines_x, 1930), fill=(244,249,255), width=2)
            delta = delta_yesterday - timedelta(days = days_delta)
            delta_format = delta.strftime("%b %d")
            draw.text((date_lines_x-60, 1935), f"{delta_format}",font=myFont, fill=(244,249,255))
            days_delta = days_delta + 15
            

        draw.line((4000, 1900, 0, 1900), fill=(244,249,255), width=2)


        

        image.save(output_path)
    
    


    async def awaitable_lrs_stats(self):
        output_path = "dailymsgs.png"

        with open ("json_files/counter-file.txt", "r") as d_m:
            data = d_m.readlines()
            d_m.close
        new_amt = data[64]
        data[0] = f"{new_amt}\n{data[0]}"
        data[59] = ""
        data[64] = "0"
        with open ("json_files/counter-file.txt", "w") as cf:
            cf.writelines(data)
            cf.close
        with open ("json_files/counter-file.txt", "r") as d_m:
            data = d_m.read().splitlines()
            d_m.close
        data = [string for string in data if string != ""]

        data_2 = list(int(x) for x in data)

        lines = round(max(data_2)/1000)
        #print(lines)
        if lines > 2:
            lines_2 = 1000

        if lines == 2:
            lines_2 = 500
            lines = 4

        if lines == 1:
            if int(round(max(data_2)/100)) >= 12 <= 15:
                lines_2 = 500
                lines = 3
            else:
                lines_2 = 250
                lines = 4

        max_1 = int(round(max(data_2)/10))
        if lines == 0:
            if max_1 <= 10:
                lines_2 = 25
                lines = 4
            if max_1 > 10 <=20:
                lines_2 = 50
                lines = 4
            if max_1 > 20 <= 30:
                lines_2 = 100
                lines = 3
            if max_1 > 30:
                lines_2 = 100
                lines = 5



        image = Image.new("RGB", (4000, 2000), (49, 51, 56))
        draw = ImageDraw.Draw(image)
        draw.fontmode = "L"
        myFont = ImageFont.truetype('ARIAL.TTF', 35)

        x1 = 140
        lines_distance = int(1500/lines) #auf 1200 ändern um oben platz zu haben
        y = int(1900-lines_distance)

        
        for n in range(1, lines+1):
            draw.line((4000, y, 0, y), fill=(244,249,255), width=2)
            draw.text((10, y-50), f"{n*lines_2} msgs",font=myFont, fill=(244,249,255))
            y = y-lines_distance

        image.save(output_path)


        image = Image.open("dailymsgs.png")
        draw = ImageDraw.Draw(image)

        for i in range(1, 61):

            maximum = lines*lines_2
            number = data_2[i-1]
            number_2 = float(number/maximum)
            number_3 = int(round(1500*number_2)) #auch 1200 hier
            
            dark_colour = random.randint(int(number_3/10), int(number_3/100*40))
            medium_colour = random.randint(int(number_3/100*20), int(number_3/100*40))
            light_colour = number_3-(dark_colour+medium_colour)
    
            x1 = x1 + 60
            x2 = x1 + 40

            draw.rectangle((x2, 1900, x1, 1900-dark_colour), fill=(20,66,49))
            draw.rectangle((x2, 1900-dark_colour, x1, 1900-dark_colour-medium_colour), fill=(34,152,108))
            draw.rectangle((x2, 1900-dark_colour-medium_colour, x1, 1900-dark_colour-medium_colour-light_colour), fill=(46,206,150)) 

        image.save(output_path)


        image = Image.open("dailymsgs.png")
        draw = ImageDraw.Draw(image)

        today = date.today()
        date_today = today.strftime("%b %d")
        days_delta = 15
        draw.line((3760, 1900, 3760, 1930), fill=(244,249,255), width=2)
        date_lines_x = 3760
        draw.text((3700, 1935), f"{date_today}",font=myFont, fill=(244,249,255))


        for n in range(1,5):
            date_lines_x = date_lines_x - 15*60
            if date_lines_x == 160:
                date_lines_x = date_lines_x + 60
                days_delta = days_delta - 1
            draw.line((date_lines_x, 1900, date_lines_x, 1930), fill=(244,249,255), width=2)
            delta = today - timedelta(days = days_delta)
            delta_format = delta.strftime("%b %d")
            draw.text((date_lines_x-60, 1935), f"{delta_format}",font=myFont, fill=(244,249,255))
            days_delta = days_delta + 15
            

        draw.line((4000, 1900, 0, 1900), fill=(244,249,255), width=2)


        

        image.save(output_path)
  
    

        

def setup(client):
    client.add_cog(levelroles(client))
