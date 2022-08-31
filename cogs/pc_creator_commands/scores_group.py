import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import Option


"""class DroppDownMenu(discord.ui.View):
    @discord.ui.select(placeholder="Choose one option", min_values=1, max_values=1, options=[
       discord.SelectOption(label="CPU", description="The CPUs scores list"),
        discord.SelectOption(label="GPU", description="The GPUs scores list"),
        discord.SelectOption(label="RAM", description="The RAMs scores list"),
        discord.SelectOption(label="All", description="All scores lists")
    ])
    async def callback(self, select, interaction : discord.Interaction):
        if select.values[0] == "CPU":
            await interaction.response.send_message("https://media.discordapp.net/attachments/838857610358292532/931919636461654046/CPU-Scores_Super_Dark_Mode_3.jpg")
        if select.values[0] == "GPU":
            await interaction.response.send_message("https://media.discordapp.net/attachments/838857610358292532/931919674134904982/GPU_Scores_Super_Dark_Mode_5.jpg")
        if select.values[0] == "RAM":
            await interaction.response.send_message("https://media.discordapp.net/attachments/838857610358292532/931919651070423100/RAM_scores_Super_Dark_Mode_4.jpg")
        if select.values[0] == "All":
            await interaction.response.send_message("https://media.discordapp.net/attachments/838857610358292532/931919636461654046/CPU-Scores_Super_Dark_Mode_3.jpg")        
            await interaction.followup.send("https://media.discordapp.net/attachments/838857610358292532/931919674134904982/GPU_Scores_Super_Dark_Mode_5.jpg")
            await interaction.followup.send("https://media.discordapp.net/attachments/838857610358292532/931919651070423100/RAM_scores_Super_Dark_Mode_4.jpg")
"""



async def pcc1_scores_slash(ctx, part, choice):
    if part in ('CPU', 'All'):
        await ctx.respond("https://media.discordapp.net/attachments/802512035224223774/948613482922782750/CPU-Scores_Super_Dark_Mode_4.jpg")
    if part in ('GPU', 'All'):
        await ctx.respond("https://media.discordapp.net/attachments/802512035224223774/948613531320860773/GPU_Scores_Super_Dark_Mode_6.jpg")
    if part in ('RAM', 'All'):
        await ctx.respond("https://media.discordapp.net/attachments/802512035224223774/948613542360256562/RAM_scores_Super_Dark_Mode_5.jpg")

                 