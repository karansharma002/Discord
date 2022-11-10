import discord
from discord.ext import commands,tasks
import json
from datetime import date,datetime,timedelta
from pytz import timezone
from dateutil import parser


bot = commands.Bot(command_prefix = '=',intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('------ POINTS CALC BOT IS RUNNING -------')
    await bot.wait_until_ready()
    gen_report.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    user = str(message.author.id)
    message_time = str(datetime.now())

    with open('DB.json') as f:
        db = json.load(f)

    
    if not user in db:
        db[user] = {}
        db[user]['Text_Seconds'] = 0
        db[user]['Voice_Minutes'] = 0 
        with open('DB.json','w') as f:
            json.dump(db,f,indent = 3)

    db[user]['Text_Seconds'] += 1
    with open('DB.json','w') as f:
        json.dump(db,f,indent = 3)  

cache = {}

@bot.event
async def on_voice_state_update(member, before, after):
    global cache

    user = str(member.id)

    voice_time = str(datetime.now())
    with open('DB.json') as f:
        db = json.load(f)
    
    
    if not user in db:
        db[user] = {}
        db[user]['Text_Seconds'] = 0
        db[user]['Voice_Minutes'] = 0 
        with open('DB.json','w') as f:
            json.dump(db,f,indent = 3)

    if not before.channel:
        cache[user] = voice_time

    elif not after.channel:
        if not user in cache:
            return

        t1 = parser.parse(voice_time)
        t2 = parser.parse(cache[user])
        t3 = t1 - t2
        t3 = round(t3.total_seconds())
        db[user]['Voice_Minutes'] += t3
        with open('DB.json','w') as f:
            json.dump(db,f,indent = 3)
        
        cache.pop(user)

@commands.has_permissions(administrator = True)
@bot.command()
async def setchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Usage: !setchannel `<#CHANNEL WHERE REPORTS ARE SENT>`')
        return
    
    with open('CNF.json') as f:
        db = json.load(f)

    db['Channel'] = channel.id
    
    with open('CNF.json','w') as f:
        json.dump(db,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel Added!')

@tasks.loop(seconds = 40)
async def gen_report():
    fmt = "%H:%M"
    now_time = datetime.now(timezone('Europe/London'))
    nw = now_time.strftime(fmt)
    if str(nw) == '23:59':
        with open('DB.json') as f:
            db = json.load(f)

        with open('CNF.json') as f:
            settings = json.load(f)
        
        if not 'Roles' in settings:
            return
        
        if not 'Channel' in settings:
            return
        
        channel = await bot.fetch_channel(settings['Channel'])
        house = {}
        for user in list(db):
            for x in settings['Roles']:
                role = discord.utils.get(channel.guild.roles,id = x)
                member = channel.guild.get_member(int(user))
                if role in member.roles:
                    if not str(role.name) in house:
                        house[str(role.name)] = ''

                    house[str(role.name)] += f"• {member.mention} | **Voice Time:** __{round(db[user]['Voice_Minutes'] / 60)}__ M | **Chat Time:** __{round(db[user]['Text_Seconds'] / 60)}__ M\n"
                    db.pop(user)
                    with open('DB.json','w') as f:
                        json.dump(db,f,indent = 3)


        for x in house:
            embed = discord.Embed(color = discord.Color.dark_gold(),description = house[x])
            embed.set_author(name = f"{x} | Report",icon_url= bot.user.avatar_url)
            await channel.send(embed = embed)

@commands.has_permissions(administrator = True)
@bot.command()
async def setrole(ctx,role:discord.Role = None):
    with open('CNF.json') as f:
        db = json.load(f)
    
    if not 'Roles' in db:
        db['Roles'] = []
    
    if not role.id in db['Roles']:
        db['Roles'].append(role.id)
        with open('CNF.json','w') as f:
            json.dump(db,f,indent = 3)
        
        await ctx.send(':white_check_mark: Role Added!')

    else:
        await ctx.send(':warning: This role already exists')

@commands.has_permissions(administrator = True)
@bot.command()
async def removerole(ctx,role:discord.Role = None):
    with open('CNF.json') as f:
        db = json.load(f)
    
    if not 'Roles' in db:
        db['Roles'] = []
    
    if  role.id in db['Roles']:
        db['Roles'].remove(role.id)
        with open('CNF.json','w') as f:
            json.dump(db,f,indent = 3)
        
        await ctx.send(':white_check_mark: Role Removed!')

    else:
        await ctx.send(':warning: Role not Found!!')

@commands.has_permissions(administrator = True)
@bot.command()
async def listroles(ctx,role:discord.Role = None):
    msg = ''
    with open('CNF.json') as f:
        db = json.load(f)
    
    if not 'Roles' in db:
        db['Roles'] = []
    
    for num,x in enumerate(db['Roles']):
        role = discord.utils.get(ctx.guild.roles,id = int(x))
        msg += f"{num +1}: {role.name}\n"
    
    if not msg == '':
        embed = discord.Embed(title = 'Roles List',color = discord.Color.orange(),description = msg)
        await ctx.send(embed = embed)
    else:
        await ctx.send('No roles Found!!')

@bot.command()
async def points(ctx):
    with open('DB.json') as f:
        db = json.load(f)

    with open('CNF.json') as f:
        settings = json.load(f)
    
    if not 'Roles' in settings:
        return
    
    house = {}
    for user in list(db):
        for x in settings['Roles']:
            role = discord.utils.get(ctx.guild.roles,id = x)
            member = ctx.guild.get_member(int(user))
            if role in member.roles:
                if not str(role.name) in house:
                    house[str(role.name)] = ''

                house[str(role.name)] += f"• {member.mention} | **Voice Time:** __{round(db[user]['Voice_Minutes'] / 60)}__ M | **Chat Time:** __{round(db[user]['Text_Seconds'] / 60)}__ M\n"

    for x in house:
        embed = discord.Embed(color = discord.Color.dark_gold(),description = house[x])
        embed.set_author(name = f"{x} | Report",icon_url= bot.user.avatar_url)
        await ctx.send(embed = embed)

bot.run('ODc3ODcxNjA5OTc1ODI0NDI1.YR47pQ.c1APTQJv8907KjVWRcOqnMVAGm0')