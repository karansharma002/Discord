import discord
from discord.ext import commands
import os
import datetime
import json
import requests
from PIL import Image, ImageOps, ImageDraw, ImageFont
from datetime import datetime,timedelta
from datetime import date as dt
import re  
from dateutil import parser
import random
from discord.ext.commands import has_permissions
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '.',case_insensitive=True,intents = intents)

bot.remove_command('help')

@bot.event
async def on_message(message):
    try:
        author = str(message.author.id)
        with open('Config/data.json','r') as f:
            data = json.load(f)
        
        if not author in data:
            data[author] = {}
            data[author]['experience'] = 0
            data[author]['level'] = 0
            data[author]['money'] = 1100
            with open('Config/data.json','w') as f:
                json.dump(data,f,indent = 3)

        with open('Config/data.json','r') as f:
            data = json.load(f)
        
        level = data[author]['level']
        if level == 0:
            level_end = 350
        elif level== 1:
            level_end = 910
        elif level== 2:
            level_end = 1110
        elif level == 3:
            level_end = 1350
        elif level == 4:
            level_end = 1500
        elif level == 5:
            level_end = 1790
        elif level == 6:
            level_end = 1800
        elif level == 7:
            level_end = 1850
        elif level == 8:
            level_end = 1900
        elif level == 9:
            level_end = 1950
        elif level == 10:
            level_end = 2000
        else:
            level_end = 2500

        if data[author]['experience'] >= level_end:
            data[author]['level'] += 1
            level = level + 1
            data[author]['experience'] = 0
            url = message.author.avatar_url
            with requests.get(url) as r:
                img_data = r.content	
                
            with open('image_name.webp', 'wb') as handler:
                handler.write(img_data)

            im = Image.open('image_name.webp')
            region = im.resize((105, 105))
            background = Image.open('Config/r.png')
            background.paste(region,(5,4))
            d2 = Image.open('Config/12.png')
            background.paste(d2,(115,84))
            background.save('Config/os.png')
            img = Image.open('Config/os.png')
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("./l_10646.ttf", 18)
            draw.text((117,60),f"{message.author}",(255, 255, 255),font=font)
            font = ImageFont.truetype("./l_10646.ttf", 14)
            draw.text((190,85),f"Level {level}",(255, 255, 255),font=font)
            img.save('Config/sample-out.png')
            await message.author.send(file=discord.File('Config/sample-out.png'))

            with open('Config/data.json','w') as f:
                json.dump(data,f,indent = 3)
        
        data[author]['experience'] += random.randint(1,5)
        with open('Config/data.json','w') as f:
            json.dump(data,f,indent = 3)
    
    except Exception as e:
        print(e)

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    guild = str(member.guild.id)
    with open('Config/guildlogs.json','r') as f:
        data = json.load(f)
    try:
        if data[guild]['Join_Message'] == 'Enabled':
            member_count = len([m for m in member.guild.members if not m.bot])
            channel = bot.get_channel(int(data[guild]['Join ID']))
            await channel.send(f":tada: Hi, {member.mention}, Welcome to {member.guild}, you're our {member_count} user! ")
    except Exception:
        pass

    try:
        if not data[guild]['Autorole'] == 'Disabled':
            role = discord.utils.get(member.guild.roles, name=data[str(member.guild.id)]['Autorole'])
            await member.add_roles(role)
    
    except KeyError:
        pass

@has_permissions(administrator = True)
@bot.command()
async def reactrole(ctx,channel: discord.TextChannel = None,max_roles:str = None,title:str = None,*,description:str = None):
    guild = str(ctx.guild.id)
    def check(m):
        return m.author == ctx.author
    
    if max_roles == None or title == None or description == None or channel == None:
        await ctx.send('Command Usage: reactrole `<#channel>` `<Max Roles Number (EX: 5)>` `<title>` `<description>`')
        return
    else:
        with open('Config/Reactions.json') as f:
            r = json.load(f)
        
        num = int(max_roles)
        iterate = 0

        while iterate < num:
            msg = await ctx.send(f'Enter the Role Name: #{iterate+1}')
            role_name = await bot.wait_for('message',check = check)
            await msg.delete()
            msg = await ctx.send(f'Enter the Reaction Emoji: #{iterate+1}')
            emoji = await bot.wait_for('message',check = check)
            role_name = role_name.content
            emoji = emoji.content
            await msg.delete()
            if not guild in r:
                r[guild] = {}
            
            r[guild][str(emoji)] = role_name        
            iterate += 1
        
        r[guild]['Channel'] = channel.id
        await ctx.send('Reaction Roles has been activated.')
        with open('Config/Reactions.json','w') as f:
            json.dump(r,f,indent = 3)

        with open('Config/Reactions.json','r') as f:
            r = json.load(f)

        embed = discord.Embed(title = title,description = description,color = 0x90e2fe)
        msg = await channel.send(embed = embed)
        for emojis in r[guild]:
            try:
                await msg.add_reaction(emojis)
            except Exception as e:
                pass


@bot.event
async def on_raw_reaction_add(payload):
    with open('Config/Reactions.json') as f:
        r = json.load(f)
    
    guild = str(payload.guild_id)
    channel = await bot.fetch_channel(payload.channel_id)
    user = channel.guild.get_member(payload.user_id)
    emoji = payload.emoji
    emoji = str(emoji)
    if guild in r:
        if channel.id == r[guild]['Channel']:
            for em in r[guild]:
                if em == emoji:
                    role = discord.utils.get(channel.guild.roles, name=r[guild][em])
                    await user.add_roles(role)    

@bot.event
async def on_raw_reaction_remove(payload):
    emoji = str(payload.emoji)
    guild = bot.get_guild(payload.guild_id)
    gi = str(guild.id)
    member = guild.get_member(payload.user_id)
    channel = payload.channel_id
    with open('Config/Reactions.json') as f:
        r = json.load(f) 
    if str(guild.id) in r:
        if channel == r[gi]['Channel']:
            for em in r[gi]:
                if em == emoji:
                    channel = await bot.fetch_channel(payload.channel_id)
                    role = discord.utils.get(guild.roles, name=r[gi][em])
                    await member.remove_roles(role)   

@bot.command()
async def help(ctx):
    
    embed=discord.Embed(color=0x955cff)
    embed.set_author(name="Commands Help")
    embed.add_field(name=":gear: **Moderations**", value="`BAN` `UNBAN` `KICK`` `CLEAR` `WARN` `REMOVEWARN`", inline=False)
    embed.add_field(name=":tada: **Giveaway**", value="`GSTART` `GSTOP`", inline=False)
    embed.add_field(name=":game_die: **Economy**", value="`ROB` `WORK`", inline=False)
    embed.add_field(name =":dna: **General**", value = "`WELCOMEMESSAGE` `AUTOROLE` `REACTIONROLE` `SETLOGS`", inline = False)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text = f'{ctx.author} ')
    await ctx.send(embed=embed)

#COGS / Command LOADING
for filename in os.listdir('./Commands/Giveaway'):
    if filename.endswith('.py'):
        bot.load_extension(f'Commands.Giveaway.{filename[:-3]}')


for filename in os.listdir('./Commands/Moderations'):
    if filename.endswith('.py'):
        bot.load_extension(f'Commands.Moderations.{filename[:-3]}')


for filename in os.listdir('./Commands/Economy'):
    if filename.endswith('.py'):
        bot.load_extension(f'Commands.Economy.{filename[:-3]}')

for filename in os.listdir('./Commands/Misc'):
    if filename.endswith('.py'):
        bot.load_extension(f'Commands.Misc.{filename[:-3]}')


bot.run('TOKEN HERE')