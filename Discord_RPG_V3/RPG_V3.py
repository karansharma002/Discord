import discord
from discord.ext import commands, tasks
import json
import os
from discord_components import Button, Select, SelectOption, ComponentsBot

from discord_components import DiscordComponents

bot = commands.Bot(command_prefix = '%', intents = discord.Intents.all())
bot.remove_command('help')

DiscordComponents(bot)

@bot.event
async def on_ready():
    print('------ RPG IS RUNNING -------')
    
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.author == bot.user:
        return
    
    author = str(message.author.id)

    with open('Config/Data.json') as f:
        data = json.load(f)

    '''
    Level 1 = 0XP
    Level 2 = 2000 XP
    Level 3 = 3000 XP
    Level 4 = 4000 XP
    Level 5 = 5000 XP.......
    ...Level 100 = 100000 XP CAP!
    '''

    if author in data:
        level = data[author]['Level']
        xp = data[author]['XP']
        
        if xp >= (level + 1) * 1000:
            data[author]['Level'] += 1
            data[author]['Points'] += 1
            with open('Config/Data.json') as f:
                json.dump(data,f,indent = 3)

            try:
                await message.author.send(':tada: You have levelled up. You have earned 1 skill point. (!distribute for more info)')
            except:
                pass
                
    await bot.process_commands(message)
        
for filename in os.listdir('./Commands'):
	if filename.endswith('.py'):
		bot.load_extension(f'Commands.{filename[:-3]}')

@bot.command()
async def help(ctx):
    msg = '''
__**Admin**__:
  deleteitem   
  deleteres    
  deleteweapon 
  edititem     
  editres      
  editweapon   
  makeitem     
  makeres      
  makeweapon   
  removeitem   
  removeres    
  removeweapon 
  spawndemon   
  spawnitem    
  spawnres     
  spawnweapon  

__**Player**__:
  attack       
  dig          
  distribute   
  dodge        
  equip        
  hunt         
  inventory    
  mine         
  mines        
  register     
  spy          
  stats    

__**Shop**__:
  iteminfo     
  shop
    '''
    embed = discord.Embed(color = discord.Color.dark_orange(), description = msg, title = 'Commands Help')
    await ctx.send(embed = embed)

bot.run('OTA5MzMxMzgxNDMwMTU3MzE0.YZCu1w.wAeKmzX5KgcfrRYMsequSqpWEP0')


        


