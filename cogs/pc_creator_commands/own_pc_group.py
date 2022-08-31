import json
import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import Option
import json




"""class Case_Select(discord.ui.View):

    with open("cases.json", "r") as f:
            cases = json.load(f)
    options = []
    for case_name, Form_Factor_dict in cases.items():
        case_form_factor = Form_Factor_dict["Form_Factor"]

        if 'Micro-ATX' in case_form_factor:
            print(case_name)


    

        options.append(discord.SelectOption(label=case_name, description=", ".join(case_form_factor)))
    @discord.ui.select(placeholder="Choose one option", min_values=1, max_values=1, options=options)
    async def callback(self, select, interaction : discord.Interaction):
        with open("cases.json", "r") as f:
            cases = json.load(f)


        case_name = select.values[0]

        global chosen_case_form_factor
        chosen_case_form_factor = cases[case_name]["Form_Factor"]
        
        case_picture = cases[case_name]["url"]

        view = Motherboard_Select()
        
        await interaction.message.edit(content=f"**{case_name}**", view=None)
        await interaction.response.send_message(case_picture)
        await interaction.followup.send("Choose a motherboard", view=view)


class Motherboard_Select(discord.ui.View):   

    with open("motherboards.json", "r") as f:
            motherboards = json.load(f)

    options_motherboard = []


    for motherboard_name, specs_dict in motherboards.items():
        motherboard_form_factor = specs_dict["form_factor"]
        socket = specs_dict["socket"]
        ram_type = specs_dict["ram_type"]
        max_ram_size = specs_dict["max_ram_size"]
        gpu_slots = specs_dict["gpu_slots"]
        ram_slots = specs_dict["ram_slots"]
        sata_slots = specs_dict["sata_slots"]
        m2_slots = specs_dict["m.2_slots"]

        #global chosen_case_form_factor
        
        #if motherboard_form_factor in chosen_case_form_factor:
    options_motherboard.append(discord.SelectOption(label=motherboard_name, description=f"{socket}, {motherboard_form_factor}, {ram_type}, {max_ram_size}, {gpu_slots}, {ram_slots}, {sata_slots}, {m2_slots}"))

    @discord.ui.select(placeholder="Choose one option", min_values=1, max_values=1, options=options_motherboard)
    async def callback(self, select, interaction : discord.Interaction):
        with open("motherboards.json", "r") as f:
            motherboards = json.load(f)

        motherboard_name = select.values[0]
        
        motherboard_picture = motherboards[motherboard_name]["url"]
        
        await interaction.message.edit(content=f"**{motherboard_name}**", view=None)
        await interaction.response.send_message(motherboard_picture)"""

    
            
       

class own_pc(commands.Cog):

    def __init__(self, client):
        self.client = client 





    """@commands.slash_command(name='own_pc', description='Shows charts with benchmark of CPUs, GPUs or RAM', guild_ids=[708218806928932896])
    async def own_pc_slash(self, ctx):
        view = Case_Select()
        await ctx.respond("Choose the case", view=view)


    @commands.command()
    async def mhm(self, ctx):
        with open("cases.json", "r") as f:
            cases = json.load(f)

            for case_name, url_dict in cases.items():
                url = url_dict["url"]

                if "https://images-ext-1.discordapp.net/external/dKMZp2ndcg8B3v0yExfEm0TUz25aI_sbJxS5ATFRTZw/https/media.discordapp.net/attachments/802512035224223774/943740610966335508/IMG_4188-removebg-preview.png" in url:
                    print(case_name, url)  


    @commands.slash_command(name="new_case", guild_ids=[708218806928932896])    
    async def case(self, ctx, case_name : Option(str), url : Option(str), form_factor : Option(str), form_factor2 : Option(str, required = False), form_factor3 : Option(str, required = False), form_factor4 : Option(str, required = False)):
        with open("cases.json", "r") as f:
            cases = json.load(f)

        if case_name in cases:
            return False
        else:
            cases[case_name] = {}
            cases[case_name]["url"] = url
            cases[case_name]["Form_Factor"] = []
            cases[case_name]["Form_Factor"].append(form_factor)
            try:
                if not form_factor2 == None:
                    cases[case_name]["Form_Factor"].append(form_factor2)
            except:
                pass
            try:
                if not form_factor3 == None:
                    cases[case_name]["Form_Factor"].append(form_factor3)
            except:
                pass
            try:
                if not form_factor4 == None:
                    cases[case_name]["Form_Factor"].append(form_factor4)
            except:
                pass        
        #cases["case"].append({case_name : url})

        with open("cases.json", "w") as f:
            json.dump(cases,f)

            await ctx.respond(f"Added {case_name} \nurl: {url} \nForm_Factors: {form_factor}, {form_factor2}, {form_factor3}, {form_factor4}")




               
    async def get_motherboards(self):
        with open("motherboards.json", "r") as f:
            motherboards = json.load(f)
        return motherboards

    async def get_cases(self):
        with open("cases.json", "r") as f:
            cases = json.load(f)
        return cases 

    async def new_case(self, case_name, url):

        cases = await self.get_cases()
        
        cases["case"] = {}
        cases["case"]["name"] = {}  
        cases["case"]["name"] = case_name
        cases["case"]["name"]["url"] = url    

        with open("cases.json", "w") as f:
            json.dump(cases,f)
        return True     



    @commands.slash_command(name="new_motherboard", guild_ids=[708218806928932896])    
    async def case(self, ctx, motherboard_name : Option(str), url : Option(str), socket : Option(str), form_factor : Option(str), ram_type : Option(str), max_ram_size : Option(str), gpu_slots : Option(str), ram_slots : Option(str), sata_slots : Option(str), m2_slots : Option(str)):
        
        motherboards = await self.get_motherboards()

        if motherboard_name in motherboards:
            return False
        else:
            motherboards[motherboard_name] = {}
            motherboards[motherboard_name]["url"] = url
            motherboards[motherboard_name]["socket"] = socket
            motherboards[motherboard_name]["form_factor"] = form_factor
            motherboards[motherboard_name]["ram_type"] = ram_type
            motherboards[motherboard_name]["max_ram_size"] = max_ram_size
            motherboards[motherboard_name]["gpu_slots"] = gpu_slots
            motherboards[motherboard_name]["ram_slots"] = ram_slots
            motherboards[motherboard_name]["sata_slots"] = sata_slots
            motherboards[motherboard_name]["m.2_slots"] = m2_slots
            

        with open("motherboards.json", "w") as f:
            json.dump(motherboards,f)

            await ctx.respond(f"Added {motherboard_name} \nurl: {url} \nForm_Factor: {form_factor} \nRAM_Type: {ram_type} \nMax_RAM_Size: {max_ram_size} \nGPU_Slots: {gpu_slots} \nRAM_Slots: {ram_slots} \nSata_Slots: {sata_slots} \nM.2_Slots: {m2_slots}")"""


    
def setup(client):
    client.add_cog(own_pc(client))