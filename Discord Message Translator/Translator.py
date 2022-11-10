import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix= '!',intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('----- TRANSLATOR BOT IS RUNNING ------')


from googletrans import Translator
translator = Translator()

Running = 'TRUE'

@bot.command()
async def translate(ctx,action:str = None,channel1:discord.TextChannel = None,channel2: discord.TextChannel = None):
    if not action:
        await ctx.send(':information_source: Usage: !translate `<ACTION (ENABLE/DISABLE/ADD)>`')
        return

    if action == 'enable:':
        global Running
        Running = 'TRUE'
        await ctx.send(':white_check_mark: Translator Enabled')
    
    elif action == 'disable':
        global Running
        Running = 'FALSE'
        await ctx.send(':white_check_mark: Translator Disabled')
    
    elif action == 'add':
        if not channel1 or not channel2:
            await ctx.send(':information_source: Usage: !translate `<add>` `<#CHANNEL1 ENGLISH>` `<#CHANNEL2 SPANISH>`')
            return
        
        with open('SP.json') as f:
            sp =  json.load(f)

        with open('EN.json') as f:
            en =  json.load(f)
        
        en[str(channel1.id)] = channel2.id
        sp[str(channel2.id)] = channel1.id
        with open('SP.json','w') as f:
            json.dump(sp,f,indent = 3)

        with open('EN.json','w') as f:
            json.dump(en,f,indent = 3)

        await ctx.send(':white_check_mark: Channel Added')
        

@bot.event
async def on_message(message):
    if message.content.startswith('&'):
        await bot.process_commands(message)
        return
        
    global translator
    global Running

    with open('Languages.json','r') as f:
        data = json.load(f)

    with open('SP.json') as f:
        sp =  json.load(f)

    with open('EN.json') as f:
        en =  json.load(f)

    def language(value):
        return data[value]
        
    if message.author == bot.user:
        return
    
    if Running == 'FALSE':
        return
    
    if str(message.channel.id) in sp:
        en_s = await bot.fetch_channel(sp[str(message.channel.id)])
        channel = await bot.fetch_channel(en_s)
        if message.reference is not None:
            reply_to = await message.channel.fetch_message(message.reference.message_id)
            result2 = translator.translate(reply_to.content, dest=language('english'))
            content=  message.content
            result = translator.translate(content, dest=language('english'))
            webhook = await channel.create_webhook(name=message.author.name)
            msg = await webhook.send(content = str(result2.text),username=message.author.name, avatar_url=message.author.avatar_url,wait = True)
            embed = discord.Embed(description = result.text)
            embed.set_author(name = message.author,icon_url = message.author.avatar_url)
            await msg.reply(f"{message.author.mention}\n{result.text}")
            webhooks = await channel.webhooks()
            for webhook in webhooks:
                await webhook.delete() 
        else:
            result = translator.translate(message.content, dest=language('english'))

            webhook = await channel.create_webhook(name=message.author.name)
            msg = await webhook.send(content = str(result.text),username=message.author.name, avatar_url=message.author.avatar_url,wait = True)

            webhooks = await channel.webhooks()
            for webhook in webhooks:
                await webhook.delete()

    elif message.channel.id in en:
        sp_s = await bot.fetch_channel(en[str(message.channel.id)])
        content=  message.content
        channel = await bot.fetch_channel(sp_s)
        if message.reference is not None:
            reply_to = await message.channel.fetch_message(message.reference.message_id)
            result2 = translator.translate(reply_to.content, dest=language('spanish'))
            content=  message.content
            result = translator.translate(content, dest=language('spanish'))
            
            webhook = await channel.create_webhook(name=message.author.name)
            msg = await webhook.send(content = str(result2.text),username=message.author.name, avatar_url=message.author.avatar_url,wait = True)
            embed = discord.Embed(description = result.text)
            embed.set_author(name = message.author,icon_url = message.author.avatar_url)
            await msg.reply(f"{message.author.mention}\n{result.text}")
            webhooks = await channel.webhooks()
            for webhook in webhooks:
                await webhook.delete() 
        
        else:
            result = translator.translate(content, dest=language('spanish'))
            webhook = await channel.create_webhook(name=message.author.name)
            msg = await webhook.send(content = str(result.text),username=message.author.name, avatar_url=message.author.avatar_url,wait = True)
            webhooks = await channel.webhooks()            
            for webhook in webhooks:
                await webhook.delete() 

bot.run('ODcyNzM5NDIzNDQyMzE3Mzk1.YQuP7Q.q_VaG4soEaGXf9YD6-Y64WDhhLo')