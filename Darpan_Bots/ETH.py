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
    print('------ ETH BOT READY -------')
    update_status.start()


@tasks.loop(seconds = 30)
async def update_status():
    url = "https://api.livecoinwatch.com/coins/single"

    payload = json.dumps({
    "currency": "USD",
    "code": "ETH",
    "meta": True
    })
    headers = {
    'content-type': 'application/json',
    'x-api-key': '5d876c7d-46a0-4e45-8c37-fdd62d07993b'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = json.loads(response.content)['rate']
    data = round(float(data), 2)

    try:
        for guild in bot.guilds:
            await guild.me.edit(nick=f"${data}")

    except:
        pass

keep_alive()
my_secret = os.environ['DISCORD_BOT_SECRET']
bot.run(my_secret)
