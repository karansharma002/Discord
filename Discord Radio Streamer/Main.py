import discord
from discord.ext import commands,tasks
import json

# Intialize BOT Instance
bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print('------------- ✅ BOT Instance is Live ✅  --------------')

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.pause()
        await ctx.send(f":pause_button: Music Paused")
    
    else:
        await ctx.send(':warning: Nothing is playing right now')

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        voice.resume()
        await ctx.send(':play_pause: Music Resumed')
    
    else:
        await ctx.send(':warning: Nothing is playing right now')

@bot.command()
async def play(ctx,*,arg:str = None):
    if not arg:
        await ctx.send(':information_source: Command Usage: !play `<url>`')
        return

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    channel = ctx.author.voice.channel
    if channel:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else: 
            voice = await channel.connect()

        if not voice.is_playing():
            voice.play(discord.FFmpegPCMAudio(source = arg, **FFMPEG_OPTIONS))
            voice.is_playing()
            name = arg.replace('http://','')
            await ctx.send(f"🎶🎶 **Now Playing:** `{name}`")
        else:
            voice.stop()
            voice.play(discord.FFmpegPCMAudio(source = arg, **FFMPEG_OPTIONS))
            voice.is_playing()
            name = arg.replace('http://','')
            await ctx.send(f"🎶🎶 **Now Playing:** `{name}`")
    else:
        await ctx.send(":warning: You're not connected to any channel!")


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    try:
        voice.stop()
    except Exception as e:
        pass
    await ctx.send(':stop_button:  Music Stopped')


@bot.command()
async def help(ctx):
    embed=discord.Embed(color=0x1afffb)
    embed.set_author(name="Commands Usage")
    embed.add_field(name="play", value="Play a music", inline=False)
    embed.add_field(name="resume", value="Resume the music", inline=False)
    embed.add_field(name="stop", value="Stop the current Music", inline=False)
    await ctx.send(embed=embed)

with open('Token.json') as f:
    s = json.load(f)

DTOKEN = s['Token']

bot.run(DTOKEN)