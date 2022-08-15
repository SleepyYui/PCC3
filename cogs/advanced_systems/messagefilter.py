
import discord
from discord.ext import commands
import json
import re

with open("json_files/mainconfig.json", encoding="utf-8-sig") as f:
    mainconfig = json.load(f)

with open("json_files/badwords.json", encoding="utf-8-sig") as e:
    badwords = json.load(e)

localmuchusedbadwords = badwords[0]["localmuchusedbadwords"]
localbadwords = badwords[0]["localbadwords"]
rolelist = [589435378147262464, 632674518317531137, 951207540472029195, 951464246506565683]
allowedroles = mainconfig["allowed_filter"] #[951207540472029195, 589435378147262464, 632674518317531137] #, 951464246506565683] #botdev, moderator, admin, testserveradmin

class messagefilter(commands.Cog):
    def __init__(self, client):
        self.client = client

    """async def get_badwords(self):
        with open("json_files/badwords.json", "r") as f:
            badwords = json.load(f)
        return badwords"""

    @commands.Cog.listener()
    async def on_message(self, message):
        if not isinstance(message.channel, discord.DMChannel):
            await self.checkfornaughtyword(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not isinstance(before.channel, discord.DMChannel):
            await self.checkfornaughtyword(after)
    
    async def checkfornaughtyword(self, message):
        if message != None:
            if not message.author.bot:
                badwordarr = localbadwords #await self.get_badwords()
                muchusedarr = localmuchusedbadwords #await self.get_muchusedbadwords()
                author = message.author
                try:
                    webhooks = await message.channel.webhooks()
                except:
                    webhooks = None
                swearword = False
                content = message.content
                #replacement = ":heart:"
                explanation = "\n\nPlease stop using swear words (rule 5).\nYou can read the rules in <#605326085328207872>.​"
                if any(role.id in allowedroles for role in author.roles):
                    return True
                #nospacecontent = content.replace(" ", "")
                for badword in badwordarr:
                    if badword.lower() in content.lower():
                        compiled = re.compile(re.escape(badword.lower()), re.IGNORECASE)
                        lengthofbadword = len(badword) - 1
                        replacement = '٭' * lengthofbadword
                        replacement = badword[0] + replacement
                        content = compiled.sub(replacement, content)
                        swearword = True
                for badword in muchusedarr:
                    badword2 = badword + " "
                    badword3 = badword
                    badword4 = " " + badword
                    badword = " " + badword + " "
                    if badword.lower() in content.lower():
                        lengthofbadword = len(badword3) - 1
                        replacement = '٭' * lengthofbadword
                        replacement = badword3[0] + replacement
                        compiled = re.compile(re.escape(badword3.lower()), re.IGNORECASE)
                        content = compiled.sub(replacement, content)
                        swearword = True
                    if content.lower().startswith(badword2.lower()):
                        lengthofbadword = len(badword3) - 1
                        replacement = '٭' * lengthofbadword
                        replacement = badword3[0] + replacement
                        compiled = re.compile(re.escape(badword3.lower()), re.IGNORECASE)
                        content = compiled.sub(replacement, content)
                        swearword = True
                    if content.lower() == badword3.lower():
                        lengthofbadword = len(badword3) - 1
                        replacement = '٭' * lengthofbadword
                        replacement = badword3[0] + replacement
                        compiled = re.compile(re.escape(badword3.lower()), re.IGNORECASE)
                        content = compiled.sub(replacement, content)
                        swearword = True
                    if content.lower().endswith(badword4.lower()):
                        lengthofbadword = len(badword3) - 1
                        replacement = '٭' * lengthofbadword
                        replacement = badword3[0] + replacement
                        compiled = re.compile(re.escape(badword3.lower()), re.IGNORECASE)
                        content = compiled.sub(replacement, content)
                        swearword = True
                if swearword == True:
                    #print(replacement)
                    await message.delete()
                    if len(content) > 1000:
                        content = content[:1000]
                    content = content + explanation
                    if webhooks != None:
                        if webhooks:
                            for webhook in webhooks:
                                await webhook.send(content=content, username=author.display_name, avatar_url=author.avatar.url)
                                break
                        elif not webhooks:
                            webhook = await message.channel.create_webhook(name="BadWordHook")
                            await webhook.send(content=content, username=author.display_name, avatar_url=author.avatar.url)
                        return True
                    else:
                        return True
                return True
            return False

    @commands.command(name="new_badword")
    async def new_item(self, ctx, list_name = "localbadwords", *, item_name = ""):
        user = ctx.author
        if any(role.id in rolelist for role in user.roles):
            item_name = item_name.lower()
            if item_name != "" and item_name != "nothing":
                with open("json_files/badwords.json", "r", encoding="utf-8-sig") as badjson:
                    items = json.load(badjson)
                if type(items) is dict:
                    items = [items]
                
                oglistname = list_name
                if list_name == "localbadwords":
                    list_name = 0
                elif list_name == "localmuchusedbadwords":
                    list_name = 1
                else:
                    await ctx.send(f"No such list: \"{item_name}\"\nMaybe try: `localbadwords` or `localmuchusedbadwords`")#, delete_after=10)
                    return False

                if item_name in items[list_name]:
                    await ctx.send(f"Could not add " + item_name + ", since it is already added.")#, delete_after=10)
                    return False

                items[list_name][oglistname].append(item_name)
                #print(items)
                with open("json_files/badwords.json", "w", encoding="utf-8-sig") as superbadwords:
                    json.dump(items, superbadwords)
                    #print(f"Badword \"{item_name}\" was added to badwords.json")
                await ctx.send(f"Added {item_name}. It will be used on the next restart")#, delete_after=10)
            else:
                await ctx.send(f"Cannot add nothing to the list since it would break the bot. Why would you even want to do that???")#, delete_after=10)
                

            

    @commands.command(name="rem_badword")
    async def rem_item(self, ctx, list_name = "localbadwords", *, item_name = "nothing"):
        user = ctx.author
        if any(role.id in rolelist for role in user.roles):
            #try:
            if True:
                item_name = item_name.lower()
                oglistname = list_name
                if list_name == "localbadwords":
                    list_name = 0
                elif list_name == "localmuchusedbadwords":
                    list_name = 1
                else:
                    await ctx.send(f"No such list: \"{item_name}\"\nMaybe try: `localbadwords` or `localmuchusedbadwords`")#, delete_after=10)
                    return False

                with open("json_files/badwords.json", "r", encoding="utf-8-sig") as badjson:
                    items = json.load(badjson)
                if type(items) is dict:
                    items = [items]
                if item_name in items[list_name][oglistname]:
                    items[list_name][oglistname].remove(item_name)
                    await ctx.send(f"Removed {item_name}")#, delete_after=10)
                    #return True
                else:
                    await ctx.send(f"Could not remove {item_name}")#, delete_after=10)
                    return False
                with open("json_files/badwords.json", "w", encoding="utf-8-sig") as superbadwords:
                    json.dump(items, superbadwords)
            #except:
                #await ctx.send(f"Something broke...", delete_after=10)

    @commands.command(name="list_badword")
    async def rem_item(self, ctx):
        user = ctx.author
        if any(role.id in rolelist for role in user.roles):
            fileObject = discord.File(f"json_files/badwords.json")
            await ctx.send("badwords file:", file=fileObject)


def setup(client):
	client.add_cog(messagefilter(client))