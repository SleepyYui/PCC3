import discord
from discord.ext import commands
from discord import Option
from discord.commands import permissions

class PreAnswer(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="preset_answer", description="For da ticket Mods")
    #@permissions.has_any_role(951207540472029195, 951464246506565683, 697728131003580537)
    async def preset_answer_slash(self, ctx, answer : Option(str, 'Choose the message', choices=["Hello", "Bye", "Contact SUPPORT", "David Bug", "explain in detail", "send screenshot", "screenshot of payment (Pro Player)", "send video", "Device not supported", "custom"], required=True), member : Option(discord.Member, required=False), custom : Option(str,"Custom Message", required=False)):

        if ctx.author.id == 695229647021015040 or ctx.author.id == 713696771188195368 or ctx.author.id == 443769343138856961:
            fileObj = None
            if answer == "Hello":
                if member:
                    message = f"Hi <@{member.id}>!\nHow can I help you today?"
                else:
                    message = f"Hi!\nHow can I help you today?"
            elif answer == "Bye":
                if member:
                    message = f"Have a good day <@{member.id}>!\nIf you need help again, just create another ticket."
                else:
                    message = f"Have a good day!\nIf you need help again, just create another ticket."
            elif answer == "Contact SUPPORT":
                if member:
                    message = f"<@{member.id}>\nWe sadly can't fix your problem.\nTo fix it, contact SUPPORT (use /ping_support to find him)."
                else:
                    message = f"We sadly can't fix your problem.\nTo fix it, contact SUPPORT (use /ping_support to find him)."
            elif answer == "custom":
                if custom != "" and custom != None:
                    message = custom
                else:
                    await ctx.respond("You need to type a message in the \"custom\" tab. -_-", ephemeral=True)
                    return
            elif answer == "David Bug":
                if member:
                    message = f"Hi <@{member.id}>!\nThis bug, the \"David Bug\", is currently only fixable by reinstalling the game and starting from scratch. There is also no guarantee that the bug will be fixed by only reinstalling. If you don't want to loose your progress, or don't want the risk of it happening again, you can wait for a bug-fix that will probably come out once the war in the Ukraine is over."
                else:
                    message = f"This bug, the \"David Bug\", is currently only fixable by reinstalling the game and starting from scratch. There is also no guarantee that the bug will be fixed by only reinstalling. If you don't want to loose your progress, or don't want the risk of it happening again, you can wait for a bug-fix that will probably come out once the war in the Ukraine is over."
            elif answer == "explain in detail":
                if member:
                    message = f"<@{member.id}>\nCan you give us more details about the problem?"
                else:
                    message = f"Can you give us more details about the problem?"
            elif answer == "send screenshot":
                if member:
                    message = f"<@{member.id}>\nCan you send us a screenshot of that problem please?"
                else:
                    message = f"Can you send us a screenshot of that problem please?"
            elif answer == "screenshot of payment (Pro Player)":
                if member:
                    message = f"<@{member.id}>\nCan you send us proof of the payment please?\nWithout that we can't give you the \"Pro Player\" role.\nIt should look like this:"
                else:
                    message = f"Can you send us proof of the payment please?\nWithout that we can't give you the \"Pro Player\" role.\nIt should look like this:"
                fileObj = discord.File(f"example_pics/proplayer_example.png")
            elif answer == "send video":
                if member:
                    message = f"<@{member.id}>\nCan you send us a screen-recording of you reproducing the bug/problem please?"
                else:
                    message = f"Can you send us a screen-recording of you reproducing the bug/problem please?"
            elif answer == "Device not supported":
                if member:
                    message = f"<@{member.id}>\nThe following devices are not supported due to technical issues:\n> Redmi 9\n> Redmi 9A\n> Redmi 9C\n> Redmi 9C NFC\n> HUAWEI Y5 LITE\n\nIf you have one of those devices, we sadly cannot help since it is a hardware related issue."
                else:
                    message = f"The following devices are not supported due to technical issues:\n> Redmi 9\n> Redmi 9A\n> Redmi 9C\n> Redmi 9C NFC\n> HUAWEI Y5 LITE\n\nIf you have one of those devices, we sadly cannot help since it is a hardware related issue."



            webhooks = await ctx.channel.webhooks()
            try:
                try:
                    if fileObj:
                        if webhooks:
                            for webhook in webhooks:
                                if webhook.name == "PreanswerHook":
                                    await webhook.send(content=message, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url, file=fileObj)
                                    await ctx.respond("Success", ephemeral=True)
                                    hook = True
                                    break
                                else:
                                    hook = False
                            if hook == False:
                                webhook = await ctx.channel.create_webhook(name="PreanswerHook")
                                await webhook.send(content=message, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url, file=fileObj)
                                await ctx.respond("Success, there was no fitting webhook though so I had to create one.", ephemeral=True)
                        elif not webhooks:
                            webhook = await ctx.channel.create_webhook(name="PreanswerHook")
                            await webhook.send(content=message, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url, file=fileObj)
                            await ctx.respond("Success, there was no webhook though so I had to create one.", ephemeral=True)
                        else:
                            await ctx.respond("I do not know how you did that, but you somehow broke an if-else statement.", ephemeral=True)
                    else:
                        if webhooks:
                            for webhook in webhooks:
                                if webhook.name == "PreanswerHook":
                                    await webhook.send(content=message, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url)
                                    await ctx.respond("Success", ephemeral=True)
                                    hook = True
                                    break
                                else:
                                    hook = False
                            if hook == False:
                                webhook = await ctx.channel.create_webhook(name="PreanswerHook")
                                await webhook.send(content=message, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url)
                                await ctx.respond("Success, there was no fitting webhook though so I had to create one.", ephemeral=True)
                        elif not webhooks:
                            webhook = await ctx.channel.create_webhook(name="PreanswerHook")
                            await webhook.send(content=message, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url)
                            await ctx.respond("Success, there was no webhook though so I had to create one.", ephemeral=True)
                        else:
                            await ctx.respond("I do not know how you did that, but you somehow broke an if-else statement.", ephemeral=True)
                except:
                    webhook = await ctx.channel.create_webhook(name="PreanswerHook")
                    await webhook.send(content=message, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url, file=fileObj)
                    await ctx.respond("Success, there an error, so i created a new hook.", ephemeral=True)
            except:
                try:
                    if webhooks:
                        for webhook in webhooks:
                            if webhook.name == "PreanswerHook":
                                await webhook.send(content=message, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url)
                                await ctx.respond("Success", ephemeral=True)
                                hook = True
                                break
                            else:
                                hook = False
                        if hook == False:
                            webhook = await ctx.channel.create_webhook(name="PreanswerHook")
                            await webhook.send(content=message, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url)
                            await ctx.respond("Success, there was no fitting webhook though so I had to create one.", ephemeral=True)
                    elif not webhooks:
                        webhook = await ctx.channel.create_webhook(name="PreanswerHook")
                        await webhook.send(content=message, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url)
                        await ctx.respond("Success, there was no webhook though so I had to create one.", ephemeral=True)
                    else:
                        await ctx.respond("I do not know how you did that, but you somehow broke an if-else statement.", ephemeral=True)
                except:
                    webhook = await ctx.channel.create_webhook(name="PreanswerHook")
                    await webhook.send(content=message, username=ctx.author.display_name, avatar_url=ctx.author.avatar.url)
                    await ctx.respond("Success, there an error, so i created a new hook.", ephemeral=True)

    @commands.command(name="getwebhookstest")
    async def getwebhooks(self, ctx, message=None):
        if ctx.author.id == 443769343138856961 or ctx.author.id == 695229647021015040 or ctx.author.id == 713696771188195368:
            await ctx.message.delete()
            webhooks = await ctx.message.channel.webhooks()
            if message is None:
                message = str(webhooks)
            else:
                message = str(webhooks) + "\n" + message
            if webhooks:
                for webhook in webhooks:
                    await webhook.send(content=message, username=ctx.author.name, avatar_url=ctx.author.avatar.url)
                    #await ctx.respond("Success", ephemeral=True)
                    break
            elif not webhooks:
                webhook = await ctx.message.channel.create_webhook(name="PreanswerHook")
                message = message + "\nNo webhook existing, created new one"
                await webhook.send(content=message, username=ctx.author.name, avatar_url=ctx.author.avatar.url)
                #await ctx.respond("Success, there was no webhook though so I had to create one.", ephemeral=True)
            #else:
                #await ctx.respond("Brok,\nSomehow at least...\nI mean you broke a if-else statement, I fear you...", ephemeral=True)
        else:
            await ctx.message.channel.send("**First of all:** How the heck did you find that command???\n**And second:** Why do you even try to use that if you are not a Bot-developer?\n||it is for debugging -_-||")

def setup(bot):
    bot.add_cog(PreAnswer(bot))