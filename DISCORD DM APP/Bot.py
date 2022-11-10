import sys
import os
import discord
from discord.ext import commands
import subprocess
bot = commands.Bot(command_prefix = '$')
import aiohttp
import json

async def restart_program():
    aiosession = aiohttp.ClientSession(loop=bot.loop)
    try:
      await aiosession.close()
    except:
       pass
    await bot.close()
    subprocess.call([sys.executable, "Bot.py"])

@bot.command()
async def restart(ctx):
    await restart_program()

@bot.event
async def on_ready():
    print(bot.user)



token = "ODI0MDU0MzQ5NTQ1MDc4Nzk0.YFpyhg.SmqKcF57apYY1VCGoGOsCDKXklw "
bot.run(token,bot = False)

#! WE NEED TO SEE IF THE BOT USER TOKEN GET'S BANNED, THEN DO SOMETHING BUT HOW? WE'LL SEE
#! WE NEED TO ROTATE TOKENS
