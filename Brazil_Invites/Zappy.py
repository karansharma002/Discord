import discord
from discord.ext import commands, tasks
import json
import asyncio

guild_id = 969506351426449458

bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

import pytz
print(pytz.all_timezones)
input()

inv = {}
last = ""

@bot.event
async def on_ready():
    print("ready!")
    await bot.wait_until_ready()
    update_time.start()

@tasks.loop(minutes = 1)
async def update_time():
    from datetime import datetime
    local_time = datetime.now()
    current_time = local_time.strftime("%I:%M %p")
    name = f"🕐 {current_time}"

    channel = await bot.fetch_channel(972335969267253278)
    await channel.edit(name = name)

    #channel = await bot.fetch_channel(969818405471387668)
    #await channel.edit(name = name)

async def fetch():
    global last
    global inv
    global guild_id
    await bot.wait_until_ready()
    while True:
        try:
            guild = await bot.fetch_guild(guild_id)
            invs = await guild.invites()
        except:
            await asyncio.sleep(2)
            continue

        tmp = []
        for i in invs:
            for s in inv:
                if s[0] == i.code:
                    if int(i.uses) > s[1]:
                        gld = str(guild.id)
                        print(int(last))

                        try:
                            usr = guild.get_member(int(last))
                            usr.name
                        except:
                            usr = await guild.fetch_member(int(last))
                        
                        author = str(i.inviter.id)

                        with open('Data.json') as f:
                            data = json.load(f)

                        
                        if not str(guild.id) in data:
                            data[str(guild.id)] = {}
                        
                        if not author in data[gld]:
                            data[str(guild.id)][author] = {}
                            data[gld][author]['Level'] = 0
                            data[gld][author]['Invites'] = 0
                            data[gld][author]["Users"] = []

                        else:
                            data[gld][author]['Level'] += 1
                            data[gld][author]['Invites'] += 1
                        
                        #if usr.id in data[gld][author]['Users']:
                        #    return
                        try:
                            if not discord.utils.get(guild.roles, name = f"{i.inviter} | grupo"):
                                role = await guild.create_role(name = f"{i.inviter} | grupo")
                            
                            role = await discord.utils.get(guild.roles, name = f"{i.inviter} | grupo")
                            
                            await usr.add_roles(role)
                        except:
                            pass

                        channels = {"968840912560082984":968840913042407435, "969506351426449458": 971108073458511913}
                        channel = await bot.fetch_channel(channels[gld])

                        embed = discord.Embed(color = discord.Color.green())
                        embed.set_author(name = f"{usr.name} has Joined.", icon_url = usr.avatar_url)
                        embed.add_field(name = 'Invited By', value = i.inviter.name, inline = False)
                        embed.add_field(name = f"{i.inviter.name} | Total Invites", value = i.uses, inline = False)
                        await channel.send(embed = embed)

                        roles = { "969506351426449458": [971991974808801321,969506351447416904,969506351447416905]}

                        #whitelists = {"968840912560082984": [969452972947955712, 969453064308260884, 969453166095663124]}

                        data[gld][author]["Users"].append(usr.id)
                        with open('Data.json', 'w') as f:
                            json.dump(data,f,indent = 3)

                        try:
                            usr = guild.get_member(int(i.inviter.id))
                            usr.name
                        except:
                            usr = await guild.fetch_member(int(i.inviter.id))


                        role = discord.utils.get(guild.roles, id = roles[gld][0])
                        if not role in usr.roles:
                            await usr.add_roles(role)

                        if i.uses <= 10 and i.uses >= 3:
                            role = discord.utils.get(guild.roles, id = roles[gld][1])
                            if not role in usr.roles:
                                await usr.add_roles(role)
                        
                        elif i.uses > 10:
                            role = discord.utils.get(guild.roles, id = roles[gld][2])
                            if not role in usr.roles:
                                await usr.add_roles(role)


                        if i.uses >= 3 and i.uses < 6:
                            level = f"Level: 1"
                            
                            if not discord.utils.get(guild.roles, name = level):
                                role = await guild.create_role(name = level)

                            else:
                                role = discord.utils.get(guild.roles, name = level)
                            
                            if not role in usr.roles:
                                await usr.add_roles(role)

                        elif i.uses >= 6 and i.uses < 9:
                            level = data[gld][author]['Level']
                            level = f"Level: 2"
                            
                            if not discord.utils.get(guild.roles, name = level):
                                role = await guild.create_role(name = level)

                            else:
                                role = discord.utils.get(guild.roles, name = level)
                            
                            if not role in usr.roles:
                                await usr.add_roles(role)

                            try:
                                role = discord.utils.get(guild.roles, name = f"Level: 1")
                                if role in usr.roles:
                                    await usr.remove_roles(role)
                            except:
                                pass

                        elif i.uses >= 9 and i.uses < 30:
                            level = data[gld][author]['Level']
                            level = f"Level: 3"
                            
                            if not discord.utils.get(guild.roles, name = level):
                                role = await guild.create_role(name = level)

                            else:
                                role = discord.utils.get(guild.roles, name = level)
                            
                            if not role in usr.roles:
                                await usr.add_roles(role)

                            try:
                                role = discord.utils.get(guild.roles, name = f"Level: 2")
                                if role in usr.roles:
                                    await usr.remove_roles(role)
                            except:
                                pass

                        elif i.uses >= 30:
                            level = data[gld][author]['Level']
                            level = f"Level: 4"
                            
                            if not discord.utils.get(guild.roles, name = level):
                                role = await guild.create_role(name = level)

                            else:
                                role = discord.utils.get(guild.roles, name = level)
                            
                            if not role in usr.roles:
                                await usr.add_roles(role)
                            
                            try:
                                role = discord.utils.get(guild.roles, name = f"Level: 3")
                                if role in usr.roles:
                                    await usr.remove_roles(role)
                            except:
                                pass

                        with open('Data.json', 'w') as f:
                            json.dump(data, f, indent = 3)

            tmp.append(tuple((i.code, i.uses)))

        inv = tmp
        await asyncio.sleep(2)

@bot.event
async def on_member_join(member):
    if not member.guild.id == 969506351426449458:
        return

    global last

    last = str(member.id)
    return 

@bot.command()
async def invites(ctx):
    with open('Data.json') as f:
        data = json.load(f)

    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == ctx.author:
            totalInvites += i.uses
            
    msg = f'You currently have **{totalInvites}** invites'
    embed = discord.Embed(color = discord.Color.dark_blue(), title = f"{ctx.author} | Invites", description = msg)
    await ctx.send(embed = embed)

@bot.command(aliases = ['top'])
async def leaderboard(ctx):
    with open('Data.json') as f:
        data = json.load(f)

    sorted_data = sorted(data, key = data.get, reverse = True)     
    msg = ''

    for num,x in enumerate(sorted_data):
        
        user = await bot.fetch_user(int(x))
        points = data[x]
        msg += "{}: {} - **{}** Invites".format(num + 1,user,points)

        if num == 20:
            break
        else:
            num += 1

    embed = discord.Embed(color = discord.Color.dark_blue(), title = 'TOP Inviters', description = msg)
    await ctx.send(embed = embed)

@bot.command()
async def stats(ctx):
    with open('Data.json') as f:
        data = json.load(f)
    
    author = str(ctx.author.id)

    if not author in data['968840912560082984']:
        await ctx.send(':warning: Insufficient Invites')
        return
    
    msg = ''

    for num, x in enumerate(data['968840912560082984'][author]['Users']):
        user = await bot.fetch_user(int(x))
        msg += f"{num + 1}: {user}\n"
    
    embed = discord.Embed(color = discord.Color.blue(), description = msg, title = f'{ctx.author} | grupo')
    await ctx.send(embed = embed)

@commands.has_permissions(administrator = True)
@bot.command()
async def export(ctx):    
    msg = ''

    for num, x in enumerate(['Level: 1', 'Level: 2', 'Level: 3', 'Level: 4']):
        role = discord.utils.get(ctx.guild.roles, name = x)
        msg = ''
        for member in role.members:
            msg += f"{num +1}: {member}\n"
        
        if msg == '':
            msg = 'None'
                
        if x == 'Level: 1':
            color = discord.Color.blue()
        
        elif x == 'Level: 2':
            color = discord.Color.purple()
        
        elif x == 'Level: 3':
            color = discord.Color.dark_purple()

        else:
            color = discord.Color.green()

        embed = discord.Embed(color = color, description = msg, title = f'{role.name} | MEMBERS')
        await ctx.send(embed = embed)

@bot.command()
async def reset(ctx,confirm:str = None):
    if not confirm:
        await ctx.send(':warning: The leaderboard will reset. Type: !reset confirm to reset the data.')
        return
    
    else:
        with open('Data.json') as f:
            data = json.load(f)
        
        data = {}
        with open('Data.json','w') as f:
            json.dump(data,f,indent = 3)
        
        await ctx.send(':white_check_mark: Leaderboard Reset!')

bot.loop.create_task(fetch())
bot.run("OTY5ODY0NzExMjcxMjUyMDA4.Ymzm5g.QCrz9YXui25dflCMMtxE3qZ-bOk")
                        
