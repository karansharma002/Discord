import discord
from discord.ext import commands, tasks
import requests
import json
import asyncio
import os
  
from keep_alive import keep_alive

bot = commands.Bot(command_prefix = '!')

GUILD = os.environ['GUILD']

@bot.event
async def on_ready():
    print('------ BNB BOT READY -------')
    update_status.start()

@tasks.loop(seconds = 30)
async def update_status():
    r = requests.get('https://api.coingecko.com/api/v3/coins/binancecoin')
    data = json.loads(r.content)

    current_price = round(data['market_data']['current_price']['usd'], 2)
    price_change = round(data['market_data']['price_change_percentage_24h'], 1)

    pc = price_change
    
    if '-' in str(price_change):
        price_change = f'↙ {price_change}'
    else:
        price_change = f'↗ {price_change}'

    description = f"${current_price} {price_change}%"

    try:
        for guild in bot.guilds:
            await guild.me.edit(nick=description)

    except:
        pass

    if '-' in str(pc):
        color = discord.Color.red()
    else:
        color = discord.Color.green() 

    guild = await bot.fetch_guild(GUILD)
    role = discord.utils.get(guild.roles, id = os.environ['ROLE'])

    try:
        await role.edit(colour=color)
    except:
        pass
    
    r = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=binancecoin&order=volume_desc&per_page=2&page=1&sparkline=false')
    data = json.loads(r.content)
    volume = data[0]['total_volume']
    description = f"24 Hour Volume: {volume}"
    await bot.change_presence(activity=discord.Game(name=description))
        
keep_alive()
my_secret = os.environ['DISCORD_BOT_SECRET']
bot.run(my_secret)
