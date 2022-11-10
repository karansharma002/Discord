import discord
from discord.ext import commands
import requests
import json
import re
import asyncio

bot = commands.Bot(command_prefix = '!')

def convert(argument):
    time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d|w))+?")
    time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400,"w": 604800}
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key, value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} is an invalid time key! h|m|s|d are valid arguments"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} is not a number!")
    return round(time)

def sec_time(secs):
    days = secs//86400
    hours = (secs - days*86400)//3600
    minutes = (secs - days*86400 - hours*3600)//60
    seconds = secs - days*86400 - hours*3600 - minutes*60
    result = ("{0} day{1}, ".format(days, "s" if days!=1 else "") if days else "") + \
    ("{0} hour{1}, ".format(hours, "s" if hours!=1 else "") if hours else "") + \
    ("{0} minute{1}, ".format(minutes, "s" if minutes!=1 else "") if minutes else "") + \
    ("{0} second{1}".format(seconds, "s" if seconds!=1 else "") if seconds else "")
    return result

async def update_status():
    await bot.wait_until_ready()

    #! GAS DATA
    while True:
        r = requests.get('https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken')
        data = json.loads(r.content)
        data = data['result']

        fast = data['FastGasPrice']
        low = data['SafeGasPrice']
        average = data['ProposeGasPrice']

        msg = "⚡ {} 🤔 {} 🐌 {}".format(fast, average, low)
        await bot.user.edit(username=msg)
        await bot.change_presence(activity=discord.Game(name = 'Fast, Avg, Slow'))

        with open('Data.json') as f:
            data = json.load(f)
        
        if not 'Update_Time' in data:
            tm = 120
        
        else:
            tm = data['Update_Time']
        
        await asyncio.sleep(tm)

@bot.command()
async def eth(ctx):
    #! ETH PRICE DATA

    key = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"

    data = requests.get(key)
    data = data.json()
    eth = data['price']
    await ctx.send(f'__**ETH**__ Price is: {eth}')


@bot.command()
async def set_color(ctx):
    pass

@bot.command()
async def update_time(ctx, duration:str = None):
    if not duration:
        await ctx.send(':information_source: Command Usage: !updatetime `#DURATION IN M/S/H [EX: 1M]`')
        return

    duration = re.sub(r"\s+", "", duration, flags=re.UNICODE)
    duration = convert(duration)
    
    with open('Data.json') as f:
        data = json.load(f)
    
    data['Update_Time'] = int(duration)

    with open('Data.json', 'w') as f:
        json.dump(data,f,indent = 3)
    
    await ctx.send(':white_check_mark: Duration Changed')

@bot.command()
async def call_action(ctx, type_:str = None,*,msg:str = None):
    if not type_ or not msg:
        await ctx.send(':information_source: Command Usage: !updatetime `<Type [EX: Decreasing / Increasing]>` `<MSG>`')
        return
    
    type_ = type_.lower()

    if not type_ in ('decreasing', 'increasing'):
        await ctx.send(':warning: Invalid Type: Allowed Type: `[DECREASING / INCREASING]`')
        return

    with open('Data.json') as f:
        data = json.load(f)
    
    data[type_] = msg

    with open('Data.json', 'w') as f:
        json.dump(data,f,indent = 3)
    
    await ctx.send(':white_check_mark: Call To Action has been Updated.')

bot.add_task(update_status())

with open('Data.json') as f:
    data = json.load(f)

TOKEN = data['Token']
bot.run(TOKEN)

