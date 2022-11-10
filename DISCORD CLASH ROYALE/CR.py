import requests
import json
import discord
from discord.ext import commands,tasks

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('------------ SERVER HAS STARTED--------------- ')

@tasks.loop(hours = 23)
async def extract():
    #!  EXECUTE IF THE SEASON ENDS
    season = ''
    if not season:
        return

    with open('Settings.json') as f:
        settings = json.load(f)
    
    if not 'Channel' in settings:
        return

    channel = await bot.fetch_channel(settings['Channel'])

    TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImExNDFkY2QzLTMzYmYtNGMxNi1hMzY1LTJlOGI4NmE1NmY4ZSIsImlhdCI6MTYyMTMzNDgxOCwic3ViIjoiZGV2ZWxvcGVyL2JlMDE1ZjMxLWZiYWYtZTk3My01MjQ3LTU0ZTRlNTEwZDYxYiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMDMuNDEuMjUuMjUzIl0sInR5cGUiOiJjbGllbnQifV19.L8MPAKvAD8cCIW4nFBtazJtTfsq__e5IDdgaO3fQ6Xoi9_8BrRga6r94s88lDRuTWl8m9NkOnMy-tJE-oVNEcA'

    headers = {'Authorization':"Bearer %s" %TOKEN}

    #! FINISH BOT FUNCTIONS
    clanTag = settings['Clan']
    params = {'clantag':clanTag}
    r = requests.get(f'https://api.clashroyale.com/v1/clans/%23{clanTag}/members',headers = headers,params = params)
    content = json.loads(r.content)
    embed = discord.Embed(color = discord.Color.green())
    embed.set_author(name = 'TOP 10 CLAN MEMBERS',icon_url=bot.user.avatar_url)
    for x in range(len(content['items'])):
        user = content['items'][x]
        name = user['name']
        tag = user['tag']
        trophies = user['trophies']
        rank = user['clanRank']
        donations = user['donations']
        role = user['role']
        embed.add_field(name = f'{x + 1}: {name.upper()}',value = f"**Tag:** {tag}\n**Trophies:** {trophies}\n**Rank:** {rank}\n**Donations**: {donations}\n**Role:** {role}",inline = False)
        if x == 9:
            await channel.send(embed = embed)
            break
    
    with open('Tournament.json') as f:
        t = json.load(f)
    
    embed = discord.Embed(color = discord.Color.red())
    embed.set_author(name = 'TOP 3 Tournament Players',icon_url=bot.user.avatar_url)
    tourna_list = sorted(t, key=lambda x : t[x].get('Score', 0), reverse=True)
    for num,user in enumerate(tourna_list):
        tag = user
        name = t[tag]['Name']
        score = t[tag]['Score']
        embed.add_field(name = f'{num + 1}: {name.upper()}',value = f"**Tag:** {tag}\n**Score:** {score}\n",inline = False)
        if num == 2:
            await channel.send(embed = embed)
            break
    
@bot.command()
async def test(ctx):
    with open('ST.json') as f:
        settings = json.load(f)

    TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImExNDFkY2QzLTMzYmYtNGMxNi1hMzY1LTJlOGI4NmE1NmY4ZSIsImlhdCI6MTYyMTMzNDgxOCwic3ViIjoiZGV2ZWxvcGVyL2JlMDE1ZjMxLWZiYWYtZTk3My01MjQ3LTU0ZTRlNTEwZDYxYiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMDMuNDEuMjUuMjUzIl0sInR5cGUiOiJjbGllbnQifV19.L8MPAKvAD8cCIW4nFBtazJtTfsq__e5IDdgaO3fQ6Xoi9_8BrRga6r94s88lDRuTWl8m9NkOnMy-tJE-oVNEcA'

    headers = {'Authorization':"Bearer %s" %TOKEN}

    #! FINISH BOT FUNCTIONS

    clanTag = settings['Clan']
    params = {'clantag':clanTag,'limit':5}
    r = requests.get(f'https://api.clashroyale.com/v1/clans/%23{clanTag}/members',headers = headers,params = params)
    print(r.status_code)
    content = json.loads(r.content)
    embed = discord.Embed(color = discord.Color.green(),title = 'TOP 5 RANKS')
    for x in range(len(content['items'])):
        user = content['items'][x]
        name = user['name']
        tag = user['tag']
        trophies = user['trophies']
        rank = user['clanRank']
        embed.add_field(name = f'{x + 1}: {name.upper()}',value = f"**Tag:** {tag}\n**Trophies:** {trophies}\n**Rank:** {rank}",inline = False)
        #- Ingame name
        #- Player Tag
        #- Trophy’s
        #- Rank in clan  
        if x == 4:
            break
    
    await ctx.send(embed = embed)

    #! TOURNAMENT BOT FUNCTIONS

    params = {'clantag':settings['ID']}
    clanTag = settings['ID']
    r = requests.get(f'https://api.clashroyale.com/v1/tournaments/%23{clanTag}',headers = headers,params = params)
    content = json.loads(r.content)

    embed = discord.Embed(color = discord.Color.green(),title = 'TOP 3 TOURNAMENT PLAYERS')
    for x in range(len(content['membersList'])):
        user = content['membersList'][x]
        tag = user['tag']
        name = user['name']
        score = user['score']
        rank = user['rank']
        print(tag,name,score,rank)
        embed.add_field(name = f'{x + 1}: {name.upper()}',value = f"**Tag:** {tag}\n**Score:** {score}\n**Rank:** {rank}",inline = False)
        if x == 2:
            break
    
    await ctx.send(embed = embed)

@bot.command()
async def setclan(ctx,*,clan:str = None):
    if not clan:
        await ctx.send(':information_source: !setclan `<CLAN ID>`')
        return
    
    with open('ST.json') as f:
        data = json.load(f)
    
    if '#' in clan:
        clan = clan.replace('#','')
    data['Clan'] = clan

    with open('ST.json','w') as f:
        json.dump(data,f,indent = 3)
    
    await ctx.send(':white_check_mark: Clan ID has been SET!')

@bot.command()
async def setchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: !setchannel `#CHANNEL`')
        return
    
    with open('ST.json') as f:
        data = json.load(f)
    
    data['Channel'] = channel.id

    with open('ST.json','w') as f:
        json.dump(data,f,indent = 3)
    
    await ctx.send(':white_check_mark: CHANNEL has been SET!')

@bot.command()
async def settournament(ctx,*,id_:str = None):
    with open('Tournament.json') as f:
        t = json.load(f)
    
    if not id_:
        await ctx.send(':information_source: Usage: !settournament `<TOURNAMENT ID>`')
        return
    
    with open('ST.json') as f:
        data = json.load(f)
    
    if '#'in id_:
        id_ = id_.replace('#','')
    
    data['ID'] = id_
    
    with open('ST.json','w') as f:
        json.dump(data,f,indent = 3)
    
    await ctx.send(':white_check_mark: TOURNAMENT ID has been SET!')
    
    #! FETCH AND STORE THE DATA of the NEW TOURNAMENT
    TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImExNDFkY2QzLTMzYmYtNGMxNi1hMzY1LTJlOGI4NmE1NmY4ZSIsImlhdCI6MTYyMTMzNDgxOCwic3ViIjoiZGV2ZWxvcGVyL2JlMDE1ZjMxLWZiYWYtZTk3My01MjQ3LTU0ZTRlNTEwZDYxYiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMDMuNDEuMjUuMjUzIl0sInR5cGUiOiJjbGllbnQifV19.L8MPAKvAD8cCIW4nFBtazJtTfsq__e5IDdgaO3fQ6Xoi9_8BrRga6r94s88lDRuTWl8m9NkOnMy-tJE-oVNEcA'

    headers = {'Authorization':"Bearer %s" %TOKEN}

    params = {'clantag':id_}
    clanTag = id_
    r = requests.get(f'https://api.clashroyale.com/v1/tournaments/%23{clanTag}',headers = headers,params = params)
    content = json.loads(r.content)
    for x in content['membersList']:
        user = content['membersList'][x]
        tag = user['tag']
        name = user['name']
        score = user['score']
        if not tag in t:
            t[tag] = {}
            t[tag]['Name'] = name
            t[tag]['Score'] = int(score)
        else:
            t[tag]['Name'] = name
            t[tag]['Score'] += int(score)

    with open('Tournament.json','w') as f:
        json.dump(t,f,indent = 3)


tk = 'ODIzNDkzOTA1MTM4OTc0NzYw.YFhodg.iBQGcKqcMGybnTzs6bkWBfKMSog'
bot.run(tk)
    
