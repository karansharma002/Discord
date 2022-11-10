import discord
from discord.ext import commands, tasks
import json

bot = commands.Bot(command_prefix = '!')

import pymongo

with open('Config.json') as f:
    config = json.load(f)

host = config['Host']
port = config['Port']

database = pymongo.MongoClient(host, port)

database_name = database[config['Database']]

mycol = database_name[config["Collection"]]


@bot.event
async def on_ready():
    print('------ BOT HAS STARTED -------')
    await bot.wait_until_ready()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    embed_dict = message.embeds[0].to_dict()
    result = ''
    for item in list(embed_dict):
        try:
            if 'successful checkout' in embed_dict[item].lower() or 'checkout successful' in embed_dict[item].lower():
                result = 'exists'
                break
        except:
            try:
                for temp_content in list(embed_dict[item].values()):
                    if 'successful checkout' in str(temp_content).lower():
                        result = 'exists'
                        break
            except:
                continue
    
    if result == '':
        return
        
    for field in list(embed_dict["fields"]):
        if any(character.lower() in field['name'].lower() for character in ('Promo Code', 'Item Price', 'Purchase Price', 'Order', 'Proxy', 'Email', 'Profile name', 'Offer ID', 'Password','Session Name', 'Account', 'Account:', 'Delay', 'Mode', 'Version')):
            embed_dict['fields'].remove(field)

        elif any(character.lower() in field['name'].lower() for character in ('Profile', 'Account','User','Session Name','Profile Name','email')):
            
            for x in mycol.find():
                if 'Profiles' in x:
                    dta = x['Profiles'].split(',')
                    print(dta)
                    print(field['value'])
                    for email in dta:
                        email = email.replace(' ','')
                        email = email.replace('"', '')
                        email = email.replace("'",'')
                        if email in field['value']:
                            field['value'] = x['User']

    embed = discord.Embed.from_dict(embed_dict)
    target = await bot.fetch_channel(942795086742290433)
    await target.send(embed = embed) 
  
bot.run('OTQyNzYxMTQyNzA5ODA1MTE4.YgpMvA.KW3bPKECfbALg2bIWBQ8HxvZ8Yk')