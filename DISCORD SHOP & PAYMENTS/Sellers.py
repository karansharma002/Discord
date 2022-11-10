import discord
from discord.ext import commands
import json

import requests
bot = commands.Bot(command_prefix = '!',intents= discord.Intents.all())

@bot.event
async def on_ready():
    print('------------ BOT HAS STARTED -------------')

@bot.command()
async def verify(ctx,*,trans_id:str = None):
    guild = str(ctx.guild.id)
    with open('SET.json') as f:
        settings = json.load(f)
    
    if 'LOCK' in settings:
        if str(ctx.guild.id) in settings['LOCK']:
            return

    if not trans_id:
        await ctx.send(':information_source: Usage: !verify `<TRANSACTION ID or UNIQ ID>`')
        return
    
    with open('Transactions.json') as f:
        trans = json.load(f)

    if trans_id in trans:
        await ctx.send(':warning: Invalid Transaction ID')
        return
    
    with open('Keys.json') as f:
        keys = json.load(f)
    
    if not 'SELLIX' in keys:
        await ctx.send(':warning: Payment Methods are not SET Currently. Contact the administrator!!')
        return

    with open('Keys.json') as f:
        keys = json.load(f)
    
    TOKEN = keys['SELLIX']['KEY']
    URL = 'https://dev.sellix.io/v1'
    ID = trans_id
    Headers = {"Authorization": f'Bearer {TOKEN}'}
    r = requests.get(URL + "/orders?id=" + ID, headers=Headers).json()
    try:
        if r['error'] == 'Invoice Not Found':
            await ctx.send('Invalid ID')
            return
    except:
        pass

    try:
        status = r['data']['orders'][0]['total']['status']
        amount = r['data']['orders'][0]['product_title']
        amount = int(''.join(filter(str.isdigit,amount)))
        if not status == 'COMPLETED' or not status == 'REFUNDED':
            await ctx.send(':warning: The transaction is not confirmed yet. Please retry!')
            return
    
    except Exception as e:
        await ctx.send(f"ERROR: {e}")
        return

    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)
    if not guild in data:
        data[guild] = {}

    if not author in data:
        data[guild][author] = {}
        data[guild][author]['Coins'] = 0
    
    coins = amount
    data[guild][author]['Coins'] += coins

    with open('Data.json','w') as f:
        json.dump(data,f,indent = 3)
    
    trans[trans_id] = 'CONFIRMED'

    with open('Transactions.json','w') as f:
        json.dump(trans,f,indent = 3)
    
    embed = discord.Embed(color = discord.Color.green(),description = f'{ctx.author.mention} You have purchased {coins} Coins')
    await ctx.send(embed  = embed)

@bot.command()
async def setup(ctx):
    if not ctx.author.id == 728722527421202444:
        return

    with open('SET.json') as f:
        settings = json.load(f)
    
    if 'LOCK' in settings:
        if str(ctx.guild.id) in settings['LOCK']:
            return
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel


    await ctx.send('> Please enter your SELLIX API KEY')
    key_v = await bot.wait_for('message',check = check,timeout = 60)
    key_ = key_v.content
    await key_v.delete()

    await ctx.send('> Please enter your SELLIX Payment Link')
    payment1 = await bot.wait_for('message',check = check,timeout = 60)
    payment = payment1.content
    await payment1.delete()

    guild = str(ctx.guild.id)
    with open('Keys.json') as f:
        keys = json.load(f)
    
    keys['SELLIX'] = {}
    keys['SELLIX']['KEY'] = key_
    keys['SELLIX']['Payment'] = payment
    with open('Keys.json','w') as f:
        json.dump(keys,f,indent = 3)
    
    await ctx.send(':white_check_mark: SELLIX Authentication has been SET')
    return

    
#! FUNCTION TO ADD THE MONEY
@bot.command()
async def add(ctx,member:discord.User = None,val:float = None):
    if not ctx.author.id == 728722527421202444:
        return
    with open('SET.json') as f:
        settings = json.load(f)
    
    if 'LOCK' in settings:
        if str(ctx.guild.id) in settings['LOCK']:
            return

    if not member or not val:
        await ctx.send(':information_source: Usage: !add `<@user>` `<AMOUNT OF COINS>`')
        return
    
    with open('Data.json') as f:
        data = json.load(f)
    
    id_ = str(member.id)
    guild = str(ctx.guild.id)
    if not guild in data:
        data[guild] = {}

    if not id_ in data:
        data[guild][id_] = {}
        data[guild][id_]['Coins'] = val

    else:
        data[guild][id_]['Coins'] += val
    
    with open('Data.json','w') as f:
        json.dump(data,f,indent = 3)
    
    await ctx.send(f':white_check_mark: Coins has been added for {member}')

#! FUNCTION TO REMOVE THE MONEY
@bot.command()
async def remove(ctx,member:discord.User = None,val:float = None):
    if not ctx.author.id == 728722527421202444:
        return
    with open('SET.json') as f:
        settings = json.load(f)
    
    if 'LOCK' in settings:
        if str(ctx.guild.id) in settings['LOCK']:
            return

    if not member or not val:
        await ctx.send(':information_source: Usage: !remove `<@user>` `<AMOUNT OF COINS>`')
        return
    
    with open('Data.json') as f:
        data = json.load(f)
    
    id_ = str(member.id)
    guild = str(ctx.guild.id)
    if not id_ in data:
        data[guild][id_] = {}
        data[guild][id_]['Coins'] = 0
    else:
        if not data[guild][id_]['Coins'] - val < 0:
            data[guild][id_]['Coins'] -= val
        else:
            data[guild][id_]['Coins'] = 0
    
    with open('Data.json','w') as f:
        json.dump(data,f,indent = 3)
    
    await ctx.send(f':white_check_mark: Coins has been removed for {member}')

@commands.has_permissions(administrator = True)
@bot.command()
async def addproduct(ctx):

    with open('SET.json') as f:
        settings = json.load(f)
    
    if 'LOCK' in settings:
        if str(ctx.guild.id) in settings['LOCK']:
            return

    with open('Product.json') as f:
        products = json.load(f)
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    guild = str(ctx.guild.id)

    await ctx.send(f':arrow_double_down: Enter the Product Name you want to add')
    product_name = await bot.wait_for('message',check = check,timeout = 20)
    product_name = product_name.content
    if not guild in products:
        products[guild] = {}

    if product_name in products[guild]:
        await ctx.send(':warning: Product already exists')
        return

    await ctx.send(f':arrow_double_down: Enter the EMOJI for the {product_name}')
    emoji = await bot.wait_for('message',check = check,timeout = 20)
    emoji = emoji.content

    await ctx.send(f':arrow_double_down: Enter the PRICE for the {product_name}')
    price = await bot.wait_for('message',check = check,timeout = 20)
    price = price.content

    await ctx.send(f':arrow_double_down: Mention the channel for the {product_name} to fetch the KEYS')
    chann = await bot.wait_for('message',check = check,timeout = 20)
    chann = chann.content
    chann = chann.replace('>','')
    chann = chann.replace('<','')
    chann = chann.replace('#','')
    products[guild][product_name] = {}
    products[guild][product_name]['Price'] = price
    products[guild][product_name]['Emoji'] = str(emoji)
    products[guild][product_name]['Channel'] = int(chann)
    with open('Product.json','w') as f:
        json.dump(products,f,indent = 2)
    
    await ctx.send(f':white_check_mark: {product_name} has been ADDED in the Products.')

@commands.has_permissions(administrator = True)
@bot.command()
async def post(ctx,channel:discord.TextChannel = None):
    with open('SET.json') as f:
        settings = json.load(f)
    
    if 'LOCK' in settings:
        if str(ctx.guild.id) in settings['LOCK']:
            return
            
    if not channel:
        await ctx.send(':information_source: Usage: !post `<#CHANNEL WHERE THE SHOP MESSAGE IS ACTIVATED>`')
        return

    with open('Product.json') as f:
        products = json.load(f)

    guild = str(ctx.guild.id)

    if not guild in products:
        await ctx.send(':warning: Products are not set')
        return

    msg = ''
    emojis = []
    for x in products[guild]:
        msg += f"{products[guild][x]['Emoji']} - {x} - ${products[guild][x]['Price']}\n"
        emojis.append(str(products[guild][x]['Emoji']))

    embed = discord.Embed(color = discord.Color.green(),title = '__React down below to choose your desired bot__', description =  msg)
    embed.set_footer(text = bot.user.name,icon_url = bot.user.avatar_url)
    msgg = await channel.send(embed = embed)
    for x in emojis:
        await msgg.add_reaction(x)


#! FUNCTION TO ADD THE PRODUCTS
@bot.command()
async def lock(ctx,guild:str = None):
    if not ctx.author.id == 728722527421202444:
        return

    if not guild:
        await ctx.send(':information_source: Usage: !lock `<GUILD ID>`')
        return
    
    try:
        await bot.fetch_guild(int(guild))
    except:
        await ctx.send(':warning: Invalid GUILD ID.')
        return

    with open('SET.json') as f:
        settings = json.load(f)
    
    if not 'LOCK' in settings:
        settings['LOCK'] = []

    settings['LOCK'].append(guild)
    with open('SET.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Access LOCKED')

#! FUNCTION TO ADD THE PRODUCTS
@bot.command()
async def unlock(ctx,guild:str = None):
    if not ctx.author.id == 728722527421202444:
        return
        
    if not guild:
        await ctx.send(':information_source: Usage: !unlock `<GUILD ID>`')
        return
    
    try:
        await bot.fetch_guild(int(guild))
    except:
        await ctx.send(':warning: Invalid GUILD ID.')
        return

    with open('SET.json') as f:
        settings = json.load(f)
    
    if not 'LOCK' in settings:
        await ctx.send(':white_check_mark: Access Unlocked')
        return

    settings['LOCK'].remove(guild)
    with open('SET.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Access Unlocked')

@bot.command()
async def balance(ctx,member:discord.User = None):
    with open('SET.json') as f:
        settings = json.load(f)
    
    if 'LOCK' in settings:
        if str(ctx.guild.id) in settings['LOCK']:
            return

    if not member:
        member = ctx.author
    
    with open('Data.json') as f:
        data = json.load(f)
    
    id_ = str(member.id)

    if not id_ in data:
        coin_bal = 0
    else:
        coin_bal = data[id_]['Coins']
    
    embed = discord.Embed(color = discord.Color.green(),description = f'{coin_bal} **__Coins__**')
    embed.set_author(name = f"{member} | Balance",icon_url=member.avatar_url)
    await ctx.send(embed = embed)

@bot.command()
async def setlogchannel(ctx,channel:discord.TextChannel = None):
    if not ctx.author.id == 728722527421202444:
        return

    with open('SET.json') as f:
        settings = json.load(f)
    
    if 'LOCK' in settings:
        if str(ctx.guild.id) in settings['LOCK']:
            return

    if not channel:
        await ctx.send(':information_source: Usage: !setlogchannel `<#CHANNEL WHERE ORDER DETAILS ARE SENT UPON PURCHASE>`')
        return
    
    guild = str(ctx.guild.id)
    if not guild in settings:
        settings[guild] = {}
    
    settings[guild]['Channel'] = channel.id

    with open('SET.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel has been set')

@bot.event
async def on_raw_reaction_add(payload):
    with open('SET.json') as f:
        settings = json.load(f)
    
    with open('Product.json') as f:
        products = json.load(f)

    guild = str(payload.guild_id)
    if not guild in products:
        return

    channel = await bot.fetch_channel(payload.channel_id)
    user = channel.guild.get_member(payload.user_id)
    emoji = payload.emoji
    emoji = str(emoji)

    for x in products[guild]:
        if products[guild][x]['Emoji'] == emoji:
            with open('Data.json') as f:
                data = json.load(f)
            
            author = str(user.id)
            if not author in data:
                await user.send(':warning: Insufficient Balance to buy the produt')
                return
            
            if data[author]['Coins'] < float(products[guild][x]['Price']):
                await user.send(':warning: Insufficient Balance to buy the produt')
                return
            
            data[author]['Coins'] -= float(products[guild][x]['Price'])
            with open('Data.json','w') as f:
                json.dump(data,f,indent = 3)
            
            await user.send(f":tada: You have bought: {x} for {float(products[guild][x]['Price'])} Coins")
            key = ''
            chann = await bot.fetch_channel(products[guild][x]['Channel'])
            messages = await chann.history(limit=5).flatten()
            for m in messages:
                key = m.content
                await m.delete()
                break

            await user.send(f"Your KEY IS: `{key}`")
            with open('SET.json') as f:
                settings = json.load(f)
            
            guild = str(guild)
            if guild in settings:
                if 'Channel' in settings[guild]:
                    ch = await bot.fetch_channel(int(settings[guild]['Channel']))
                    embed = discord.Embed(color = discord.Color.green())
                    embed.set_author(name = f"{user} Bought product",icon_url= user.avatar_url)
                    embed.add_field(name = 'Product Name',value = x,inline = False)
                    embed.add_field(name = 'Price', value = products[guild][x]['Price'],inline = False)
                    await ch.send(embed = embed)

@bot.command()
async def addpackage(ctx):
    if not ctx.author.id == 728722527421202444:
        return

    with open('SET.json') as f:
        settings = json.load(f)
    
    if 'LOCK' in settings:
        if str(ctx.guild.id) in settings['LOCK']:
            return

    with open('Package.json') as f:
        products = json.load(f)
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    guild = str(ctx.guild.id)

    await ctx.send(f':arrow_double_down: Enter the Package Name you want to add')
    product_name = await bot.wait_for('message',check = check,timeout = 20)
    product_name = product_name.content
    if not guild in products:
        products[guild] = {}

    if product_name in products[guild]:
        await ctx.send(':warning: Package already exists and has been REPLACED.')


    await ctx.send(f':arrow_double_down: Enter the PRICE for the {product_name}')
    price = await bot.wait_for('message',check = check,timeout = 20)
    price = price.content


    products[guild][product_name] = int(price)
    with open('Package.json','w') as f:
        json.dump(products,f,indent = 2)
    
    await ctx.send(f':white_check_mark: {product_name} has been ADDED in the Packages.')
    
@bot.command()
async def postpackage(ctx,channel: discord.TextChannel = None):
    if not ctx.author.id == 728722527421202444:
        return

    with open('SET.json') as f:
        settings = json.load(f)
    
    if 'LOCK' in settings:
        if str(ctx.guild.id) in settings['LOCK']:
            return

    with open('Keys.json') as f:
        keys = json.load(f)

    with open('Package.json') as f:
        products = json.load(f)

    
    guild = str(ctx.guild.id)
    if not guild in products:
        await ctx.send(':warning: No Package Found!! Please add the Packages using !addpackage')
        return

    if not 'SELLIX' in keys:
        SELLIX = 'Not Available'
    else:
        SELLIX = keys['SELLIX']['Payment']

    with open('Keys.json') as f:
        keys = json.load(f)
    
    description = f'''
    **__Information__**
    *If you have not made the payment yet, please send the total amount of EURO to the address below.*\n
    **SELLIX Address**: `{SELLIX}`\n
    **__Note:__** *``Please use: !verify (YOUR TRANS / UNIQ ID) to confirm the Transaction``*.
    '''
    embed = discord.Embed(color = discord.Color.green(),title = 'Buying Coins Help',description = description)
    sorted_list = sorted(products[guild],key = products[guild].get,reverse = True)
    for x in sorted_list:
        embed.add_field(name = x,value = f"Price: {products[guild][x]}",inline = False)
    
    await ctx.send(embed = embed)

bot.run('ODc0NTU4MDExNjEwMzcwMDU4.YRItng.Drffb_VTKNFAGXI-fTO2FIrN9Ps')

    
