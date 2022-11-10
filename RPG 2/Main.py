import discord
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions
import json
from datetime import datetime
import random
from discord.ext.commands.core import command
import os
from dateutil import parser

bot = commands.Bot(command_prefix = '=',intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('----------------- BOT HAS LAUNCHED ---------------')
    print(f'-- LOGGED IN FOR {len(bot.guilds)} GUILDS')
    print('-- VERSION: 1.0')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if not message.content.startswith('='):
        return

    with open('Config/Bans.json') as f:
        bans = json.load(f)
    
    user = str(message.author.id)
    print(user)
    if user in bans:
        t1 = parser.parse(str(bans[user]))
        t2 = parser.parse(str(datetime.now()))
        t3 = t1 - t2
        t3 = round(t3.total_seconds() / 60)
        if t3 <= 0:
            bans.pop(user)
            with open('Config/Bans.json','w') as f:
                json.dump(bans,f,indent = 3)
            
            await message.author.send(':tada: Your ban time has expired. You have been UNBANNED NOW.')
            await bot.process_commands(message)
            return

        else:
            embed = discord.Embed(description = f':warning: {message.author.mention}, You are currently __BANNED__',color = discord.Color.red())
            await message.channel.send(embed = embed)
            return
    
    else:
        await bot.process_commands(message)

@bot.command()
async def undo(ctx,val:str = None):
    role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
    if role1 in ctx.author.roles:
        pass
    else:
        await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
        return
    if not val:
        await ctx.send(':information_source: Usage: =undo `<registerchannel>` or `<scorechannel>` or `<botchannel>` ')
        return
    
    with open('Config/Settings.json') as f: 
        settings = json.load(f)
    
    val = val.lower()

    if val == 'registerchannel':
        if 'Register_Channel' in settings:
            settings.pop('Register_Channel')
            with open('Config/Settings.json','w') as f:
                json.dump(settings,f,indent = 3)
        
            await ctx.send(':white_check_mark: Registeration Channel has been RESETTED')
        
        else:
            await ctx.send(':information_source: `NO REGISTERATION CHANNEL WAS SET BY DEFAULT`')
            return

    elif val == 'scorechannel':
        if 'Score_Channel' in settings:
            settings.pop('Score_Channel')
            with open('Config/Settings.json','w') as f:
                json.dump(settings,f,indent = 3)
        
            await ctx.send(':white_check_mark: Score Channel has been RESETTED')
        
        else:
            await ctx.send(':information_source: `NO SCORE CHANNEL WAS SET BY DEFAULT`')
            return

    elif val == 'botchannel':
        if 'Bot_Channel' in settings:
            settings.pop('Bot_Channel')
            with open('Config/Settings.json','w') as f:
                json.dump(settings,f,indent = 3)
        
            await ctx.send(':white_check_mark: Bot Channel has been RESETTED')
        
        else:
            await ctx.send(':information_source: `NO BOT CHANNEL WAS SET BY DEFAULT`')
            return
    
    else:
        await ctx.send(':warning: Invalid OPTION')

@bot.command()
async def register_channel(ctx,channel:discord.TextChannel = None):
    role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
    if role1 in ctx.author.roles:
        pass
    else:
        await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
        return
        
    if not channel:
        await ctx.send(':information_source: Usage: =register_channel `<#CHANNEL>` (The channel for registeration)')
        return

    with open('Config/Settings.json') as f:
        settings = json.load(f)
    
    settings['Register_Channel'] = channel.id
    with open('Config/Settings.json','w') as f:
        json.dump(settings,f,indent = 3)
    await ctx.send(':white_check_mark: Channel has been changed')

@bot.command()
async def bot_channel(ctx,channel:discord.TextChannel = None):
    role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
    if role1 in ctx.author.roles:
        pass
    else:
        await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
        return
    if not channel:
        await ctx.send(':information_source: Usage: =bot_channel `<#CHANNEL>` (The channel for bot)')
        return

    with open('Config/Settings.json') as f:
        settings = json.load(f)
    
    settings['Bot_Channel'] = channel.id
    with open('Config/Settings.json','w') as f:
        json.dump(settings,f,indent = 3)
    await ctx.send(':white_check_mark: Channel has been changed')

@bot.event
async def on_member_update(before, after):
    if str(before.status) in ('dnd','online','idle') and after.status is discord.Status.offline:
        with open('Config/Queue.json','r') as f:
            queue = json.load(f)
        
        with open('Config/Cache.json') as f:
            cache = json.load(f)

        if after.id in queue[str(cache['Game_Num'])] and after.guild.id == queue['Guild']:


            channel = await bot.fetch_channel(queue['Channel'])
            await channel.send(f':warning: {str(after)} has been removed from the queue due to becoming OFFLINE.')
            queue[str(cache['Game_Num'])].remove(after.id)
            with open('Config/Queue.json','w') as f:
                json.dump(queue,f,indent = 3) 
            return

for filename in os.listdir('./Commands'):
	if filename.endswith('.py'):
		bot.load_extension(f'Commands.{filename[:-3]}')


token = 'ODIwODkwNDYxMjQ5NjAxNTQ2.YE7v0Q.a9G2VPcwrf4GPJKeDTCN3J4C0CM'
bot.run(token)