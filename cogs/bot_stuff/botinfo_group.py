
from datetime import datetime, timedelta
from platform import architecture, python_version
from time import time
import cpuinfo
from discord import Embed#, client
from discord.ext import commands
from psutil import Process, virtual_memory, cpu_percent
from discord import __version__ as discord_version
from discord import SlashCommandGroup
import discord
#from slash_commands_group import test
import json
#mport slash_commands_group


#command -> bot_group


async def info(ctx, client1):
    embed = Embed(title="Bot info", colour=ctx.author.colour, timestamp=datetime.now())
    embed.set_thumbnail(url=client1.user.avatar)

    proc = Process()
    with proc.oneshot():
        uptime = timedelta(seconds=time()-proc.create_time())
        cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
        mem_total = virtual_memory().total / (1024**2)
        mem_of_total = proc.memory_percent()
        mem_usage = mem_total * (mem_of_total / 100)
        #mem_usage = int(str(mem_usage).split(".")[0]) same Value???
        processor = cpuinfo.get_cpu_info()['brand_raw']
        cpuusage = cpu_percent()
        #cputype = cpuinfo.arch

    memusage = f"{mem_usage:,.3f}"
    memusage = int(memusage.split(".")[0])
    memtotal = str(f"{mem_total:,.0f}")
    memotoal = int(memtotal.replace(",",""))

    cputime = str(cpu_time)
    lencputime = len(cputime)
    cputime = cputime[:lencputime - 4] + "s"
    cputime = cputime.split(":")[2]

    uptime = str(uptime)
    lenuptime = len(uptime)
    uptime = uptime.split(".")[0]# + " HH/MM/SS"

    fields = [
        ("Bot version:", "1.11.0", True),
        ("Python version:", python_version(), True),
        ("Discord-API version:", discord_version, False),
        ("Uptime:", uptime, False),
        ("CPU:", processor, False),
        ("CPU usage:", f"{cpuusage}%", True),
        ("CPU timedelta:", cputime, True),
        ("Memory usage", f"{memusage} MiB / {memotoal} MiB ({mem_of_total:.0f}%):", False),
        ("Release-Github-Repo:", "https://github.com/YES-German/PC_Creator_2", False),
        ("Testing-Github-Repo:", "https://github.com/SleepyYui/PCC3", False),
    ]

    for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

    await ctx.respond(embed=embed)

