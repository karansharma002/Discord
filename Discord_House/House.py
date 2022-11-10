import discord
from discord.ext import commands
import random
import datetime
from dateutil import parser
import json
import datetime

bot = commands.Bot(command_prefix= '!', intents = discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    print('====== BOT HAS STARTED ======')
    await bot.wait_until_ready()

@bot.command()
async def mine(ctx):
    author = str(ctx.author.id)

    with open('Data.json') as f:
        data = json.load(f)

    if not author in data:
        await ctx.send('<:info_1:970931983624577055> You have not set your Computers. Use: `!setup`')
        return

    else:
        if data[author]['Computers']['Computer1'] == {}:
            import datetime
            embed = discord.Embed(title = '!status to check the status of MINING.', color = discord.Color.greyple())
            embed.add_field(name = f":computer: {data[author]['Computers']['Total']} Computers", value = f":green_circle: Mining Started At {data[author]['Specs']['Speed']} GHZ Speed", inline = False)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

            data[author]['Computers']['Computer1']['Status'] = 'Online'
            data[author]['Computers']['Computer1']['Started'] = str(datetime.datetime.now())
            data[author]['Computers']['Computer1']['Mined'] = 0
            with open('Data.json', 'w') as f:
                json.dump(data, f, indent = 3)
        
        else:
            import datetime
            started_at = data[author]['Computers']['Computer1']['Started']
            t1 = parser.parse(str(started_at))
            t2 = parser.parse(str(datetime.datetime.now()))
            t3 = t2 - t1
            t3 = round(t3.total_seconds() / 3600)
            if t3 >= data[author]['Specs']['Time']:
                import datetime
                embed = discord.Embed(title = '!status to check the status of MINING.', color = discord.Color.greyple())
                embed.add_field(name = ':computer: Computer 1', value = f":green_circle: Mining Started At {data[author]['Specs']['Speed']} GHZ Speed", inline = False)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed = embed)

                data[author]['Computers']['Computer1']['Status'] = 'Online'
                data[author]['Computers']['Computer1']['Started'] = str(datetime.datetime.now())
            
                with open('Data.json', 'w') as f:
                    json.dump(data,f,indent = 3)
    
            else:
                await ctx.send('<:info_1:970931983624577055> Already Mining. Use: `!status` for more information.')
                return

@bot.command()
async def status(ctx):
    author = str(ctx.author.id)

    with open('Data.json') as f:
        data = json.load(f)

    if not author in data:
        await ctx.send('<:info_1:970931983624577055> You have not set your Computers. Use: `!setup`')
        return
    
    if data[author]['Computers']['Computer1'] == {}:
        await ctx.send('<:info_1:970931983624577055> The Computers are Offline. Use: `!mine` to Start Them.')
        return
    
    else:
        import datetime
        started_at = data[author]['Computers']['Computer1']['Started']
        t1 = parser.parse(str(started_at))
        t2 = parser.parse(str(datetime.datetime.now()))
        t3 = t2 - t1
        t4 = round(t3.total_seconds())
        t3 = round(t3.total_seconds() / 3600)
        if t3 >= data[author]['Specs']['Time']:
            speed = data[author]['Specs']['Speed']
            embed = discord.Embed(title = 'Mining Information',description = f"*The total time has exceeded and Computers Turned OFF Automatically.", color = discord.Color.red())
            embed.add_field(name = 'Tokens Mined', value = speed * t4, inline = False)
            await ctx.send(embed = embed)
            if not data[author]['Computers']['Computer1']['Status'] == 'Offline':
                data[author]['Computers']['Computer1']['Status'] = 'Offline'
                data[author]['Tokens'] += round(speed * t3 * data[author]['Computers']['Total'])
                with open('Data.json', 'w') as f:
                    json.dump(data,f,indent = 3)

        else:
            speed = data[author]['Specs']['Speed']
            embed = discord.Embed(title = 'Mining Information', color = discord.Color.green())
            embed.add_field(name = 'Computers Online', value = f"{data[author]['Computers']['Total']} :computer:", inline = False)
            embed.add_field(name = 'Tokens Mined', value = round(speed * t3) * data[author]['Computers']['Total'], inline = False)
            if t4 <= 0:
                embed.add_field(name = 'Time Elapsed', value = f"{t4} Seconds", inline =  False)
            
            else:
                t4 = round(t4 / 60)
                embed.add_field(name = 'Time Elapsed', value = f"{t4} Minutes", inline =  False)

            embed.add_field(name = 'Time Remaining', value = f"{data[author]['Specs']['Time'] * 60 - t4} Minutes", inline = False)
            await ctx.send(embed = embed)


@bot.command()
async def setup(ctx):
    author = str(ctx.author.id)

    with open('Data.json') as f:
        data = json.load(f)
    
    if not author in data:
        data[author] = {}
        data[author]['Tokens'] = 0
        data[author]['Coins'] = 0
        data[author]['Computers'] = {}
        data[author]['Computers']['Computer1'] = {}
        data[author]['Computers']['Total'] = 1
        data[author]['Computers']['Slots'] = 1
        data[author]['Specs'] = {}
        data[author]['Specs']['Time'] = 2
        data[author]['Specs']['Speed'] = 0.2

        with open('Data.json', 'w') as f:
            json.dump(data,f,indent = 3)
        
        await ctx.send(f'*{ctx.author.mention}, You have started your Journey at your Parents House. You Have a :computer: Computer to Use. Use: `!mine` to go further.*')
    
    else:
        await ctx.send(':warning: The computers are already online.')

@bot.command()
async def leaderboard(ctx):
    
    with open('Data.json','r') as f:
        users = json.load(f)

    high_score_list1 = sorted(users, key=lambda x : users[x].get('Tokens', 0), reverse=True)
    msg1 = ''
    for number,user in enumerate(high_score_list1):
        author = await bot.fetch_user(int(user))
        number += 1
        level = users[user]['Tokens']
        msg1 += f"**‣ {number}**. {author} ⁃ **Tokens:** __{level}__\n"
        if number == 15:
            break
        else:
            number += 1

    if msg1 == '':
        msg1 = 'None'

    embed = discord.Embed(
        title= ":money_with_wings: Global Leaderboard ",
        color= 0x05ffda,
        description= msg1
        )
            
    await ctx.send(embed = embed)

@commands.has_permissions(administrator = True)
@bot.command()
async def reset(ctx, confirm:str = None):
    if not confirm:
        await ctx.send(':warning: **THIS WILL RESET THE CURRENT SEASON, TO CONFIRM Type:** `!reset confirm`')
        return
    
    elif confirm.lower() == 'confirm':
        with open('Data.json') as f:
            data = json.load(f)
        
        data = {}

        with open('data.json', 'w') as f:
            json.dump(data, f, indent = 3)
        
        await ctx.send('<:info_1:970931983624577055> Season Reset Successfull')
    
    else:
        await ctx.send('-------- INVALID ARGUMENT ---------')
        return


@bot.command()
async def upgrade(ctx, number:int = None):
    author = str(ctx.author.id)

    with open('Data.json') as f:
        data = json.load(f)

    if not author in data:
        await ctx.send('<:info_1:970931983624577055> Nothing to Upgrade. You have not set your Computers. Use: `!setup`')
        return

    if not number:
        embed = discord.Embed(title = 'Upgrading Portal', color = discord.Color.dark_green())
        embed.add_field(name = ':one: + 0.1 GHZ CPU Speed', value = '300 Tokens', inline = False)
        embed.add_field(name = ':two: + 1 Computer', value = '610 Tokens', inline = False)
        embed.add_field(name = ':three: + 1 Hour Timer', value = '290 Tokens', inline = False)
        embed.add_field(name = ':four: Venue (+2 Computer Solots)', value = '700 Coins', inline = False)
        embed.set_footer(text = 'To Buy: Use: !upgrade <CHOICE NUMBER>')
        await ctx.send(embed  = embed)
    
    else:
        if number <= 0 or number > 4:
            await ctx.send(':warning: Invalid Choice Number.')
            return
        
        if number == 1:
            if data[author]['Tokens'] < 300:
                await ctx.send(':warning: Insufficient number of Tokens to Upgrade.')
                return
            
            data[author]['Tokens'] -= 300
            data[author]['Specs']['Speed'] += 0.1
            with open('Data.json', 'w') as f:
                json.dump(data,f,indent =  3)
            
            msg = f"<:info_1:970931983624577055> *Added + 0.1 GHZ CPU Speed for 300 Tokens*"
            embed = discord.Embed(title = 'Upgrade Successfull',description = msg, color = discord.Color.green())
            await ctx.send(embed = embed)
        
        elif number == 2:
            if data[author]['Tokens'] < 610:
                await ctx.send(':warning: Insufficient number of Tokens to Upgrade.')
                return

            if data[author]['Computers']['Total'] + 1 > data[author]['Computers']['Slots']:
                await ctx.send(':warning: You dont have enough :wastebasket: Storage to Place a new Computer.')
                return
            
    
            data[author]['Tokens'] -= 610
            data[author]['Computers']['Total'] += 1
            with open('Data.json', 'w') as f:
                json.dump(data,f,indent =  3)
            
            msg = f"<:info_1:970931983624577055> *Placed 1 :computer: Computer for 300 Tokens*"
            embed = discord.Embed(title = 'Upgrade Successfull',description = msg, color = discord.Color.green())
            await ctx.send(embed = embed)
            

        elif number == 3:
            if data[author]['Tokens'] < 290:
                await ctx.send(':warning: Insufficient number of Tokens to Upgrade.')
                return
            
            data[author]['Tokens'] -= 290
            data[author]['Specs']['Time'] += 1
            with open('Data.json', 'w') as f:
                json.dump(data,f,indent =  3)
            
            msg = f"<:info_1:970931983624577055> *Added + 1 Hour Timer for 290 Tokens*"
            embed = discord.Embed(title = 'Upgrade Successfull',description = msg, color = discord.Color.green())
            await ctx.send(embed = embed)
        
        elif number == 4:
            await ctx.send(':warning: Insufficient number of Coins to upgrade.')
            return

@bot.command()
async def help(ctx):
    embed=discord.Embed(color = discord.Color.blue())
    embed.set_author(name=f"{bot.user.name} | Commands Help", icon_url = ctx.author.avatar_url)
    embed.add_field(name="!setup", value="Setup your Computers in the Room.", inline=False)
    embed.add_field(name="!mine", value="Start Mining with your Computers.", inline=False)
    embed.add_field(name="!status", value="Check the status Mining Status.", inline=False)
    embed.add_field(name="!upgrade", value="Upgrade the Stats", inline=False)
    embed.add_field(name="!leaderboard ", value="View the Top Tokens Holder", inline=False)
    await ctx.send(embed=embed)

bot.run('ODQyNDU1NzY1MDExNjYwODAx.YJ1kEg.Q_T_nDZjrcIx3XokG8ueX-wIZ2U')