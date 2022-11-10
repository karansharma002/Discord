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

@tasks.loop(minutes = 1)
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
        channel = await bot.fetch_channel(949156073657495572)

        content = ''

        for x in config[dt2]:
            content += x + '\n\n'
        
        title = f"{channel.name} | {dt}"
        url = "https://pawmaji.com/wp-json/wp/v2/posts"
        user = "pawmajiadmin2021"
        password = "ocrF cAWp rNB7 E9YY ns9k 55B7"
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
        

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    channel = str(message.channel.id)
    
    if channel == '949156073657495572':
        with open('Config.json') as f:
            config = json.load(f)
        
        content = message.content
        try:
            import datetime
            dt = datetime.datetime.today().strftime('%d-%m-%Y')
            dt = str(dt)

            if not dt in config:
                config[dt] = []

            if content == '':
                embed = message.embeds[0]
                embed_dict = embed.to_dict()
                content = embed_dict['description']
            
            config[dt].append(content)
            with open('Config.json', 'w') as f:
                json.dump(config, f, indent = 3)
            
        except Exception as e:
            print(e)
            return

    await bot.process_commands(message)
 
bot.run('ODk1MzIxNjA5Njk3NjQ0NjM0.YV23Og.nx6BOFlXYMxvT71CCBgRSjI7fR8')
