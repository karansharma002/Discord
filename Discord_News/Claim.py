import discord
from discord.ext import commands, tasks
import json

bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('Ready')
    feed_fetch.start()

@tasks.loop(seconds = 60)
async def feed_fetch():
    import feedparser

    url = 'https://screenrant.com/feed/'

    feed = feedparser.parse(url)

    sent = []
    for x in feed.entries:
        title = x.title
        title = f":newspaper: **| {title}**"
        link = x.link
        summary = x.summary
        if not title in sent:
            msg = f"{title}\n\n{link}"
            sent.append(title)
            channel = await bot.fetch_channel(886983311535247361)
            await channel.send(msg)
        
        else:
            pass

@bot.event
async def on_message(message):
    channel = str(message.channel.id)

    with open('Settings.json') as f:
        settings = json.load(f)
    
    if channel in settings['Channels']:
        await message.add_reaction('👍')
    
    await bot.process_commands(message)

    
@bot.event
async def on_raw_reaction_add(payload):
    message = payload.message_id
    member = payload.user_id
    channel = str(payload.channel_id)

    with open('Settings.json') as f:
        settings = json.load(f)

    
    if channel in settings['Channels']:
        if channel in settings:
            return
        
        else:
            for role in settings['Roles']:
                ch = await bot.fetch_channel(int(channel))
                need_role = discord.utils.get(ch.guild.roles, id = int(role))
                user = discord.utils.get(bot.get_all_members(), id=int(member))
                if need_role in user.roles:
                    settings[str(channel)] = user

                    with open('Settings.json', 'w') as f:
                        json.dump(settings,f,indent = 3)
                    
                    for members in ch.guild.members:
                        if members.guild_permissions.administrator:
                            try:
                                await members.send(f'{user} has claimed the article. ID: {message} in {ch.mention}')
                            except:
                                continue
                    return

@bot.command()
async def addchannel(ctx, channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !addchannel `#CHANNEL`')
        return

    with open('Settings.json') as f:
        settings = json.load(f)
    
    if not str(channel.id) in settings['Channels']:
        settings['Channels'].append(str(channel.id))

        with open('Settings.json', 'w') as f:
            json.dump(settings,f,indent = 3)

        await ctx.send(':white_check_mark: Channel Added')
    else:
        await ctx.send(':warning: Channel already exists in the database.')

@bot.command()
async def removechannel(ctx, channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !removechannel `#CHANNEL`')
        return

    with open('Settings.json') as f:
        settings = json.load(f)
    
    if str(channel.id) in settings['Channels']:
        settings['Channels'].remove(str(channel.id))

        with open('Settings.json', 'w') as f:
            json.dump(settings,f,indent = 3)

        await ctx.send(':white_check_mark: Channel Removed')

    else:
        await ctx.send(':warning: Channel not exists in the database.')

@bot.command()
async def removerole(ctx, role:discord.Role = None):

    if not role:
        await ctx.send(':information_source: Usage: !removerole `#role`')
        return

    with open('Settings.json') as f:
        settings = json.load(f)
    
    if str(role.id) in settings['Roles']:
        settings['Roles'].remove(str(role.id))

        with open('Settings.json', 'w') as f:
            json.dump(settings,f,indent = 3)

        await ctx.send(':white_check_mark: Role Removed')

    else:
        await ctx.send(':warning: Role not exists in the database.')

@bot.command()
async def addrole(ctx, role:discord.Role = None):

    if not role:
        await ctx.send(':information_source: Usage: !addrole `#role`')
        return

    with open('Settings.json') as f:
        settings = json.load(f)
    
    if not str(role.id) in settings['Roles']:
        settings['Roles'].append(str(role.id))

        with open('Settings.json', 'w') as f:
            json.dump(settings,f,indent = 3)

        await ctx.send(':white_check_mark: Role Added')

    else:
        await ctx.send(':warning: Role already exists in the database.')

bot.run('ODMwMTA3NDUwMjgyNjA2NTkz.YHB3zg.IqQagJ21xe5_ie5ov9LKVpdU840')

 

