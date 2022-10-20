import re
import discord, json
from discord.ext import commands


data_file_name = "json_files/data.json"
class PersistentButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    """@discord.ui.button(
        label="Create Ticket",
        style=discord.ButtonStyle.link,
        url="https://discord.com/channels/@me/986681363858071552",
        emoji="🎟️"
    )
    async def createticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        return
        with open(data_file_name) as f:
            data = json.load(f)
        ticket_number = int(data["ticket-counter"])
        ticket_number += 1
        ticket_category = discord.utils.get(interaction.user.guild.categories, name="TICKETS")
        ticket_channel = await interaction.user.guild.create_text_channel("ticket-{}".format(ticket_number), category=ticket_category)#interaction.user.guild.get_channel(interaction.channel_id).category)
        await ticket_channel.set_permissions(interaction.user.guild.get_role(interaction.user.guild.id), send_messages=False, read_messages=False)
        await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        for role_id in data["ticket-support-roles"]:
            role = interaction.user.guild.get_role(int(role_id))
            await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
        em = discord.Embed(title="New ticket from {}#{}".format(interaction.user.name, interaction.user.discriminator), color=13565696)
        em.add_field(name="Don't worry", value="Don't worry " + interaction.user.mention + ", you will get help soon.")
        pinged_msg_content = ""
        pinged_content_msg = ""
        if data["roles-to-mention"] != []:
            for role_id in data["roles-to-mention"]:
                role = interaction.user.guild.get_role(int(role_id))
                pinged_msg_content += role.mention
                pinged_msg_content += "\n"
                pinged_content_msg += role.mention
                pinged_content_msg += " "
        if pinged_msg_content != "":
            em.add_field(name = "Support team", value = pinged_msg_content)
        await ticket_channel.send(content=f"{interaction.user.mention} {pinged_content_msg}", embed=em)
        data["ticket-channel-ids"].append(ticket_channel.id)
        data["ticket-counter"] = int(ticket_number)
        with open(data_file_name, 'w') as f:
            json.dump(data, f)
        await interaction.response.send_message(f"Created Ticket in {ticket_channel.mention}", ephemeral=True)"""

class PersistentButtonLoad(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        with open(data_file_name, encoding="utf-8-sig") as f:
                data = json.load(f)
        channel = self.client.get_guild(int(data["ticket-react-guild-id"])).get_channel(int(data["ticket-react-channel-id"]))
        await self.client.http.delete_message(channel.id, int(data["ticket-react-message-id"]))
        embed = discord.Embed(title="Support Ticket", description="React to this message with 🎟️ to open a ticket.", color=13565696)
        embed.add_field(name="Info", value="We provide help with any problems you have with the game or server. If you don't know how to do something; or even want to report someone on this server, just create a ticket and we try to help as soon as possible.", inline=True)
        embed.add_field(name="UPDATE", value="You can now also use the `/support` command to create a Ticket.", inline=True)
        embed.set_footer(text="Creating a ticket without a reason can lead to a warn. Not answering (creating a ticket and not writing anything in it) is also counted as unreasonable.")
        a=PersistentButton()
        a.add_item(discord.ui.Button(label="Create Ticket 🎟️",style=discord.ButtonStyle.link,url="https://discord.com/channels/@me/986681363858071552"))
        message = await channel.send(embed=embed, view=a)
        data["ticket-react-message-id"] = int(message.id)
        with open(data_file_name, 'w') as f:
                json.dump(data, f)

class TicketCog(commands.Cog):
    def __init__(self, client):
        self.bot = client

    async def dataExists(ctx,isAdmin=False):
        try:
            with open(data_file_name, encoding="utf-8-sig") as f:
                data = json.load(f)
                return data
        except:
            contact = ""
            if not isAdmin:
                contact = ", please contact an bot developer."
            await ctx.send('[ERROR]: File '+ data_file_name +' doesn\'t exist'+contact)
            return

    async def SendLog(self, ctx, file):
        with open(data_file_name) as f:
            data = json.load(f)
        try:
            ticket_log_channel = discord.utils.get(ctx.guild.channels, name="ticket-logs")
            await ticket_log_channel.send("Ticket Closed. Here is the log:", file=file)
        except:
            ticket_category = discord.utils.get(ctx.guild.categories, name="TICKETS")
            ticket_log_channel = await ctx.guild.create_text_channel("ticket-logs", category=ticket_category)
            await ticket_log_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
            for role_id in data["ticket-support-roles"]:
                role = ctx.guild.get_role(int(role_id))
                await ticket_log_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
            await ticket_log_channel.send("Ticket Closed. Here is the log:", file=file)
        return True

    @commands.command(name='create_ticket', brief='Creates a ticket message')
    @commands.has_permissions(administrator=True)
    async def create_ticket(self, ctx):
        await ctx.message.delete()
        data = await TicketCog.dataExists(ctx, True)
        if  data is None :
            return
        embed = discord.Embed(title="Support Ticket", description="React to this message with 🎟️ to open a ticket.", color=13565696)
        embed.add_field(name="Info", value="We provide help with any problems you have with the game or server. If you don't know how to do something; or even want to report someone on this server, just create a ticket and we try to help as soon as possible.", inline=True)
        embed.set_footer(text="Creating a ticket without a reason can lead to a warn. Not answering (creating a ticket and not writing anything in it) is also counted as unreasonable.")
        message = await ctx.send(embed=embed, view=PersistentButton())
        data["ticket-react-message-id"] = int(message.id)
        data["ticket-react-guild-id"] = int(message.guild.id)
        data["ticket-react-channel-id"] = int(message.channel.id)
        try:
            with open(data_file_name, 'w') as f:
                json.dump(data, f)
        except:
            await ctx.send('[ERROR]: File '+ data_file_name+', it isn\'t writable try again')

    @commands.command(name='ticket_help', brief='Shows help', description='[prefix]ticket_help shows the ticket commands')
    async def ticket_help(self, ctx):
        data = await TicketCog.dataExists(ctx)
        if  data is None :
            return
        valid_user = False
        for role_id in data["ticket-support-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        if ctx.author.guild_permissions.administrator or valid_user:
            em = discord.Embed(title="Ticket Help", description="", color=13565696)
            em.add_field(name="create_ticket", value="Creates a Reaction message to create tickets.")
            em.add_field(name="close", value="Closes the ticket channel")
            em.add_field(name="addsupport <role_id> <mentionRole=True>", value="Add role to ticket support")
            em.add_field(name="delsupport <role_id>", value="Remove role from ticket support")
            em.add_field(name="addmentionrole <role_id>", value="Adds a mentioned role")
            em.add_field(name="delmentionrole <role_id>", value="Removes a mentioned role")
            await ctx.send(embed=em)


    @commands.command(name='close', brief='Close ticket', description='closes the ticket')
    async def close(self, ctx):
        data = await TicketCog.dataExists(ctx)
        if  data is None :
            return
        if ctx.channel.id in data["ticket-channel-ids"]:
            channel_id = ctx.channel.id
            em = discord.Embed(title="Closing ticket", description="Are you sure you want to close this ticket? Reply with 'close' if you are.", color=13565696)
            await ctx.send(embed=em)
            ans = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            if ans.content.lower() == "close":
                messages = await ctx.channel.history(limit=None, oldest_first=True).flatten()
                ticketContent = " ".join(
                    [f"{message.author.name} | {message.content}\n" for message in messages]
                )
                ticket_name = ctx.channel.name
                with open(f"tickets/{ticket_name}.txt", "w", encoding="utf8") as f:
                    f.write(f"Here is the message log for ticket: {ticket_name}\n----------\n\n")
                    f.write(ticketContent)
                await ctx.channel.delete()
                index = data["ticket-channel-ids"].index(channel_id)
                del data["ticket-channel-ids"][index]
                with open('json_files/data.json', 'w') as f:
                    json.dump(data, f)
                fileObject = discord.File(f"tickets/{ticket_name}.txt")
                await TicketCog.SendLog(self, ctx, fileObject)
            else:
                await ctx.send("Ok, didn't close the ticket.")


    @commands.command(name='addsupport', brief='Add support role')
    async def addsupport(self, ctx, role_id : discord.Role, mentionRole = "true"):
        data = await TicketCog.dataExists(ctx)
        if  data is None :
            return
        valid_user = False

        for role_id in data["ticket-support-roles"]:
            try:
                if ctx.guild.get_role(role_id.id) in ctx.author.roles:
                    valid_user = True
            except:
                pass

        if valid_user or ctx.author.guild_permissions.administrator:
            if role_id not in data["ticket-support-roles"]:
                try:
                    data["ticket-support-roles"].append(str(role_id.id))
                    if str(mentionRole) == "true":
                        data["roles-to-mention"].append(str(role_id.id))
                    with open('json_files/data.json', 'w') as f:
                        json.dump(data, f)
                    em = discord.Embed(title="Add support", description="You have successfully added `{}` to the support team.".format(role_id.name), color=13565696)
                    await ctx.send(embed=em)
                except:
                    em = discord.Embed(title="Add support", description="This isn't a valid role ID. Please try again with a valid role ID.")
                    await ctx.send(embed=em)
            else:
                em = discord.Embed(title="Add support", description="That role already has access to tickets!", color=13565696)
                await ctx.send(embed=em)
        else:
            em = discord.Embed(title="Add support", description="Sorry, you don't have permission to use that command.", color=13565696)
            await ctx.send(embed=em)


    @commands.command(name='delsupport', brief='Delete support role')
    async def delsupport(self, ctx, role_id : discord.Role):
        data = await TicketCog.dataExists(ctx)
        if  data is None :
            return
        valid_user = False
        for role in data["ticket-support-roles"]:
            try:
                if ctx.guild.get_role(role) in ctx.author.roles:
                    valid_user = True
            except:
                pass

        if valid_user or ctx.author.guild_permissions.administrator:
            try:
                valid_roles = data["ticket-support-roles"]
                if str(role_id.id) in valid_roles:
                    index = valid_roles.index(str(role_id.id))
                    del valid_roles[index]
                    data["ticket-support-roles"] = valid_roles
                    with open('json_files/data.json', 'w') as f:
                        json.dump(data, f)
                    em = discord.Embed(title="Delete Support", description="You have successfully removed `{}` from the support team.".format(role_id.name), color=13565696)
                    await ctx.send(embed=em)
                else:
                    em = discord.Embed(title="Delete Support", description="That role already does not have access to tickets!", color=13565696)
                    await ctx.send(embed=em)
            except:
                em = discord.Embed(title="Delete Support", description="This is not a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)
        else:
            em = discord.Embed(title="Delete Support", description="Sorry, you don't have permission to use that command.", color=13565696)
            await ctx.send(embed=em)

    @commands.command(name='addmentionrole', brief='Add mentionable role')
    async def addmentionrole(self, ctx, role_id : discord.Role):
        data = await TicketCog.dataExists(ctx)
        if  data is None :
            return
        valid_user = False
        for role_id in data["ticket-support-roles"]:
            try:
                if ctx.guild.get_role(role_id.id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        if valid_user or ctx.author.guild_permissions.administrator:
            if role_id not in data["roles-to-mention"]:
                try:
                    data["roles-to-mention"].append(str(role_id.id))
                    with open('json_files/data.json', 'w') as f:
                        json.dump(data, f)
                    em = discord.Embed(title="Add mention", description="You have successfully added `{}` to the list of mentioned roles.".format(role_id.name), color=13565696)
                    await ctx.send(embed=em)
                except:
                    em = discord.Embed(title="Add mention", description="This isn't a valid role ID. Please try again with a valid role ID.")
                    await ctx.send(embed=em)
            else:
                em = discord.Embed(title="Add mention", description="That role already receives pings when tickets are created.", color=13565696)
                await ctx.send(embed=em)
        else:
            em = discord.Embed(title="Add mention", description="Sorry, you don't have permission to use that command.", color=13565696)
            await ctx.send(embed=em)


    @commands.command(name='delmentionrole', brief='Delete mentionable role')
    async def delmentionrole(self, ctx, role_id : discord.Role):
        data = await TicketCog.dataExists(ctx)
        if  data is None :
            return
        valid_user = False
        for role in data["ticket-support-roles"]:
            try:
                if ctx.guild.get_role(role) in ctx.author.roles:
                    valid_user = True
            except:
                pass

        if valid_user or ctx.author.guild_permissions.administrator:
            try:
                pinged_roles = data["roles-to-mention"]
                if str(role_id.id) in pinged_roles:
                    index = pinged_roles.index(str(role_id.id))
                    del pinged_roles[index]
                    data["roles-to-mention"] = pinged_roles
                    with open('json_files/data.json', 'w') as f:
                        json.dump(data, f)
                    em = discord.Embed(title="Delete mention", description="You have successfully removed `{}` from the list of mentioned roles.".format(role.name), color=13565696)
                    await ctx.send(embed=em)
                else:
                    em = discord.Embed(title="Delete mention", description="That role isn't getting pinged when new tickets are created!", color=13565696)
                    await ctx.send(embed=em)
            except:
                em = discord.Embed(title="Delete mention", description="This is not a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)
        else:
            em = discord.Embed(title="Delete mention", description="Sorry, you don't have permission to run that command.", color=13565696)
            await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(TicketCog(bot))
    bot.add_cog(PersistentButtonLoad(bot))