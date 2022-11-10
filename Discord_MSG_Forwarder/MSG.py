import discord
from discord.ext import commands
import json

#! CHANGE TOKEN


channels_data = {
    "951616970665635910": "https://discord.com/api/webhooks/965632281270190220/_HxjsliNO-rKZWN1uqe7xWTrZH4cLebZKBk1t59dSIRlNjkYHTagpQEBUs915a_9c24J", 
    "953375551219974165": "https://discord.com/api/webhooks/965632380993957958/NBUBwIT92QZBGpLL-nRg6MHw1rmfeGXI64ezq02Z371oCbo4Pf9ADwjIJuEHFjnlnuhK", 
    "960634867605991434": "https://discord.com/api/webhooks/965632457380614145/SKmDb-2SHKLCOkXmwzuTXBUosXWld4bxDW-GewehHDXaMR9fRHwCU5K6F55R422tXHkf",
    "957343292759101460": "https://discord.com/api/webhooks/965632543552577536/8agut9k6L2nDET9EVAO3vGpGK2BWReMKE-h6cyiUxky_N4eqIszxLdu6V0cBzdoSzlqK",
    "957119678470295582": "https://discord.com/api/webhooks/965603873786064916/wcPfsmx95de9AQhDhMCGThqafkM1SSI86E35Pgjb0SShrxp61eq7-4p3ZvU7DOCcRC1c", 
    "959113865453535232": "https://discord.com/api/webhooks/965632619452702830/657U-zetV0UeLaygKgel8D-CI_iud4OD3c8hhcQ4XAgg2J-7t40vNsNgRjiVzHfpf579"

}


bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print('------- STARTED FORWARDING -------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!'):
        await bot.process_commands(message)
        return
        
    with open('Config.json') as f:
        config = json.load(f)

    if 'Target' in config:
        if message.channel.id == config['Target']:
            if not 'Embed' in config:
                color = discord.Color.dark_gold()
            else:
                r = config['Embed'][0]
                b = config['Embed'][1]
                g = config['Embed'][2]

                color = discord.Color.from_rgb(r,b,g) 
            
            

            with open('Data.json') as f:
                data = json.load(f)

            for ch in list(data):
                channel = await bot.fetch_channel(int(ch))
                content = message.content + ' ' + data[ch] if not data[ch] == 'None' else message.content
                embed = discord.Embed(color = color, description = content)
                await channel.send(embed = embed)

    await bot.process_commands(message)

@bot.command()
async def embed(ctx,r:int = None, g:int = None, b:int = None):
    if not r or not g or not b:
        await ctx.send(':information_source: Command Usage: !embed `<R CODE>` `<G CODE>` `<B CODE>` [RGB]')
        return
    
    with open('Config.json') as f:
        config = json.load(f)
    
    config['Embed'] = [r,g,b]

    with open('Config.json', 'w') as f:
        json.dump(config,f,indent = 3)
    
    await ctx.send(':white_check_mark: Embed_Color Modified')


@bot.command()
async def subscribe(ctx):
    with open('Data.json') as f:
        config = json.load(f)
    
    if str(ctx.channel.id) in config:
        await ctx.send(f':warning: {ctx.channel.mention} is already subscribed.')
        return

    config[str(ctx.channel.id)] = 'None'

    with open('Data.json', 'w') as f:
        json.dump(config,f,indent = 3)
    
    await ctx.send(f':white_check_mark: {ctx.channel.mention} SUBSCRIBED')


@bot.command()
async def unsubscribe(ctx):
    with open('Data.json') as f:
        config = json.load(f)
    
    if str(ctx.channel.id) in config:
        config.pop(str(ctx.channel.id))
    
    else:
        await ctx.send(f':warning: {ctx.channel.mention} is not subscribed.')
        return

    with open('Data.json', 'w') as f:
        json.dump(config,f,indent = 3)
    
    await ctx.send(f':white_check_mark: {ctx.channel.mention} UNSUBSCRIBED')

@bot.command()
async def changemention(ctx, mention:str = None):
    if not mention:
        await ctx.send(':information_source: Command Usage: !changemention #NEW MENTION')
        return

    with open('Data.json') as f:
        config = json.load(f)
    
    config[str(ctx.channel.id)] = mention

    with open('Data.json', 'w') as f:
        json.dump(config,f,indent = 3)
    
    await ctx.send(':white_check_mark: Mention Modified')

@bot.command()
async def target(ctx, target:discord.TextChannel = None):
    if not target:
        await ctx.send(':information_source: Command Usage: !target #CHANNEL [To Forward the Messages From]')
        return

    with open('Config.json') as f:
        config = json.load(f)
    
    config['Target'] = target.id

    with open('Config.json', 'w') as f:
        json.dump(config,f,indent = 3)
    
    await ctx.send(':white_check_mark: Target Modified')

bot.run('ODYzMzkyNTE0NjQ2ODY3OTc4.YOmO8A.H3A__sdwt1Q90SiqgX5G7EaJm84')