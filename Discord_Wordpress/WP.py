import discord
from discord.ext import commands, tasks
import requests
import json


bot = commands.Bot(command_prefix='!')

import base64

@bot.event
async def on_ready():
    print('----------- BOT HAS STARTED --------------')
    await bot.wait_until_ready()
    update_post.start()

@tasks.loop(minutes = 2)
async def update_post():
    with open('Config.json') as f:
        config = json.load(f)
    
    
    import datetime
    dt = datetime.datetime.today().strftime('%d-%m-%Y')
    dt = str(dt)
    dt2 = datetime.datetime.today() - datetime.timedelta(days = 1)
    dt2 = dt2.strftime('%d-%m-%Y')
    dt2 = str(dt2)

    if dt2 in config:
        content = ''
        
        for x in config[dt2]:
            for y in config[dt2][x]:
                content += x + '\n\n'

            content = content.replace('<replacestrongwithstart>', '<strong>')
            content = content.replace('<replacestrongwithend>', '</strong>')


            for guild in config['Guilds']:
                if y in config['Guilds'][guild]['Channels']:
                    url = config['Guilds'][guild]['URL']
                    user = config['Guilds'][guild]['Name']
                    password = config['Guilds'][guild]['Password']

                    title = f"stepn - {dt}"
                    url = f"{url}/wp-json/wp/v2/posts"
                    user = f"{user}"
                    password = f"{password}"
                    credentials = user + ':' + password
                    token = base64.b64encode(credentials.encode())
                    header = {'Authorization': 'Basic ' + token.decode('utf-8')}
                    post = {
                    'title'    : title,
                    'status'   : 'publish', 
                    'content'  : content,
                    'categories': 6
                    }

                    response = requests.post(url , headers=header, json=post)

                    config.pop(dt2)
                    with open('Config.json', 'w') as f:
                        json.dump(config, f, indent = 3)
                    
                    break

@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return

    await bot.process_commands(message)


    channel = str(message.channel.id)
    
    with open('Config.json') as f:
        config = json.load(f)
    
    if not message.guild:
        return

    guild = str(message.guild.id)

    if guild in config['Guilds']:
        if not int(channel) in config['Guilds'][guild]['Channels']:
            return

        try:
            import datetime
            dt = datetime.datetime.today().strftime('%d-%m-%Y')
            dt = str(dt)

            dt2 = datetime.datetime.today().strftime('%H:%M')
            dt2 = str(dt2)

            if not dt in config:
                config[dt] = {}
            


            if not channel in config[dt]:
                config[dt][channel] = []
            
            content = f"<replacestrongwithstart>{message.author.id}: {dt2}<replacestrongwithend>\n"

            if message.content == '':
                embed = message.embeds[0]
                embed_dict = embed.to_dict()
                ct = embed_dict['description']

            else:
                ct = message.content

            content += ct

            config[dt][channel].append(content)
            with open('Config.json', 'w') as f:
                json.dump(config, f, indent = 3)
            
        except Exception as e:
            print(e)
            return

   

@commands.has_permissions(administrator = True)
@bot.command()
async def setup(ctx):
    with open('Config.json') as f:
        config = json.load(f)
    
    guild = str(ctx.guild.id)

    try:
        await ctx.author.send('Please follow the following instructions to setup the BOT')
    except discord.Forbidden:
        await ctx.send(':warning: `---- USER DM ARE DISABLED ----')
        return
    

    def check(m):
        return m.author == ctx.author and isinstance(m.channel, discord.DMChannel)

    await ctx.author.send(':one: Please enter the website URL including http or https:')
    url = await bot.wait_for('message', check = check, timeout = 120)
    url = url.content

    await ctx.author.send(':two: Please enter the website Username')
    username = await bot.wait_for('message', check = check, timeout = 120)
    username = username.content

    await ctx.author.send(':three: Please enter the Application Password Generated from Plugin')
    password = await bot.wait_for('message', check = check, timeout = 120)
    password = password.content

    config['Guilds'][guild] = {}
    config['Guilds'][guild]['URL'] = url
    config['Guilds'][guild]['Name'] = username
    config['Guilds'][guild]['Password'] = password
    config['Guilds'][guild]['Channels'] = []

    await ctx.author.send(':white_check_mark: Website added. You can now set the channels using !addchannel COMMAND')

    with open('Config.json', 'w') as f:
        json.dump(config,f,indent = 3)

@bot.command()
async def addchannel(ctx, channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':warning: Command Usage: !addchannel #CHANNEL MENTION')
        return

    guild = str(ctx.guild.id)
    with open('Config.json') as f:
        config = json.load(f)
    
    if not guild in config['Guilds']:
        await ctx.send(':warning: Guild is not SET. Please setup using !setup')
        return
    
    if not channel.id in config['Guilds'][guild]['Channels']:
        config['Guilds'][guild]['Channels'].append(channel.id)
        with open('Config.json', 'w') as f:
            json.dump(config,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel Added')

bot.run('ODk1MzIxNjA5Njk3NjQ0NjM0.YV23Og.nx6BOFlXYMxvT71CCBgRSjI7fR8')
