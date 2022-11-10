import discord
import random
import praw
import json
from discord.ext import commands, tasks
import asyncio


bot = commands.Bot(command_prefix = '.', intents = discord.Intents.all())

gld = 937414943786024960
invites = {}
last = ""

async def fetch():
    global last
    global invites
    await bot.wait_until_ready()
    
    while True:

        guild = await bot.fetch_guild(gld)
        invs = await guild.invites()
        tmp = []
        for i in invs:
            for s in invites:
                if s[0] == i.code:
                    if int(i.uses) > s[1]:
                        with open('Config.json') as f:
                            config = json.load(f)

                        if 'Invite_Channel' in config:
                            logs = await bot.fetch_channel(int(config['Invite_Channel']))
                            usr = guild.get_member(int(last))
                            usr = await bot.fetch_user(int(last))
                            testh = f"{usr.name} **joined**; Invited by **{i.inviter.name}** (**{str(i.uses)}** invites)"
                            await logs.send(testh)

            tmp.append(tuple((i.code, i.uses)))

        invites = tmp
        await asyncio.sleep(2)

@bot.command()
async def setinviteschannel(ctx, channel:discord.TextChannel = None):
    if not channel:
        await ctx.send('Usage: .setinviteschannel <#CHANNEL WHERE MEMES ARE SENT>')
        return
    
    with open('Config.json', 'r') as f:
        config = json.load(f)
    
    config['Invite_Channel'] = channel.id

    with open('Config.json', 'w') as f:
        json.dump(config,f,indent = 3 )
    
    await ctx.send(':white_check_mark: Channel Added')

@bot.command()
async def setmemechannel(ctx, channel:discord.TextChannel = None):
    if not channel:
        await ctx.send('Usage: .setmemechannel <#CHANNEL WHERE MEMES ARE SENT>')
        return
    
    with open('Config.json', 'r') as f:
        config = json.load(f)
    
    config['Meme_Channel'] = channel.id

    with open('Config.json', 'w') as f:
        json.dump(config,f,indent = 3 )
    
    await ctx.send(':white_check_mark: Channel Added')

@bot.event
async def on_member_join(member):
    global last
    last = str(member.id)
    return 

@tasks.loop(minutes = 30)
async def post_meme():

    with open('Config.json') as f:
        config = json.load(f)
    
    if not 'Meme_Channel' in config:
        return

    channel = await bot.fetch_channel(int(config['Meme_Channel']))

    reddit = praw.Reddit(client_id='jgf86Zu-MVQb0g',

    client_secret='Y2wYXcNd40piWqGRLGlBAGk8Eqs',
    user_agent="Karma breakdown 1.0 by /u/_Daimon_ github.com/Damgaard/Reddit-Bots/")

    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 10)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    embed=discord.Embed(color=0xff8000)
    embed.set_author(name =submission.title, url = submission.url)
    embed.set_image(url = submission.url)
    await channel.send(embed = embed)

@bot.command()
async def invites(ctx):
    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == ctx.author:
            totalInvites += i.uses
            
    msg = f'You currently have **{totalInvites}** invites.'
    embed = discord.Embed(color = discord.Color.dark_blue(), title = f"{ctx.author} | Total Invites", description = msg)
    await ctx.send(embed = embed)

bot.loop.create_task(fetch())

bot.run('ODE4MDk1MzY3Njc2NjI0OTA5.YETErw.RokmAgVoNk-DR1FGsnKAAJzdvrg')