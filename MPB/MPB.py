import discord
from discord.ext import commands
import os
import datetime
import json
import asyncio
import discord
import discord.utils
from discord import file
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions
import json
import requests
from PIL import Image, ImageOps, ImageDraw, ImageFont
import random
import youtube_dl  # youtube-dl-2020.3.1
import traceback, os, json
from youtube_search import YoutubeSearch 
import time
import sched
from datetime import datetime,timedelta
from datetime import date as dt
import re  
from dateutil import parser

song_queue = []
#CUSTOM PREFIX LOAD.

def get_prefix(bot,message):
    with open('Config/prefixes.json','r') as f:
        data = json.load(f)
    try:
        return data[str(message.guild.id)]['Prefix']

    except KeyError:
        return '!'

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = get_prefix,case_insensitive=True,intents = intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(" '''''''''''''' STARTED ''''''''''''''")
    print(len(bot.guilds))

@bot.event
async def on_message(message):
	if bot.user in message.mentions:
		with open('Config/prefixes.json','r') as f:
			data = json.load(f)

		guild = str(message.guild.id)
		prefix = data[guild]['Prefix']
		await message.channel.send(f'<:c_q:680368071537459200> Bot Prefix in this server is: `{prefix}`')

	await bot.process_commands(message)

#ON COMMAND EVENT
@bot.event
async def on_command(command):
	guild = str(command.guild.id)
	with open('Config/prefixes.json','r') as f:
		rv = json.load(f)	

	if not guild in rv:
		rv[guild] = {}
		rv[guild]['Prefix'] = 'cq!'
		with open('Config/prefixes.json','w') as f:
			json.dump(rv,f,indent = 3)

	author = str(command.author.id)
	with open('Config/data.json','r') as f:
		data = json.load(f)

	if not author in data:
		data[author] = {}
		data[author]['experience']  = 0
		data[author]['level'] = 0
		data[author]['money'] = 1150
		data[author]['bank'] = 0
		data[author]['rank'] = 'none'
		data[author]['command'] = 0
		data[author]['buffs'] = 0
		data[author]['items'] = {}
		data[author]['Rob_Time'] = 0
		data[author]['Last Robbery'] = 0
		data[author]['Loss'] = 0
		data[author]['items']['Gift Box'] = 0
		data[author]['items']['Double XP'] = '0'
		data[author]['items']['Profile Privacy'] = '0'
		data[author]['items']['Rose'] = 0
		data[author]['items']['Bomb'] = 0
		data[author]['items']['Undo Card'] = 0
		data[author]['items']['Vault'] = '0'
		data[author]['Badge1'] = 0
		data[author]['Badge2'] = 0
		data[author]['Badge3'] = 0
		data[author]['Badge4'] = 0
		with open('Config/data.json','w') as f:
			json.dump(data,f,indent = 3)
	
	#experience = data[author]['experience']
	level = data[author]["level"]

	if level == 0:
		level_end = 520
	elif level== 1:
		level_end = 910
	elif level== 2:
		level_end = 1110
	elif level == 3:
		level_end = 1350
	elif level == 4:
		level_end = 1500
	elif level == 5:
		level_end = 1790
	elif level == 6:
		level_end = 1800
	elif level == 7:
		level_end = 1850
	elif level == 8:
		level_end = 1900
	elif level == 9:
		level_end = 1950
	elif level == 10:
		level_end = 2000
	else:
		level_end = 2500
	
	data[author]["command"] += 1
	if random.randint(1,50) < 30:
		if not data[author]['items']['Double XP'] == 0:
			data[author]['experience'] += 2 * random.randint(1,4)
		else:
			data[author]['experience'] += 2 * random.randint(1,4)

	with open('Config/data.json','w') as f:
		json.dump(data,f,indent = 3)	

	with open('Config/data.json','r') as f:
		data = json.load(f)

	if data[author]['experience'] >= level_end:
		level = data[author]['level']
		data[author]['level'] += 1
		level = level + 1
		data[author]['experience'] = 0

	with open('Config/data.json','w') as f:
		json.dump(data,f,indent = 3)
	

def search(arg):
    ydl_opts = {'format': 'bestaudio'}
    yt = YoutubeSearch(arg, max_results=1).to_json()
    yt_id = str(json.loads(yt)['videos'][0]['id'])
    yt_url = 'https://www.youtube.com/watch?v='+yt_id
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(yt_url, download=False)
        URL = info['formats'][0]['url']    
    
    return ({'source': URL, 'title': info['title']})

def skips(ctx):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    global song_queue
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if len(song_queue) > 1:
        del song_queue[0]
        voice.play(discord.FFmpegPCMAudio(source = song_queue[0]['title'], **FFMPEG_OPTIONS), after=lambda e: skips(ctx))
        voice.is_playing()
        
@bot.command()
async def queue(ctx):
    global song_queue
    msg = ''
    for num, x in enumerate(song_queue):
        num += 1
        msg += f"{num} - {x['title']}\n"
    
    embed=discord.Embed(description=f"```css\n{msg}\n```",color=0x61e7ff)
    embed.set_author(name="🎶🎶 Music List")
    await ctx.send(embed=embed)


@bot.command()
async def play(ctx,*,arg:str = None):
    global song_queue
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    channel = ctx.author.voice.channel
    if channel:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        song = search(arg)
        song_queue.append(song)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else: 
            voice = await channel.connect()

        if not voice.is_playing():
            voice.play(discord.FFmpegPCMAudio(source = song['source'], **FFMPEG_OPTIONS), after=lambda e: self.skips(ctx))
            await ctx.send(f"Playing `{song['title']}` - `{song['Duration']}`\nRequested by: {ctx.author.mention}")

        else:
            await ctx.send(f"Added `{song['title']}` - `{song['Duration']}` to the queue by {ctx.author.mention}")
    else:
        await ctx.send("you must be connected to a channel to play some jams!")
    

@bot.command()
async def skip(ctx):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    global song_queue
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not len(song_queue) == 0:
        a = voice.is_playing()
        if a: 
            del song_queue[0]
            voice.stop()
            voice.play(discord.FFmpegPCMAudio(source = song_queue[0]['source'], **FFMPEG_OPTIONS), after=lambda e: skips(ctx))
            await ctx.send("Looks like no one liked this song, skipping it.")
        else:
            await ctx.send("i'm not playing music !")
    else:
        await ctx.send('There are no songs in the QUEUE, Stopped playing the jams!')
    
    
@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    #voice = await ctx.author.voice.channel.connect()
    if voice and voice.is_playing():
        voice.pause()
        await ctx.send(f":pause_button: Music Paused")
    
    else:
        await ctx.send('Music is already Paused.')

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    #voice = await ctx.author.voice.channel.connect()
    if voice and voice.is_paused():
        voice.resume()
        await ctx.send(':play_pause: Music Resumed')
    
    else:
        await ctx.send('Music already playing')

@bot.command()
async def stop(ctx):
    global song_queue
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        voice.stop()
    except Exception as e:
        pass
    song_queue = []
    await ctx.send(':stop_button:  Music Stopped')
    return song_queue

@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        await voice.disconnect()
    except Exception:
        pass

    await ctx.send(':white_check_mark: Left Channel')

@bot.command()
async def join(ctx):
    voice = ctx.author.voice.channel
    
    try:
        await voice.connect()
    except Exception:
        pass
    
    await ctx.send(':white_check_mark:  Join Channel')
#Events
@bot.event
async def on_guild_join(guild):

    '''
    In te following statement, We store the Guild Information, with
    Guild ID and It's prefix as ! in the JSON File.
    '''

    with open('Config/prefixes.json','r') as f:
        rv = json.load(f)	

    guild = str(guild.id)
    if not guild in rv:
        rv[guild] = {}
        rv[guild]['Prefix'] = '!'
        with open('Config/prefixes.json','w') as f:
            json.dump(rv,f,indent = 3)

@bot.event
async def on_member_join(member):
    guild = str(member.guild.id)
    with open('Config/guildlogs.json','r') as f:
        data = json.load(f)
    try:
        if data[guild]['Join_Message'] == 'Enabled':
            member_count = len([m for m in member.guild.members if not m.bot])
            channel = bot.get_channel(int(data[guild]['Join ID']))
            await channel.send(f":tada: Hi, {member.mention}, Welcome to {member.guild}, you're our {member_count} user! ")
    except Exception:
        pass

    try:
        if not data[guild]['Autorole'] == 'Disabled':
            role = discord.utils.get(member.guild.roles, name=data[str(member.guild.id)]['Autorole'])
            await member.add_roles(role)
    
    except KeyError:
        pass

@bot.command()
async def help(ctx):
    
    embed=discord.Embed(color=0x955cff)
    embed.set_author(name="Commands Help")
    embed.add_field(name=":gear: **Moderations**", value="`BAN` `UNBAN` `MUTE` `UNMUTE` `KICK` `LOCK`\n`UNLOCK` `CLEAR` `WARN` `REMOVEWARN` `SETWARN`", inline=False)
    embed.add_field(name=":tada: **Giveaway**", value="`GSTART` `GSTOP`", inline=False)
    embed.add_field(name=":tada: **Music**", value="`play` `queue` `stop` `join` `leave` `skip` `pause` `resume`", inline=False)
    embed.add_field(name=":game_die: **Games**", value="`RACE` `BET` `HIGHLOW` `KENO` `SLOTS` `ROULETTE`\n`BACCARAT` `DUELBET` `LEADERBOARD` ", inline=False)
    embed.add_field(name =":dna: **General**", value = "`STATS` `WELCOMEMESSAGE` `PREFIX` `AUTOROLE`", inline = False)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text = f'{ctx.author} ')
    await ctx.send(embed=embed)

#COGS / Command LOADING
for filename in os.listdir('./Commands/Giveaway'):
    if filename.endswith('.py'):
        bot.load_extension(f'Commands.Giveaway.{filename[:-3]}')


for filename in os.listdir('./Commands/Moderations'):
    if filename.endswith('.py'):
        bot.load_extension(f'Commands.Moderations.{filename[:-3]}')


for filename in os.listdir('./Commands/Games'):
    if filename.endswith('.py'):
        bot.load_extension(f'Commands.Games.{filename[:-3]}')

for filename in os.listdir('./Commands/General'):
    if filename.endswith('.py'):
        bot.load_extension(f'Commands.General.{filename[:-3]}')


token = 'ODMwMTA3NDUwMjgyNjA2NTkz.YHB3zg.kKEaQmry36BZ0DIpWE5xF4OZ0CY'
bot.run(token)