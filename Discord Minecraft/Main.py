import discord
from discord.ext import commands
import json
import random

bot = commands.Bot(command_prefix= '!')

coal = '<:coal:886128204610412595>'
stone = '<:stone:886128327528681492>'
rotten = '<:rotten:886129242981666826>'
zombie = '<:zombie2:886129455993614416>'
wood = '<:wood2:886130301829537812>'

'''
#SWORDS
Hyperion <:Iron_Sword:886119216602820639>
Aspect of the Dragons <:Diamond_Sword:886119233099030528>
Aspect of the End  <:Diamond_Sword:886119233099030528>
Shadow Fury  <:Diamond_Sword:886119233099030528>
Livid Dagger <:Iron_Sword:886119216602820639>
Valkyrie <:Iron_Sword:886119216602820639>
Astraea <:Iron_Sword:886119216602820639>
Scylla  <:Iron_Sword:886119216602820639>
Flower of Truth <:Enchanted_Poppy:886120078104469515>
'''

@bot.command()
async def shop(ctx,val:str = None,name:str = None):
    if not val:
        msg = '''
• pickaxe
• axe
• sword
• enchantments
• redstone
        '''
        embed = discord.Embed(color = discord.Color.orange(),description = msg)
        embed.set_author(name = "Available Shops",icon_url= ctx.author.avatar_url)
        await ctx.send(embed  = embed)
    
    else:
        if val == 'sword':
            msg = '''
<:Iron_Sword:886119216602820639> Hyperion - $1M
<:Diamond_Sword:886119233099030528> Aspect of the Dragons - $2M
<:Diamond_Sword:886119233099030528> Aspect of the End - $3M
<:Diamond_Sword:886119233099030528> Shadow Fury - $4M
<:Iron_Sword:886119216602820639> Livid Dagger - $10M
<:Iron_Sword:886119216602820639> Valkyrie - $12M
<:Iron_Sword:886119216602820639> Astraea - $15M
<:Iron_Sword:886119216602820639> Scylla - $20M
<:Enchanted_Poppy:886120078104469515> Flower of Truth - $30M
            '''  
            embed = discord.Embed(color = discord.Color.orange(),description = msg)
            embed.set_author(name = "Buy Sword",icon_url= ctx.author.avatar_url)
            await ctx.send(embed  = embed)   
         

@bot.event
async def on_ready():
    print('---------- MINECRAFT BOT STARTED --------------')

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(message.author.id)
    if not author in data:
        data[author] = {}
        data[author]['Items'] = {}


@bot.command()
async def mine(ctx):
    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)

    num1 = random.randint(1,4)
    num2 = random.randint(1,4)
    pickaxe = author['Equiped']['Pickaxe']
    await ctx.send(f'You mined {num1} {coal}, {num2} {stone} with your {pickaxe}')

    data[author]['Items']['Coal'] += 1
    data[author]['Items']['Stone'] += 1

    with open('Data.json','w') as f:
        json.dump(data,f,indent = 3)


@bot.command()
async def fight(ctx):
    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)
    num = random.randint(1,15)
    sword = author['Equiped']['Sword']
    await ctx.send(f'You killed a Zombie {zombie} with your {sword} and got {num} {rotten}')

    data[author]['Items']['Food'] += 1
    with open('Data.json','w') as f:
        json.dump(data,f,indent = 3)

@bot.command()
async def chop(ctx):
    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)
    num = random.randint(1,15)
    axe = author['Equiped']['Sword']
    await ctx.send(f'You chopped {num} {wood} with your {axe}')
    data[author]['Items']['Wood'] += 1
    with open('Data.json','w') as f:
        json.dump(data,f,indent = 3)

@bot.command()
async def chest(ctx):
    await ctx.send("You don't have any chests. Explore more to find one!!")
    
@bot.command()
async def shop(ctx):
    pass

@bot.command()
async def trade(ctx):
    pass

@bot.command()
async def give(ctx,user:discord.User = None,amount:int = None,*,name:str = None):
    if not amount or not name:
        await ctx.send(':information_source: Usage: !give `<@user>` `amount>` `<item name>`')
        return

    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)
    author2 = str(user.id)
    if not author2 in data:
        data[author2] = {}
    
    if not name in data[author]['Items']:
        await ctx.send(':warning: Invalid Item Name')
        return
    elif amount > data[author]['Item'][name] or amount <= 0:
        await ctx.send(":warning: You don't have that amount")
        return

    else:
        data[author]['Items'][name] -= amount
        data[author2]['Items'][name] += amount
        await ctx.send(':white_check_mark: You gave {amount} of {name} to {user}')
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)
        
@bot.command()
async def inventory(ctx):
    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)
    level = data[author]['Level']
    xp = data[author]['XP']
    money = data[author]['Money']
    stones = data[author]['Items']['Stone']
    coals = data[author]['Items']['Coal']
    woods = data[author]['Items']['Wood']
    flesh = data[author]['Items']['Food']
    embed = discord.Embed(title = ctx.author,color = discord.Color.orange())
    embed.add_field(name = 'Info',value = f"Money: ${money}\nLevel: {level}\nXP: {xp}",inline = True)
    embed.add_field(name = 'Ore',value = f"{stone} Stone: {stones}\n{coal} Coal: {coals}",inline = True)
    embed.add_field(name = 'Drops',value = f"{rotten} Rotten Flesh: {flesh}",inline = True)
    embed.add_field(name = 'Wood',value = f"{wood} Oak: {woods}",inline = True)
    await ctx.send(embed = embed)

@bot.command()
async def stats(ctx):
    pass

@bot.command()
async def level(ctx):
    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)
    level = data[author]['Level']
    xp = data[author]['XP']
    embed = discord.Embed(color = discord.Color.orange(),description = f"Level: {level}\nXP: {xp}")
    embed.set_author(name = ctx.author,icon_url = ctx.author.avatar_url)
    await ctx.send(embed = embed)


@bot.command()
async def axes(ctx):
    pass

@bot.command()
async def swords(ctx):
    pass

@bot.command()
async def pickaxes(ctx):
    pass

bot.run('')