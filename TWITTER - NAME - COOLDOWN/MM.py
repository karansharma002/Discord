from gc import get_stats
import discord
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions
from dateutil import parser
from datetime import datetime, timedelta, tzinfo
from datetime import date
import re
import pandas as pd
bot = commands.Bot(command_prefix= '!',intents = discord.Intents.all())
from dateutil.tz import gettz
data = {}
@bot.event
async def on_ready():
    print('-------------- SERVER HAS STARTED ---------------')
    update_time.start()

@tasks.loop(seconds = 60)
async def update_time():
    await bot.wait_until_ready()
    global data
    if data == {}:
        return

    t3 = parser.parse(str(data['Date']))
    t4 = parser.parse(str(datetime.now()))
    c = t3 - t4
    seconds = c.total_seconds()

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    days = round(days)
    hours = round(hours)
    minutes = round(minutes)

    if days == 0:

        msg = '{}H {}M'.format(hours,minutes)
    
    else:
        msg = '{}D {}H {}M'.format(days,hours,minutes)

    await bot.change_presence(status=discord.Status.online,activity=discord.Game(msg))


@bot.command()
async def setcountdown(ctx,days:str = None,tm:str = None):
    global data

    if days == None or tm == None:
        await ctx.send(':information_source:Usage: !setcooldown `<duration (EXAMPLE: (DATE) (TIME))>`')
        return

    else:
        dte = datetime.strptime(days,'%d/%m/%y')
        dt = str(dte)
        a = str(pd.to_datetime(str(dt)+' '+ str(tm)))
        t3 = parser.parse(a)
        t4 = parser.parse(str(datetime.now()))
        c = t3 - t4
        seconds = c.total_seconds()

        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        days = round(days)
        hours = round(hours)
        minutes = round(minutes)

        if days == 0:

            msg = '{}H {}M'.format(hours,minutes)
        
        else:
            msg = '{}D {}H {}M'.format(days,hours,minutes)

        await bot.change_presence(status=discord.Status.online,activity=discord.Game(msg))

        await ctx.send(':white_check_mark:  Cooldown has been Activated.')
        data['Date'] = a

@bot.command()
async def countdown(ctx):
    msg = '**Details of the next pump:**\n\n'

    global data
    if data == {}:
        return
    
    dt = {'Etc/GMT-9':'GMT+9 (Seoul)','Europe/London':'GMT (London)','America/New_York':"EST (New York)"}
    for x in dt.keys():
        a = datetime.now(gettz(x))
        a = a.replace(tzinfo= None)
        a = a.isoformat()

        b = data['Date']
        dts = datetime.fromisoformat(str(b))
        import pytz
        dts = dts.astimezone(gettz(x))
        ab = dts.strftime("%A, %B %d %Y")#%Y %I:%M:%S")
        ac = dts.strftime("%I:%M")
        a = f"{ab} | {ac}"
        msg += f'{a} {dt[x]}\n'

    await ctx.send(msg)


bot.run('ODMzNDE1MDA0ODE1ODg0Mjg4.YHyANQ.OdnTf9L-GR6vQX81-1XnQvWI56g')
