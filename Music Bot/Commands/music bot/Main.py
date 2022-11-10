import discord
from discord.ext import commands
import json
import time
from youtube_search import YoutubeSearch
import youtube_dl 
from datetime import datetime

song_queue = []
class Music(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    def search(self,arg):
        ydl_opts = {'format': 'bestaudio'}
        yt = YoutubeSearch(arg, max_results=1).to_json()
        yt_id = str(json.loads(yt)['videos'][0]['id'])
        yt_url = 'https://www.youtube.com/watch?v='+yt_id
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_url, download=False)
            URL = info['formats'][0]['url']    
        
        duration = time.strftime('%H:%M:%S', time.gmtime(info['duration']))
        img = info['thumbnails'][0]['url']
        return {'source': URL, 'title': info['title'],'Duration':duration,'Song_URL':yt_url,'Image_URL':img}

    def skips(self,ctx):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        global song_queue
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if len(song_queue) > 1:
            del song_queue[0]
            voice.play(discord.FFmpegPCMAudio(source = song_queue[0]['title'], **FFMPEG_OPTIONS), after=lambda e: self.skips(ctx))
            voice.is_playing()

    @commands.command()
    async def queue(self,ctx):
        global song_queue
        msg = ''
        for num, x in enumerate(song_queue):
            msg += f"**{num+1}** - {x['title']} - `{x['Duration']}`\n"
        
        if msg == '':
            msg = 'Empty'
        await ctx.send(msg)

    @commands.command()
    async def skip(self,ctx):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        global song_queue
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not len(song_queue) == 0:
            a = voice.is_playing()
            if a: 
                del song_queue[0]
                voice.stop()
                voice.play(discord.FFmpegPCMAudio(source = song_queue[0]['source'], **FFMPEG_OPTIONS), after=lambda e: self.skips(ctx))
                await ctx.send("Looks like no one liked this song, skipping it.")
            else:
                await ctx.send("i'm not playing music !")
        else:
            await ctx.send('There are no songs in the QUEUE, Stopped playing the jams!')
        

    @commands.command()
    async def play(self,ctx,*,args):
        global song_queue
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        try:
            channel = ctx.author.voice.channel
            if channel:
                voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
                song = self.search(args)
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
        
        except Exception as e:
            print(e)
            await ctx.send("Oops something went wrong!")

    @commands.command()
    async def seek(self,ctx,val:str = None):
        def get_sec(val):
            m, s = val.split(':')
            return int(m) * 60 + int(s)
        
        if val == None:
            await ctx.send('Give me the duration to seek')
            return

        global song_queue
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': f'-vn -ss {get_sec(val)}'}
        try:
            channel = ctx.author.voice.channel
            if channel:
                voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
                if len(song_queue) == 0:
                    await ctx.send("i'm not playing music !")
                    return

                song = song_queue[0]

                if voice.is_playing():
                    voice.stop()
                    voice.play(discord.FFmpegPCMAudio(source = song['source'], **FFMPEG_OPTIONS), after=lambda e: self.skips(ctx))
                    voice.is_playing()
                    await ctx.send(f"Skipped to {val}")

                else:
                    await ctx.send("i'm not playing music !")
            else:
                await ctx.send("you must be connected to a channel")
        
        except Exception as e:
            await ctx.send(f'ERROR: {e}')

    @commands.command()
    async def pause(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        #voice = await ctx.author.voice.channel.connect()
        if voice and voice.is_playing():
            voice.pause()
            await ctx.send('Paused Playing Jams')
        
        else:
            await ctx.send("i'm not playing music !")

    @commands.command()
    async def stop(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()
            await ctx.send('Stopped the music!')
        
        else:
            await ctx.send("i'm not playing music !")

    @commands.command()
    async def resume(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        #voice = await ctx.author.voice.channel.connect()
        if voice and voice.is_paused():
            voice.resume()
            await ctx.send('Started Playing Jams')
        
        else:
            await ctx.send("i'm not playing music !")

    @commands.command(aliases = ['np','get'])
    async def nowplaying(self,ctx):
        global song_queue
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            duration = song_queue[0]['Duration']
            embed=discord.Embed(color = discord.Color.random(),description=f"**[{song_queue[0]['title']}]({song_queue[0]['Song_URL']})**")
            embed.set_author(name = 'Now Playing 🎵',url = song_queue[0]['Song_URL'])
            embed.add_field(name="Length:", value=duration, inline=False)
            embed.add_field(name="Requested By:", value=f"{ctx.author.name} ({ctx.author})", inline=False)
            embed.set_thumbnail(url = song_queue[0]['Image_URL'])
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed = embed)
        else:
            await ctx.send("i'm not playing music !")

    @commands.command()
    async def leave(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice:
            await voice.disconnect()
            await ctx.send('Disconnected from the Voice Channel')
        
        else:
            await ctx.send('I am not connected to any channel.')

        
def setup(bot):
    bot.add_cog(Music(bot))
    