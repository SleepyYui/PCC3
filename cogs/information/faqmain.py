import discord
from discord.ext import commands
from datetime import datetime
from discord.ui import Button, View
from discord import Option
from discord.commands import permissions

class faqmain(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    """@commands.command()
    async def faq_ask(self, ctx, *, reason=None): 
        if ctx.channel.name in ["faq-ask"]:
            if reason == None or reason.lower() == "suggestion":
                await ctx.send("You have to use ,faq_ask with a question", delete_after=10)
            else:
                await ctx.message.delete()
                embed=discord.Embed(title="Question:", description=reason, color=13565696, timestamp=datetime.utcnow())   
                embed.set_author(name=f"{ctx.author.display_name} ({ctx.author.id})", icon_url=ctx.author.avatar.url)
                message = await ctx.send(embed=embed)
                await message.add_reaction("✅")
                await message.add_reaction("❌")
        else:
            await ctx.send("This command only works in #faq-ask", delete_after=10)"""


    @commands.slash_command(name="faq_ask", description="Ask things in relation with PCC / PCC2")
    async def faq_ask_slash(self, ctx, question: Option(str, required=True)): 
        if ctx.channel.name in ["faq-ask"]:
            await ctx.respond("Added your Question, we may answer it soon in #faq", ephemeral=True)
            embed=discord.Embed(title="Suggestion:", description=question, color=13565696, timestamp=datetime.utcnow())   
            embed.set_author(name=f"{ctx.author.display_name} ({ctx.author.id})", icon_url=ctx.author.avatar.url)
            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")

        else:
            await ctx.respond("This command only works in #faq-ask", ephemeral=True)

    @commands.slash_command(name="faq_answer", description="For Moderators / Admins to answer questions", guild_ids=[951463924279181322])
    #@permissions.has_any_role(951207540472029195, 589435378147262464, 632674518317531137, 951464246506565683)
    async def faq_answer(self, ctx, question: Option(str, required=True), answer: Option(str, required=True)):
        channel = discord.utils.get(ctx.guild.channels, name="faq")
        embed=discord.Embed(title=None, description=None)
        #embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        embed.add_field(name="__**Question**__", value="**Q:** " + question + "\n **A:** " + answer, inline=False)
        #embed.add_field(name=None, value="A: " + answer, inline=False)
        embed.set_footer(text="Ask a question by using faq_ask.")
        message = await channel.send(embed=embed)
        await ctx.respond(f"Answered Question [here](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}/)", ephemeral=True)

def setup(client):
    client.add_cog(faqmain(client))