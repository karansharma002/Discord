from typing import Text
import discord
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def help(self,ctx):
        embed = discord.Embed(color = discord.Color.random())
        embed.add_field(name = "play [music name or link]",value = "Play a music",inline = False)
        embed.add_field(name = "stop",value = "End the music",inline = False)
        embed.add_field(name = "skip",value = "Skip the current played music",inline = False)
        embed.add_field(name = "queue",value = "Display the music queue",inline = False)
        embed.add_field(name = "np",value = "Gets Current Song",inline = False)
        embed.add_field(name = "pause",value = "Pauses Current Song",inline = False)
        embed.add_field(name = "resume",value = "Resumes Current Song",inline = False)
        embed.add_field(name = "seek",value = "Skips to TimeStamp",inline = False)
        embed.add_field(name = "leave",value = "Leave the voice channel",inline = False)
        embed.add_field(name = "lyrics",value = "Get the lyrics for the music",inline = False)
        await ctx.send(embed = embed)
def setup(bot):
    bot.add_cog(Music(bot))