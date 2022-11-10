import discord
from discord.ext import commands,tasks
import json
import pandas as pd
from datetime import date
from datetime import timedelta
from datetime import datetime
from dateutil import parser

bot = commands.Bot(command_prefix= '%')

@bot.event
async def on_ready():
    print('---------- SERVER HAS STARTED ---------')
    await bot.wait_until_ready()
    trigger.start()

@tasks.loop(seconds = 45)
async def trigger():
    with open('Settings.json') as f:
        s = json.load(f)
    
    if not 'TIME' in s or not 'COMMAND' in s or not 'Channel' in s:
        return
    
    try:
        tm = s['TIME1']
        t1 = parser.parse(str(tm))
        t2 = parser.parse(str(datetime.now().strftime('%d/%m/%y %H:%M:%S')))
        t3 = t1 - t2
        t3 = round(t3.total_seconds())
        print(t3)
        if t3 <= 0:
            cmd = s['COMMAND']
            channel = await bot.fetch_channel(s['Channel'])
            msg = await channel.send(cmd)
            #await msg.delete()
            dt = datetime.strptime(tm, '%d/%m/%y %H:%M:%S')
            dt = dt + timedelta(days = 1)
            s['TIME1'] = str(dt)
            with open('Settings.json','w') as f:
                json.dump(s,f,indent = 3)

        tm = s['TIME2']
        t1 = parser.parse(str(tm))
        t2 = parser.parse(str(datetime.now().strftime('%d/%m/%y %H:%M:%S')))
        t3 = t1 - t2
        t3 = round(t3.total_seconds())
        print(t3)
        if t3 <= 0:
            cmd = s['COMMAND']
            channel = await bot.fetch_channel(s['Channel'])
            msg = await channel.send(cmd)
            #await msg.delete()
            dt = datetime.strptime(tm, '%d/%m/%y %H:%M:%S')
            dt = dt + timedelta(days = 1)
            s['TIME2'] = str(dt)
            with open('Settings.json','w') as f:
                json.dump(s,f,indent = 3)
        

    except Exception as e:
        print(e)
        return
        

@bot.command()
async def setchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !setchannel `<CHANNEL WHERE THE COMMAND IS EXECUTED>`')
        return


    with open('Settings.json', 'r') as f:
        settings = json.load(f)

    settings['Channel'] = channel.id

    with open('Settings.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel has been set')  

@bot.command()
async def settime(ctx,var1:str = None,var2:str = None):
    if not var1 or not var2:
        await ctx.send(':information_source: Usage: !settime `<TIME1>` `<TIME2>` `(EXAMPLE: 04:10 HH:MM)`')
        return
    
    if var2.count(':') > 1:
        await ctx.send(':warning: Invalid Format')
        return

    if var1.count(':') > 1:
        await ctx.send(':warning: Invalid Format')
        return

    with open('Settings.json', 'r') as f:
        settings = json.load(f)
    
    dt = datetime.now()
    a = pd.to_datetime(str(dt)+' '+ str(var1))
    a = a.strftime('%d/%m/%y %H:%M:%S')
    settings['TIME1'] = a
    dt = datetime.now()
    b = pd.to_datetime(str(dt)+' '+ str(var2))
    b = b.strftime('%d/%m/%y %H:%M:%S')
    settings['TIME2'] = b

    with open('Settings.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Time has been set')  
    
@bot.command()
async def setcommand(ctx,*,var:str = None):
    if not var:
        await ctx.send(':information_source: Usage: !setcommand `<COMMAND NAME TO TRIGGER>`')
        return
    
    with open('Settings.json') as f:
        settings = json.load(f)
    
    settings['COMMAND'] = var

    with open('Settings.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Command has been set')

TOKEN = 'YOUR TOKEN HERE'
bot.run(TOKEN)