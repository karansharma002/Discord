from inspect import trace
import discord
from discord.ext import commands
from discord.ext.commands.core import command
import json
import random
import string
import os
from datetime import datetime, timedelta

from PIL import Image, ImageOps, ImageDraw, ImageFont


CURRENCY = 'exon(s)'
def get_prefix(bot,message):
    guild = str(message.guild.id)
    with open('Prefixes.json','r') as f:
        data = json.load(f)
    try:
        prefix = data[guild]['Prefix']
        return prefix

    except:
        return '!'

bot = commands.Bot(command_prefix = get_prefix)


@commands.has_permissions(manage_guild = True)
@bot.command()
async def prefix(ctx,*,val:str = None):
    with open('Prefixes.json','r') as f:
        data = json.load(f)
    

    if val == None:
        try:
            a = data[str(ctx.guild.id)]['Prefix']
        except KeyError:
            a = "!"
        await ctx.send(f':information_source: (`{ctx.guild})` **Prefix is:** (`{a})`\n:information_source: **Use:** **{a}{prefix}** `<newprefix>` **to change.**')

    elif not val == None:
        if not str(ctx.guild.id) in data:
            data[str(ctx.guild.id)] = {}
        data[str(ctx.guild.id)]['Prefix'] = val
        await ctx.send(f':white_check_mark: ** Server Prefix Has been Changed**\n:white_check_mark: **Your New Prefix Is:** (`{val}`)')
        with open('Prefixes.json','w') as f:
            json.dump(data,f,indent = 4)

@prefix.error
async def prefix_error(ctx,error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(':warning: You are missing the: `Manage Server` Permission.')

@bot.command(aliases = ['p'])
async def profile(ctx):
    author = str(ctx.author.id)
    
    with open('DT.json') as f:
        data = json.load(f)
    
    if not author in data:
        data[author] = {}
        data[author]['Coins'] = 0
        data[author]['Regular_Card'] = []
        data[author]['Event_Card'] = []
        data[author]['Space'] = 20
        with open('DT.json','w') as f:
            json.dump(data,f,indent = 3)
    
    balance = str(data[author]['Coins']) + ' ' + CURRENCY
    regular_card = len(data[author]['Regular_Card'])
    event_card = len(data[author]['Event_Card'])

    embed = discord.Embed(color = discord.Color.orange())
    embed.set_author(name = f"{ctx.author} | Profile",icon_url = ctx.author.avatar_url)
    embed.add_field(name = 'Balance', value = balance,inline = False)
    embed.add_field(name = 'Regular Cards', value = regular_card,inline = False)
    embed.add_field(name = 'Event Cards', value = event_card,inline = False)
    await ctx.send(embed = embed)

@bot.command(aliases = ['bal'])
async def balance(ctx):
    author = str(ctx.author.id)
    
    with open('DT.json') as f:
        data = json.load(f)
    
    if not author in data:
        data[author] = {}
        data[author]['Coins'] = 0
        data[author]['Regular_Card'] = []
        data[author]['Event_Card'] = []
        data[author]['Space'] = 20
        with open('DT.json','w') as f:
            json.dump(data,f,indent = 3)
    
    balance = str(data[author]['Coins']) + ' ' + CURRENCY

    embed = discord.Embed(color = discord.Color.orange(),description = f"**Balance:** __{balance}__")
    embed.set_author(name = f"{ctx.author} | Balance",icon_url = ctx.author.avatar_url)
    await ctx.send(embed = embed)

@bot.command()
async def donate(ctx,user:discord.User = None,amount:int = None):
    if not user or not amount:
        await ctx.send(f':information_source: Usage: !donate `<@user>` `<amount of {CURRENCY}>`')
        return
    

    author = str(ctx.author.id)
    author2 = str(user.id)

    with open('DT.json') as f:
        data = json.load(f)
    

    if not author in data:
        data[author] = {}
        data[author]['Coins'] = 0
        data[author]['Regular_Card'] = []
        data[author]['Event_Card'] = []
        with open('DT.json','w') as f:
            json.dump(data,f,indent = 3)
    
    if data[author]['Coins'] < amount:
        await ctx.send(':warning: Insufficient Balance!!')
        return

    if not author2 in data:
        data[author2] = {}
        data[author2]['Coins'] = 0
        data[author2]['Regular_Card'] = 0
        data[author2]['Event_Card'] = []
        data[author2]['Space'] = 20
        with open('DT.json','w') as f:
            json.dump(data,f,indent = 3)
    
    balance = str(amount) + ' ' + CURRENCY

    embed = discord.Embed(color = discord.Color.orange(),description = f"{ctx.author.mention}, You have donated {balance} to {user}")
    await ctx.send(embed = embed)

    data[author]['Coins'] -= amount
    data[author2]['Coins'] += amount
    with open('DT.json','w') as f:
        json.dump(data,f,indent = 3)


@commands.cooldown(1,86400,commands.BucketType.user)
@bot.command()
async def daily(ctx):
    with open('DT.json','r') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)
    COIN = str(random.randint(25,100))
    await ctx.send(f"{ctx.author.mention} :tada: You received __{COIN + ' ' + CURRENCY}__  as a Daily Gift. :tada:")
    data[author]['Coins'] += int(COIN)

    with open('DT.json','w') as f:
        json.dump(data,f,indent = 4)

@daily.error
async def dailyerror(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        if int(error.retry_after * 0.000277778) == 0:
            await ctx.send(f":warning `You already Claimed the Reward. Try again after` {int(error.retry_after * 0.0166667)} Minutes.") 
        else:
            await ctx.send(f":warning `You already Claimed the Reward. Try again after` {int(error.retry_after * 0.000277778)} hour(s).")

@bot.command(aliases = ['b'])
async def burn(ctx,code:str = None):
    if not code:
        await ctx.send(':information_source: !burn `<CARD CODE>`')
        return
    
    author = str(ctx.author.id)

    with open('DT.json') as f:
        data = json.load(f)
    
    if not author in data:
        await ctx.send(':warning: Invalid card code or you dont own any of these!!')
        return
    
    #! PENDING REFUND

    if code in data[author]['Regular_Card']:
        data[author]['Regular_Card'].remove(code)
        await ctx.send(':white_check_mark: You have burnt the Card.')
        with open('DT.json','w') as f:
            json.dump(data,f,indent = 4)

    elif code in data[author]['Event_Card']:
        data[author]['Event_Card'].remove(code)
        await ctx.send(':white_check_mark: You have burnt the Card.')
        with open('DT.json','w') as f:
            json.dump(data,f,indent = 4)

    else:
        await ctx.send(':warning: Invalid card code or you dont own any of these!!')
        return

@bot.command(aliases = ['v'])
async def view(ctx,code:str = None):
    if not code:
        await ctx.send(':information_source: !view `<CARD CODE>`')
        return
    
    with open('Cards.json') as f:
        cards = json.load(f)
    
    if not code in cards:
        await ctx.send(':warning: Invalid card code!!')
        return
    
    for x in os.listdir():
        if code in x:
            fp = x
            owner = await bot.fetch_user(cards[code]['Owner']) if not cards[code]['Owner'] == 'None' else 'None'
            url = x
            file = discord.File(x)
            embed = discord.Embed(color = discord.Color.purple())
            embed.set_author(name = 'Owned By: {owner}',icon_url= bot.user.avatar_url)
            embed.set_image(url = f'attachment://{x}')
            await ctx.send(embed = embed,file = file)
            return

@bot.command()
async def botban(ctx,member:discord.User = None):
    if member == None:
        await ctx.send(':information_source: Usage: !botban `<@USER>`')
        return

    else:
        with open('Bans.json') as f:
            bans = json.load(f)
        
        bans[str(member.id)] = 'BANNED'
        with open('Bans.json','w') as f:
            json.dump(bans,f,indent = 3)

        await ctx.send(f':white_check_mark: {member}, has been Banned.')

@bot.command()
async def botunban(ctx,member:discord.User = None):
    if not member:
        await ctx.send(':information_source: !botunban `<@user>`')
        return
        
    else:
        with open('Bans.json') as f:
            bans = json.load(f)
        
        user = str(member.id)
        if not user in bans:
            await ctx.send(f':warning: {member} is not BANNED')
            return
            
        else:
            bans.pop(user)
            await ctx.send(':white_check_mark: {member} has been Unbanned.')
            with open('Bans.json','w') as f:
                json.dump(bans,f,indent = 3)

@bot.command(aliases = ['deleteinv'])
async def deleteinventory(ctx,user:discord.User = None):
    if not user:
        await ctx.send(':information_source: Usage: !deleteinventory `<@user>`')
        return
    
    with open('DT.json') as f:
        data = json.load(f)
    
    author = str(user.id)

    data[user]['Regular_Card'] = []
    data[user]['Event_Card'] = []
    with open('DT.json','w') as f:
        json.dump(data,f,indent = 3)
    
    await ctx.send(f':white_check_mark: {user}, Inventory has been deleted!!')
    
@bot.command(aliases = ['cd'])
async def cooldown(ctx):
    pass

@bot.command()
async def trade(ctx):
    pass

@bot.command()
async def refurbish(ctx):
    pass

@commands.cooldown(1,1800,commands.BucketType.user)
@bot.command()
async def drop(ctx):

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    with open('Cards.json') as f:
        cards = json.load(f)
    
    cr = []
    num = 1 
    for x in os.listdir():
        if not x.endswith(('Cards','ttf','py','.json','.db')):
            if cards[x.split('.')[0]]['Rarity'] == 5:
                if random.randrange(100) <= 5:
                    file = discord.File(x)
                    embed = discord.Embed(color = discord.Color.purple())
                    embed.set_author(name = f"CODE: {x.split('.')[0]}",icon_url= bot.user.avatar_url)
                    embed.set_image(url = f'attachment://{x}')
                    await ctx.send(embed = embed,file = file)
                    num += 1
                    if num >= 3:
                        break

                    cr.append(x)

            elif cards[x.split('.')[0]]['Rarity'] == 4:
                if random.randrange(100) <= 10:
                    file = discord.File(x)
                    embed = discord.Embed(color = discord.Color.purple())
                    embed.set_author(name = f"CODE: {x.split('.')[0]}",icon_url= bot.user.avatar_url)
                    embed.set_image(url = f'attachment://{x}')
                    await ctx.send(embed = embed,file = file)
                    num += 1
                    if num >= 3:
                        break
                    cr.append(x)
            elif cards[x.split('.')[0]]['Rarity'] == 3:
                if random.randrange(100) <= 20:
                    file = discord.File(x)
                    embed = discord.Embed(color = discord.Color.purple())
                    embed.set_author(name = f"CODE: {x.split('.')[0]}",icon_url= bot.user.avatar_url)
                    embed.set_image(url = f'attachment://{x}')
                    await ctx.send(embed = embed,file = file)
                    num += 1
                    if num >= 3:
                        break
                    cr.append(x)

            elif cards[x.split('.')[0]]['Rarity'] == 2:
                if random.randrange(100) <= 25:
                    file = discord.File(x)
                    embed = discord.Embed(color = discord.Color.purple())
                    embed.set_author(name = f"CODE: {x.split('.')[0]}",icon_url= bot.user.avatar_url)
                    embed.set_image(url = f'attachment://{x}')
                    await ctx.send(embed = embed,file = file)
                    num += 1
                    if num >= 3:
                        break
                    cr.append(x)

            elif cards[x.split('.')[0]]['Rarity'] == 1:
                if random.randrange(100) <= 25:
                    file = discord.File(x)
                    embed = discord.Embed(color = discord.Color.purple())
                    embed.set_author(name = f"CODE: {x.split('.')[0]}",icon_url= bot.user.avatar_url)
                    embed.set_image(url = f'attachment://{x}')
                    await ctx.send(embed = embed,file = file)
                    num += 1
                    if num >= 3:
                        break

                    cr.append(x)
            elif cards[x.split('.')[0]]['Rarity'] == 0:
                if random.randrange(100) <= 15:
                    file = discord.File(x)
                    embed = discord.Embed(color = discord.Color.purple())
                    embed.set_author(name = f"CODE: {x.split('.')[0]}",icon_url= bot.user.avatar_url)
                    embed.set_image(url = f'attachment://{x}')
                    await ctx.send(embed = embed,file = file)
                    num += 1
                    if num >= 3:
                        break
                    cr.append(x)
    
    if not cr == []:
        await ctx.send(':arrow_right: Enter the Card Code in Chat to Choose: ')
        msg = await bot.wait_for('message',check = check)
        msg = msg.content
        if msg.content in cards:
            await ctx.send(':tada: You have CLAIMED the card. :tada:')
            cards[msg]['Owner'] = ctx.author.id
            with open('Cards.json','w') as f:
                json.dump(cards,f,indent = 3)

            with open('DT.json') as f:
                data = json.load(f)
            
            data['Regular_Card'].append(str(ctx.author.id))
            with open('DT.json','w') as f:
                json.dump(data,f,indent = 3)

        else:
            await ctx.send('Invalid Card Code, Please Retry!!')
    
    else:
        await ctx.send('Oops, No cards were dropped for you. Please retry after sometime!!')
        return


@drop.error
async def droperror(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        if int(error.retry_after * 0.000277778) == 0:
            await ctx.send(f":warning `You have recentlu used this command. Try again after` {int(error.retry_after * 0.0166667)} Minutes.") 
        else:
            await ctx.send(f":warning `You have recentlu used this command. Try again after` {int(error.retry_after * 0.000277778)} hour(s).")


@bot.command()
async def addcard(ctx,name:str = None,rr:int = None):
    if not name or not rr:
        await ctx.send(':information_source: Usage: !addcard `<NAME>` `<RARITY IN NUMBER 0-5>` `<CARD IMAGE AS ATTACHMENT>`')
        return
  
    if rr == 0:
        rarity = '✧✧✧✧✧'
    
    elif rr == 1:
        rarity = '✦✧✧✧✧'
    
    elif rr == 2:
        rarity = '✦✦✧✧✧'

    elif rr == 3:
        rarity = '✦✦✦✧✧'

    elif rr == 4:
        rarity = '✦✦✦✦✧'

    elif rr == 5:
        rarity = '✦✦✦✦✦'
    
    else:
        await ctx.send(':warning: Invalid Rarity Number')
        return


    with open('Cards.json') as f:
        cards = json.load(f)
    
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)) 
        code = str(code)
        if not code in cards:
            break

    for attachment in ctx.message.attachments:
        split_v1 = str(ctx.message.attachments).split("filename='")[1]
        filename = str(split_v1).split("' ")[0]
        import os
        extension = os.path.splitext(filename)[1]
        await attachment.save('Cards/'+code+extension)

    if not 'NUM' in cards:
        cards['NUM'] = 1
        cards[code] = {}
        cards[code]['Owner'] = 'None'
        cards[code]['URL'] = code
        cards[code]['Rarity'] = rr

    else:
        cards['NUM'] += 1
        cards[code] = {}
        cards[code]['Owner'] = 'None'
        cards[code]['URL'] = code
        cards[code]['Rarity'] = rr

    img = Image.open(code+extension)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./l_10646.ttf", 39)
    draw.text((40,790),f"{name}",(0, 0, 0),font=font)
    font = ImageFont.truetype("./l_10646.ttf", 30)
    draw.text((40,835),f"#1",(0, 0, 0),font=font)
    font = ImageFont.truetype("./arial.ttf", 20)
    draw.text((275,855),rarity,(0, 0, 0),font=font)
    img.save(code+extension)

    with open('Cards.json','w') as f:
        json.dump(cards,f,indent = 3)
    
    await ctx.send(f':white_check_mark: Card added!!\nCode: `{code}`')


bot.run('ODc5NTU1NjM1MDU2ODg5ODY2.YSRcBA.pkLAeclyy-woY8wSvf5RWLMdjy8')



