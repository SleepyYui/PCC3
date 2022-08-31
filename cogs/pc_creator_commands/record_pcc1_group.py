import discord
from discord.ext import commands
import json

#command -> pcc1_group


async def record_slash(ctx): 
    embed = discord.Embed(title="__World Record__", description="This is the current World Record PC", color=13565696)
    embed.add_field(name=f":small_blue_diamond: Achieved by", value="<@695229647021015040> ¥£$#7660 (695229647021015040)", inline=False)
    embed.add_field(name=f":small_blue_diamond: Details", value="Overclocks are needed to get the highest score \n**CPU**: 153 Base 22 Boost \n**RAM**: 4680 \n**GPU**: 7840 and 40300 \n• ZALMVN ZMX55 Thermal Paste is required and needs to cover \n100% of the CPU \n• Max overclocking skill is required.", inline=False)
    embed.add_field(name=f":small_blue_diamond: Score achieved", value="`207,231`", inline=False)
    embed.set_image(url="https://cdn.discordapp.com/attachments/838857610358292532/905766073557729290/record.jpg")

    await ctx.respond(embed=embed)    