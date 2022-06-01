import discord
from discord.ext import commands
from datetime import datetime
import json
from datetime import timedelta
from datetime import date
from discord.utils import get
import schedule
import time
from PIL import Image, ImageDraw, ImageFont
import asyncio
from discord.ext import tasks
from discord import Option
from discord.commands import permissions

if True:
    if True:
        with open ("json_files/counter-file.txt", "r") as d_m:
            data = d_m.readlines()
            d_m.close
        new_amt = data[64]
        data[0] = f"{new_amt}\n{data[0]}"
        data[59] = ""
        data[64] = "0"
        with open ("json_files/counter-file.txt", "w") as cf:
            cf.writelines(data)
            cf.close
        with open ("json_files/counter-file.txt", "r") as d_m:
            data = d_m.read().splitlines()
            d_m.close
        data = [string for string in data if string != ""]

        data_2 = list(int(x) for x in data)
        hundreds = round(max(data_2)/100 + .5)
        if hundreds == 0:
            hundreds = 1

        divier_5 = False
        if hundreds >= 10:
            while divier_5 == False:
                if hundreds % 5 == 0:
                    divier_5 = True
                    hundreds_1 = int(hundreds / 5)
                else:
                    hundreds += 1
        
        x = 1
        y = 500/hundreds_1
        line = Image.open("lrs_stats_tabelle.png")
        draw = ImageDraw.Draw(line)
        for i in range(hundreds):
            y_1 = 500-y*x+2
            draw.line((4, y_1, 724, y_1), fill=(45, 48, 52), width=2)
            x += 1
        draw.line((4, 502, 724, 502), fill=(45, 48, 52), width=2)
        x_punkte = 0
        punktn = int(0)
        for i in range(60):
            y_multi = data[punktn]
            y_punkte = int(500/hundreds/100*int(y_multi))
            y_punkte = 500-y_punkte
            xy = [(716-x_punkte, y_punkte-1),(724-x_punkte, y_punkte+7)]
            draw.ellipse(tuple(xy),fill=(88, 101, 242), outline=(88, 101, 242))
            x_punkte += 12
            punktn += 1
        punktn = int(0)
        x_punkte = 5
        punktn = int(0)
        for i in range(59):
            y_multi = data[punktn]
            y_punkte_1 = int(500-(500/hundreds/100*int(y_multi)))
            punktn += 1
            y_multi = data[punktn]
            y_punkte_2 = int(500-(500/hundreds/100*int(y_multi)))
            xy = [(714-x_punkte, y_punkte_2+3),(724-x_punkte, y_punkte_1+3)]
            draw.line(xy, fill=(88, 101, 242), width=3)
            x_punkte += 12
        lrs_picture = Image.open("lrs_stats_fertig.png")
        lrs_picture.paste(line, (5, 46))
        lrs_picture_text = ImageDraw.Draw(lrs_picture)
        lrs_picture_text.fontmode = "1"
        myFont = ImageFont.truetype('calibri.ttf', 20)
        x = 0
        y = 500/hundreds
        text = hundreds_1
        for i in range(text):
            y_1 = y*x+40
            if divier_5 == False:
                lrs_picture_text.text((731, y_1), f"{(hundreds-x)*100} msgs/day",font=myFont, fill=(255, 255, 255))
                x += 1
            elif divier_5 == True:
                hundreds_2 = hundreds
                if (hundreds_2-x)*100 % 1000 == 0:
                    lrs_picture_text.text((731, y_1), f"{(hundreds_2-x)*100} msgs/day",font=myFont, fill=(255, 255, 255))
                x += 5
        lrs_picture_text.text((731, 540), "0 msgs/day",font=myFont, fill=(255, 255, 255))
        lrs_picture.save("dailymsgs.png")

input()