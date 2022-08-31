from optparse import Option
from discord import SlashCommandGroup
from discord.ext import commands
import discord
from discord import Option

from cogs.pc_creator_commands.record_pcc2_group import record_pcc2


class pcc2_group(commands.Cog):

    def __init__(self, client):
        self.client = client


    pcc2 = SlashCommandGroup("pcc2", "PC Creator one related stuff")

    
    @pcc2.command(name="record", description="Shows the best PC in PCC2")
    async def record_group(self, ctx):
        await record_pcc2(ctx)


def setup(client):
    client.add_cog(pcc2_group(client))