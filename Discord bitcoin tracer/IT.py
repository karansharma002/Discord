from typing import final
import discord
from discord.ext import commands,tasks
import json
from discord.ext.commands.core import has_permissions
import requests
from bs4 import BeautifulSoup
import random
import os
import datetime
from datetime import timedelta
from dateutil import parser

bot = commands.Bot(command_prefix= '!',intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('------------- SERVER HAS STARTED -----------')


@has_permissions(administrator = True)
@bot.command()
async def setchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !setchannel `<#channel (Where the message is sent)>`')
        return

    with open('meta20.json') as f:
        data = json.load(f)
    
    mg = '**How to Purchase?**\nReact to this message with :question:\n\n**Available Items**'
    embed=discord.Embed(title = 'Welcome',description = mg,color=0xc2becb)

    for x in data['721']['41f8d833f43a40e247599c4b4f8033cf8f0b683425f87bfc3c27ec65']:
        embed.add_field(name=x, value=1)
    msg = await channel.send(embed=embed)
    with open('Config.json') as f:
        config = json.load(f)
    
    config['Channel'] = channel.id
    await ctx.send(':white_check_mark: Message has been dispatched')
    await msg.add_reaction('❓')
    with open('Config.json','w') as f:
        json.dump(config,f,indent = 3)

@bot.event
async def on_raw_reaction_add(payload):
    with open('meta20.json') as f:
        data = json.load(f)
    
    with open('Config.json') as f:
        config = json.load(f)
     
    guild = str(payload.guild_id)
    channel = await bot.fetch_channel(payload.channel_id)
    user = channel.guild.get_member(payload.user_id)
    emoji = payload.emoji
    emoji = str(emoji)

    if channel.id == config['Channel']:
        if emoji == '❓':
            address = '41f8d833f43a40e247599c4b4f8033cf8f0b683425f87bfc3c27ec65'
            items = []
            for x in data['721'][address]:
                items.append(x)

            msg = f'Relax, We have found you the {items[0]}.\
                \n- Please send the **exact amount** to the following address\
                \n- You have 20 minutes to make a valid payment or the reservation will be lost'
            
            amount = round(random.uniform(30.100000,30.000001),6)
            embed = discord.Embed(title = f"{items[0]} has been reserved for you!",description = msg,color = discord.Color.green())
            embed.add_field(name = 'Amount (ADA)',value = amount,inline = False)
            embed.add_field(name = 'Address',value = address,inline = False)
            await user.send(embed = embed)
            message = await channel.fetch_message(payload.message_id)
            reaction = discord.utils.get(message.reactions, emoji='❓')
            await reaction.remove(user)
            am = str(amount)
            am = am.replace('.','')

            timeout = str(datetime.datetime.now() + timedelta(minutes = 20))

            while True:
                r = requests.get('https://cardanoscan.io/transactions')
                soup = BeautifulSoup(r.content,'lxml')
                app = soup.find_all('span',class_ = 'adaAmount text-success')
                amounts = []
                for x in app:
                    x = str(x.text)
                    x = x.replace(' ', '')
                    amounts.append(x)

                if am in amounts:
                    msg = f'Thank you for purchasing **{items[0]}**!\
                        \nIf you need to purchase another, return back to the server and react to the message again.'
                    
                    msg2 = ''
                    traits = data['721'][address][items[0]]
                    for x in traits['traits']:
                        msg2 += f"{x},"
                    
                    embed = discord.Embed(title = 'Congrats',description = msg,color = discord.Color.blurple())
                    embed.add_field(name = 'Name:',value = traits['name'],inline = False)
                    embed.add_field(name = 'Type:',value = traits['type'],inline = False)
                    embed.add_field(name = 'Attributes',value = msg2,inline = False)
                    embed.set_image(url = traits['image'])
                    await user.send(embed = embed)
                    
                    data['721'][address].pop(items[0])
                    with open('meta20.json','w') as f:
                        json.dump(data,f,indent = 3)
                    return
                
                t1 = parser.parse(str(datetime.datetime.now()))
                t2 = parser.parse(str(timeout))
                t3 = t2 - t1
                seconds = t3.total_seconds()
                if seconds <= 0:
                    await user.send(':warning: Request Timed-out')
                    return


#bot.run('ODIzNDkzOTA1MTM4OTc0NzYw.YFhodg.iBQGcKqcMGybnTzs6bkWBfKMSog')


#wget.download('https://scontent.fluh1-2.fna.fbcdn.net/v/t1.6435-9/184381242_2976012539348639_5612415109922498997_n.png?_nc_cat=101&ccb=1-3&_nc_sid=8024bb&_nc_ohc=yzW8wwEjL80AX8JzfNW&_nc_ht=scontent.fluh1-2.fna&oh=1c824c278450c34315462c27e1bb2ee3&oe=60C1E6A3')
