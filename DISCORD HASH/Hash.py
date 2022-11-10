
import string
import random
import discord
from discord.ext import commands, tasks
from datetime import datetime
import json

import os

bot = commands.Bot(command_prefix = 'pb!')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('------------- DISCORD BOT INSTANCE STARTED ---------------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)
    if message.content.startswith('pb!'):
        return

    if message.author.bot or message.webhook_id:
        pass

    else:
        return

    with open('Rules.json') as f:
        rules = json.load(f)
    
    content = message.content
    id_ = str(message.channel.id)
    if id_ in rules:
        for x in rules[id_]:
            if any(key_ in content for key_ in rules[id_][x]['Keyword']):
                text = ''
                role = discord.utils.get(message.guild.roles,id = rules[id_][x]['Role'])
                if not rules[id_][x]['Text'] == 'NONE':
                    text = f"{rules[id_][x]['Text'].replace('$','')} {role.mention}"
                else:
                    text = f"{role.mention}"
                await message.channel.send(text)

            elif any(key_.replace('+','') in content for key_ in rules[id_][x]['Keyword']):
                text = ''
                role = discord.utils.get(message.guild.roles,id = rules[id_][x]['Role'])
                if not rules[id_][x]['Text'] == 'NONE':
                    text = f"{rules[id_][x]['Text'].replace('$','')} {role.mention}"
                else:
                    text = f"{role.mention}"
                await message.channel.send(text)             
    

@bot.command()
async def add(ctx,channel:discord.TextChannel = None,role:discord.Role = None,keyword:str = None,*,msg:str = None):
    if not channel or not role or not keyword:
        await ctx.send(':information_source: Usage: pb!add `<#CHANNEL>` `<@ROLE>` `<KEYWORD or KEYWORDS WITH / SEPARTED>` `<TEXT>`')
        return

    with open('Rules.json') as f:
        rules = json.load(f)

    id_ = str(channel.id)
    if not id_ in rules:    
        rules[id_] = {}
    
    if not keyword.startswith('+'):
        await ctx.send('The keyword should begin with `+`')
        return
    
    if msg:
        if not msg.startswith('$'):
            await ctx.send('Text Message should begin with `$`')
    
    if '/' in keyword:
        keyword = keyword.replace(' ','').split('/')
    
    else:
        keyword = [keyword]

    while True:
        hash = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)) 
        hash = str(hash)
        if not hash in rules[id_]:
            break

    rules[id_][hash] = {}
    rules[id_][hash]['Keyword'] = keyword
    rules[id_][hash]['Role'] = role.id
    rules[id_][hash]['Text'] = 'NONE' if not msg else msg

    with open('Rules.json','w') as f:
        json.dump(rules,f,indent = 3)

    await ctx.send(':white_check_mark: Rule Added')

async def addrole(ctx,name:str = None,role:discord.Role = None):
    if not name or not role:
        await ctx.send(':information_source: Usage: pb!addrole `<Rule Name>` `<#ROLE MENTION>`')
        return
    
    with open('Rules.json') as f:
        rules = json.load(f)

    with open('CH.json') as f:
        cache = json.load(f)
    
    if not name in cache:
        await ctx.send(':warning: Rule not found!')
        return

    id_ = str(cache[name])
        
    if not 'Role' in rules[id_][name]:
        rules[id_][name]['Role'] = []

    rules[id_][name]['Role'].append(role.name) 
    with open('Rules.json','w') as f:
        json.dump(rules,f,indent = 3)
    
    await ctx.send(':white_check_mark: Role Added')

@bot.command()
async def delete(ctx,hash:str = None):
    if not hash:
        await ctx.send(':information_source: Usage: pb!delete `<HASH>`')
        return

    with open('Rules.json') as f:
        rules = json.load(f)
    
    for x in rules:
        print(rules[x])
        if hash in rules[x]:
            rules[x].pop(hash)
            with open('Rules.json','w') as f:
                json.dump(rules,f,indent = 3)
            
            await ctx.send(':white_check_mark: Rule Deleted')
            return
    
    await ctx.send("Hash doesn't exist!")
    
@bot.command()
async def channels(ctx):
    id_ = str(ctx.channel.id)
    
    with open('Rules.json') as f:
        rules = json.load(f)     

    msg = {}
    for x in rules:
        for y in rules[x]:
            if not x in msg:
                msg[x] = ""
            
            role = discord.utils.get(ctx.guild.roles,id = rules[x][y]['Role'])
            if rules[x][y]['Text'] == 'NONE':    
                msg[x] += f"```css\nKeyword(s): {rules[x][y]['Keyword']}\nHash: {y}\n```" 
            else:
                msg[x] += f"```css\nKeyword(s): {rules[x][y]['Keyword']}\nMessage: {rules[x][y]['Text']}\nHash: {y}\n```"
        
        channel = await bot.fetch_channel(int(x))
        await ctx.send(f'__**Rules List for channel "{channel.name}"**__')
        role = discord.utils.get(ctx.guild.roles,id = rules[x][y]['Role'])
        await ctx.send(f'> **@{role.name}**')
        await ctx.send(msg[x])
        msg.pop(x)
        
@bot.command()
async def fetchrule(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: pb!fetchrule <#CHANNEL>`')
        return

    with open('Rules.json') as f:
        rules = json.load(f)     

    msg = {}
    x = str(channel.id)
    if not x in rules:
        await ctx.send('--- NO Data Found for the Given Channel!! ---')
        return

    await ctx.send(f'**__Rules List for channel "{channel.name}"**__')

    for y in rules[x]:
        if not x in msg:
            msg[x] = ""
        
        if rules[x][y]['Text'] == 'NONE':    
            msg[x] += f"```css\nKeyword(s): {rules[x][y]['Keyword']}\nHash: {y}\n```" 
        else:
            msg[x] += f"```css\nKeyword(s): {rules[x][y]['Keyword']}\nMessage: {rules[x][y]['Text']}\nHash: {y}\n```"
        
    role = discord.utils.get(ctx.guild.roles,id = rules[x][y]['Role'])
    await ctx.send(f'> **@{role.name}**')
    await ctx.send(msg[x])

@bot.command()
async def backup(ctx,action:str = None):
    await ctx.send(f':white_check_mark: DATA Backup Successful')
    with open("Rules.json", "r") as f:
        rules = json.load(f)
    
    to = rules

    with open("Backup.json", "w") as f:
        json.dump(to,f,indent = 3)

@bot.command()
async def restore(ctx,action:str = None):
    if not 'Backup.json' in os.listdir():
        await ctx.send(':warning: No backup found!!')
        return
        
    await ctx.send(f':white_check_mark: Data Restored')
    with open("Backup.json", "r") as f:
        rules = json.load(f)
    
    to = rules

    with open("Rules.json", "w") as f:
        json.dump(to,f,indent = 3)

@bot.command()
async def help(ctx):
    msg = '''
    __Adding Rules__
    pb!add #channel @Role +keyword $message text

    __Delete Rules__
    pb!delete hash

    __Displaying all channels a Rule is set up in__
    pb!channels

    __Displaying all Rules and Hashes per channel__
    pb!fetchrule #channel

    __Creating a backup of all Data and Rules__
    pb!backup

    __Restoring a backup of all Data and Rules__
    pb!restore

    __Adding a Keyword__
    pb!addkeyword hash +keyword

    __Removing a Keyword__
    pb!removekeyword hash +keyword
    '''
    CUSTOM_GREEN = discord.Color.from_rgb(57,162,68) 
    embed = discord.Embed(title = 'Command List',color = CUSTOM_GREEN,description = msg)
    await ctx.send(embed = embed)

@bot.command()
async def addkeyword(ctx,hash:str = None,keyword:str = None):
    if not hash or not keyword:
        await ctx.send(':information_source: pb!addkeyword `<HASH>` `<KEYWORD>`')
        return
    
    with open('Rules.json') as f:
        rules = json.load(f)

    if not keyword.startswith('+'):
        await ctx.send('The keyword should begin with `+`')
        return

    for x in rules:
        if hash in rules[x]:
            rules[x][hash]['Keyword'].append(keyword)
            with open('Rules.json','w') as f:
                json.dump(rules,f,indent = 3)
            
            await ctx.send(':white_check_mark: Keyword Added')
            return
    
    await ctx.send("Hash doesn't exist!")


@bot.command()
async def removekeyword(ctx,hash:str = None,keyword:str = None):
    if not hash or not keyword:
        await ctx.send(':information_source: pb!removekeyword `<#HASH>` `<KEYWORD>`')
        return
    
    with open('Rules.json') as f:
        rules = json.load(f)
    
    for x in rules:
        if hash in rules[x]:
            rules[x][hash]['Keyword'].remove(keyword)
            with open('Rules.json','w') as f:
                json.dump(rules,f,indent = 3)
            
            await ctx.send(':white_check_mark: Keyword Removed')
            return
    
    await ctx.send("Hash doesn't exist!")

bot.run('ODc1Nzc1MzMxNzg3NzM5MTM3.YRabVg.JSmvor8NJw4NibTEf64jjeItQfI')