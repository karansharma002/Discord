

# Loading Modules
import enum
from logging import exception
from attr import has
import discord
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions
from discord.ext.commands.core import command
from datetime import datetime
from dateutil import parser
import json

#GLOBAL DATA DICTIONARY
data = {}

# Intialize bot Instance
bot = commands.Bot(command_prefix = '!',intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('-------- SERVER STARTED -------')
    
    # Start our Main Loop
    await user_check.start()

# Main loop for checking Activities
@tasks.loop(seconds = 20)
async def user_check():
    try:
            
        await bot.wait_until_ready()
        with open('Settings.json') as f:
            settings = json.load(f)
        
        s = sorted(settings, key=settings.get, reverse=True)
        global data
        for x in data:
            # MAIN STATEMENT TO CHECK IF USER HAS PASSED CERTAIN CONDITIONS
            if 'Join_Time' in data[x]:
                for num,y in enumerate(s):
                    t1 = parser.parse(str(data[x]['Join_Time']))
                    t2 = parser.parse(str(datetime.now()))
                    final = t2 - t1
                    final = round(final.seconds / 60)
                    if final >= int(y):
                        channel = await bot.fetch_channel(data[x]['Channel'])
                        user = channel.guild.get_member(int(x))
                        role = discord.utils.get(channel.guild.roles,name = settings[y])
                        if role in user.roles:
                            break
                        else:
                            await user.add_roles(role)
                            role_list = list(s)

                        try:
                            if (num+1) > (len(role_list) - 1):
                                break

                            role = discord.utils.get(channel.guild.roles,name = settings[role_list[num+1]])
                            await user.remove_roles(role)
                            break
                        
                        except Exception:
                            import traceback
                            print(traceback.format_exc())
                            break
            
            elif 'Left_Time' in data:
                # Check if user is inactive for more than 14 days?
                t1 = parser.parse(str(data[x]['Left_Time']))
                t2 = parser.parse(str(datetime.now()))
                left_time = t2 - t1
                left_time = round(left_time.seconds / 86400)
                user = channel.guild.get_member(int(x))
                if left_time >= 14:
                    for role in user.roles:
                        try:
                            await user.remove_roles(role)
                        except Exception:
                            pass
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())

@bot.event
async def on_voice_state_update(member, before, after):
    global data
    member = str(member.id)
    
    if not before.channel:
        data[str(member)] = {}
        data[str(member)]['Channel'] = after.channel.id
        data[str(member)]['Join_Time'] = str(datetime.now())

    elif not after.channel:
        data.pop(member)
        data[member] = {}
        data[member]['Channel'] = before.channel.id
        data[member]['Left_Time'] = str(datetime.now())

    else:
        # LEFT + JOINED
        pass
    

@bot.command()
async def setup(ctx,num:int = None):
    def check(m):
        return m.author == ctx.author

    if not num:
        await ctx.send(':information_source: Command Usage: !setup `Total Roles (EX 3)`')
        return
    
    with open('Settings.json') as f:
        s = json.load(f)
    
    s = {}
    iterate = 0
    while iterate < num:
        await ctx.send(f'Enter the Role Name: #{iterate+1}')
        role_name = await bot.wait_for('message',check = check)
        role_name = str(role_name.content)
        await ctx.send('Enter the Time in Minutes: ')
        tm = await bot.wait_for('message',check = check)
        tm = str(tm.content)
        iterate += 1
        s[tm] = role_name
    
    with open('Settings.json','w') as f:
        json.dump(s,f,indent = 3)
    
    await ctx.send(':white_check_mark: Sucessfully Saved')

with open('Token.json') as f:
    token = json.load(f)



bot.run(token['Token'])


 

