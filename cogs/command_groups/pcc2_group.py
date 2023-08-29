from optparse import Option
from discord import SlashCommandGroup
from discord.ext import commands
import discord
from discord import Option
from cogs.pc_creator_commands.record_pcc2_group import record_pcc2, pcc2_user, pcc2_status, pcc2_promo


class pcc2_group(commands.Cog):

    def __init__(self, client):
        self.client = client


    pcc2 = SlashCommandGroup("pcc2", "PC Creator two related stuff")

    
    @pcc2.command(name="record", description="Shows the best PC in PCC2")
    async def record_group(self, ctx):
        await record_pcc2(ctx)
    
    @pcc2.command(name="user", description="Get info on a user from a trade code (ID)")
    async def user(self, ctx, code: Option(int, name="code", description="Trade code (ID)", min_value=100000, max_value=999999)):
        await pcc2_user(ctx, code)

    @pcc2.command(name="status", description="Shows the status of PCC2")
    async def status(self, ctx):
        await pcc2_status(ctx)

    @pcc2.command(name="promocode", description="Get info on promocode(s)")
    async def promocode(self, ctx, code: Option(name="code", description="Promocode", required=False)):
        await pcc2_promo(ctx, code)

def setup(client):
    client.add_cog(pcc2_group(client))
