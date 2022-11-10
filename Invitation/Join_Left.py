import discord
from discord.ext import commands

import asyncio

bot = commands.bot(command_prefix = '/', intents = discord.Intents.all())


@bot.event
async def on_ready():
    print('------------ SERVER READY -----------')

@bot.event
async def on_member_leave(member):
    msg = f'''
:MC_Personne: ︙{member} | {member.id}

:MC_Idee: ︙Compte créé {member.created_at}.

:MC_PartNotif: ︙A rejoint grâce à l'invitation de {member} qui a invité 0 membres

    '''
    embed = discord.Embed(color = discord.Color.green(), title = "ARRIVEE D'UN MEMBRE :", description = msg)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_image(url = 'https://zupimages.net/up/22/04/b758.png')
    embed.set_footer(text = f'{len(member.guild.members)} membres sur le serveur')
    channel = await bot.fetch_channel(945683900791922738)
    await channel.send(embed = embed)

@bot.event
async def on_member_join(member):

    msg = f'''
:MC_Personne: ︙{member} | {member.id}

:MC_Idee: ︙Compte créé {member.created_at}.

:MC_PartNotif: ︙A rejoint grâce à l'invitation de {member} qui a invité 0 membres

    '''
    embed = discord.Embed(color = discord.Color.red(), title = "DEPART D'UN MEMBRE :", description = msg)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_image(url = 'https://zupimages.net/up/22/04/b758.png')
    embed.set_footer(text = f'{len(member.guild.members)} membres sur le serveur')
    channel = await bot.fetch_channel(945683900791922738)
    await channel.send(embed = embed)

