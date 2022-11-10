from logging import exception
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
from github import Github
from github.GithubException import GithubException
import random
import os

bot = commands.Bot(command_prefix = '$')


with open('Config/Tokens.json') as f:
    t = json.load(f)

GTOKEN = t['Github API Key']
DTOKEN = t['Discord API Token']
g = Github(GTOKEN)
try:

    for repo in g.get_user().get_repos():
        a = repo.get_commits().totalCount
        print(a)
except GithubException:
    pass

@bot.event
async def on_ready():
    print('----------- READY ----------')

@bot.event
async def on_message(m):
    global GTOKEN
    with open('Config/Settings.json') as f:
        s = json.load(f)
    
    if 'bot up' in str(m.content).lower():
        if 'Insult' in s:
            if s['Insult'] == 'ON':
                words2 = ['Jerome, You are as useless as the "ueue" in "Queue"',
                'Mirrors cannot talk. Lucky for you Jerome, they cannot laugh either.',
                'If I had a face like yours Jerome, I would sue my parents.',
                'You must have been born on a highway Jerome because that is where the most accidents happen.',
                'If laughter is the medicine, you face must be curing the world Jerome.',
                'I am glad to see you are not letting your education get in the way of your ignorance Jerome.',
                'Is your ass jealous of the amount of shit that just came out of your mouth Jerome?',
                'So, a thought just crossed your mind? Must have been a long and lonely journey Jerome.',
                'I would agree with you Jerome but then we would both be wrong.',
                'When I see your face Jerome then there is not a thing I would change... Except the direction I was walking in.'
                ]

                a = random.choice(words2)
                await m.channel.send(a.replace('Jerome',m.author.mention))
    
  
    if str(m.channel.id) in s:
        if not str(m.attachments) == "[]":
            split_v1 = str(m.attachments).split("filename='")[1]
            filename = str(split_v1).split("' ")[0]
            if filename.endswith(".iss") or filename.endswith('.aa') or filename.endswith('.xml') or filename.endswith('zip'):
                # Check the formats
                await m.attachments[0].save(fp=filename)
            
            #UPLOADING TO GITHUB
            g = Github(GTOKEN) 
            repo = g.get_user().get_repo(s['Repo'])
            all_files = []
            try:

                contents = repo.get_contents("")
                while contents:
                    file_content = contents.pop(0)
                    if file_content.type == "dir":
                        contents.extend(repo.get_contents(file_content.path))
                    else:
                        file = file_content
                        all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

            except:
                all_files = []

            # Upload to github
            git_file = filename
            with open('Config/Logs.json') as f:
                l = json.load(f)

            if git_file in all_files:

                contents = repo.get_contents(git_file)
                repo.update_file(contents.path, "committing files", filename, contents.sha, branch="master")
                msg = await m.channel.send('✅ Files Updated')
            
                if l == {}:
                    l['Num'] = 1
                    l['Upload1'] = {}
                    l['Upload1']['File'] = filename
                    l['Upload1']['Repo'] = s['Repo']
                
                else:
                    num = l['Num']
                    num = num+1
                    if num == 6:
                        num = 1
                    else:
                        num = num
                    
                    num = str(num)
                    if not f'Upload{num}' in l:
                        l[f"Upload{num}"] = {}

                    l[f'Upload{num}']['File'] = filename
                    l[f'Upload{num}']['Repo'] = s['Repo']
                    l['Num'] = int(num)
                
                with open('Config/Logs.json','w') as f:
                    json.dump(l,f,indent = 3)

            else:
                repo.create_file(git_file, "committing files", filename, branch="master")
                msg = await m.channel.send('✅ Files Uploaded')

                if l == {}:
                    l['Num'] = 1
                    l['Upload1'] = {}
                    l['Upload1']['File'] = filename
                    l['Upload1']['Repo'] = s['Repo']
                
                else:
                    num = l['Num']
                    num = num+1
                    if num == 6:
                        num = 1
                    else:
                        num = num

                    num = str(num)
                    if not 'Upload'+num in l:
                        l[f"Upload{num}"] = {}

                    l[f'Upload{num}']['File'] = filename
                    l[f'Upload{num}']['Repo'] = s['Repo']
                    l['Num'] = int(num)
                
                with open('Config/Logs.json','w') as f:
                    json.dump(l,f,indent = 3)
                
            os.remove(filename)
                
    await bot.process_commands(m)

@bot.command()
async def toggle(ctx):
    with open('Config/Settings.json') as f:
        s = json.load(f)
    
    if not 'Insult' in s:
        s['Insult'] = 'ON'
        status = 'Enabled'
    else:
        if s['Insult'] == 'ON':
            s['Insult'] = 'OFF'
            status = 'Disabled'
        else:
            s['Insult'] = 'ON'
            status = 'Enabled'
        
    with open('Config/Settings.json','w') as f:
        json.dump(s,f,indent =3)

    await ctx.send(f':white_check_mark: Insult Feature has been: `{status}`')

@bot.command()
async def setchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Command Usage: $setchannel `#channel`')
        return

    with open('Config/Settings.json') as f:
        s = json.load(f)
    
    s[str(channel.id)] = 'Verified'
    
    with open('Config/Settings.json','w') as f:
        json.dump(s,f,indent = 3)

    await ctx.send(f':white_check_mark: Channel Changed Successfully!')

@bot.command()
async def createrepo(ctx,*,rp:str = None):
    global GTOKEN
    if not rp:
        await ctx.send(':information_source: Command Usage: $createrepo `Repo Name`')
        return

    g = Github(GTOKEN) 
    u = g.get_user()
    try:
        repo = u.create_repo(rp)
        await ctx.send(':white_check_mark: New Repo has been created.')
        return
    
    except:
        await ctx.send(':warning: Repo Already Exists with the Name.')

@bot.command()
async def setrepo(ctx,*,rp:str = None):
    global GTOKEN
    if not rp:
        await ctx.send(':information_source: Command Usage: $setrepo `Repo Name`')
        return
    else:
        with open('Config/Settings.json','r') as f:
            s = json.load(f)

        g = Github(GTOKEN)  # safer alternative, if you have an access token
        try:
            a = g.get_user().get_repo(rp)
            s['Repo'] = rp
            with open('Config/Settings.json','w') as f:
                json.dump(s,f,indent = 3)
            
            await ctx.send(f':white_check_mark: `{rp}` has been selected as Default Repo.')
            return
        
        except:
            await ctx.send(':warning: Repo not found. Please create one via: `createrepo`')
            return

@bot.command()
async def searchfiles(ctx,filename:str = None,*,repos:str = None):
    if not filename or not repos:
        await ctx.send(':information_source: Command Usage: $search `<filename>` `<REPO Name>`')
        return
    else:
        try:
            g = Github(GTOKEN) 
            repo = g.get_user().get_repo(repos)
            name = g.get_user()
            name = name.login
            contents = repo.get_contents("")
            all_files = []
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    file = file_content
                    all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))
            
            if not filename in all_files:
                await ctx.send('File not found in the Repository')
                return
            else:
                await ctx.send(f'https://raw.githubusercontent.com/{name}/{repos}/master/{filename}')
                return

        except:
            await ctx.send(':warning: Repository Not Found!')

@bot.command()
async def searchrepo(ctx,*,rep:str = None):
    if not rep:
        await ctx.send(':information_source: Command Usage: $searchrepo `<REPO Name>`')
        return
    else:
        try:
            g = Github(GTOKEN) 
            repo = g.get_user().get_repo(rep)
            name = g.get_user()
            name = name.login
            await ctx.send(f'https://github.com/{name}/{rep}')
            return

        except:
            await ctx.send(':warning: Repository Not Found!')


@bot.command()
async def recentuploads(ctx):

    g = Github(GTOKEN) 
    name = g.get_user()
    name = name.login

    with open('Config/Logs.json') as f:
        l = json.load(f)
    
    rp = []
    for x in l:
        if not x == 'Num':
            rep = l[x]['Repo']
            if not rep in rp:
                rp.append(rep)
    
    msg = ''
    for num, z in enumerate(rp):
        num += 1
        msg += f"\n{num}: https://github.com/{name}/{z}\n"
    
    await ctx.send(f"```\n{msg}\n```")

@bot.command()
async def play(ctx,*,arg:str = None):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    channel = ctx.author.voice.channel
    if channel:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else: 
            voice = await channel.connect()

        if not voice.is_playing():
           voice.play(discord.FFmpegPCMAudio('http://stream.laut.fm/1000oldies',**FFMPEG_OPTIONS))

        
bot.run(DTOKEN)
