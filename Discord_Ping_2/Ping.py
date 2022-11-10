import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all())


@bot.event
async def on_ready():
    print('------- PING BOT HAS STARTED ---------')

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    with open('Config.json') as f:
        config = json.load(f)
    
    if not 'Text' in config:
        return
    
    text = config['Text']
    if not message.embeds == []:
        em = message.embeds[0].to_dict()  
        for y in em.keys():
            if y == 'fields':
                content = em.get(y)
                for z in content:
                    for yz in z.values():
                        if 'for real time alerts, NFT charts, portfolio tracking and' in yz:
                            await message.channel.send(text)
                            return

            else:
                content = str(em.get(y))
                if 'for real time alerts, NFT charts, portfolio tracking and' in content:
                    await message.channel.send(text)
                    return
        
@bot.command()
async def addtext(ctx,*,text:str = None):
    if not text:
        await ctx.send(':information_source: Usage: !addtext `<#TEXT WHICH IS SENT AS A PING>`')
        return
    
    with open('Config.json') as f:
        config = json.load(f)
    
    config['Text'] = text
    with open('Config.json','w') as f:
        json.dump(config,f,indent = 3)
    
    await ctx.send(':white_check_mark: Text Added')

bot.run('OTM4MzU1NTc0NTM2NTM2MDY0.YfpFug.AE1eC8S67W6GX_8ARMYO4avvbtY')