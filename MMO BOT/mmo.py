import discord
from discord.ext import commands, tasks
import json

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print('READY')

@bot.event
async def on_message(message):
    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(message.author.id)
    if not author in data:
        data[author] = {}
        data[author]['Points'] = 0
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)
    
    await bot.process_commands(message)

#! ADMIN COMMAND

@bot.command()
async def createcoin(ctx, name:str = None, emoji:str = None):
    if not name or not emoji:
        await ctx.send(':warning: Usage: !createcoin `<currency name>` `<emoji>`')
        return

    with open('Config.json') as f:
        config = json.load(f)
    
    config['Currency'] = {}
    config['Currency']['Name'] = name + ' ' + emoji
    
    with open('Config.json', 'w') as f:
        json.dump(config,f,indent = 3)
    
    await ctx.send(':white_check_mark: Currency Modified')

@bot.command()
async def givecoins(ctx, role:discord.Role,points:int):
    with open('Data.json') as f:
        data = json.load(f)

    num = 0
    for user in role.members:
        num += 1
        author = str(user.id)        
        if not author in data:
            data[author] = {}
            data[author]['Points'] = 0
        
        data[author]['Points'] += points
        
    with open('Data.json', 'w') as f:
        json.dump(data,f,indent = 3)

    await ctx.send(f':white_check_mark: Added {points} {currency()} to {num} of Users.')

@bot.command()
async def removecoins(ctx, role:discord.Role,points:int):
    with open('Data.json') as f:
        data = json.load(f)
        
    num = 0
    for user in role.members:
        num += 1
        author = str(user.id)        
        if not author in data:
            data[author] = {}
            data[author]['Points'] = 0
        
        if not data[author]['Points'] == 0:
            data[author]['Points'] -= points
    
    with open('Data.json', 'w') as f:
        json.dump(data,f,indent = 3)

    await ctx.send(f':white_check_mark: Added {currency()} to {num} of Users.')

@bot.command()
async def income(ctx, role:discord.Role, points:int = None, max:int = None):
    if not role or not points or not max:
        await ctx.send(':information_source: Command Usage: !income <role> <points> <max points per day>')
        return
    
    await ctx.send(':white_check_mark: INCOME Modified.')


@bot.command()
async def additem(ctx,name:str = None,price:int = None,chance:str = None):
    if not name or not price or not id:
        await ctx.send(':information_source: Usage: !additem `<NAME>` `<PRICE>` `<chance>` `<IMAGE AS ATTACHMENT>`')
        return

    with open('ID.json') as f:
        id_ = json.load(f)

    if id in id_:
        await ctx.send(':warning: Another Product already exists with the SAME ID.')
        return

    with open('Products.json') as f:
        products = json.load(f)

    if ctx.message.attachments == []:
        await ctx.send(':warning: Product Image is not attached.')
        return

    products[name] = {}
    products[name]['Price'] = price
    products[name]['Chance'] = chance

    for attachment in ctx.message.attachments:
        split_v1 = str(ctx.message.attachments).split("filename='")[1]
        filename = str(split_v1).split("' ")[0]
        import os
        extension = name + os.path.splitext(filename)[1]
        products[name]['Path'] = extension
        await attachment.save(extension)
    
    with open('Products.json','w') as f:
        json.dump(products,f,indent = 3)

    await ctx.send(':white_check_mark: Item Added!')

@bot.command()
async def shop(ctx,num:int = None):

    with open('Products.json') as f:
        products = json.load(f)
    
    with open('STA.json') as f:
        settings =  json.load(f)

    if not num:
        embed = discord.Embed(title = 'Shop',color = discord.Color.blurple())
        for num,x in enumerate(products):
            embed.add_field(name = f"{num+1}: {x}",value = f"**Price:** __{products[x]['Price']}__\n**ID:** __{products[x]['ID']}__",inline = False)
        
        embed.set_footer(text = 'To Buy: !shop product number',icon_url= bot.user.avatar_url)
        await ctx.send(embed = embed)
        return
    
    else:
        num -= 1
        try:
            product = list(products.keys())[num]
        except IndexError:
            await ctx.send(':warning: Invalid Product')
            return
        
        author = str(ctx.author.id)

        name = products[product]
        price = products[product]['Price']
        chance = products[product]['Chance']

        with open('Data.json') as f:
            data = json.load(f)
        
        if not author in data:
            await ctx.send(':warning: Insufficient Balance!')
            return
            
        if data[author]['Points'] < price or price <= 0:
            await ctx.send(':warning: Insufficient Balance!')
            return
        
        data[author]['Points'] -= price
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)
        
        embed = discord.Embed(color = discord.Color.greyple(),description = f":tada: You've bought {name} for {price} {currency()}.")
        await ctx.send(embed = embed)

        embed = discord.Embed(color = discord.Color.green())
        embed.set_author(name = f'{ctx.author} | Item Bought',icon_url= ctx.author.avatar_url)
        embed.add_field(name = 'Product', value = name,inline = False)
        embed.add_field(name = 'Price', value = price,inline = False)
        await ctx.send(embed = embed)


@bot.command()
async def profile(ctx):
    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)

    embed = discord.Embed(title = ctx.author.name)
    embed.add_field(name = f'{currency}', value = data[author]['Points'], inline = False)
    embed.add_field(name = f'Items', value = 'None', inline = False)
    await ctx.send(embed = embed)

@bot.command()
async def leaderboard(ctx):
    with open('Data.json','r') as f:
        users = json.load(f)

    high_score_list1 = sorted(users, key=lambda x : users[x].get('Points', 0), reverse=True)
    msg1 = ''
    msg2 = ''
    for number,user in enumerate(high_score_list1):
        author = await bot.fetch_user(int(user))
        number += 1
        xp = users[user]['Points']
        msg1 += f"**‣ {number}**. {author} ⁃ Points: **{xp}**\n"
        if number == 15:
            break
        else:
            number += 1

    embed = discord.Embed(
        title= ":money_with_wings: Leaderboard",
        color= 0x05ffda,
        description= msg1
        )
        
    await ctx.send(embed = embed)

@bot.command()
async def russianroulette(ctx, bet:int = None):
    if not bet:
        await ctx.send(':information_source: Usage: !russianroulette `<BET AMOUNT>`')
        return
    
    if bet < 100:
        await ctx.send(':warning: Bet Amount should be greater than 100')
        return
    
    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)
    if data[author]['Points'] < 100:
        await ctx.send(f':warning: Insufficient {currency()}')
        return

@bot.command()
async def racing(ctx, bet:int = None):
    if not bet:
        await ctx.send(':information_source: Usage: !racing `<BET AMOUNT>`')
        return
    
    if bet < 100:
        await ctx.send(':warning: Bet Amount should be greater than 100')
        return
    
    else:
        await ctx.send(':warning: You dont have any PET.')
        return
    

@bot.command()
async def arena(ctx, user:discord.User = None, bet:int = None):
    if not user or not bet:
        await ctx.send(':information_source: Command Usage: !arena `<@USER>` `<BET AMOUNT>`')
        return
    
    else:
        await ctx.send(':warning: You dont have any equipments')
        return

@bot.command()
async def adjustlotto(ctx, coins:int = None, income:int = None):
    if not coins or not income:
        await ctx.send(':information_source: Usage: !adjustlotto `<COINS>` `<INCOME>`')
        return

    with open('Config.json', 'r') as f:
        config = json.load(f)
    
    config['Coins'] = coins
    config['Income'] = income
    with open('Config.json', 'w') as f:
        json.dump(config,f,indent = 3)
    
    await ctx.send(':white_check_mark: Lotto Settings Modified')

@bot.command()
async def lotto(ctx):
    with open('Config.json', 'r') as f:
        config = json.load(f)
    
    if not 'Coins' in config:
        coins = 200
    else:
        coins = config['Coins']
    
    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)
    if data[author]['Points'] < coins:
        await ctx.send(f':warning: Insufficient {currency()}')
        return
    
    await ctx.send(':white_check_mark: You have put a bet in LOTTO. Winners announcing soon!!')

bot.run('ODI5OTUxNzQxNDUzNTMzMTg2.YG_myg.BBfSHEkoq9r3f_Q5_IMB_PxMwm8')