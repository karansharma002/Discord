import discord
from discord.ext import commands, tasks
import requests
import json
import asyncio
import os




input()

@tasks.loop(seconds = 30)
async def update_status():
	r = requests.get('https://api.coingecko.com/api/v3/coins/binancecoin')
	data = json.loads(r.content)

	current_price = round(data['market_data']['current_price']['usd'], 2)
	price_change = round(data['market_data']['price_change_percentage_24h'], 1)

	if '-' in str(price_change):
		price_change = f'↙ {price_change}'
	else:
		price_change = f'↗ {price_change}'
	
	description = f"${current_price} {price_change}%"
    
	await bot.change_presence(activity=discord.Game(name=description))


print(data)
input()

from keep_alive import keep_alive
bot = commands.Bot(command_prefix = '!')

#! ENTER YOUR GUILD ID
GUILD = os.environ['GUILD']
api_key = os.environ['API_KEY']

@bot.event
async def on_ready():
  print('SERVER IS READY')

async def update_status():
    await bot.wait_until_ready()
    while True:
        url = "https://api.livecoinwatch.com/coins/single"

        payload = json.dumps({
        "currency": "USD",
        "code": "AVAX",
        "meta": True
        })
        headers = {
        'content-type': 'application/json',
        'x-api-key': api_key
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        data = json.loads(response.content)['rate']
        data = round(float(data), 2)
        gas = data * 0.001575
        gas = round(gas, 2)
        await bot.change_presence(activity=discord.Game(name=f'AVAX PRICE: ${data}'))

        await asyncio.sleep(25)

        url = "https://api.livecoinwatch.com/coins/single"

        payload = json.dumps({
        "currency": "USD",
        "code": "AVAX",
        "meta": True
        })
        headers = {
        'content-type': 'application/json',
        'x-api-key': api_key
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        data = json.loads(response.content)['rate']
        data = round(float(data), 2)
        gas = data * 0.001575
        gas = round(gas, 2)
        await bot.change_presence(activity=discord.Game(name=f'GAS PRICE: ${gas}'))
        await asyncio.sleep(25)

async def update_name():
    await bot.wait_until_ready()
    while True:
        if GUILD == 0:
            await asyncio.sleep(60)
            continue

        from bs4 import BeautifulSoup as bs

        r = requests.get('https://snowtrace.io/gastracker')
        soup = bs(r.content, 'lxml')

        app = soup.find_all('div', class_ = 'h4 text-success mb-1')

        data = []
        for x in app:
            data.append(x.text.replace('nAVAX',''))

        app = soup.find_all('div', class_ = 'h4 text-primary mb-1')
        for x in app:
            fast = x.text
            fast = fast.replace('nAVAX', '')
            data.append(fast)

        low = data[0].replace(' ','')
        average = data[2].replace(' ','')
        fast = data[1].replace(' ','')

        msg = "{} | {} | {}".format(low, average, fast)

        try:
            for guild in bot.guilds:
                await guild.me.edit(nick=msg)
        except:
            pass

        guild = await bot.fetch_guild(GUILD)
        role = discord.utils.get(guild.roles, id = os.environ['ROLE'])

        average = round(float(average))
        low = round(float(low))
        fast = round(float(fast))
        if average < 40 or low < 40 or fast < 40:
            color = discord.Color.green()

        elif average >= 40 and average < 80 or fast >= 40 and fast < 80 or low >= 40 and low < 80:
            color = discord.Color.orange()

        else:
            color = discord.Color.dark_red() 
          
        try:
          await role.edit(colour=color)

        except:
          pass
          
        await asyncio.sleep(25)

@bot.command()
async def gas(ctx):
    await ctx.send(f'Gas Price Is: __**{bot.user.mention}**__')

@bot.command()
async def price(ctx):
    #! AVEX PRICE
    url = "https://api.livecoinwatch.com/coins/single"

    payload = json.dumps({
    "currency": "USD",
    "code": "AVAX",
    "meta": True
    })
    headers = {
    'content-type': 'application/json',
    'x-api-key': '5d876c7d-46a0-4e45-8c37-fdd62d07993b'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = json.loads(response.content)['rate']
    data = round(float(data), 2)
    await ctx.send(f'AVAX Price Is: __**{data}**__')

bot.loop.create_task(update_name())
bot.loop.create_task(update_status())
keep_alive()
my_secret = os.environ['DISCORD_BOT_SECRET']
bot.run(my_secret)
