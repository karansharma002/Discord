import discord
from discord import embeds
from discord.ext import commands
import json
import os
import imagehash
from PIL import Image

bot = commands.Bot(command_prefix = '$',intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('------------ SERVER STARTED -----------------')

@bot.event
async def on_message(message):

    await bot.process_commands(message)
    author = str(message.author.id)
    channel = message.channel.id

    with open('DRT.json') as f:
        data = json.load(f)
    
    with open('SETG.json') as f:
        settings = json.load(f)

    with open('Warns.json') as f:
        warns = json.load(f)

    if settings == {}:
        return
    
    if message.author.bot:
        return
    
    if message.author == bot.user:
        return

    if not author in data:
        data[author] = {}
        data[author]['Name'] = str(message.author.name)
        data[author]['Points'] = 0
        data[author]['Wallet'] = 'Not Registered'

        with open('DRT.json','w') as f:
            json.dump(data,f,indent = 3)
    
    if 'Channel' in settings:
        if channel == settings['Channel']:
            if not author in data:
                data[author] = {}
                data[author]['Name'] = message.author
                data[author]['Points'] = 0

            data[author]['Wallet'] = message.content

            with open('DRT.json','w') as f:
                json.dump(data,f,indent = 3)
            
            try:
                await message.author.send(':white_check_mark: Wallet Address Updated!!')
            except:
                return

    if not message.attachments == []:
        split_v1 = str(message.attachments).split("filename='")[1]
        filename = str(split_v1).split("' ")[0]
        if filename.lower().endswith(('jpeg','jpg','png','gif','svg','webp')):
            await message.attachments[0].save(filename)

        try:
            if channel == settings['1xChannel']:
                with open('Image_Hash.json') as f:
                    hash_img = json.load(f)

                with Image.open(filename) as img:
                    temp_hash = imagehash.average_hash(img, 70)
                    if str(temp_hash) in hash_img:
                        try:
                            if not author in warns:
                                warns[author] = 1
                            else:
                                warns[author] += 1
                            with open('Warns.json','w') as f:
                                json.dump(warns,f,indent = 3)
                            await message.author.send(':warning: You have received 1 warning for duplicate image.')
                        except:
                            pass
                        
                        
                    else:
                        hash_img[str(temp_hash)] = filename
                        with open('Image_Hash.json','w') as f:
                            json.dump(hash_img,f,indent = 3)

                        data[author]['Points'] += 1
                        with open('DRT.json','w') as f:
                            json.dump(data, f,indent = 3)
                os.remove(filename)

        except KeyError:
            pass

        try:
            if channel == settings['50xChannel']:
                with open('Image_Hash.json') as f:
                    hash_img = json.load(f)

                with Image.open(filename) as img:
                    temp_hash = imagehash.average_hash(img, 70)
                    if str(temp_hash) in hash_img:
                        try:
                            if not author in warns:
                                warns[author] = 1
                            else:
                                warns[author] += 1
                            with open('Warns.json','w') as f:
                                json.dump(warns,f,indent = 3)
                            await message.author.send(':warning: You have received 1 warning for duplicate image.')
                        except:
                            pass
                        
                        
                    else:
                        hash_img[str(temp_hash)] = filename
                        with open('Image_Hash.json','w') as f:
                            json.dump(hash_img,f,indent = 3)

                        data[author]['Points'] += 50
                        with open('DRT.json','w') as f:
                            json.dump(data, f,indent = 3)
                
                os.remove(filename)

        except KeyError:
            pass


@bot.command()
async def set1xchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !set1xchannel `<#CHANNEL>`')
        return

    with open('SETG.json') as f:
        settings = json.load(f)
    
    settings['1xChannel'] = channel.id

    with open('SETG.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel Saved!!')

@bot.command()
async def set50xchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !set50xchannel `<#CHANNEL>`')
        return

    
    with open('SETG.json') as f:
        settings = json.load(f)
    
    settings['50xChannel'] = channel.id

    with open('SETG.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel Saved!!')

@commands.has_permissions(administrator = True)
@bot.command()
async def givewarn(ctx,member:discord.User = None):
    if not member:
        await ctx.send(':information_source: !givewarn `<@user>`')
        return

    with open('Warns.json') as f:
        warns = json.load(f)
    
    author = str(member.id)

    if not author in warns:
        warns[author] = 0
    
    warns[author] += 1
    with open('Warns.json','w') as f:
        json.dump(warns,f,indent = 3)
    
    await ctx.send(f':white_check_mark: {member} has received 1 warning.')

@commands.has_permissions(administrator = True)
@bot.command()
async def removewarn(ctx,member:discord.User = None):
    if not member:
        await ctx.send(':information_source: !removewarn `<@user>`')
        return

    with open('Warns.json') as f:
        warns = json.load(f)
    
    author = str(member.id)

    if not author in warns:
        await ctx.send(":warning: User don't have any warnings")
        return
    
    if warns[author] - 1 <= 0:
        warns.pop(author)
    else:
        warns[author] -= 1

    with open('Warns.json','w') as f:
        json.dump(warns,f,indent = 3)
    
    await ctx.send(f':white_check_mark: 1 warning has been removed for {member}')

@bot.command()
async def leaderboard(ctx):
    with open('DRT.json','r') as f:
        data = json.load(f)
    
    with open('Warns.json') as f:
        warns = json.load(f)
    
    high_score = sorted(data, key=lambda x : data[x].get('Points', 0), reverse=True)
    msg = ''
    for num,x in enumerate(high_score):
        pt = data[x]['Points']
        if x in warns:
            msg += f"{num + 1}: {data[x]['Name']} | **Points**: __{pt}__ | **Warnings**: __{warns[x]}__\n"
        else:
            msg += f"{num + 1}: {data[x]['Name']} | **Points**: __{pt}__ | **Warnings**: __0__\n"

        if num == 15:
            break
        else:
            num += 1
    
    embed = discord.Embed(color = discord.Color.blurple(),description = msg)
    embed.set_author(name = f"Top {num} Users",icon_url = bot.user.avatar_url)
    await ctx.send(embed = embed)

@bot.command()
async def details(ctx,member:discord.Member = None):
    with open('DRT.json','r') as f:
        data = json.load(f)
    
    with open('Warns.json') as f:
        warns = json.load(f)
    
    if not member:
        user = ctx.author
        name = ctx.author.name
        url = ctx.author.avatar_url
        author = str(ctx.author.id)
    else:
        user = member
        name = member.name
        url = member.avatar_url
        author = str(member.id)
    
    if author in warns:
        wr = warns[author]
    else:
        wr = 0
    
    if not author in data:
        data[author] = {}
        data[author]['Name'] = name
        data[author]['Points'] = 0
        data[author]['Wallet'] = 'Not Registered'

        with open('DRT.json','w') as f:
            json.dump(data,f,indent = 3)

    points = data[author]['Points']
    wallet = data[author]['Wallet']    
    embed = discord.Embed(color = discord.Color.blue())
    embed.set_author(name = f"{user} | Details",icon_url= url)    
    embed.add_field(name = 'Points',value = points,inline = False)
    embed.add_field(name = 'Wallet',value = wallet,inline = False)
    embed.add_field(name = 'Warnings',value = wr,inline = False)
    await ctx.send(embed = embed)

@commands.has_permissions(administrator = True)
@bot.command()
async def setpoints(ctx,user:discord.User = None,points:int = None):
    if not user or not points:
        await ctx.send(":information_source: Usage: !setpoints `<@user>` `<POINTS>`")
        return
    
    with open('DRT.json') as f:
        data = json.load(f)
    
    author = str(user.id)
    if not author in data:
        data[author] = 0
    data[author] += points
    with open('DRT.json','w') as f:
        json.dump(data, f, indent=3)
    
    await ctx.send(f':white_check_mark: Added {points} to {user}')

@commands.has_permissions(administrator = True)
@bot.command()
async def removepoints(ctx,user:discord.User = None,points:int = None):
    if not user or not points:
        await ctx.send(":information_source: Usage: !removepoints `<@user>` `<POINTS>`")
        return
    
    with open('DRT.json') as f:
        data = json.load(f)
    
    author = str(user.id)
    if not author in data:
        data[author] = 0

    data[author] -= points if not data[author] - points < 0 else data[author]

    with open('DRT.json','w') as f:
        json.dump(data, f, indent=3)
    
    await ctx.send(f':white_check_mark: Removed {points} from {user}')

@bot.command()
async def setchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !setchannel `<#CHANNEL to Register Wallet Address>`')
        return

    with open('SETG.json') as f:
        settings = json.load(f)
    
    settings['Channel'] = channel.id

    with open('SETG.json','w') as f:
        json.dump(settings,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel Saved!!')



bot.run('ODc0NTU4MDExNjEwMzcwMDU4.YRItng.Drffb_VTKNFAGXI-fTO2FIrN9Ps')
