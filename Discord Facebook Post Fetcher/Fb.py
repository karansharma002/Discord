from inspect import trace
from attr import has
import discord
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions
import requests
import wget
import json
import os
import traceback
import pyshorteners

bot = commands.Bot(command_prefix= '!')

@bot.event
async def on_ready():
    print(' ------- ready ------')
    print(bot.user)
    await fetch_data.start()

@tasks.loop(seconds = 20)
async def fetch_data():
    with open('Sent.json') as f:
        sent = json.load(f)
    
    with open('Token.json') as f:
        tk = json.load(f)
    
    if not 'Channel' in tk or not 'Token' in tk:
        return

    channel = await bot.fetch_channel(tk['Channel'])
    Token = tk['Token']

    params = {"access_token":Token}
    
    url = f'https://graph.facebook.com/v10.0/2994709387221321/published_posts?fields=attachments'
    r = requests.get(url,params = params)
    data = json.loads(r.content)
    try:
        message = data['data'][0]['id']
        if message in sent:
            return
        
        
        source = data['data'][0]['attachments']['data'][0]['media']['source']
        wget.download(source)
        url = f'https://graph.facebook.com/v10.0/{message}'
        r = requests.get(url,params = params)
        data2 = json.loads(r.content)
        sent[message] = 'Sent'
        message = data2['message']
        files = os.listdir()
        for x in files:
            if not x.endswith(('.py','db','json')):
                filename = x
        try:
            await channel.send(message,file = discord.File(filename))
        except:
            shortener = pyshorteners.Shortener()
            image_url_shorted = shortener.tinyurl.short(source)
            await channel.send(message+f'\n\nMedia Url: {image_url_shorted}')
        os.remove(filename)
        with open('Sent.json','w') as f:
            json.dump(sent,f,indent = 3)
        return

    except KeyError:
        try:
            message = data['data'][0]['id']
            if str(message) in sent:
                return            
                        
            source = data['data'][0]['attachments']['data'][0]['media']['image']['src']
            wget.download(source)
            url = f'https://graph.facebook.com/v10.0/{message}'
            r = requests.get(url,params = params)
            data3 = json.loads(r.content)
            sent[message] = 'Sent'
            message = data3['message']
            files = os.listdir()
            for x in files:
                if not x.endswith(('.py','db','json')):
                    filename = x
            
            if filename.endswith('.jpeg','jpg','png','webp','svg','gif'):
                await channel.send(message,file = discord.File(filename))
            else:
                shortener = pyshorteners.Shortener()
                image_url_shorted = shortener.tinyurl.short(source)
                await channel.send(message+f'\n\nMedia Url: {image_url_shorted}')
            os.remove(filename)
            with open('Sent.json','w') as f:
                json.dump(sent,f,indent = 3)
            return
    
        except KeyError:
            message = data['data'][0]['id']
            if message in sent:
                return
            
            sent[message] = 'Sent'
            url = f'https://graph.facebook.com/v10.0/{message}'
            r = requests.get(url,params = params)
            data = json.loads(r.content)
            message = data['message']
            await channel.send(message)
            with open('Sent.json','w') as f:
                json.dump(sent,f,indent = 3)
            return

@has_permissions(administrator = True)
@bot.command()
async def setchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !setchannel `#CHANNEL (Where posts are sent)`')
        return
    
    with open('Token.json') as f:
        tk = json.load(f)
    tk['Channel'] = channel.id
    with open('Token.json','w') as f:
        json.dump(tk,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel has been SET!')

@has_permissions(administrator = True)
@bot.command()
async def settoken(ctx,*,token:str = None):
    if not token:
        await ctx.send(':information_source: Usage: !settoken `TOKEN`')
        return
    
    with open('Token.json') as f:
        tk = json.load(f)
    tk['Token'] = token
    with open('Token.json','w') as f:
        json.dump(tk,f,indent = 3)  
    
    await ctx.send(':white_check_mark: TOKEN has been SET!')


