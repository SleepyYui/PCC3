import json
import discord
from discord.ext import commands
import asyncio
import random
from discord.commands import Option
 
bot_channel = 962765009006506024
forbidden_channels = []


level = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
levelnum = [2500,5000,10000,20000,40000]
 

lsj = "json_files/levelsystem.json"
 

class levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client
 
    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        if message.channel.id not in forbidden_channels:
            if not message.author.bot:
                await self.new_member(message.author)
                users = await self.get_levels()
                ranxp = random.randint(1, 5)
                users[str(user.id)] = int(users[str(user.id)]) + int(ranxp)
                with open(lsj, "w") as f:
                    json.dump(users,f)  
                for i in levelnum[::-1]:
                    if users[str(user.id)] >= i:
                        pos = levelnum.index(i)
                        userlevel = level[pos]
                        pos += 1
                        if userlevel.lower() not in [y.name.lower() for y in message.author.roles]:
                            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=userlevel))
                            embed = discord.Embed(description=f"Congrats! {message.author.mention}! You leveled up to **level: {pos}**!\nYour new role: **{userlevel}**!!!", color=13565696)
                            embed.set_thumbnail(url=message.author.avatar.url)
                            await message.channel.send(embed=embed)
                            break
                        else:
                            break
 
    @commands.slash_command(name="xp")
    async def ranklist(self, ctx, member: Option(discord.Member, required = True)):
        user = member
        if True:
            #try:
            with open(lsj, "r") as f:
                users = json.load(f)
            countnumber = 0
            sortedusers = sorted(users.items(), key= lambda x: x[1], reverse=True)[:5]
            #print(sortedusers)
            pos = ctx.guild.member_count
            for entry in sortedusers[:1000]:
                countnumber += 1
                user_id, xp_count = entry
                #print(str(user_id) + " " + str(user.id))
                if str(user_id) == str(user.id):
                    #print(str(user_id) + " " + str(user.id))
                    pos = countnumber
                    break

            nextxp = levelnum[0]
            for userlevel in level[::-1]:
                if userlevel.lower() in [y.name.lower() for y in user.roles]:
                    if not level[::-1][0].lower() in [y.name.lower() for y in user.roles]:
                        position = level.index(userlevel)
                        nextxp = levelnum[position + 1]
                        boxes = users[str(user.id)] / nextxp
                        boxes = boxes * 100
                        boxes = boxes / 5
                        boxes = round(boxes)
                        break
                    else:
                        boxes = 20
                        nextxp = users[str(user.id)]
                        break

            embed = discord.Embed(title=f"{ctx.author.display_name}'s level stats", color=13565696)
            embed.add_field(name="Name", value=ctx.author.mention, inline=True)
            embed.add_field(name="XP", value=f"{users[str(user.id)]}/{nextxp}", inline=True)
            embed.add_field(name="Rank", value=f"{pos}/{ctx.guild.member_count}", inline=True)
            embed.add_field(name="Progress Bar", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
            embed.set_thumbnail(url=user.avatar.url)
            await ctx.respond(embed=embed)
            #except:
                #await ctx.channel.send("Something went wrong... Please try again.")

    @commands.slash_command(name="xplead")
    async def leaderboard(self, ctx, unused: Option(str, required = True)):
        with open(lsj, "r") as f:
            data = json.load(f)

            leaderboard = sorted(data.items(), key= lambda x: x[1], reverse=True)[:5]
            user_id_1st, msg_count_1st = leaderboard[0]
            user_id_2nd, msg_count_2nd = leaderboard[1]
            user_id_3rd, msg_count_3rd = leaderboard[2]
            user_id_4th, msg_count_4th = leaderboard[3]
            user_id_5th, msg_count_5th = leaderboard[4]
            embed= discord.Embed(title="Leaderboard", color=13565696)
            embed.add_field(name="Top users by XP", value=f"`1.` <@{user_id_1st}>: {msg_count_1st} \n`2.` <@{user_id_2nd}>: {msg_count_2nd} \n`3.` <@{user_id_3rd}>: {msg_count_3rd} \n`4.` <@{user_id_4th}>: {msg_count_4th} \n`5.` <@{user_id_5th}>: {msg_count_5th}")
            await ctx.respond(embed=embed) 

    """@commands.command()
    async def transferlrstoxp(self, ctx, member:discord.Member):
        user = member
        with open("json_files/userLevels.json", "r") as f:
            userlrs = json.load(f)
        with open(lsj, "r") as f:
            userxp = json.load(f)
        userlrs = userlrs[str(user.id)]
        userxp[str(user.id)] = round(userlrs * 2.5)
        with open(lsj, "w") as f:
            json.dump(userxp,f)
        await ctx.send(f"Converted {userlrs} messages to {userxp[str(user.id)]}")"""

    async def new_member(self, user):
        users = await self.get_levels()
        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)] = 0        
        with open(lsj, "w") as f:
            json.dump(users,f)
        return True

    async def get_levels(self):
        with open(lsj, "r") as f:
            users = json.load(f)
        return users   

def setup(client):
    client.add_cog(levelsys(client))