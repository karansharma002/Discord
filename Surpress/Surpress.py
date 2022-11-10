import discord
from discord.ext import commands

import asyncio

bot = commands.Bot(command_prefix = 'msup.', intents = discord.Intents.all())


@bot.event
async def on_ready():
    print('------------ SERVER READY -----------')
    

setups = []

import re

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


@commands.has_permissions(administrator = True)
@bot.command(name="add", description = 'Purge the channel after given time')
async def add(ctx, time:str):
    global setups
    await ctx.message.delete()
    duration = re.sub(r"\s+", "", time, flags=re.UNICODE)
    remaining = convert(duration)
    await ctx.send(f':white_check_mark: Added {time} DURATION!')
    setups.append([time, ctx.channel.id])

    await asyncio.sleep(remaining)

    if not [time, ctx.channel.id] in setups:
        return
    
    else:
        await ctx.channel.purge()

@commands.has_permissions(administrator = True)
@bot.command(name="remove", description = 'Remove the Setup')
async def remove(ctx, time:str):
    global setups
    if [time, ctx.channel.id] in setups:
        await ctx.send(':white_check_mark: Removed {time} DURATION!')
        setups.remove([time, ctx.channel.id])
        return
    
    else:
        await ctx.send(':warning: No configuration found for the given duration.')
        return


bot.run('OTQzNTcxMzk2NTg2NTA4Mjg4.Yg0_Vw.PIWI2Y-LwQRpOJ58ccFJIHccuio')