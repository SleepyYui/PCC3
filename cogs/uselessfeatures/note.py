from datetime import datetime, timedelta
from random import choice
from discord import Embed
from discord.ext.commands import Cog
import discord, json
from discord.ext import commands
from discord.utils import get
from discord import Option
import datetime

class note(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.slash_command(name="note")
	async def notethis(self, ctx, note: Option(required = True)): #DAS DING IST CURSED, AENDERT NIX BITTE
		user = ctx.author
		with open("json_files/notes.json", "r") as f:
			notes = json.load(f)
		if str(user.id) not in notes:
			if note != "":
				notes[str(user.id)] = {}
				notes[str(user.id)]["1"] = note
				notes[str(user.id)]["2"] = ""
				notes[str(user.id)]["3"] = ""
				notes[str(user.id)]["4"] = ""
				notes[str(user.id)]["5"] = ""
				with open("json_files/notes.json", "w") as f:
					json.dump(notes,f)
				await ctx.respond("Noted")
			else:
				await ctx.respond("You can't note nothing.")
		else:
			if note != "":
				if notes[str(user.id)]["1"] == "":
					notes[str(user.id)]["1"] = note
				elif notes[str(user.id)]["2"] == "":
					notes[str(user.id)]["2"] = note
				elif notes[str(user.id)]["3"] == "":
					notes[str(user.id)]["3"] = note
				elif notes[str(user.id)]["4"] == "":
					notes[str(user.id)]["4"] = note
				elif notes[str(user.id)]["5"] == "":
					notes[str(user.id)]["5"] = note
				else:
					await ctx.respond(f"You can't have more than 5 notes.\nUse `.notes list` to list your notes, and `.notes delete X` to delete a note (with X as your note-number).\n<@{user.id}>")
					return
				with open("json_files/notes.json", "w") as f:
					json.dump(notes,f)
				await ctx.respond("Noted")
			else:
				await ctx.respond("You can't note nothing.")
		

	@commands.slash_command(name="notes")
	async def notes(self, ctx, subcommand: Option(required = True, choices=["help", "list", "delete"]), notenum: Option(int, required = False)):
		user = ctx.author
		if subcommand == "help":
			await ctx.respond("**Note commands:**\n\n`note` note something\n`notes list` list all your notes\n`notes delete` delete a note")
		elif subcommand == "list":
			with open("json_files/notes.json", encoding="utf-8-sig") as f:
				notes = json.load(f)
			userid = str(ctx.author.id)
			if userid in notes:
				await ctx.respond("<@" + str(ctx.author.id) + ">, your Notes:\n\n**Note** `1`**:** " + notes[userid]["1"] + "\n**Note** `2`**:** " + notes[userid]["2"] + "\n**Note** `3`**:** " + notes[userid]["3"] + "\n**Note** `4`**:** " + notes[userid]["4"] + "\n**Note** `5`**:** " + notes[userid]["5"])
			else:
				await ctx.respond("You don't have anything noted.")
		elif subcommand == "delete":
			if True:
				if notenum != None:
					notenum = str(notenum)
					#note2 = int(note)
					if notenum != "1" and notenum != "2" and notenum != "3" and notenum != "4" and notenum != "5":
						await ctx.respond("correct use: `notes delete X` with X as a Number between 1 and 5.")
					else:
						with open("json_files/notes.json", encoding="utf-8-sig") as f:
							notes = json.load(f)
						notes[str(user.id)][notenum] = ""
						with open("json_files/notes.json", "w") as f:
							json.dump(notes,f)
						await ctx.respond("Deleted note number " + notenum)
				#else:
					#await ctx.send("correct use: `notes delete X` with X as a Number between 1 and 5.")
			#except:
				#await ctx.send("correct use: `notes delete X` with X as a Number between 1 and 5.")
		else:
			await ctx.respond("Invalid argument. Use **/notes help** to get help.")


def setup(bot):
	bot.add_cog(note(bot))
