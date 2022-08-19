import discord
import pytz
from discord.ext import commands
from datetime import datetime
import json

with open("json_files/mainconfig.json", encoding="utf-8-sig") as f:
    mainconfig = json.load(f)

MEMBER_LOGS=mainconfig["main_logging"] #572673322891083776 #for membersided logging --> Default: 572673322891083776 FOR MEMBER UPDATE
SERVER_LOGS=mainconfig["secondary_logging"] #572673322891083776 #for serversided logging --> Default: 572673322891083776 FOR SERVER UPDATES

class logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """@commands.Cog.listener()
    async def on_message_delete(self, message):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        e=discord.Embed(color=discord.Color.red())
        try:
            e.set_author(name=f'{message.author}', icon_url=message.author.avatar.url)
        except:
            e.set_author(name=f'{message.author}')       
        e.description=f"**Message sent by {message.author.mention} deleted in {message.channel.mention}.**"
        if len(message.content) > 1000:
            content = message.content[:900] + "..."
            e.add_field(name="Message Content:", value=f"`{content}`")
        else:
            e.add_field(name="Message Content:", value=f"`{message.content}` \u200b")
        if len(message.attachments) > 0:
            attachmentlinks = ""
            for attachment in message.attachments:
                attachmentlinks = attachmentlinks + attachment.url + "\n"
            e.add_field(name="Attachment Links:", value=f"{attachmentlinks}", inline=False)
        e.set_footer(text=f"User ID: {message.author.id} | Message ID: {message.id}")
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        guild = messages[0].channel.guild
        e=discord.Embed(color=discord.Color.red())
        e.set_author(name=f"{guild.name}", icon_url=guild.icon.url)
        e.description=f"**Bulk messages deleted in {messages[0].channel.mention}, {len(messages)} messages deleted.**"
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        e=discord.Embed(color=discord.Color.orange())
        try:
            e.set_author(name=f"{before.author}", icon_url=f"{before.author.avatar.url}")
        except:
            e.set_author(name=f"{before.author}")    
        e.set_footer(text=f"User ID: {after.author.id}")
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))
        if before.author.bot:
            return
        if before.content != after.content or before.attachments != after.attachments:
            e.description=f"**Message sent by {before.author.mention} edited in {before.channel.mention}.**\n[Jump to message](https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id}/)"
            if before.content == after.content:
                e.add_field(name="Changes:", value=f"**`ONLY ATTACHMENTS REMOVED`**")
            else:
                if len(before.content) > 1000:
                    content = before.content[:900] + "..."
                    e.add_field(name="Before:", value=f"`{content}`")
                else:
                    e.add_field(name="Before:", value=f"`{before.content}` \u200b")
                if len(after.content) > 1000:
                    content = after.content[:900] + "..."
                    e.add_field(name="After:", value=f"`{content}`")
                else:
                    e.add_field(name="After:", value=f"`{after.content}` \u200b")
            if len(before.attachments) > 0:
                attachmentlinks = ""
                for attachment in before.attachments:
                    attachmentlinks = attachmentlinks + attachment.url + "\n"
                e.add_field(name="Attachment Links:", value=f"{attachmentlinks}", inline=False)
            await log_channel.send(embed=e)
        else:
            if before.pinned == True and after.pinned == False:
                e.description=f"**Message unpinned in {after.channel.mention}.**\n[Jump to message](https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id}/)"
                await log_channel.send(embed=e)
            elif before.pinned == False and after.pinned == True:
                e.description=f"**Message was pinned in {after.channel.mention}.**\n[Jump to message](https://discord.com/channels/{after.guild.id}/{after.channel.id}/{after.id}/)"
                await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.green())
        e.set_author(name=f"{channel.guild.name}", icon_url=channel.guild.icon.url)
        e.description=f"**Channel created: {channel.mention} | #{channel.name}**"
        e.set_footer(text=f"Channel ID: {channel.id}")
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.red())
        e.set_author(name=f"{channel.guild.name}", icon_url=channel.guild.icon.url)
        e.description=f"**Channel deleted: #{channel.name}**"
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.blue())
        e.set_author(name=f"{before.guild.name}", icon_url=before.guild.icon.url)
        e.description=f"**Channel {before.mention} updated.**"
        e.set_footer(text=f"Channel ID: {before.id}")
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))
        if before.name != after.name:
            e.add_field(name="Channel's name changed:", value=f"**Before:** {before.name}\n**After:** {after.name}", inline=False)
            await log_channel.send(embed=e)
        if before.category != after.category:
            e.add_field(name="Channel's category changed:", value=f"**Before:** {before.category}\n**After:** {after.category}", inline=False)
            await log_channel.send(embed=e)
        if str(before.type) == 'text':
            if before.topic != after.topic or before.is_nsfw() != after.is_nsfw():
                if before.topic != after.topic:
                    e.add_field(name="Channel's topic changed:", value=f"**Before:** {before.topic}\n**After:** {after.topic}", inline=False)
                if before.is_nsfw() == True and after.is_nsfw() == False:
                    e.add_field(name="NSFW settings changed:", value=f"{after.mention} is not an NSFW channel anymore.", inline=False)
                if before.is_nsfw() == False and after.is_nsfw() == True:
                    e.add_field(name="NSFW settings changed:", value=f"{after.mention} is an NSFW channel now.", inline=False)
                await log_channel.send(embed=e)

        if str(before.type) == 'voice':
            if before.bitrate != after.bitrate:
                e.add_field(name="Channel's bitrate changed:", value=f"**Before:** {before.bitrate}\n**After:** {after.bitrate}", inline=False)
                await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        e=discord.Embed(color=discord.Color.green())
        try:
            e.set_author(name="Member joined", icon_url=member.avatar.url)
        except:    
            e.set_author(name="Member joined")
        e.description=f"{member.mention} | `{member.name}#{member.discriminator}`"
        try:
            e.set_thumbnail(url=member.avatar.url)
        except:
            pass    
        e.add_field(name="Account age:", value=member.created_at)
        e.set_footer(text=f"User ID: {member.id}")
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        e=discord.Embed(color=discord.Color.red())
        try:
            e.set_author(name="Member left", icon_url=member.avatar.url)
        except:
            e.set_author(name="Member left") 
        e.description=f"{member.mention} | `{member.name}#{member.discriminator}`\nJoined at `{member.joined_at.date()}`"
        #test
        try:
            e.set_thumbnail(url=member.avatar.url)
        except:
            pass    
        e.set_footer(text=f"User ID: {member.id}")
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        e=discord.Embed(color=discord.Color.orange())
        try:
            e.set_author(name="Member Updated", icon_url=after.avatar.url)
        except:
            e.set_author(name="Member Updated")   
        e.set_footer(text=f"User ID: {after.id}")
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))
        r_before = [role.id for role in before.roles]
        r_after = [role.id for role in after.roles]
        if before.nick != after.nick:
            e.description=f"{after.mention}'s Nickname changed."
            e.add_field(name="Before:", value=f"{before.nick}", inline=False)
            e.add_field(name="After:", value=f"{after.nick}", inline=False)
            await log_channel.send(embed=e)
        try:    
            if before.avatar.url != after.avatar.url:
                e.description=f"{after.mention}'s Avatar changed."
                #try:
                e.add_field(name="Before:", value=f"{before.avatar.url}", inline=False)
                #except:
                    #e.add_field(name="Before:", value="None", inline=False)
                #try:    
                e.add_field(name="After:", value=f"{after.avatar.url}", inline=False)
                #except:
                    #e.add_field(name="After:", value="None" ,inline=False)    
                await log_channel.send(embed=e)
            else:
                pass    
        except:
            e.description=f"{after.mention}'s Avatar changed."
            #try:
            e.add_field(name="Before:", value=f"{before.avatar.url}", inline=False)
            #except:
                #e.add_field(name="Before:", value="None", inline=False)
            #try:    
            e.add_field(name="After:", value=f"{after.avatar.url}", inline=False)
            #except:
                #e.add_field(name="After:", value="None" ,inline=False)    
            await log_channel.send(embed=e)            
        if before.roles != after.roles:
            r = list(set(r_before) ^ set(r_after))
            if True:
                if len(before.roles) < len(after.roles):
                    e.description=f"**{after.mention} was given the <@&{r[0]}> role.**"
                elif len(before.roles) > len(after.roles):
                    e.description=f"**{after.mention} was revoked the <@&{r[0]}> role.**"
                await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.blue())
        e.set_author(name="Server Updated", icon_url=after.icon.url)
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))
        if before.name != after.name or before.region != after.region or before.afk_timeout != after.afk_timeout or before.afk_channel != after.afk_channel or before.icon != after.icon or before.owner_id != after.owner_id or before.banner != after.banner:
            if before.name != after.name:
                e.add_field(name="Server's name changed:", value=f"**Before:** `{before.name}`\n**After:** `{after.name}`", inline=False)
            if before.region != after.region:
                e.add_field(name="Server's region changed:", value=f"**Before:** `{before.region}`\n**After:** `{after.region}`", inline=False)
            if before.afk_timeout != after.afk_timeout:
                e.add_field(name="Server's afk timeout changed:", value=f"**Before:** `{before.afk_timeout}`\n**After:** `{after.afk_timeout}`", inline=False)
            if before.afk_channel != after.afk_channel:
                e.add_field(name="Server's afk channel changed:", value=f"**Before:** `{before.afk_channel}`\n**After:** `{after.afk_channel}`", inline=False)
            if before.icon != after.icon:
                e.add_field(name="Server's icon changed:", value=f"**Now:** {after.icon.url}\n**Before:**", inline=False)
                e.set_image(url=before.icon.url)
            if before.owner_id != after.owner_id:
                e.add_field(name="Server's owner changed:", value=f"**Before:** <@{before.owner_id}>\n**After:** <@{after.owner_id}>", inline=False)
            if before.banner != after.banner:
                e.add_field(name="Server's banner changed:", value=f"**Now:** {after.banner.url}\n**Before:**", inline=False)
                e.set_image(url=before.banner.url)
            await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.green())
        e.set_author(name="Role Created", icon_url=role.guild.icon.url)
        e.description=f"{role.mention} | `{role.name}`"
        e.set_footer(text=f"Role ID: {role.id}")
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.red())
        e.set_author(name="Role Deleted", icon_url=role.guild.icon.url)
        e.description=f"@{role.name}"
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))

        await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        log_channel = self.bot.get_channel(SERVER_LOGS)
        e=discord.Embed(color=discord.Color.blue())
        e.set_author(name="Role Updated", icon_url=after.guild.icon.url)
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))
        if before.name != after.name or before.color != after.color:
            if before.name != after.name:
                e.add_field(name="Role's name changed:", value=f"**Before:** `{before.name}`\n**After:** `{after.name}`", inline=False)
            if before.color != after.color:
                e.add_field(name="Role's color changed:", value=f"**Before:** `{before.color.value}`\n**After:** `{after.color.value}`", inline=False)
            await log_channel.send(embed=e)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        log_channel = self.bot.get_channel(MEMBER_LOGS)
        e=discord.Embed(color=discord.Color.yellow())
        try:
            e.set_author(name=f"{member}", icon_url=member.avatar.url)
        except:
            e.set_author(name=f"{member}")
        e.timestamp = datetime.now(pytz.timezone('Europe/Vienna'))
        if before.channel != after.channel:
            if before.channel == None and after.channel != None:
                e.description=f"{member.mention} **joined voice channel {after.channel.mention}**"
                e.color = discord.Color.green()
                e.set_footer(text=f"Channel ID: `{after.channel.id}`")
            elif before.channel != None and after.channel == None:
                e.description=f"{member.mention} **left voice channel {before.channel.mention}**"
                e.color = discord.Color.red()
                e.set_footer(text=f"Channel ID: `{before.channel.id}`")
            elif before.channel != None and after.channel != None and before.channel != after.channel:
                e.description=f"{member.mention} **moved to {after.channel.mention}**"
                e.color = discord.Color.blue()
                e.set_footer(text=f"Channel ID before: `{before.channel.id}` | Channel ID after: `{after.channel.id}`")
            await log_channel.send(embed=e)"""


def setup(bot):
    bot.add_cog(logs(bot))
