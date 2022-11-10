import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import datetime
import requests
import random
import asyncio
from datetime import datetime


bot = commands.Bot(command_prefix= '$',intents = discord.Intents.all(), case_insenstive = False)
bot.remove_command('help')
file_name = ''
word = ''
event_time = ''
@bot.event
async def on_ready():
    print('------------ DISCORD INSTANCE STARTED ----------')

@has_permissions(administrator = True)
@bot.command()
async def setup(ctx,channel:discord.TextChannel = None):
    if channel == None:
        await ctx.send(':information_source:  Command Usage: setup `#channel`')
        return
    else:
        with open('Config/Servers.json') as f:
            s = json.load(f)
        
        guild = str(ctx.guild.id)

        s[guild] = channel.id

        with open('Config/Servers.json','w') as f:
            json.dump(s,f,indent = 3)
        
        await ctx.send(':white_check_mark: Channel has been SET')

@has_permissions(administrator = True)
@bot.command()
async def upload(ctx,hashs:str = None):
    global word

    with open('Config/Servers.json') as f:
        s = json.load(f)
    
    if ctx.guild.id == s['Restricted']:
        global event_time
        attachment_url = ctx.message.attachments[0].url
        file_request = requests.get(attachment_url)
        with open(f'{hashs}.txt','w') as f:
            f.write(file_request.content.decode('UTF-8'))
        
        await ctx.send(':white_check_mark: File has been Uploaded')
        global file_name
        file_name = hashs
        words = [line.strip() for line in open(f'{file_name}.txt')]
        words = [x for x in words if x.strip()]
        name = random.choice(words)   
        word = name

@has_permissions(administrator = True)
@bot.command()
async def setduration(ctx,duration:str = None,max_servers:int = None):
    global word

    guild = str(ctx.guild.id)
    try:

        with open('Config/Servers.json') as f:
            s = json.load(f)
        
        global file_name
        if duration == None or max_servers == None:
            await ctx.send(':information_source: Command Usage: setduration `TIME (EXAMPLE: 01:40:00)`')
            return
        else:
            event_time = duration
            await ctx.send(f':white_check_mark: Event Duration Successfully SET\n`(Announcements will be sent at: {duration})`')
            f = '%H:%M:%S'
            nw = datetime.strftime(datetime.now(), f)
            diff = (datetime.strptime(event_time, f) - datetime.strptime(nw, f)).total_seconds()
   
            #HASH            
            await asyncio.sleep(diff)
            channel = await bot.fetch_channel(s[guild])
            embed=discord.Embed(description = word,color=0x00ff84)
            embed.set_author(name=f"Selected from ({file_name})")
            embed.timestamp = datetime.utcnow()
            await channel.send(embed = embed)

    except Exception:

        import traceback
        traceback.print_exc()   

@has_permissions(administrator = True)
@bot.command()
async def help(ctx):
    with open('Config/Servers.json') as f:
        s = json.load(f)
    
    if ctx.guild.id == s['Restricted']:
        embed=discord.Embed(color=0x6a57ff)
        embed.set_author(name="Commands Help")
        embed.add_field(name="setup", value="Set the channel to receive the messages", inline=False)
        embed.add_field(name="upload", value="Upload a text file", inline=False)
        embed.add_field(name="setduration", value="Set the event time", inline=False)
        embed.timestamp = datetime.utcnow()
        embed.set_footer(text = f'{ctx.author}')
        await ctx.send(embed=embed)

@has_permissions(administrator = True)
@bot.command()
async def restrict(ctx):
    with open('Config/Servers.json') as f:
        s = json.load(f)
    
    if not 'Restricted' in s:
        s['Restricted'] = ctx.guild.id
        with open('Config/Servers.json','w') as f:
            json.dump(s,f,indent = 3)
        
        await ctx.send(':lock: Restrictions APPLIED.')
    else:
        return


bot.run('ODIyMzQ1OTQ5MzUwNzIzNTg2.YFQ7WA.EEavLJ22N4pa2eXYg-zrU_TdXdc')