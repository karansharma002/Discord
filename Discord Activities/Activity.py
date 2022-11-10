import discord
from discord.ext import commands, tasks
import json
import asyncio
import datetime
from dateutil import parser
from json2html import *
import json

bot = commands.Bot(command_prefix = '%',intents = discord.Intents.all())

ad = []
@bot.event
async def on_ready():
    global ad
    print('------ ACTIVITY BOT INSTANCE HAS STARTED ------')

    await bot.wait_until_ready()

    user_check.start()

@bot.event
async def on_member_join(member):

    def check(msg):
        return msg.author == member and msg.channel.type == discord.ChannelType.private

    with open('STA.json') as f:
        settings = json.load(f)
    
    if not 'Orders_Channel' in settings:
        return
    
    try:
        await member.send(':tada: Welcome to the Server. Please fill the following details to continue.')
    
    except:
        if 'Log_Channel' in settings:
            channel = await bot.fetch_channel(settings['Log_Channel'])
            await channel.send(f'{member}, Your DM is Disabled. Welcome Message FAILED.')
            return

    message = "**__Step 1- Enter your name__**"
    embed = discord.Embed(color = discord.Color.blurple(),description = message)
    await member.send(embed = embed)
    name  = await bot.wait_for('message',check = check,timeout = 120)
    name = name.content

    message = "**__Step 2- Enter your email__**"
    embed = discord.Embed(color = discord.Color.blurple(),description = message)
    await member.send(embed = embed)
    email  = await bot.wait_for('message',check = check,timeout = 120)
    email = email.content

    message = "**__Step 3- Enter your Phone Number__**"
    embed = discord.Embed(color = discord.Color.blurple(),description = message)
    await member.send(embed = embed)
    phone  = await bot.wait_for('message',check = check,timeout = 120)
    phone = phone.content

    embed = discord.Embed(title = f"{member} Has filled the form",color = discord.Color.blurple())
    embed.add_field(name = 'Name',value = name,inline = False)
    embed.add_field(name = 'Email',value = email,inline = False)
    embed.add_field(name = 'Phone',value = phone,inline = False)
    embed.timestamp = datetime.datetime.utcnow()

    with open('Data.json') as f:
        data = json.load(f)
    
    id_ = str(member.id)

    if not id_ in data:
        data[id_] = 0
    
    if 'Form_Points' in settings:
        p = settings['Form_Points']
        data[id_] += settings['Form_Points']
    else:
        data[id_] += 2
        p = 2

    with open('Data.json','w') as f:
        json.dump(data,f,indent = 3)
    
    await member.send(f':tada: Thank you for filling the form. You have been given __{p}__ Points as a GIFT. Enjoy!!')
    try:
        channel  = await bot.fetch_channel(settings['Forms_Channel'])
        await channel.send(embed = embed)
    
    except:
        pass

msg_cooldowns = {}
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.author == bot.user:
        return
    
    content = str(message.content)
    global ad
    if content.startswith('%'):
        await bot.process_commands(message)
        return

    if message.author.guild_permissions.administrator:
        return

    author = str(message.author.id)

    with open('STA.json') as f:
        settings = json.load(f)
    
    if 'EVENT_COOLDOWN' in settings:
        tm = settings['EVENT_COOLDOWN']
    else:
        tm = 0

    with open('Data.json') as f:
        data = json.load(f)
    
    with open('Cache.json') as f:
        cache = json.load(f)

    if not author in data:
        data[author] = 0
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)
    
    if not str(datetime.date.today()) in cache:
        cache[str(datetime.date.today())] = {}
        with open('Cache.json','w') as f:
            json.dump(cache,f,indent = 3)

    if not author in cache[str(datetime.date.today())]:
        cache[str(datetime.date.today())][author] = {}
        with open('Cache.json','w') as f:
            json.dump(cache,f,indent = 3)

    if 'Max_Points' in cache[str(datetime.date.today())][author]:
        if cache[str(datetime.date.today())][author]['Max_Points'] >= settings['Max_Points']:
            await message.author.send(f'Congratulations, you have earned it all today. Tomorrow is a new day and new beginning to start earning {eco()} again!')
            return  

    if message.mentions:
        if author in msg_cooldowns:
            if 'TAG' in msg_cooldowns[author]:
                t1 = parser.parse(str(msg_cooldowns[str(author)]['TAG']))
                t2 = parser.parse(str(datetime.datetime.now()))
                t3 = t1 - t2
                t3 = round(t3.total_seconds())

                if not t3 <= 0:
                    return

        if 'Tag_Points' in settings:
            if str(datetime.date.today()) in cache:
                if author in cache[str(datetime.date.today())]:
                    if 'Tag_Points' in cache[str(datetime.date.today())][author]:
                        if cache[str(datetime.date.today())][author]['Tag_Points'] >= settings['Tag_Maxpoints']:
                            await message.author.send(f'Congratulations, you have earned the maximum amount of {eco()} for this activity today!')
                            return
                    
            data[author] += settings['Tag_Points']
            if not 'Tag_Points' in cache[str(datetime.date.today())][author]:
                cache[str(datetime.date.today())][author]['Tag_Points'] = settings['Tag_Points']
                cache[str(datetime.date.today())][author]['Max_Points'] = settings['Tag_Points']
            else:
                cache[str(datetime.date.today())][author]['Tag_Points'] += settings['Tag_Points']
                cache[str(datetime.date.today())][author]['Max_Points'] += settings['Tag_Points']
            
            with open('Cache.json','w') as f:
                json.dump(cache,f,indent = 3)

            with open('Data.json','w') as f:
                json.dump(data,f,indent = 3)    

            num = settings['Tag_Points']
            await message.author.send(f':tada: You have earned __{num}__ {eco()}  for tagging a member in your message.')
            await message.author.send(f'Your total is: __{data[author]}__')   
            if 'Log_Channel' in settings:
                channel = await bot.fetch_channel(settings['Log_Channel'])
                await channel.send(f"{message.author.mention}, :tada: You have earned __{num}__ {eco()}  for tagging a member in your message.\
                    \nYour total is: __{data[author]}__'")

            if not author in msg_cooldowns:
                msg_cooldowns[str(author)] = {}
            
            msg_cooldowns[str(author)]['TAG'] = str(datetime.datetime.now() + datetime.timedelta(seconds = tm))
            return

    if 'https' in content or 'http' in content or 'www' in content:
        if author in msg_cooldowns:
            if 'LINK' in msg_cooldowns[author]:
                t1 = parser.parse(str(msg_cooldowns[str(author)]['LINK']))
                t2 = parser.parse(str(datetime.datetime.now()))
                t3 = t1 - t2
                t3 = round(t3.total_seconds())

                if not t3 <= 0:
                    return

        if 'Link_Points' in settings:
            if str(datetime.date.today()) in cache:
                if author in cache[str(datetime.date.today())]:
                    if 'Link_Points' in cache[str(datetime.date.today())][author]:
                        if cache[str(datetime.date.today())][author]['Link_Points'] >= settings['Link_Maxpoints']:
                            await message.author.send(f'Congratulations, you have earned the maximum amount of {eco()} for this activity today!')
                            return
                        
            data[author] += settings['Link_Points']

            if not 'Link_Points' in cache[str(datetime.date.today())][author]:
                cache[str(datetime.date.today())][author]['Link_Points'] = settings['Link_Points']
                cache[str(datetime.date.today())][author]['Max_Points'] = settings['Link_Points']
            else:
                cache[str(datetime.date.today())][author]['Link_Points'] += settings['Link_Points']
                cache[str(datetime.date.today())][author]['Max_Points'] += settings['Link_Points']
            
            with open('Cache.json','w') as f:
                json.dump(cache,f,indent = 3)

            with open('Data.json','w') as f:
                json.dump(data,f,indent = 3)       
            
            num = settings['Link_Points']
            await message.author.send(f':tada: You have earned __{num}__ {eco()}  for sending a message with a link.')
            await message.author.send(f'Your total is: __{data[author]}__') 
            if 'Log_Channel' in settings:
                channel = await bot.fetch_channel(settings['Log_Channel'])
                await channel.send(f"{message.author.mention}, :tada: You have earned __{num}__ {eco()}  for sending a message with a link.\
                    \nYour total is: __{data[author]}__'")
            if not author in msg_cooldowns:
                msg_cooldowns[str(author)] = {}
            
            msg_cooldowns[str(author)]['LINK'] = str(datetime.datetime.now() + datetime.timedelta(seconds = tm))
            return

    if message.reference is not None:
        if author in msg_cooldowns:
            if 'REPLY' in msg_cooldowns[author]:
                t1 = parser.parse(str(msg_cooldowns[str(author)]['REPLY']))
                t2 = parser.parse(str(datetime.datetime.now()))
                t3 = t1 - t2
                t3 = round(t3.total_seconds())

                if not t3 <= 0:
                    return

        if 'Reply_Points' in settings:
            if str(datetime.date.today()) in cache:
                if author in cache[str(datetime.date.today())]:
                    if 'Reply_Points' in cache[str(datetime.date.today())][author]:
                        if cache[str(datetime.date.today())][author]['Reply_Points'] >= settings['Reply_Maxpoints']:
                            await message.author.send(f'Congratulations, you have earned the maximum amount of {eco()} for this activity today!')
                            return
                        
            data[author] += settings['Reply_Points']

            if not 'Reply_Points' in cache[str(datetime.date.today())][author]:
                cache[str(datetime.date.today())][author]['Reply_Points'] = settings['Reply_Points']
                cache[str(datetime.date.today())][author]['Max_Points'] = settings['Reply_Points']
            else:
                cache[str(datetime.date.today())][author]['Reply_Points'] += settings['Reply_Points']
                cache[str(datetime.date.today())][author]['Max_Points'] += settings['Reply_Points']
            
            with open('Cache.json','w') as f:
                json.dump(cache,f,indent = 3)

            with open('Data.json','w') as f:
                json.dump(data,f,indent = 3)       

            num = settings['Reply_Points']
            await message.author.send(f':tada: You have earned __{num}__ {eco()}  for replying to a member.')
            await message.author.send(f'Your total is: __{data[author]}__') 
            if 'Log_Channel' in settings:
                channel = await bot.fetch_channel(settings['Log_Channel'])
                await channel.send(f"{message.author.mention}, :tada: You have earned __{num}__ {eco()}  for replying to a member.\
                    \nYour total is: __{data[author]}__'")
            if not author in msg_cooldowns:
                msg_cooldowns[str(author)] = {}
            
            msg_cooldowns[str(author)]['REPLY'] = str(datetime.datetime.now() + datetime.timedelta(seconds = tm))
            return

    if not str(message.attachments) == "[]":
        if author in msg_cooldowns:
            if 'IMAGE' in msg_cooldowns[author]:
                t1 = parser.parse(str(msg_cooldowns[str(author)]['IMAGE']))
                t2 = parser.parse(str(datetime.datetime.now()))
                t3 = t1 - t2
                t3 = round(t3.total_seconds())

                if not t3 <= 0:
                    return

        split_v1 = str(message.attachments).split("filename='")[1]
        filename = str(split_v1).split("' ")[0]
        if filename.lower().endswith(('jpeg','jpg','png','gif','svg','webp')):
            if 'Image_Points' in settings:
                if str(datetime.date.today()) in cache:
                    if author in cache[str(datetime.date.today())]:
                        if 'Image_Points' in cache[str(datetime.date.today())][author]:
                            if cache[str(datetime.date.today())][author]['Image_Points'] >= settings['Image_Maxpoints']:
                                await message.author.send(f'Congratulations, you have earned the maximum amount of {eco()} for this activity today!')
                                return
                            
                data[author] += settings['Image_Points']

                if not 'Image_Points' in cache[str(datetime.date.today())][author]:
                    cache[str(datetime.date.today())][author]['Image_Points'] = settings['Image_Points']
                    cache[str(datetime.date.today())][author]['Max_Points'] = settings['Image_Points']
                else:
                    cache[str(datetime.date.today())][author]['Image_Points'] += settings['Image_Points']
                    cache[str(datetime.date.today())][author]['Max_Points'] += settings['Image_Points']
                
                with open('Cache.json','w') as f:
                    json.dump(cache,f,indent = 3)
                with open('Data.json','w') as f:
                    json.dump(data,f,indent = 3)           

                num = settings['Image_Points']
                await message.author.send(f':tada: You have earned __{num}__ {eco()}  for sharing an image.')
                await message.author.send(f'Your total is: __{data[author]}__') 
            if 'Log_Channel' in settings:
                channel = await bot.fetch_channel(settings['Log_Channel'])
                await channel.send(f"{message.author.mention}, :tada: You have earned __{num}__ {eco()}  for sending an image.\
                    \nYour total is: __{data[author]}__'")

            if not author in msg_cooldowns:
                msg_cooldowns[str(author)] = {}
            
            msg_cooldowns[str(author)]['IMAGE'] = str(datetime.datetime.now() + datetime.timedelta(seconds = tm))
            return
            
    if 'Channels' in settings:
        if author in msg_cooldowns:
            if 'MSG' in msg_cooldowns[author]:
                t1 = parser.parse(str(msg_cooldowns[str(author)]['MSG']))
                t2 = parser.parse(str(datetime.datetime.now()))
                t3 = t1 - t2
                t3 = round(t3.total_seconds())

                if not t3 <= 0:
                    return

        if message.channel.id in settings['Channels']:
            if 'Channel_Points' in settings:
                if str(datetime.date.today()) in cache:
                    if author in cache[str(datetime.date.today())]:
                        if 'Channel_Points' in cache[str(datetime.date.today())][author]:
                            if cache[str(datetime.date.today())][author]['Channel_Points'] >= settings['Channel_Maxpoints']:
                                await message.author.send(f'Congratulations, you have earned the maximum amount of {eco()} for this activity today!')
                                return
                            
                data[author] += settings['Channel_Points']
                if not 'Channel_Points' in cache[str(datetime.date.today())][author]:
                    cache[str(datetime.date.today())][author]['Channel_Points'] = settings['Channel_Points']
                    cache[str(datetime.date.today())][author]['Max_Points'] = settings['Channel_Points']
                else:
                    cache[str(datetime.date.today())][author]['Channel_Points'] += settings['Channel_Points']
                    cache[str(datetime.date.today())][author]['Max_Points'] += settings['Channel_Points']
                
                with open('Cache.json','w') as f:
                    json.dump(cache,f,indent = 3)

                with open('Data.json','w') as f:
                    json.dump(data,f,indent = 3)       

                num = settings['Channel_Points']
            await message.author.send(f':tada: You have earned __{num}__ {eco()}  for sending a message.')
            await message.author.send(f'Your total is: __{data[author]}__')  
            if 'Log_Channel' in settings:
                channel = await bot.fetch_channel(settings['Log_Channel'])
                await channel.send(f"{message.author.mention}, :tada: You have earned __{num}__ {eco()}  for sending a message.\
                    \nYour total is: __{data[author]}__'")

            if not author in msg_cooldowns:
                msg_cooldowns[str(author)] = {}

            msg_cooldowns[str(author)]['MSG'] = str(datetime.datetime.now() + datetime.timedelta(seconds = tm))
            return     

    await bot.process_commands(message)


@bot.command()
async def setchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !setchannel `<#CHANNEL>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    if not 'Channels' in settings:
        settings['Channels'] = []
    
    settings['Channels'].append(channel.id)
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel Added!')

@bot.command()
async def removechannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !removechannel `<#CHANNEL>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    if not 'Channels' in settings:
        settings['Channels'] = []
    
    if channel.id in settings['Channels']:
        settings['Channels'].remove(channel.id)
    
    else:
        await ctx.send(':warning: Channel was not a part of the Functionality. Already removed!')
        return

    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel Added!')

@bot.command()
async def channelpoints(ctx,cp:int = None,mp:int = None):
    if not cp or not mp:
        await ctx.send(':information_source: Usage: !channelpoints `<POINTS GIVEN>` `<MAX POINTS EARNED>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['Channel_Points'] = cp
    settings['Channel_Maxpoints'] = mp
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel Points Modified')

@bot.command()
async def formpoints(ctx,cp:int = None):
    if not cp:
        await ctx.send(':information_source: Usage: !formpoints `<POINTS EARNED>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['Form_Points'] = cp
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Form Points Modified')

@bot.command()
async def maxpoints(ctx,cp:int = None):
    if not cp:
        await ctx.send(':information_source: Usage: !maxpoints `<MAX POINTS EARNED>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['Max_Points'] = cp
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Max Points Modified')

@bot.command()
async def replypoints(ctx,cp:int = None,mp:int = None):
    if not cp or not mp:
        await ctx.send(':information_source: Usage: !replypoints `<POINTS EARNED>` `<MAX POINTS EARNED>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['Reply_Points'] = cp
    settings['Reply_Maxpoints'] = mp
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Reply Points Modified')

@bot.command()
async def reactpoints(ctx,cp:int = None,mp:int = None):
    if not cp or not mp:
        await ctx.send(':information_source: Usage: !reactpoints `<POINTS EARNED>` `<MAX POINTS EARNED>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['React_Points'] = cp
    settings['React_Maxpoints'] = mp
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Reaction Points Modified')

@bot.command()
async def linkpoints(ctx,cp:int = None,mp:int = None):
    if not cp or not mp:
        await ctx.send(':information_source: Usage: !linkpoints `<POINTS EARNED>` `<MAX POINTS EARNED>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['Link_Points'] = cp
    settings['Link_Maxpoints'] = mp
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Link Points Modified')


@bot.command()
async def imagepoints(ctx,cp:int = None,mp:int = None):
    if not cp or not mp:
        await ctx.send(':information_source: Usage: !imagepoints `<POINTS EARNED>` `<MAX POINTS EARNED>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['Image_Points'] = cp
    settings['Image_Maxpoints'] = mp
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Image Points Modified')


@bot.command()
async def tagpoints(ctx,cp:int = None,mp:int = None):
    if not cp or not mp:
        await ctx.send(':information_source: Usage: !tagpoints `<POINTS EARNED>` `<MAX POINTS EARNED>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['Tag_Points'] = cp
    settings['Tag_Maxpoints'] = mp
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: User Tag Points Modified')

@bot.command()
async def thumbpoints(ctx,cp:int = None):
    if not cp:
        await ctx.send(':information_source: Usage: !tagpoints `<POINTS EARNED / DEDUCTED>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['Thumb_Points'] = cp
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Thumb Points Modified')

@bot.command()
async def voicepoints(ctx,cp:int = None,mp:int = None):
    if not cp or not mp:
        await ctx.send(':information_source: Usage: !voicepoints `<TIME IN MINUTES>` `<POINTS EARNED>`')
        return
    
    with open('TIMER.json') as f:
        settings = json.load(f)
    
    settings[str(cp)] = mp

    with open('TIMER.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Voice Points Modified')

cooldowns = {}
@bot.event
async def on_raw_reaction_add(payload):
    global cooldowns

    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    author = message.author

    user = await bot.fetch_user(payload.user_id)
    if user == author:
        return
    
    if str(user.id) in cooldowns:
        t1 = parser.parse(str(cooldowns[str(user.id)]))
        t2 = parser.parse(str(datetime.datetime.now()))
        t3 = t1 - t2
        t3 = round(t3.total_seconds())

        if not t3 <= 0:
            return

    emoji = payload.emoji
    emoji = str(emoji)

    with open('STA.json') as f:
        settings = json.load(f)
    
    tm = settings['TIME_SEC']


    with open('Data.json') as f:
        data = json.load(f)
    
    with open('Cache.json') as f:
        cache = json.load(f)

    
    if not str(author.id) in data:
        data[str(author.id)] = 0
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)
    
    if not str(datetime.date.today()) in cache:
        cache[str(datetime.date.today())] = {}

    if not str(author.id) in cache[str(datetime.date.today())]:
        cache[str(datetime.date.today())][str(author.id)] = {}

    if not str(user.id) in cache[str(datetime.date.today())]:
        cache[str(datetime.date.today())][str(user.id)] = {}

    if emoji == '👍':
        if 'Thumb_Points' in settings:
            pt = settings['Thumb_Points']
        else:
            pt = 1

        if 'MSG_ID' in cache[str(datetime.date.today())][str(user.id)]:
            if message.id in cache[str(datetime.date.today())][str(user.id)]['MSG_ID']:
                return
        else:
            cache[str(datetime.date.today())][str(user.id)]['MSG_ID'] = []

        cache[str(datetime.date.today())][str(user.id)]['MSG_ID'].append(message.id) 
        data[str(author.id)] += pt#settings['React_Points']
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)   

        await message.author.send(f':tada: You have earned __{pt}__ {eco()} for getting a thumbs-up on your message.')
        await message.author.send(f'Your total is: __{data[str(author.id)]}__') 
        with open('Cache.json','w') as f:
            json.dump(cache,f,indent = 3)

    elif emoji == '👎':
        if 'Thumb_Points' in settings:
            pt = settings['Thumb_Points']
        else:
            pt = 1

        if 'MSG_ID' in cache[str(datetime.date.today())][str(user.id)]:
            if message.id in cache[str(datetime.date.today())][str(user.id)]['MSG_ID']:
                return
        else:
            cache[str(datetime.date.today())][str(user.id)]['MSG_ID'] = []

        cache[str(datetime.date.today())][str(user.id)]['MSG_ID'].append(message.id) 

        data[str(author.id)] -= pt#settings['React_Points']
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)  
        
        await message.author.send(f':tada: You have lost __{pt}__ {eco()} for getting a thumbs-down on your message.')
        await message.author.send(f'Your total is: __{data[str(author.id)]}__') 
        with open('Cache.json','w') as f:
            json.dump(cache,f,indent = 3)
    
    else:
        if 'React_Points' in settings:
            if 'MSG_ID' in cache[str(datetime.date.today())][str(user.id)]:
                if message.id in cache[str(datetime.date.today())][str(user.id)]['MSG_ID']:
                    return
            else:
                cache[str(datetime.date.today())][str(user.id)]['MSG_ID'] = []

            cache[str(datetime.date.today())][str(user.id)]['MSG_ID'].append(message.id)
            
            data[str(user.id)] += settings['React_Points']
            if not 'React_Total' in cache[str(datetime.date.today())][str(user.id)]:
                cache[str(datetime.date.today())][str(user.id)]['React_Total'] = settings['React_Points']
            else:
                if cache[str(datetime.date.today())][str(user.id)]['React_Total'] >= settings['React_Maxpoints']:
                    await user.send(f'Congratulations, you have earned the maximum amount of {eco()} for this activity today!')
                    return
                
                elif cache[str(datetime.date.today())][str(user.id)]['Max_Points'] >= settings['Max_Points']:
                    await user.send(f'Congratulations, you have earned it all today. Tomorrow is a new day and new beginning to start earning {eco()} again!')
                    return  

                cache[str(datetime.date.today())][str(user.id)]['React_Total'] += settings['React_Points']

            with open('Data.json','w') as f:
                json.dump(data,f,indent = 3)  
            
            num = settings['React_Points']
            await user.send(f':tada: You have earned __{num}__ {eco()} for reacting to a message.')
            await user.send(f'Your total is: __{data[str(user.id)]}__') 

            with open('Cache.json','w') as f:
                json.dump(cache,f,indent = 3)
            
            cooldowns[str(user.id)] = str(datetime.datetime.now() + datetime.timedelta(seconds = tm))
            return cooldowns

@bot.command()
async def coins(ctx,user:discord.Member = None):
    if not user:
        user2 = str(ctx.author.id)
        author = ctx.author
    else:
        user2 = str(user.id)
        author = user

    with open('Data.json') as f:
        data = json.load(f)
    
    if not user2 in data:
        data[user2] = 0
        with open('Data.json','w') as f:
            json.dump(data,f,indent  = 3)
    
    embed = discord.Embed(color = discord.Color.blurple(),description = f'**Total {eco()}:** __{data[user2]}__')
    embed.set_author(name = f"{author} | {eco()} Balance",icon_url= author.avatar_url)    
    await ctx.send(embed = embed)


@bot.command()
async def remove(ctx,member:discord.User = None,val:int = None):
    if not member or not val:
        await ctx.send(f':information_source: Usage: !remove `<@user>` `<AMOUNT OF {eco()}>`')
        return
    
    with open('Data.json') as f:
        data = json.load(f)
    
    id_ = str(member.id)

    if not id_ in data:
        data[id_] = 0
    else:
        if not data[id_] - val < 0:
            data[id_] -= val
        else:
            data[id_] = 0
    
    with open('Data.json','w') as f:
        json.dump(data,f,indent = 3)
    
    await ctx.send(f':white_check_mark: Removed {val} {eco()} from {member} inventory.')

@bot.command()
async def add(ctx,member:discord.User = None,val:int = None):
    if not member or not val:
        await ctx.send(f':information_source: Usage: !remove `<@user>` `<AMOUNT OF {eco()}>`')
        return
    
    with open('Data.json') as f:
        data = json.load(f)
    
    id_ = str(member.id)

    if not id_ in data:
        data[id_] = 0
    else:
        data[id_] += val
    
    with open('Data.json','w') as f:
        json.dump(data,f,indent = 3)
    
    await ctx.send(f':white_check_mark: Added {val} {eco()} in {member} inventory.')

@bot.command()
async def leaderboard(ctx):
    with open('Data.json') as f:
        users = json.load(f)


    high_score_list1 = sorted(users, key = users.get,reverse = True)

    msg1 = ''
    for number,user in enumerate(high_score_list1):
        author = await bot.fetch_user(int(user))
        number += 1
        xp = users[user]
        msg1 += f"**‣ {number}**. {author} ⁃\n{eco()}: **{xp}**\n\n"
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
async def live(ctx):
    with open('Data.json') as f:
        users = json.load(f)

    high_score_list1 = sorted(users, key = users.get,reverse = True)
    msg1 = ''
    for number,user in enumerate(high_score_list1):
        author = await bot.fetch_user(int(user))
        number += 1
        xp = users[user]
        msg1 += f"**‣ {number}**. {author} ⁃\n{eco()}: **{xp}**\n\n"
        if number == 20:
            break
        else:
            number += 1

    embed = discord.Embed(
        title= ":money_with_wings: Live Leaderboard",
        color= 0x05ffda,
        description= msg1
        )
    
    msg = await ctx.send(embed = embed)
    await ctx.message.delete()
    while True:
        await asyncio.sleep(2)
        with open('Data.json') as f:
            users = json.load(f)

        high_score_list1 = sorted(users, key = users.get, reverse = True)
        msg1 = ''
        for number,user in enumerate(high_score_list1):
            author = await bot.fetch_user(int(user))
            number += 1
            xp = users[user]
            msg1 += f"**‣ {number}**. {author} ⁃\n{eco()}: **{xp}**\n\n"
            if number == 20:
                break
            else:
                number += 1

        embed = discord.Embed(
            title= ":money_with_wings: Live Leaderboard",
            color= 0x05ffda,
            description= msg1
            )
        
        await msg.edit(embed = embed)

@bot.command()
async def setlogchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: !setlogchannel `<CHANNEL FOR THE DEFAULT DM>`')
        return

    with open('STA.json') as f:
        settings = json.load(f)
        
    settings['Log_Channel'] = channel.id
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Logs Channel Added!')

@bot.command()
async def orderchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: !orderchannel `<CHANNEL FOR THE ORDERS INFO>`')
        return

    with open('STA.json') as f:
        settings = json.load(f)
        
    settings['Orders_Channel'] = channel.id
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Order Channel Added!')

@bot.command()
async def setreactcooldown(ctx,tm:str = None):
    if not tm:
        await ctx.send(':information_source: !setreactcooldown `<TOTAL SECONDS>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['TIME_SEC'] = int(tm)
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Time Saved')

@bot.command()
async def seteventcooldown(ctx,tm:str = None):
    if not tm:
        await ctx.send(':information_source: !seteventcooldown `<TOTAL SECONDS>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['EVENT_COOLDOWN'] = int(tm)
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Time Saved')

dta = {}
@tasks.loop(seconds = 10)
async def user_check():    
    global dta

    with open('Cache.json') as f:
        cache = json.load(f)
    
    with open('STA.json') as f:
        settings =  json.load(f)
    
    with open('TIMER.json') as f:
        timer = json.load(f)
    
    sta = {}
    tm = sorted(timer.keys(),reverse = True)
    for x in tm:
        sta[x] = timer[x]

    if not str(datetime.date.today()) in cache:
        cache[str(datetime.date.today())] = {}
        with open('Cache.json','w') as f:
            json.dump(cache,f,indent = 3)

    for x in list(dta):
        if 'Join_Time' in dta[x]:
            for num,y in enumerate(sta):
                t1 = parser.parse(str(dta[x]['Join_Time']))
                t2 = parser.parse(str(datetime.datetime.now()))
                final = t2 - t1
                final = round(final.seconds / 60)
                if final >= int(y):
                    if 'Total_Time' in dta[x]:
                        if not int(y) > dta[x]['Total_Time']:
                            continue

                    with open('Data.json') as f:
                        data = json.load(f)
                    
                    if not x in data:
                        data[x] = 0

                    data[x] += sta[y]
                    with open('Data.json','w') as f:
                        json.dump(data,f,indent = 3)
                    
                    author = await bot.fetch_user(int(x))
                    dta[x]['Total_Time'] = int(y)

                    await author.send(f'You have earned {sta[y]} {eco()} for spending {y} mins in a voice channel.\nYour total is {data[x]}.')
                    
                    if not 'Voice' in cache[str(datetime.date.today())][str(x)]:
                        cache[str(datetime.date.today())][x]['Voice'] = sta[y]
                    else:
                        cache[str(datetime.date.today())][x]['Voice'] += sta[y]

                    with open('Cache.json','w') as f:
                        json.dump(cache,f,indent = 3)
                    
                    if cache[str(datetime.date.today())][x]['Voice'] >= 700:
                        dta.pop(x)
                        await author.send(f'Congratulations, you have earned the maximum amount of {eco()} for this activity today!')
                        return

@bot.command()
async def voicemaxpoints(ctx,mp:int = None):
    if not mp:
        await ctx.send(':information_source: Usage: !voicepoints `<MAX EARNED>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['VOICE_MAX'] = mp
    
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Voice MAX Points Modified')


@bot.event
async def on_voice_state_update(member, before, after):
    usr = member
    global dta
    member = str(member.id)
    with open('Cache.json') as f:
        cache = json.load(f)

    with open('STA.json') as f:
        settings = json.load(f)

    if not str(datetime.date.today()) in cache:
        cache[str(datetime.date.today())] = {}

    if not member in cache:
        cache[str(datetime.date.today())][member] = {}
    
    if not before.channel:
        if 'VOICE_JOIN' in cache[str(datetime.date.today())][member]:
            try:
                await usr.send('----- You will not receive any points as you have exceeded the JOIN limit for this day -----')
                return
            except:
                if 'Log_Channel' in settings:
                    channel = await bot.fetch_channel(settings['Log_Channel'])
                    await channel.send(f'{usr}, Your DM is Disabled. VOICE Event Message NOT SENT.')
                return

        dta[str(member)] = {}
        dta[str(member)]['Channel'] = after.channel.id
        dta[str(member)]['Join_Time'] = str(datetime.datetime.now())
        cache[str(datetime.date.today())][member]['VOICE_JOIN'] = 'CONFIRMED'
        with open('Cache.json','w') as f:
            json.dump(cache,f,indent = 3)

    elif not after.channel:
        try:
            dta.pop(member)
        except KeyError:
            pass
        
    else:
        if 'VOICE_JOIN' in cache[str(datetime.date.today())][member]:
            try:
                await member.send('----- You will not receive any points as you have exceeded the JOIN limit for this day -----')
            except:
                pass

            return

@bot.command()
async def addproduct(ctx,name:str = None,price:int = None,id:str = None):
    if not name or not price or not id:
        await ctx.send(':information_source: Usage: !addproduct `<NAME>` `<PRICE>` `<ID>` `<IMAGE AS ATTACHMENT>`')
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
    products[name]['ID'] = id
    id_[id] = name



    for attachment in ctx.message.attachments:
        split_v1 = str(ctx.message.attachments).split("filename='")[1]
        filename = str(split_v1).split("' ")[0]
        import os
        extension = name + os.path.splitext(filename)[1]
        products[name]['Path'] = extension
        await attachment.save(extension)
    
    with open('Products.json','w') as f:
        json.dump(products,f,indent = 3)

    with open('ID.json','w') as f:
        json.dump(id_,f,indent = 3)

    await ctx.send(':white_check_mark: Product Added!')

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
        id_ = products[product]['ID']

        with open('Data.json') as f:
            data = json.load(f)
        
        if not author in data:
            await ctx.send(':warning: Insufficient Balance!')
            return
            
        if data[author] < price or price <= 0:
            await ctx.send(':warning: Insufficient Balance!')
            return
        
        data[author] -= price
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)
        
        embed = discord.Embed(color = discord.Color.greyple(),description = f":tada: You've bought {product} for {price} {eco()}.")
        await ctx.send(embed = embed)

        if 'Orders_Channel' in settings:
            channel = await bot.fetch_channel(settings['Orders_Channel'])

            embed = discord.Embed(color = discord.Color.green())
            embed.set_author(name = '{ctx.author} | Product Bought',icon_url= ctx.author.avatar_url)
            embed.add_field(name = 'Product', value = product,inline = False)
            embed.add_field(name = 'Price', value = price,inline = False)
            embed.add_field(name = 'ID', value = id_,inline = False)
            await channel.send(embed = embed)

@bot.command()
async def pinfo(ctx,var:str = None):
    if not var:
        await ctx.send(':information_source: Usage: !info `<PRODUCT NAME (CASE SENSITIVE)>`')
        return
    
    with open('Products.json') as f:
        products = json.load(f)

    with open('ID.json') as f:
        id_ = json.load(f)

    if var in products:
        img = products[var]['Path']
        file = discord.File(img)
        embed = discord.Embed(color = discord.Color.blurple(),title = f'{var} - Product Information')
        embed.add_field(name = 'Price', value = products[var]['Price'],inline = False)
        embed.set_image(url=f"attachment://{img}")
        await ctx.send(embed = embed,file = file)
    
    elif var in id_:
        var = id_[var]
        img = products[var]['Path']
        file = discord.File(img)
        embed = discord.Embed(color = discord.Color.blurple(),title = f'{var} - Product Information')
        embed.add_field(name = 'Price', value = products[var]['Price'],inline = False)
        embed.set_image(url=f"attachment://{img}")
        await ctx.send(embed = embed,file = file)

    else:
        await ctx.send(':warning: Product Not Found!!')
        return

@bot.command()
async def dailyamount(ctx,val:int = None):
    if not val:
       await ctx.send(f':information_source: Usage: !dailyamount `<MAX {eco()} GIVEN>`')
       return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['COINS'] = val
    
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(f':white_check_mark: DAILY {eco()} Modified')

@commands.cooldown(1,86400,commands.BucketType.user)
@bot.command()
async def daily(ctx):
    with open('STA.json','r') as f:
        settings = json.load(f)
    
    if not 'COINS' in settings:
        return

    COIN = settings['COINS']
    with open('Data.json','r') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)
    await ctx.send(f'{ctx.author.mention} :tada: You **received** :coin: __{COIN}__ **{eco()}** as a **Daily Gift.** :tada:')
    data[author] += COIN

    with open('Config/data.json','w') as f:
        json.dump(data,f,indent = 4)

@bot.command()
async def setcurrency(ctx,*,val:str = None):
    if not val:
       await ctx.send(':information_source: Usage: !setcurrency `<CURRENCY NAME>`')
       return
    
    with open('STA.json') as f:
        settings = json.load(f)
    
    settings['CURRENCY'] = val
    
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: CURRENCY Modified') 

@daily.error
async def dailyerror(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        if int(error.retry_after * 0.000277778) == 0:
            await ctx.send(f":warning `You already Claimed the Reward. Try again after` {int(error.retry_after * 0.0166667)} Minutes.") 
        else:
            await ctx.send(f":warning `You already Claimed the Reward. Try again after` {int(error.retry_after * 0.000277778)} hour(s).")

def eco():
    with open('STA.json') as f:
        settings = json.load(f)
    
    if 'CURRENCY' in settings:
        return settings['CURRENCY']
    else:
        return 'COINS'

@bot.command()
async def endseason(ctx):
    with open('Data.json') as f:
        data = json.load(f)
    
    data = {}

    with open('Data.json','w') as f:
        json.dump(data,f,indent = 3)
    
    await ctx.send(':white_check_mark: Season ENDED')


@bot.command()
async def export(ctx):
    msg = await ctx.send('------ EXPORTING THE DATA (This may take a while) -------')
    try:
        with open('Data.json') as f:
            data = json.load(f)

        x = sorted(data,key = data.get,reverse = True)

        temp = {}
        for y in x:
            try:
                user = await bot.fetch_user(int(y))
            except:
                continue
            
            try:
                temp[str(user.name)] = data[y]
            except:
                temp[str(user.id)] = data[y]



        data = json2html.convert(json = temp)
        file = open("Leaderboard.html","w",encoding = 'utf-8')
        file.write(data)
        file.close()
        file = discord.File('Leaderboard.html')
        await ctx.send(file = file)
        await msg.delete()
    
    except Exception as e:
        print(e)

@bot.command()
async def formchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !formchannel `<#CHANNEL>`')
        return
    
    with open('STA.json') as f:
        settings = json.load(f)

    
    settings['Forms_Channel'] = channel.id
    with open('STA.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel Added!')

@bot.command()
async def exportform(ctx):
    import chat_exporter
    file = await chat_exporter.quick_export(ctx)
    await ctx.send(file = file)
    

bot.run('ODQzMDgzNTEzMDI4MDE4MjA2.YJ-stQ.E4EhsMsqTUMLHouGRW3FC85jhlQ')