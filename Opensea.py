from asyncio import tasks
import requests
from bs4 import BeautifulSoup as bs
import discord
from discord.ext import commands,tasks
import json
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix= '!')

@bot.event
async def on_ready():
    print('------ BOT HAS STARTED -----')
    print(f'LOGGED IN FOR: ({len(bot.guilds)})')
    fetcher.start()

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0

    return '%.1f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

@bot.command()
async def floor(ctx):
    url = "https://api.opensea.io/api/v1/collections"

    querystring = {"asset_owner":"0x08d6499ae1bd25148c3c8ba62658225d37b2e55f","offset":"0","limit":"300"}

    headers = {"X-API-KEY": "4c0bc196e3834d84a95c6b90ebab3b18."}

    response = requests.request("GET", url, headers=headers, params=querystring)
    s = json.loads(response.content)
    floor_price = s[0]['stats']['floor_price']
    
    embed = discord.Embed(color = discord.Color.blue(),description = f'**Floor Price**: __{floor_price}__')
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text = f'Requested By: {ctx.author}',icon_url= ctx.author.avatar_url)
    await ctx.send(embed = embed)
    
@bot.command()
async def owners(ctx):
    url = "https://api.opensea.io/api/v1/collections"

    querystring = {"asset_owner":"0x08d6499ae1bd25148c3c8ba62658225d37b2e55f","offset":"0","limit":"300"}

    headers = {"X-API-KEY": "4c0bc196e3834d84a95c6b90ebab3b18."}

    response = requests.request("GET", url, headers=headers, params=querystring)
    s = json.loads(response.content)
    owners_ = s[0]['stats']['num_owners']
    owners_ = human_format(owners_)
    embed = discord.Embed(color = discord.Color.blue(),description = f'**Owners**: __{owners_}__')
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text = f'Requested By: {ctx.author}',icon_url= ctx.author.avatar_url)
    await ctx.send(embed = embed)

@bot.command()
async def setchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !setchannel `<#CHANNEL MENTION WHERE SALES LOG ARE SENT>`')
        return

    with open('Config/Settings.json') as f:
        settings = json.load(f)
    
    settings['Channel'] = channel.id

    with open('Config/Settings.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel Added!')

@tasks.loop(minutes = 5)
async def fetcher():
    with open('Config/Settings.json') as f:
        settings = json.load(f)
    
    if not 'Channel' in settings:
        return

    timestamp = datetime.now() - timedelta(days = 1)
    timestamp = timestamp.timestamp()

    url = "https://api.opensea.io/api/v1/events"

    querystring = {"account_address":"0x08d6499ae1bd25148c3c8ba62658225d37b2e55f","only_opensea":"false","offset":"0","limit":"30","occurred_after":timestamp}

    headers = {
        "Accept": "application/json",
        "X-API-KEY": "4c0bc196e3834d84a95c6b90ebab3b18"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    s = json.loads(response.content)
    for x in s['asset_events']:
        type_ = x['event_type']
            continue
        with open('Config/Transactions.json') as f:
            transactions = json.load(f)
        
        hash_id = x['transaction']['block_hash']
        if hash_id in transactions:
            continue

        image = x['asset']['image_url']
        price = x['total_price']
        token = x['asset']['token_id']
        asset_address = x['asset']['asset_contract']['address']
        seller = x['seller']['address']
        seller_name = str(seller[:4])+ "..." + str(seller[-4:])
        seller = "https://etherscan.io/address/{}".format(seller)
        type_ = x['transaction']['event_type']
        buyer = x['transaction']['from_account']['address']
        buyer_name = str(buyer[:4])+ "..." + str(buyer[-4:])
        buyer = "https://etherscan.io/address/{}".format(buyer)

        price = str(price).replace('0','')
        price = float(price) / 1000

        asset_url = f"https://opensea.io/assets/{asset_address}/{token}"
        rarity = 'https://rarity.tools/rebelbots/view/{}'.format(token)

        embed = discord.Embed(color = discord.Color.blue())
        embed.set_author(name = f"RebelBot {token} sold!",url = asset_url)
        embed.add_field(name = 'Amount',value =f'{price} ETH',inline = False)
        embed.add_field(name = 'Buyer',value =f"[{buyer_name}]({buyer})",inline = False)
        embed.add_field(name = 'Seller',value = f'[{seller_name}]({seller})',inline = False) 
        embed.add_field(name = 'Rarity',value = f'[Click Here]({rarity})',inline = False)
        embed.set_image(url = image)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(icon_url= bot.user.avatar_url)

        channel = await bot.fetch_channel(settings['Channel'])
        await channel.send(embed = embed)

        transactions[hash_id] = 'CONFIRMED'
        with open('Config/Transactions.json','w') as f:
            json.dump(transactions,f,indent = 3)


    
bot.run('ODc0MTQyNjkwMTk4MDI4MzI5.YRCq0g.0YXoBf6UybLXH2L5IxgMYbHrFGA')