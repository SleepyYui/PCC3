from optparse import Option
from discord import SlashCommandGroup
from discord.ext import commands
import discord
from discord import Option
from cogs.pc_creator_commands.record_pcc2_group import record_pcc2, pcc2_user, pcc2_status, pcc2_promo, pcc2_leaderboard, pcc2_inspect, is_staff, pcc2_promocode_edit

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

    @pcc2.command(name="promocode", description="Get info on promocodes")
    async def promocode(self, ctx):
        await pcc2_promo(ctx)
    
    @pcc2.command(name="leaderboard", description="View ingame leaderboards")
    async def leaderboard(self, ctx, category: Option(name="category", description="Leaderboard category", choices=["PC Score", "Bitcoin", "Ethereum", "Dogecoin"])):
        await pcc2_leaderboard(ctx, category)
    
    @pcc2.command(name="inspect", description="Inspect user account")
    async def inspect(self, ctx, method: Option(name="method", description="Account data retrieval method", choices=["Email", "Trading ID", "UserHash", "UserID"]), data: Option(name="data", description="The data (email, id etc)")):
        if is_staff(ctx.author):
            await pcc2_inspect(ctx, method, data)
        else:
            await ctx.respond("This command is only for staff!", ephemeral=True)
        
    @pcc2.command(name="promocode_change", description="Add/remove promocode")
    async def promocode_change(self, ctx, promo: Option(name="promo", description="Promocode to add/remove")):
        if is_staff(ctx.author):
            await pcc2_promocode_edit(ctx, promo)
        else:
            await ctx.respond("This command is only for staff!", ephemeral=True)

def setup(client):
    client.add_cog(pcc2_group(client))
