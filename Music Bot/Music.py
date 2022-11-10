from logging import exception
import discord
from discord.ext import commands
import os

import lyricsgenius

bot = commands.Bot(command_prefix='.')#,intents = discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    print('-------- BOT INSTANCE HAS STARTED --------')

@bot.command()
async def lyrics(ctx,artist:str = None,title:str = None):
    await ctx.send('Lyrics are not available for this music.')

for files in os.listdir('./CMD'):
    for filename in os.listdir("./CMD/"+files):
        if filename.endswith('.py'):
            bot.load_extension(f'CMD.{files}.{filename[:-3]}')

bot.run('ODY3MDQwMTA1NDM2NTQ1MDU5.YPbUBQ.ISfTGUx5iwDJoSm5634IffTKgxE')
