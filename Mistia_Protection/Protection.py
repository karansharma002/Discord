import discord
from discord.ext import commands, tasks
import json
import datetime
bot = commands.Bot(command_prefix = 'mp.', intents = discord.Intents.all())
max_msg_per_window = 5
author_msg_times = {}
    
@bot.event
async def on_ready():
    print('----- PROTECTION BOT HAS STARTED -----')
    await bot.wait_until_ready()
    time_ = time.time()

time_window_milliseconds = 5000
max_msg_per_window = 5
author_msg_times = {}

import time


THRESHOLD = 3

members_data = []

time_ = []

def antiraid(member):
    global members_data
    global time_
    members_data.append(member)
    time_.append([member, time.time()])

    if not time_ == []:
        print(time_)
        if round(time.time() - time_[0][1]) <= 15:
            print('triggered')
            if len(members_data) >= THRESHOLD:
                return 'True'
            else:
                return 'False'

        print(members_data)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)

    '''
    global author_msg_counts

    author_id = message.author.id
    curr_time = datetime.datetime.now().timestamp() * 1000

    if not author_msg_times.get(author_id, False):
        author_msg_times[author_id] = []

    author_msg_times[author_id].append(curr_time)

    expr_time = curr_time - time_window_milliseconds

    expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
    ]

    for msg_time in expired_msgs:
        author_msg_times[author_id].remove(msg_time)
        
    if len(author_msg_times[author_id]) >= max_msg_per_window:
        embed = discord.Embed(description = f"{message.author.mention} a été expulsé pour spam.", title = "ANTI-SPAM", color = discord.Color.red())
        await message.channel.send(embed = embed)
        await message.channel.purge(limit = len(author_msg_times[author_id]), check = lambda x: x.author.id == message.author.id, oldest_first=False) #purges the channel
        return
    
    '''
    
import discord
import numpy as np
import random
import string
import os
import shutil
import asyncio
import time
from discord.ext import commands
from discord.utils import get
from PIL import ImageFont, ImageDraw, Image
import Augmentor

is_raid_active = False

@bot.command()
async def raid_on(ctx):
    global is_raid_active
    if is_raid_active:
        await ctx.send(":warning: Le mode Raid est déjà actif. Utilisez : `mp.raid_off` pour éteindre ")
        return
    
    else:
        is_raid_active = True
        embed = discord.Embed(color = discord.Color.red(), title = 'MODE RAID :', description = f'{ctx.author.mention} a activé le mode raid.')
        channel = await bot.fetch_channel(945684284826591292)
        await channel.send(embed = embed)

@bot.command()
async def raid_off(ctx):
    global is_raid_active

    if not is_raid_active:
        await ctx.send(":warning: Le mode Raid est déjà désactivé. Utilisez : `mp.raid_on` pour l’activer")
        return
    
    else:
        is_raid_active = False
        embed = discord.Embed(color = discord.Color.green(), title = 'MODE RAID :', description = f'{ctx.author.mention} a désactivé le mode raid.')
        channel = await bot.fetch_channel(945684284826591292)
        await channel.send(embed = embed)

@bot.event
async def on_member_join(member):
    global members_data
    global time_

    if member.bot:
        return
    
    if member.id == bot.user.id:
        return

    global is_raid_active

    if is_raid_active:
        await member.send(":warning: Vous avez été exclu de Sofia -'s server car ce serveur est en mode raid ! Retentez de le rejoindre ultérieurement.")
        await member.kick(reason = 'Raid Mode Active')
        return

    bool_ = antiraid(member.id)
    print(bool_)
    if bool_ == 'True':
        print('HERE')
        data = ''
        for x in list(members_data):
            user = member.guild.get_member(x)
            unixtime = f"<t:{int(user.created_at.timestamp())}:R>"
            data += f"> {user} - Compte créé {unixtime}\n"
            await user.send('<:MC_Idee:906936886415753290>︙Vous avez été exclu du serveur MISTIA Conceptions | Graphismes & Serveurs car une action anti-raid a été déclenchée.  Reessayez plus tard !')
            await user.kick(reason = ':warning: Anti-Raid Triggered')

        msg = f'''
Le mode raid a été déclenché car trop de personnes ont rejoint le serveur dans les 5 dernières secondes.

<:MC_Avis:906936886063411251> ︙ **Personnes exclues:**
{data}
• Pour supprimer le mode raid : mp. raid-off.
• Pour réactiver le mode raid : mp.raid-on
    '''
        embed = discord.Embed(title = "ACTION ANTI-RAID", description = msg, color = discord.Color.green())
        channel = await bot.fetch_channel(945684284826591292)
        await channel.send(embed = embed)
        embed = discord.Embed(color = discord.Color.red(), title = 'MODE RAID :', description = f'{bot.user.mention} a activé le mode raid.')
        is_raid_active = True
        await channel.send(embed = embed)
        members_data = []
        time_ = []
        return is_raid_active


    # Read configuration.json
    data = {}
    captchaChannel = await bot.fetch_channel(945683807028252702)

    memberTime = f"{member.joined_at.year}-{member.joined_at.month}-{member.joined_at.day} {member.joined_at.hour}:{member.joined_at.minute}:{member.joined_at.second}"
    # Give temporary role
    
    role = discord.utils.get(member.guild.roles, id = 948260845199171614)
    try:
        await member.add_roles(role)
    except:
        pass

    # Create captcha
    image = np.zeros(shape= (100, 350, 3), dtype= np.uint8)

    # Create image 
    image = Image.fromarray(image+255) # +255 : black to white

    # Add text
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font= "./arial.ttf", size= 60)

    text = ' '.join(random.choice(string.ascii_uppercase) for _ in range(6)) # + string.ascii_lowercase + string.digits

    # Center the text
    W, H = (350,100)
    w, h = draw.textsize(text, font= font)
    draw.text(((W-w)/2,(H-h)/2), text, font= font, fill= (90, 90, 90))

    # Save
    ID = member.id
    folderPath = f"{member.guild.id}/captcha_{ID}"

    try:
        os.mkdir(folderPath)
    except:
        if os.path.isdir(f"{member.guild.id}") is False:
            os.mkdir(f"{member.guild.id}")
        if os.path.isdir(folderPath) is True:
            shutil.rmtree(folderPath)
        os.mkdir(folderPath)

    image.save(f"{folderPath}/captcha{ID}.png")

    # Deform
    p = Augmentor.Pipeline(folderPath)
    p.random_distortion(probability=1, grid_width=4, grid_height=4, magnitude=14)
    p.process()

    # Search file in folder
    path = f"{folderPath}/output"
    files = os.listdir(path)
    captchaName = [i for i in files if i.endswith('.png')]
    captchaName = captchaName[0]

    image = Image.open(f"{folderPath}/output/{captchaName}")
    
    # Add line
    width = random.randrange(6, 8)
    co1 = random.randrange(0, 75)
    co3 = random.randrange(275, 350)
    co2 = random.randrange(40, 65)
    co4 = random.randrange(40, 65)
    draw = ImageDraw.Draw(image)
    draw.line([(co1, co2), (co3, co4)], width= width, fill= (90, 90, 90))
    
    # Add noise
    noisePercentage = 0.25 # 25%

    pixels = image.load() # create the pixel map
    for i in range(image.size[0]): # for every pixel:
        for j in range(image.size[1]):
            rdn = random.random() # Give a random %
            if rdn < noisePercentage:
                pixels[i,j] = (90, 90, 90)

    # Save
    image.save(f"{folderPath}/output/{captchaName}_2.png")

    # Send captcha
    captchaFile = discord.File(f"{folderPath}/output/{captchaName}_2.png")
    captchaEmbed = await captchaChannel.send("> **Bonjour {}**\n> Afin de vérifier votre compte et avoir accès au serveur, merci de remplir ce captcha :".format(member.mention), file= captchaFile)
    # Remove captcha folder

    try:
        shutil.rmtree(folderPath)
    except Exception as error:
        print(f"Delete captcha file failed {error}")

    # Check if it is the right user
    def check(message):
        if message.author == member and  message.content != "":
            return message.content

    try:
        msg = await bot.wait_for('message', timeout=120.0, check=check)
        # Check the captcha
        password = text.split(" ")
        password = "".join(password)
        if msg.content.lower() == password.lower():
            unixtime = f"<t:{int(member.created_at.timestamp())}:R>"
            msgg = f"<:MC_Personne:906936886755491870>︙{member} | `{member.id}`\na complété correctement le CAPTCHA"
            embed = discord.Embed(description = msgg, color = discord.Color.green(), title = 'CAPTCHA VALIDE :')
            try:
                await msg.delete()
            except:
                pass

            try:
                await captchaEmbed.delete()

            except discord.errors.NotFound:
                pass

            await captchaChannel.send(embed=embed, delete_after = 5)
            
            try:
                getrole = discord.utils.get(member.guild.roles, id = 948260879550521385)
                await member.add_roles(getrole)

            except:
                pass

            try:
                getrole = discord.utils.get(member.guild.roles, id = 948260845199171614)
                await member.remove_roles(getrole)
            except:
                pass


            unixtime = f"<t:{int(member.created_at.timestamp())}:R>"
            
            id_  = await bot.fetch_channel(945684204748951613 )
            await id_.send(embed=embed)

            msgg = f"<:MC_Personne:906936886755491870>︙{member} | `{member.id}`\na complété correctement le CAPTCHA"
            embed = discord.Embed(description = msgg, color = discord.Color.green(), title = 'CAPTCHA VALIDE :')
            try:
                await member.send(embed = embed)
            except:
                pass

        else:
            link = await captchaChannel.create_invite(max_age=172800) # Create an invite
            msgg = f"<:MC_Personne:906936886755491870>︙{member} | `{member.id}`\nn'a pas complété correctement le CAPTCHA"
            embed = discord.Embed(description = msgg, color = discord.Color.red(), title = 'CAPTCHA NON VALIDE :')
            await captchaChannel.send(embed = embed, delete_after = 5)
            id_  = await bot.fetch_channel(945684204748951613)
            await id_.send(embed = embed)

            embed = discord.Embed(title = 'CAPTCHA NON VALIDE :', description = f"<:MC_Personne:906936886755491870>︙{member} | `{member.id}`\
                \n\n<:MC_Idee:906936886415753290>︙Vous avez raté le Captcha.\
                \n\n<:MC_Partager:906936886629638174>︙Voici le lien d'invitation : {link}", color = 0xff0000)
            try:
                await member.send(embed=embed)

            except discord.errors.Forbidden:
                pass

            await member.kick()

            time.sleep(3)

            try:
                await captchaEmbed.delete()
            except discord.errors.NotFound:
                pass

            try:
                await msg.delete()
            except discord.errors.NotFound:
                pass

    except (asyncio.TimeoutError):
        msgg = f"<:MC_Personne:906936886755491870>︙{member} | `{member.id}`\nn'a pas complété correctement le CAPTCHA"
        embed = discord.Embed(description = msgg, color = discord.Color.red(), title = 'DÉLAI CAPTCHA')
        id_  = await bot.fetch_channel(945684204748951613)
        await id_.send(embed = embed)

        link = await captchaChannel.create_invite(max_age=172800)
        msgg = f"<:MC_Personne:906936886755491870>︙{member} | `{member.id}`\nn'a pas complété correctement le CAPTCHA"
        embed = discord.Embed(description = msgg, color = discord.Color.red(), title = 'DÉLAI CAPTCHA')
        await captchaChannel.send(embed = embed, delete_after = 5)

        try:
            embed = discord.Embed(title = 'CAPTCHA NON VALIDE :', description = f"<:MC_Personne:906936886755491870>︙{member} | `{member.id}`\
                \n\n<:MC_Idee:906936886415753290>︙Vous avez raté le Captcha.\
                \n\n<:MC_Partager:906936886629638174>︙Voici le lien d'invitation : {link}", color = 0xff0000)

            await member.kick() 

        except:
            pass

        await captchaEmbed.delete()


bot.run('OTQzNTcxNDc2ODczODk2MDI2.Yg0_ag.arSqgarHqTTjyBMfmwXbCNuZwUM')