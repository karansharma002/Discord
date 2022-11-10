import requests
import discord
from discord.ext import commands
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
bot = commands.Bot(command_prefix='.',intents = discord.Intents.all())


@bot.command()
async def setupticket(ctx,channel:discord.TextChannel = None,*,role:str = None):
    if not channel:
        await ctx.send(':information_source: Usage: .setupticket `<#channel> (Where reaction will be active)` `<ROLE>`')
        return

    else:
        with open('Settings.json') as f:
            s = json.load(f)
        
        s['Channel'] = channel.id
        s['Role'] = role

        await ctx.send(':white_check_mark: Ticket system has been activated')
        embed=discord.Embed(title="Open a Ticket", description="Need help? React below", color=0xff0000)
        msg = await channel.send(embed=embed)
        await msg.add_reaction('🖐️')
        with open('Settings.json','w') as f:
            json.dump(s,f,indent = 3)


@bot.event
async def on_raw_reaction_add(payload):
    print(payload.user_id)
    with open('Settings.json') as f:
        r = json.load(f)
    
    guild = await bot.fetch_guild(payload.guild_id)
    channel = await bot.fetch_channel(payload.channel_id)
    member = channel.guild.get_member(payload.user_id)
    print(member)
    emoji = payload.emoji
    emoji = str(emoji)
    if channel.id == r['Channel']:
        if emoji == '🖐️':
            role = discord.utils.get(channel.guild.roles, name=r['Role'])
            await member.add_roles(role)    

@bot.command()
async def viphelp(ctx):
    msg = ':gear: **Moderations**\nupload\ntimeframe\nsetx\nsetupimages\nsetup\nsetticketschannel\nsettickets\nsetprize\nsetlogs\nsetchannel\nset_winning_channel\noutputtickets\nforcedraw\
        \n\n:coin: **Utility**\nleaderboard\nprizes\ntickets'
    embed=discord.Embed(title = 'Commands Help',description = msg,color=0xce2727)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text = 'AMG Proxies',icon_url= 'https://i.imgur.com/0EdVhZe.jpg')
    await ctx.send(embed=embed)
bot.run('ODIzNDkzOTA1MTM4OTc0NzYw.YFhodg.iBQGcKqcMGybnTzs6bkWBfKMSog')