import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import Option
import json
import random

class dontusethiscommand(commands.Cog):

    def __init__(self, client):
        self.client = client 




    @commands.slash_command(name="dontusethiscommand", description="Reward: Special Role   Try your luck and be the next sherlock")
    async def dontusethiscommand(self, ctx, password : Option(str, required=True)):

        answers = ["LMAO thats wrong. Try it again :rofl:", 
                    "C'mon its not that hard <:LOL:720879922008031246>",
                    "Maybe you should use your brain :exploding_head:", 
                    "La-da-da-da-dahh its the motherfucking D-O-double-G... Ok I'm not high but I think you are high because this is completely wrong",
                    "Oh wow this is right :partying_face: \n\n\n\n\n Oh wait. My bad its wrong lmao <:LOL:720879922008031246>",
                    "Find the hints :handshake:",
                    "Maybe you are just stupid <:wat:720879883269570630>",
                    "use the ,password command for one hint"
                    ]

        answers_send = random.choice(answers)            

        if password == "YouDontHaveALife":

            await ctx.respond("Bro what is wrong with you\nCongratulations you are the new Sherlock. DM <@695229647021015040> to get the prize")

        if password == "helpme":

            help_chance = random.randrange(0,11)
            print(help_chance)

            if help_chance == 1: 
                await ctx.respond("What about the modlogs")

            else:
                await ctx.respond("Hmmmmmmmm something went wrong...")    

        else:
            await ctx.respond(answers_send)    


    @commands.command(name="yourname")
    async def yourname(self, ctx, *, reason):
        if reason == ctx.author.display_name:
            await ctx.send("maybe **YouDontHaveALife**")
        else:
            await ctx.send("Bro just use ,yourname [your name]")      


    @commands.command(name="password")
    async def password(self, ctx):
        await ctx.send("try password: 'helpme'")
                      

            


def setup(client):
    client.add_cog(dontusethiscommand(client))