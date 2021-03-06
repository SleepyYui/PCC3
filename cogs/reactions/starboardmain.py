from datetime import datetime, timedelta
from random import choice
from discord import Embed
from discord.ext.commands import Cog
import discord, json
from discord.ext import commands
from discord.utils import get
import datetime

class Reactions(Cog):
	def __init__(self, client):
		self.client = client

	@Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.emoji.name == "⭐":
			channel = self.client.get_channel(payload.channel_id)
			message = await channel.fetch_message(payload.message_id)
			reaction = get(message.reactions, emoji=payload.emoji.name)
			if reaction and reaction.count >= 5:
				with open("json_files/starboard.json") as f:
					data = json.load(f)
				messagecontent = message.content
				messageid = payload.message_id
				try:
					attachments = message.attachments[0]
				except:
					attachments = None
				if messageid in data["staredmessages"]:
					return
				else:
					embed = discord.Embed(title=None, color=message.author.color, timestamp=message.created_at)
					if messagecontent != "":
						embed.add_field(name="I ( {}#{} / `{}` ) wrote following in #{}:".format(message.author.name, message.author.discriminator, message.author.id, message.channel.name), value=messagecontent)
						embed.add_field(name="Where?", value="[I ({}#{}) wrote that here](".format(message.author.name, message.author.discriminator) + message.jump_url + ")", inline=False)
					else:
						embed.add_field(name="I ( {}#{} / `{}` ) wrote nothing in #{}:".format(message.author.name, message.author.discriminator, message.author.id, message.channel.name), value="I just sent a picture :/")
						embed.add_field(name="Where?", value="[I ({}#{}) sent that here](".format(message.author.name, message.author.discriminator) + message.jump_url + ")", inline=False)
					embed.set_footer(text='Apparently more than 5 people liked it.')
					guild = self.client.get_guild(payload.guild_id)
					try:
						embed.set_image(url=message.attachments[0].url)
						#print(message.attachments[0].url)
						addimage = True
					except:
						addimage = False
					try:
						starchannel = discord.utils.get(guild.channels, name="starboard")
						webhooks = await starchannel.webhooks()
						if webhooks:
							for webhook in webhooks:
								await webhook.send(embed=embed, username=message.author.display_name, avatar_url=message.author.avatar.url)
								break
						elif not webhooks:
							webhook = await starchannel.create_webhook(name="StarboardHook")
							await webhook.send(embed=embed, username=message.author.display_name, avatar_url=message.author.avatar.url)
					except:
						return
						#return
						"""starchannel = await guild.create_text_channel("starboard")
						webhooks = await starchannel.webhooks()
						await starchannel.set_permissions(guild.get_role(guild.id), send_messages=False, read_messages=True, add_reactions=False, embed_links=False, attach_files=False, read_message_history=True, external_emojis=False)
						if webhooks:
							for webhook in webhooks:
								await webhook.send(embed=embed, username=message.author.display_name, avatar_url=message.author.avatar.url)
								break
						elif not webhooks:
							webhook = await message.channel.create_webhook(name="StarboardHook")
							await webhook.send(embed=embed, username=message.author.display_name, avatar_url=message.author.avatar.url)
							await never.gonna(give=you.up[0])"""
					data["staredmessages"].append(messageid)
					with open("json_files/starboard.json", 'w') as f:
						json.dump(data, f)



def setup(bot):
	bot.add_cog(Reactions(bot))