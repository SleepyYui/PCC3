import discord
from discord.ext import commands
from discord.commands import permissions
from discord import Option
import json
from datetime import timedelta

rolelist = [589435378147262464, 648546626637398046, 632674518317531137, 571032502181822506, 697002610892341298]
rolelist2 = [697728131003580537]
class warns(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.command(name="twarn")
    async def twarn(self, ctx, member: discord.Member):
        user = ctx.author
        #print("e")
        if any(role.id in rolelist2 for role in user.roles):

            
            reason = "Useless ticket"
            
            category = discord.utils.get(ctx.author.guild.categories, name="TICKETS")
            role = discord.utils.get(ctx.guild.roles, name="Helper")
            #print("e")

            if ctx.channel.category == category:
                #print("e")
                if role in ctx.author.roles:
                    #print("e")

                    await self.new_warn_member(member)
                    await ctx.message.delete()

                    if not any(role.id in rolelist for role in member.roles) and not member.bot:
                        
                        await self.new_warn_member(member)
                        warns = await self.get_warns()
                        warn_count = warns[str(member.id)]["warn_count"] 

                        channel = self.client.get_channel(933768368970932254)
                        ochannel = self.client.get_channel(989272480671739954)
                        
                        
                    
                        if warn_count == 0:
                            try:
                                await member.send(f"You have been warned in {ctx.guild.name} for `{reason}`.")
                                await ctx.send(f"{member.mention} has been warned for {reason}. This is their first warning.", delete_after=10)
                            except:
                                await ctx.send(f"{member.mention} has been warned for {reason}. This is their first warning.\nThis user has disabled DMs from server members, so the message could not be sent.", delete_after=10)

                            await self.update_warns(member, reason + " (1)")
                            await ochannel.send(f"{member.mention} has been warned for the first time by {ctx.author.mention} for {reason}")
                            return

                        elif warn_count == 1:
                            try:
                                await member.send(f"You have been muted in {ctx.guild.name} for `{reason}`.")
                                await ctx.send(f"{member.mention} has been muted for {reason}. This is their second warning. (6h mute)", delete_after=10)
                            except:
                                await ctx.send(f"{member.mention} has been muted for {reason}. This is their second warning. (6h mute)\nThis user has disabled DMs from server members, so the message could not be sent.", delete_after=10)
                            
                            duration = timedelta(days = 0, hours = 6, minutes = 0, seconds = 0)
                            await member.timeout_for(duration, reason = reason)
                            embed = discord.Embed(title="Timeout", color=13565696)
                            embed.add_field(name="Muted:", value=f"{member.mention}")
                            embed.add_field(name="Moderator:", value=f"{ctx.author.mention}")
                            embed.add_field(name="Duration:", value=f"**{0}** days, **{6}** hours,\n**{0}** minutes, and **{0}** second",inline=False)
                            embed.add_field(name="Reason:", value=reason)
                            await ochannel.send(f"{member.mention} has been warned for the second time (mute 6h) by {ctx.author.mention} for {reason}")
                            await channel.send(embed=embed)

                            await self.update_warns(member, reason + " (2)")
                            await self.update_mutes(member, reason)
                            return
                            
                        elif warn_count == 2:
                            try:
                                await member.send(f"You have been muted in {ctx.guild.name} for `{reason}`.")
                                await ctx.send(f"{member.mention} has been muted for {reason}. This is their third warning. (24h mute)", delete_after=10)
                            except:
                                await ctx.send(f"{member.mention} has been muted for {reason}. This is their third warning. (24h mute)\nThis user has disabled DMs from server members, so the message could not be sent.", delete_after=10)

                            duration = timedelta(days = 0, hours = 24, minutes = 0, seconds = 0)
                            await member.timeout_for(duration, reason = reason)
                            embed = discord.Embed(title="Timeout", color=13565696)
                            embed.add_field(name="Muted:", value=f"{member.mention}")
                            embed.add_field(name="Moderator:", value=f"{ctx.author.mention}")
                            embed.add_field(name="Duration:", value=f"**{0}** days, **{24}** hours,\n**{0}** minutes, and **{0}** second",inline=False)
                            embed.add_field(name="Reason:", value=reason)
                            await channel.send(embed=embed)
                            
                            await ochannel.send(f"{member.mention} has been warned for the third time (mute 24h) by {ctx.author.mention} for {reason}")
                            await self.update_warns(member, reason + " (3)")
                            await self.update_mutes(member, reason)
                            return

                        elif warn_count == 3:
                            try:
                                await member.send(f"You have been soft-banned from {ctx.guild.name} for `{reason}`. All of the messages you sent in the last 7 days were deleted.")
                                await ctx.send(f"{member.mention} has been muted for {reason}. This is their fourth warning. (Soft-Ban)", delete_after=10)
                            except:
                                await ctx.send(f"{member.mention} has been muted for {reason}. This is their fourth warning. (Soft-Ban)\nThis user has disabled DMs from server members, so the message could not be sent.", delete_after=10)

                            await member.ban(reason=reason)
                            await member.unban(reason=reason)
                            
                            embed = discord.Embed(title="Softban", color=13565696)
                            embed.add_field(name="Softbanned:", value=f"{member.mention}")
                            embed.add_field(name="Moderator:", value=f"{ctx.author.mention}")
                            embed.add_field(name="Reason:", value=reason)
                            await channel.send(embed=embed)

                            await ochannel.send(f"{member.mention} has been warned for the fourth time (softban) by {ctx.author.mention} for {reason}")
                            await self.update_warns(member, reason + " (4)")
                            await self.update_bans(member, reason)
                            return

                        elif warn_count == 4:
                            try:
                                await member.send(f"You have been warned for the last time in {ctx.guild.name} for `{reason}`. This is your last warning. If you don't behave the next time, you will be banned.")
                                await ctx.send(f"{member.mention} has been warned for {reason}. This is their final warning.", delete_after=10)
                            except:
                                await ctx.send(f"{member.mention} has been warned for {reason}. This is their final warning.\nThis user has disabled DMs from server members, so the message could not be sent.", delete_after=10)
                                
                            await ochannel.send(f"{member.mention} has been warned for the fifth time (last warn) by {ctx.author.mention} for {reason}")
                            await self.update_warns(member, reason + " (5)")
                            return

                        elif warn_count == 5:
                            try:
                                await member.send(f"You have been banned from {ctx.guild.name} for `{reason}`. To appeal, please contact <@695229647021015040> on discord.")
                                await ctx.send(f"{member.mention} has been muted for {reason}. This is their 6th warning. (Banned)", delete_after=10)
                            except:
                                await ctx.send(f"{member.mention} has been muted for {reason}. This is their 6th warning. (Banned)\nThis user has disabled DMs from server members, so the message could not be sent.", delete_after=10)
                            
                            await member.ban(reason=reason)
                            embed = discord.Embed(title="Ban", color=13565696)
                            embed.add_field(name="Banned:", value=f"{member.mention}")
                            embed.add_field(name="Moderator:", value=f"{self.client.user.mention}")
                            embed.add_field(name="Reason:", value=reason)
                            await channel.send(embed=embed)
                            
                            await ochannel.send(f"{member.mention} has been warned for the sixth time (ban) by {ctx.author.mention} for {reason}")
                            await self.update_warns(member, reason + " (6)")
                            await self.update_bans(member, reason)
                            return

                        else:
                            await member.send(f"You have been warned in {ctx.guild.name} for `{reason}`.")
                            await ctx.send(f"{member.mention} has been warned for {reason}. This is their {warn_count}th warning.", delete_after=10)
                            await self.update_warns(member, reason + " ("+ str(warn_count) + ")")
                            return
        else:
            return
            

 
    @commands.command(name="warn")
    async def warn(self, ctx, member: discord.Member, *, reason = None):
        user = ctx.author
        if any(role.id in rolelist for role in user.roles):
            await ctx.message.delete()
            
            if reason != None:
                
                await self.new_warn_member(member)

                if not any(role.id in rolelist for role in member.roles) and not member.bot:
                    
                    #print("e")
                    
                    await self.new_warn_member(member)
                    warns = await self.get_warns()
                    warn_count = warns[str(member.id)]["warn_count"] 

                    #print("e")

                    channel = self.client.get_channel(933768368970932254)
                    ochannel = self.client.get_channel(989272480671739954)
                    #await ochannel.send(f"{member.mention} has been warned by {ctx.author.mention} for {reason}")
                    
                    #print("a")
                
                    if warn_count == 0:
                        #print("e")
                        try:
                            await member.send(f"You have been warned in {ctx.guild.name} for `{reason}`.")
                            await ctx.send(f"{member.mention} has been warned for {reason}. This is their first warning.", delete_after=10)
                        except:
                            await ctx.send(f"{member.mention} has been warned for {reason}. This is their first warning.\nThis user has disabled DMs from server members, so the message could not be sent.", delete_after=10)

                        await ochannel.send(f"{member.mention} has been warned for the first time by {ctx.author.mention} for {reason}")
                        await self.update_warns(member, reason + " (1)")
                        return

                    elif warn_count == 1:
                        try:
                            await member.send(f"You have been muted in {ctx.guild.name} for `{reason}`.")
                            await ctx.send(f"{member.mention} has been muted for {reason}. This is their second warning. (6h mute)", delete_after=10)
                        except:
                            await ctx.send(f"{member.mention} has been muted for {reason}. This is their second warning. (6h mute)\nThis user has disabled DMs from server members, so the message could not be sent.", delete_after=10)
                        
                        duration = timedelta(days = 0, hours = 6, minutes = 0, seconds = 0)
                        await member.timeout_for(duration, reason = reason)
                        embed = discord.Embed(title="Timeout", color=13565696)
                        embed.add_field(name="Muted:", value=f"{member.mention}")
                        embed.add_field(name="Moderator:", value=f"{ctx.author.mention}")
                        embed.add_field(name="Duration:", value=f"**{0}** days, **{6}** hours,\n**{0}** minutes, and **{0}** second",inline=False)
                        embed.add_field(name="Reason:", value=reason)
                        await channel.send(embed=embed)

                        await self.update_warns(member, reason + " (2)")
                        await ochannel.send(f"{member.mention} has been warned for the second time (mute 6h) by {ctx.author.mention} for {reason}")
                        await self.update_mutes(member, reason)
                        return
                        
                    elif warn_count == 2:
                        try:
                            await member.send(f"You have been muted in {ctx.guild.name} for `{reason}`.")
                            await ctx.send(f"{member.mention} has been muted for {reason}. This is their third warning. (24h mute)", delete_after=10)
                        except:
                            await ctx.send(f"{member.mention} has been muted for {reason}. This is their third warning. (24h mute)\nThis user has disabled DMs from server members, so the message could not be sent.", delete_after=10)

                        duration = timedelta(days = 0, hours = 24, minutes = 0, seconds = 0)
                        await member.timeout_for(duration, reason = reason)
                        embed = discord.Embed(title="Timeout", color=13565696)
                        embed.add_field(name="Muted:", value=f"{member.mention}")
                        embed.add_field(name="Moderator:", value=f"{ctx.author.mention}")
                        embed.add_field(name="Duration:", value=f"**{0}** days, **{24}** hours,\n**{0}** minutes, and **{0}** second",inline=False)
                        embed.add_field(name="Reason:", value=reason)
                        await channel.send(embed=embed)
                        
                        await ochannel.send(f"{member.mention} has been warned for the third time (mute 24h) by {ctx.author.mention} for {reason}")
                        await self.update_warns(member, reason + " (3)")
                        await self.update_mutes(member, reason)
                        return

                    elif warn_count == 3:
                        try:
                            await member.send(f"You have been soft-banned from {ctx.guild.name} for `{reason}`. All of the messages you sent in the last 7 days were deleted.")
                            await ctx.send(f"{member.mention} has been muted for {reason}. This is their fourth warning. (Soft-Ban)", delete_after=10)
                        except:
                            await ctx.send(f"{member.mention} has been muted for {reason}. This is their fourth warning. (Soft-Ban)\nThis user has disabled DMs from server members, so the message could not be sent.", delete_after=10)

                        await member.ban(reason=reason)
                        await member.unban(reason=reason)
                        
                        embed = discord.Embed(title="Softban", color=13565696)
                        embed.add_field(name="Softbanned:", value=f"{member.mention}")
                        embed.add_field(name="Moderator:", value=f"{ctx.author.mention}")
                        embed.add_field(name="Reason:", value=reason)
                        await channel.send(embed=embed)
                        
                        await ochannel.send(f"{member.mention} has been warned for the fourth time (softban) by {ctx.author.mention} for {reason}")
                        await self.update_warns(member, reason + " (4)")
                        await self.update_bans(member, reason)
                        return

                    elif warn_count == 4:
                        try:
                            await member.send(f"You have been warned for the last time in {ctx.guild.name} for `{reason}`. This is your last warning. If you don't behave the next time, you will be banned.")
                            await ctx.send(f"{member.mention} has been warned for {reason}. This is their final warning.", delete_after=10)
                        except:
                            await ctx.send(f"{member.mention} has been warned for {reason}. This is their final warning.\nThis user has disabled DMs from server members, so the message could not be sent.", delete_after=10)
                            
                        await ochannel.send(f"{member.mention} has been warned for the fifth time (last warn) by {ctx.author.mention} for {reason}")
                        await self.update_warns(member, reason + " (5)")
                        return

                    elif warn_count == 5:
                        try:
                            await member.send(f"You have been banned from {ctx.guild.name} for `{reason}`. To appeal, please contact <@695229647021015040> on discord.")
                            await ctx.send(f"{member.mention} has been muted for {reason}. This is their 6th warning. (Banned)", delete_after=10)
                        except:
                            await ctx.send(f"{member.mention} has been muted for {reason}. This is their 6th warning. (Banned)\nThis user has disabled DMs from server members, so the message could not be sent.", delete_after=10)
                        
                        await member.ban(reason=reason)
                        embed = discord.Embed(title="Ban", color=13565696)
                        embed.add_field(name="Banned:", value=f"{member.mention}")
                        embed.add_field(name="Moderator:", value=f"{self.client.user.mention}")
                        embed.add_field(name="Reason:", value=reason)
                        await channel.send(embed=embed)
                        
                        await ochannel.send(f"{member.mention} has been warned for the sixth time (ban) by {ctx.author.mention} for {reason}")
                        await self.update_warns(member, reason + " (6)")
                        await self.update_bans(member, reason)
                        return

                    else:
                        print("f")
                        await member.send(f"You have been warned in {ctx.guild.name} for `{reason}`.")
                        await ctx.send(f"{member.mention} has been warned for {reason}. This is their {warn_count}th warning.", delete_after=10)
                        await self.update_warns(member, reason + " ("+ str(warn_count) + ")")
                        return
                else:
                    await ctx.send(f"Nono", delete_after=10)

            else:
                await ctx.send(f"You have to specify a reason -_-", delete_after=10)
        else:
            return



    @commands.slash_command(name="modlogs", description="Check the warns/mutes etc. of a member")      
    async def modlogs(self, ctx, member: Option(discord.Member, required = False)):
        if member == None:
                member = ctx.author
        else:
            if not any(role.id in rolelist for role in ctx.author.roles) and not member.id == ctx.author.id:
                await ctx.respond("You can't check the warns of someone else.", ephemeral=True)
                return 

        if member.id not in [1]:

            await self.new_warn_member(member)
            warns = await self.get_warns()

            warn_count = warns[str(member.id)]["warn_count"] 
            warn_count_1 = warns[str(member.id)]["warn_count"] + 1 

            mute_count = warns[str(member.id)]["mute_count"]
            mute_count_1 = warns[str(member.id)]["mute_count"] + 1

            ban_count = warns[str(member.id)]["ban_count"]
            ban_count_1 = warns[str(member.id)]["ban_count"] + 1

            kick_count = warns[str(member.id)]["kick_count"]  
            kick_count_1 = warns[str(member.id)]["kick_count"] + 1

            embed = discord.Embed(title=f"{member.name}'s modlogs", description=f"warn count: {warn_count} \nmute count: {mute_count} \nkick count: {kick_count} \nban count: {ban_count}", color=13565696)
            try:    
                embed.set_thumbnail(url=member.avatar.url)
            except:
                pass    
        
            try:
                for x in range(1,warn_count_1):
                    warn_reason = warns[str(member.id)][f"warn {x}"]
                    embed.add_field(name=f"warn {x}:", value=warn_reason, inline=False)    
            except:
                pass

            try:    
                for x in range(1,mute_count_1):
                    mute_reason = warns[str(member.id)][f"mute {x}"]
                    embed.add_field(name=f"mute {x}:", value=mute_reason, inline=False)
            except:
                pass

            try:
                for x in range(1,kick_count_1):
                    kick_reason = warns[str(member.id)][f"kick {x}"]
                    embed.add_field(name=f"kick {x}:", value=kick_reason, inline=False)
            except:
                pass

            try:
                for x in range(1,ban_count_1):
                    ban_reason = warns[str(member.id)][f"ban {x}"]
                    embed.add_field(name=f"ban {x}:", value=ban_reason, inline=False)      
            except:
                pass 

            await ctx.respond(embed=embed)
        else:
            if member == None:
                member = ctx.author

            await self.new_warn_member(member)
            warns = await self.get_warns()

            warn_count = warns[str(member.id)]["warn_count"] 
            warn_count_1 = warns[str(member.id)]["warn_count"] + 1 

            mute_count = warns[str(member.id)]["mute_count"]
            mute_count_1 = warns[str(member.id)]["mute_count"] + 1

            ban_count = warns[str(member.id)]["ban_count"]
            ban_count_1 = warns[str(member.id)]["ban_count"] + 1

            kick_count = warns[str(member.id)]["kick_count"]  
            kick_count_1 = warns[str(member.id)]["kick_count"] + 1

            embed = discord.Embed(title=f"{member.name}'s modlogs", description=f"warn count: {warn_count} \nmute count: {mute_count} \nkick count: {kick_count} \nban count: {ban_count}", color=13565696)
            try:    
                embed.set_thumbnail(url=member.avatar.url)
            except:
                pass    

            warn_reason = ""
            try:
                for x in range(1,warn_count_1):
                    warn_reason += ", " +  warns[str(member.id)][f"warn {x}"]
                embed.add_field(name=f"warn {x}:", value=warn_reason, inline=False)
            except:
                pass

            mute_reason = ""
            try:    
                for x in range(1,mute_count_1):
                    mute_reason += ", " + warns[str(member.id)][f"mute {x}"]
                embed.add_field(name=f"mute {x}:", value=mute_reason, inline=False)
            except:
                pass

            kick_reason = ""
            try:
                for x in range(1,kick_count_1):
                    kick_reason += ", " +  warns[str(member.id)][f"kick {x}"]
                embed.add_field(name=f"kick {x}:", value=kick_reason, inline=False)
            except:
                pass

            ban_reason = ""
            try:
                for x in range(1,ban_count_1):
                    ban_reason += ", " +  warns[str(member.id)][f"ban {x}"]
                embed.add_field(name=f"ban {x}:", value=ban_reason, inline=False)   
            except:
                pass 

            await ctx.respond(embed=embed)

                 
            

           

    async def get_warns(self):
        with open("json_files/warns.json", "r") as f:
                warns = json.load(f)
        return warns

    async def new_warn_member(self, member):

            warns = await self.get_warns()

            if str(member.id) in warns:
                return False
            else:
                warns[str(member.id)] = {}
                warns[str(member.id)]["warn_count"] = 0
                warns[str(member.id)]["mute_count"] = 0
                warns[str(member.id)]["ban_count"] = 0
                warns[str(member.id)]["kick_count"] = 0

            with open("json_files/warns.json", "w") as f:
                json.dump(warns,f)
            return True     

    async def update_warns(self, member, reason):

        warns = await self.get_warns()
        
        warn_count_old = warns[str(member.id)]["warn_count"]
        warn_count_new = warn_count_old + 1
        warns[str(member.id)]["warn_count"] = warn_count_new
        warns[str(member.id)][f"warn {warn_count_new}"] = str(reason)    

        with open("json_files/warns.json", "w") as f:
            json.dump(warns,f)      
            
    async def update_mutes(self, member, reason):

        warns = await self.get_warns()
        
        warn_count_old = warns[str(member.id)]["mute_count"]
        warn_count_new = warn_count_old + 1
        warns[str(member.id)]["mute_count"] = warn_count_new
        warns[str(member.id)][f"mute {warn_count_new}"] = str(reason)    

        with open("json_files/warns.json", "w") as f:
            json.dump(warns,f)
            
    async def update_bans(self, member, reason):

        bans = await self.get_warns()

        ban_count_old = bans[str(member.id)]["ban_count"]
        ban_count_new = ban_count_old + 1
        bans[str(member.id)]["ban_count"] = ban_count_new
        bans[str(member.id)][f"ban {ban_count_new}"] = str(reason)
        
        with open("json_files/warns.json", "w") as f:
            json.dump(warns,f) 

def setup(client):
    client.add_cog(warns(client)) 
