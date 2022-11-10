from turtle import update
import discord
from discord.ext import commands, tasks
import json
import asyncio

gld = 0

bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

inv = {}
last = ""

@bot.event
async def on_ready():
    print("ready!")
    await bot.wait_until_ready()
    update_time.start()

@tasks.loop(minutes = 1)
async def update_time():
    import pytz
    from datetime import datetime
    timezone = pytz.timezone("Singapore")
    local_time = datetime.now(timezone)
    current_time = local_time.strftime("%I:%M %p")
    name = f"🕐 {current_time}"

    channel = await bot.fetch_channel(969816631175970846)
    await channel.edit(name = name)

    channel = await bot.fetch_channel(969818405471387668)
    await channel.edit(name = name)

async def fetch():
    global last
    global inv
    await bot.wait_until_ready()
    while True:
        guild = await bot.fetch_guild(gld)
        invs = await guild.invites()
        tmp = []
        for i in invs:
            for s in inv:
                if s[0] == i.code:
                    if int(i.uses) > s[1]:
                        gld = str(guild.id)
                        usr = guild.get_member(int(last))

                        channels = {"968840912560082984":969506351648755766, "969506351426449458": 968840913042407435}
                        channel = await bot.fetch_channel(channels[gld])

                        msg = f"{usr.name} **joined**; Invited by **{i.inviter.name}**, Now Has (**{str(i.uses)}** invites)"
                        embed = discord.Embed(color = discord.Color.green())
                        embed.set_author(name = f"{usr.name} has Joined.", avatar = usr.avatar_url)
                        embed.add_field(name = 'Invited By': i.inviter.name, inline = False)
                        embed.add_field(name = f"{i.inviter.name} | Total Invites", value = i.uses, inline = False)
                        await channel.send(embed = embed)
                        roles = {"968840912560082984": [968840912560082985,968847568970842173,968847466852143145], 
                        "969506351426449458": [969506351447416903,969506351447416904,969506351447416905]}

                        whitelists = {"968840912560082984": [969452972947955712, 969453064308260884, 969453166095663124]}

                        author = str(i.inviter.id)

                        with open('Data.json') as f:
                            data = json.load(f)

                        
                        if not str(guild.id) in data:
                            data[str(guild.id)] = {}
                        
                        if not author in data[gld]:
                            data[str(guild.id)][author] = {}
                            data[gld][author]['Level'] = 0
                            data[gld][author]['Invites'] = 0

                        data[gld][author]['Level'] += 1
                        data[gld][author]['Invites'] += 1

                        role = discord.utils.get(guild.roles, id = roles[gld][0])
                        await usr.add_roles(role)

                        if data[str(guild.id)][author] == 5:
                            role = discord.utils.get(guild.roles, id = roles[gld][1])
                            await usr.add_roles(role)
                        
                        elif data[str(guild.id)][author] > 5:
                            role = discord.utils.get(guild.roles, id = roles[gld][2])
                            await usr.add_roles(role)


                        with open('Data.json', 'w') as f:
                            json.dump(data,f,indent = 3)

                        level = data[author]['Level']
                        level = f"Level: {level}"
                        
                        if not discord.utils.get(guild.roles, name = level):
                            role = await guild.create_role(name = level)

                        else:
                            role = discord.utils.get(guild.roles, name = level)
                        
                        if not role in usr:
                            await usr.add_roles(role)

                        level = data[author]['Level'] - 1
                        level = f"Level: {level}"

                        with open('Data.json', 'w') as f:
                            json.dump(data, f, indent = 3)
                        
                        try:
                            role = discord.utils.get(guild.roles, name = level)
                            if role in usr.roles:
                                await usr.remove_roles(role)
                        except:
                            pass

                        try:
                            if level == 3:
                                role  = whitelists[gld][0]
                            
                            elif level == 20:
                                role = whitelists[gld][1]
                            
                            elif level == 30:
                                role = whitelists[gld][2]

                            role = discord.utils.get(guild.roles, id = role)
                            if role in usr.roles:
                                await usr.remove_roles(role)
                        except:
                            pass


            tmp.append(tuple((i.code, i.uses)))

        inv = tmp
        await asyncio.sleep(2)

@bot.event
async def on_member_join(member):
    global last
    global gld

    last = str(member.id)
    gld = int(member.guild.id)
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
    embed = discord.Embed(color = discord.Color.dark_blue(), title = ctx, description = msg)
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
                        
