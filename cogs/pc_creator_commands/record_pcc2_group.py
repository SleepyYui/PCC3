import discord
from discord.ext import commands

   

async def record_pcc2(ctx): 
    embed = discord.Embed(title="__PCC2 World Record__", description="This is the current PCC2 World Record PC", color=13565696)
    embed.add_field(name=f":small_blue_diamond: Achieved by", value="<@530725164703416340> Vinrellren#9894 (530725164703416340)", inline=False)
    embed.add_field(name=f":small_blue_diamond: Details", value="Max overclocks are needed to get the highest score \n• MX-4 45 Thermal Paste is required and needs to cover \n100% of the CPU \n• Max overclocking skill is required.", inline=False)
    embed.add_field(name=f":small_blue_diamond: Score achieved", value="`3.313.336`", inline=False)
    embed.set_image(url="https://media.discordapp.net/attachments/748122380383027210/959825115485470790/1648910536234.jpg")

    await ctx.respond(embed=embed)   

