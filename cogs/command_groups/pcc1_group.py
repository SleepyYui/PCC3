#from optparse import Option
from discord import SlashCommandGroup
from discord.ext import commands
import discord
from discord import Option
from cogs.pc_creator_commands.bitcoinpc_group import miner
from cogs.pc_creator_commands.customcpu_group import customcpu
from cogs.pc_creator_commands.levels_group import levels_slash
from cogs.pc_creator_commands.main_group import main_slash_pcc1
from cogs.pc_creator_commands.optimize_group import optimize_slash
from cogs.pc_creator_commands.quantum_group import quantum__slash_pcc1
from cogs.pc_creator_commands.record_pcc1_group import record_slash
from cogs.pc_creator_commands.scores_group import pcc1_scores_slash


class pcc1_group(commands.Cog):

    def __init__(self, client):
        self.client = client


    pcc1 = SlashCommandGroup("pcc1", "PC Creator one related stuff")


    @pcc1.command(name="miner", description="Shows a chart with good mining setups for every level")
    async def miner_group(self, ctx):
        await miner(ctx)

    @pcc1.command(name="custom_cpu", description="How custom CPUs were made")
    async def custom_cpu_group(self, ctx):
        await customcpu(ctx)

    @pcc1.command(name="levels", description="Returns a picture with information about the levels in PCC1")    
    async def levels_group(self, ctx):
        await levels_slash(ctx)

    @pcc1.command(name="main_screen", description="Shows a picture of the main screen in game with information about the buttons")   
    async def main_group(self, ctx):
        await main_slash_pcc1(ctx) 

    @pcc1.command(name="optimize", description="Sends a helpful text about optimize FPS task")
    async def optimize_group(self, ctx):
        await optimize_slash(ctx)

    @pcc1.command(name="quantum", description="Sends a picture of a quantum PC in-game")
    async def quantum_group(self, ctx):
        await quantum__slash_pcc1(ctx)

    @pcc1.command(name="record", description="Shows the best PC in PCC1")
    async def record_pcc1_group(self, ctx):
        await record_slash(ctx)    

    @pcc1.command(name='scores', description='Shows charts with benchmark of CPUs, GPUs or RAM')
    async def scores_group(self, ctx, part: Option(str, 'Choose the parts you need', choices=['CPU', 'GPU', 'RAM', 'All'], required=True)):
        choice = part
        await pcc1_scores_slash(ctx, part, choice)


def setup(client):
    client.add_cog(pcc1_group(client))
