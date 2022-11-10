import discord
from discord.ext import commands
import json
from datetime import datetime, timedelta
from dateutil import parser

bot = commands.Bot(command_prefix = '!',intents = discord.Intents.all())

THRESHOLD = 5
m = []

def antiraid(last_time,member):
    global m

    m.append(member)
    t1 = parser.parse(str(last_time))
    t2 = parser.parse(str(datetime.now()))
    t3 = t2 - t1
    seconds = round(t3.total_seconds())
    m.append(member)
    if seconds <= 10:
        if len(m) >= THRESHOLD:
            return True
        else:
            return False
        

@bot.event
async def on_member_join(member):
    with open('Cache.json') as f:
        cache = json.load(f)
    
    if 'Last_Time' in cache:
        last_time = cache['Last_Time']
    else:
        last_time = datetime.now()
    
    raid = antiraid(last_time,member.id)
    if raid:
        role = discord.utils.get(member.guild.roles,id = settings[guild]['Role'])
        channel = await bot.fetch_channel()    