import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
import json
import tweepy
import asyncio
from dateutil import parser
import datetime

#! Initialize The Bot Client
bot = commands.Bot(command_prefix = '!')
bot.remove_command('help')

with open('Config.json', 'r') as f:
    config = json.load(f)

guild_id = config['Server_ID']

#! Pass the Bot Client to the Slash Library and Sync the Commands
slash = SlashCommand(bot, sync_commands=True)

#! TASK LOOP TO CHECK THE TWITTER API AND TASKS EVERY 30 SECONDS [DO NOT EDIT THE NUMBER]
@tasks.loop(seconds = 30)
async def fetch_points():
    with open('Config.json', 'r') as f:
        config = json.load(f)

    #! AUTHORISE THE TWITTER API
    api = tweepy.Client(bearer_token=config['Bearer_Token'])

    with open('Tasks.json') as f:
        task_ = json.load(f)
    
    with open('Data.json') as f:
        data = json.load(f)
    
    #!SEARCHING THE TASKS LIST

    for x in task_:
        t1 = parser.parse(str(datetime.datetime.now()))
        t2 = parser.parse(str(config[x]['Timer']))
        t3 = t2 - t1
        t4 = round(t3.total_seconds() / 3600)
        if t4 <= 0:
            t4 = round(t3.total_seconds() / 60)
            if t4 <= 0:
                continue
            
        #! USING THE TWEET ID AS A SEARCH PARAMETER AS TWITTER TAKES THE TWEET ID
        tweet_id = task_[x]['Tweet_ID']

        try:
            #! GET USERS WHO RETWEETED THE TWEET ID
            users = api.get_retweeters(id=tweet_id, user_fields=['profile_image_url'])
            for user in users.data:
                for y in list(data):
                    if str(user) == data[y]['Twitter']:
                        #! CHECKING IF THE TASK IS NOT COMPLETED BY THE USER
                        if task_[x]['Name'] in data[y]['Tasks']:
                            if 'RetweetPoints' in data[y]['Tasks'][task_[x]['Name']]:
                                pass

                            else:
                                data[y]['Tasks'][task_[x]['Name']]['RetweetPoints'] = task_[x]['RetweetPoints']
                                #! ADD THE POINTS TO THE USER POINTS VARIABLE
                                data[y]['Points'] += task_[x]['RetweetPoints']
                    
                                with open('Data.json', 'w') as f:
                                    json.dump(data,f,indent = 3)

                        else:
                            #! ADD THE COMPLETED TASKS INTO USER DATABASE
                            data[y]['Tasks'][task_[x]['Name']] = {}
                            data[y]['Tasks'][task_[x]['Name']]['RetweetPoints'] = task_[x]['RetweetPoints']
                            #! ADD THE POINTS TO THE USER POINTS VARIABLE
                            data[y]['Points'] += task_[x]['RetweetPoints']
                
                            with open('Data.json', 'w') as f:
                                json.dump(data,f,indent = 3)

        except:
            pass

        try:
            #! GET USERS WHO LIKED THE TWEET ID
            users = api.get_liking_users(id=tweet_id, user_fields=['profile_image_url'])

            for user in users.data:
                for y in list(data):
                    if str(user) == data[y]['Twitter']:
                        if task_[x]['Name'] in data[y]['Tasks']:
                            if 'LikePoints' in data[y]['Tasks'][task_[x]['Name']]:
                                pass
                        
                            else:
                                data[y]['Tasks'][task_[x]['Name']]['LikePoints'] = task_[x]['LikePoints']
                                #! ADD THE POINTS TO THE USER POINTS VARIABLE
                                data[y]['Points'] += task_[x]['LikePoints']
                    
                                with open('Data.json', 'w') as f:
                                    json.dump(data,f,indent = 3)

                        else:
                            #! ADD THE COMPLETED TASKS INTO USER DATABASE
                            data[y]['Tasks'][task_[x]['Name']] = {}
                            data[y]['Tasks'][task_[x]['Name']]['LikePoints'] = task_[x]['LikePoints']
                            #! ADD THE POINTS TO THE USER POINTS VARIABLE
                            data[y]['Points'] += task_[x]['LikePoints']
                
                            with open('Data.json', 'w') as f:
                                json.dump(data,f,indent = 3)

        except:
            pass

        try:

            with open('Config.json', 'r') as f:
                config = json.load(f)

            auth = tweepy.OAuthHandler(config['api_key'], config['api_key_secret'])
            auth.set_access_token(config['access_token'], config['access_token_secret'])

            api = tweepy.API(auth, wait_on_rate_limit=True)

            for y in list(data):
                user_name = data[y]['Twitter']
                replies = tweepy.Cursor(api.search_tweets, q='from:{}'.format(user_name),
                                                    since_id=tweet_id, tweet_mode='extended', count = 20).items()
                for z in replies:
                    try:
                        s = z._json
                        s = s['user']
                        if str(s['screen_name']) == user_name:
                            if task_[x]['Name'] in data[y]['Tasks']:
                                if 'CommentPoints' in data[y]['Tasks'][task_[x]['Name']]:
                                    pass

                                else:
                                    data[y]['Tasks'][task_[x]['Name']]['CommentPoints'] = task_[x]['CommentPoints']
                                    #! ADD THE POINTS TO THE USER POINTS VARIABLE
                                    data[y]['Points'] += task_[x]['CommentPoints']
                        
                                    with open('Data.json', 'w') as f:
                                        json.dump(data,f,indent = 3)

                            else:
                                #! ADD THE COMPLETED TASKS INTO USER DATABASE
                                data[y]['Tasks'][task_[x]['Name']] = {}
                                data[y]['Tasks'][task_[x]['Name']]['CommentPoints'] = task_[x]['CommentPoints']
                                #! ADD THE POINTS TO THE USER POINTS VARIABLE
                                data[y]['Points'] += task_[x]['CommentPoints']
                    
                                with open('Data.json', 'w') as f:
                                    json.dump(data,f,indent = 3)

                    except:
                        continue
        
        except:
            pass

#! PREBUILT EVENT TO CHECK IF THE BOT IS READY TO WORK       
@bot.event
async def on_ready():
    print('READY')

    await bot.wait_until_ready()
    #! STARTING THE TASKS EVENT
    fetch_points.start()

#! ---------------------------------------------- COMMANDS ARE BELOW ------------------------------------------------

@commands.has_permissions(administrator=True)
@slash.slash(name = 'create_task', description = 'Create a new Task', guild_ids = [guild_id])
async def create_task(ctx, name:str, timer:int, twitter_link, retweet_points:int, comment_points:int, like_points:int, tweet_id:str):
    try:
        with open('Tasks.json') as f:
            config = json.load(f)
        
        config[twitter_link] = {}
        config[twitter_link]['Name'] = name
        config[twitter_link]['Timer'] = str(datetime.datetime.now() + datetime.timedelta(hours = timer))
        config[twitter_link]['TwitterLink'] = twitter_link
        config[twitter_link]['RetweetPoints'] = retweet_points
        config[twitter_link]['LikePoints'] = like_points
        config[twitter_link]['CommentPoints'] = comment_points
        config[twitter_link]['Tweet_ID'] = int(tweet_id)
        with open('Tasks.json', 'w') as f:
            json.dump(config, f, indent = 3)

        await ctx.send(':white_check_mark: Task Added')
    except:
        import traceback
        traceback.print_exc()
        

@slash.slash(name = 'givepoints', description = 'Give Points to the User', guild_ids = [guild_id])
async def givepoints(ctx, user:discord.User,points:int, reason:str):
    author = str(user.id)

    with open('Data.json') as f:
        data = json.load(f)
    
    if not author in data:
        await ctx.send(':warning: User Profile registered.')
        return
    
    data[author]['Points'] += points

    with open('Data.json', 'w') as f:
        json.dump(data,f,indent = 3)

    await ctx.send(f':white_check_mark: Added {points} to {user}')

@slash.slash(name = 'lowestscore', description = 'Shows the Users with the Lowest Score', guild_ids = [guild_id])
async def lowestscore(ctx):
    with open('Data.json','r') as f:
        users = json.load(f)

    high_score_list1 = sorted(users, key=lambda x : users[x].get('Points', 0), reverse=False)
    msg1 = ''
    msg2 = ''

    for number,user in enumerate(high_score_list1):
        author = await bot.fetch_user(int(user))
        number += 1
        xp = users[user]['Points']
        msg1 += f"**‣ {number}**. {author} ⁃ Points: **{xp}**\n"
        if number == 10:
            break
        else:
            number += 1
    
    embed = discord.Embed(colo = discord.Color.red(), title = 'Users with the Lowest Score', description = msg1)
    await ctx.send(embed = embed)

@slash.slash(name = 'profile', description = 'Shows the Users Profile', guild_ids = [guild_id])
async def profile(ctx):
    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)

    if not author in data:
        await ctx.send(':warning: User Profile registered.')
        return
        
    wallet = data[author]['Wallet']
    twitter_username = data[author]['Twitter']

    embed = discord.Embed(title = ctx.author.name)
    embed.add_field(name = 'Wallet Address', value = wallet, inline = False)
    embed.add_field(name = 'Twitter Username', value = twitter_username, inline = False)
    await ctx.send(embed = embed)

@slash.slash(name = 'createprofile', description = 'Create a new Profile', guild_ids = [guild_id])
async def createprofile(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg1 = await ctx.send('1️⃣ Enter your Twitter Username')

        msg2 = await bot.wait_for('message', check = check, timeout = 60)
        twitter_username = msg2.content

        await msg1.delete()
        await msg2.delete()

        msg1 = await ctx.send('2️⃣ Enter your Wallet Number')
        msg2 = await bot.wait_for('message', check = check, timeout = 60)
        wallet = msg2.content

        await msg1.delete()
        await msg2.delete()

        with open('Data.json') as f:
            data = json.load(f)
        
        author = str(ctx.author.id)
        data[author] = {}
        data[author]['Points'] = 0
        data[author]['Twitter'] = twitter_username
        data[author]['Wallet'] = wallet
        data[author]['Tasks'] = {}

        with open('Data.json', 'w') as f:
            json.dump(data,f,indent = 3)
        
        await ctx.send(':white_check_mark: Profile Registered.')
        return
    
    except asyncio.TimeoutError:
        await ctx.send(':warning: Request Timed Out!!')
        return

@slash.slash(name = 'editprofile', description = 'Edit a Profile: [Params: username/wallet]', guild_ids = [guild_id])
async def editprofile(ctx, to_edit:str,*, new_value):
    author = str(ctx.author.id)
    with open('Data.json') as f:
        data = json.load(f)
    
    if not author in data:
        await ctx.send(':warning: User Profile is not registered.')
        return


    if to_edit.lower() == 'username':
        data[author]['Twitter'] = new_value
    
    elif to_edit.lower() == 'wallet':
        data[author]['Wallet'] = new_value
    
    else:
        await ctx.send(':warning: Invalid Option. [Allowed: Username / Wallet]')

    with open('Data.json', 'w') as f:
        json.dump(data,f,indent = 3)
    
    await ctx.send(':white_check_mark: Profile Edited.')
    return

@slash.slash(name = 'score', description = 'Shows the Users Total Points [Score]', guild_ids = [guild_id])
async def score(ctx):
    author = str(ctx.author.id)

    with open('Data.json') as f:
        data = json.load(f)
    
    if not author in data:
        await ctx.send(':warning: User Profile registered.')
        return
    
    points = data[author]['Points']

    embed = discord.Embed(title = f'{ctx.author} | Points', description = f'Your total Points are: __**{points}**__')
    await ctx.send(embed = embed)

@slash.slash(name = 'leaderboard', description = 'Shows the Users with the Highest Score', guild_ids = [guild_id])
async def leaderboard(ctx):
    with open('Data.json','r') as f:
        users = json.load(f)

    high_score_list1 = sorted(users, key=lambda x : users[x].get('Points', 0), reverse=True)
    msg1 = ''
    msg2 = ''
    for number,user in enumerate(high_score_list1):
        author = await bot.fetch_user(int(user))
        number += 1
        xp = users[user]['Points']
        msg1 += f"**‣ {number}**. {author} ⁃ Points: **{xp}**\n"
        if number == 15:
            break
        else:
            number += 1

    embed = discord.Embed(
        title= ":money_with_wings: Leaderboard ",
        color= 0x05ffda,
        description= msg1
        )
        
    await ctx.send(embed = embed)

@slash.slash(name = 'tasks', description = 'Shows the available Tasks', guild_ids = [guild_id])
async def tasks(ctx):
    with open('Tasks.json') as f:
        config = json.load(f)
    
    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)
    if not author in data:
        await ctx.send(':warning: User Profile registered.')
        return

    msg = ''
    
    for x in config:
        t1 = parser.parse(str(datetime.datetime.now()))
        t2 = parser.parse(str(config[x]['Timer']))
        t3 = t2 - t1
        t4 = round(t3.total_seconds() / 3600)
        if t4 <= 0:
            t4 = round(t3.total_seconds() / 60)
            if t4 <= 0:
                continue
        
        elif config[x]['Name'] in data[author]['Tasks']:
            embed = discord.Embed(title = 'Current Tasks', color = discord.Color.red())
            embed.add_field(name = 'Task Name', value = config[x]['Name'], inline = False)
            embed.add_field(name = 'Task Description', value = config[x]['TwitterLink'], inline = False)
            for y in ('RetweetPoints', 'LikePoints', 'CommentPoints'):
                if y in data[author]['Tasks'][config[x]['Name']]:
                    continue
                else:
                    msg = 'ADDED'
                    embed.add_field(name = y, value = config[x][y], inline = False)

            if  msg == 'ADDED':
                await ctx.send(embed = embed)
                msg = 'SENT'
            else:
                break
        
        else:
            embed = discord.Embed(title = 'Current Tasks', color = discord.Color.red())
            embed.add_field(name = 'Task Name', value = config[x]['Name'], inline = False)
            embed.add_field(name = 'Task Description', value = config[x]['TwitterLink'], inline = False)
            embed.add_field(name = 'RetweetPoints', value = config[x]['RetweetPoints'], inline = False)
            embed.add_field(name = 'LikePoints', value = config[x]['LikePoints'], inline = False)
            embed.add_field(name = 'CommentPoints', value = config[x]['CommentPoints'], inline = False)
            await ctx.send(embed = embed)
            msg = 'SENT'

    
    if not msg == 'SENT':
        await ctx.send(':warning: No tasks are available.')
    
    return

@slash.slash(name = 'completed_tasks', description = 'Shows the Completed Tasks', guild_ids = [guild_id])
async def completed_tasks(ctx):    
    with open('Data.json') as f:
        data = json.load(f)

    author = str(ctx.author.id)
    if not author in data:
        await ctx.send(':warning: User Profile registered.')
        return
    
    if data[author]['Tasks'] == {}:
        embed = discord.Embed(color = discord.Color.green(), title = f"{ctx.author} | Tasks", description = 'ZERO COMPLETED')
        await ctx.send(embed = embed)
        return
        
    embed = discord.Embed(color = discord.Color.green(), title = f"{ctx.author} | Tasks")
    for y in data[author]['Tasks']:
        embed.add_field(name = y, value = data[author]['Tasks'][y], inline = False)

    await ctx.send(embed = embed)

@slash.slash(name = 'help', description = 'Commands Help', guild_ids = [guild_id])
async def help(ctx):
    if ctx.author.guild_permissions.administrator:
        msg = '''    
**ADMIN Commands**
`/create_task` - Create a new Task
`/givepoints`  - Give Points to the User

**USER Commands**
`/lowestscore` - Shows the Users with the Lowest Score
`/profile` - Shows the Users Profile
`/createprofile` - Create a new Profile
`/editprofile` - Edit a profile
`/score` - Shows the Users total points
`/leaderboard`  - Shows the Users with the Highest Score
`/tasks` - Shows the available tasks
`/completed_tasks` - Shows the Completed Tasks
    '''
        embed = discord.Embed(title = 'Commands Help', color = discord.Color.red(), description = msg)
        await ctx.send(embed = embed)
    
    else:
        msg = '''    
`/lowestscore` - Shows the Users with the Lowest Score
`/profile` - Shows the Users Profile
`/createprofile` - Create a new Profile
`/editprofile` - Edit a profile
`/score` - Shows the Users total points
`/leaderboard`  - Shows the Users with the Highest Score
`/tasks` - Shows the available tasks
`/completed_tasks` - Shows the Completed Tasks
    '''
        embed = discord.Embed(title = 'Commands Help', color = discord.Color.red(), description = msg)
        await ctx.send(embed = embed)    

with open('Config.json', 'r') as f:
    tk = json.load(f)

TOKEN = tk['Bot_Token']
bot.run(TOKEN)