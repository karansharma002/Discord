import discord
from discord import channel
from discord.ext.commands.core import check
import psutil
import json
from dateutil import parser
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
from datetime import timedelta
from asyncio import sleep

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = '.',case_insensitive=True,intents = intents)
bot.remove_command('help')


# On Ready Event
@bot.event
async def on_ready():
    print('Server --- Started ')
    check_payments.start()


# Payments Check Task/ Main Event
@tasks.loop(hours = 2)
async def check_payments():
    await bot.wait_until_ready()
    with open('Config/Users.json') as f:
        users = json.load(f)
    
    with open('Config/settings.json') as f:
        settings = json.load(f)
    

    #! Intialize the GUILD ID
    guild = bot.get_guild(637754403063070721)
    channel = bot.get_channel(settings['Channel'])

    # Intialiaze Driver
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-infobars')
    driver = webdriver.Chrome(options=options)
    
    # GET LOGIN URL AND LOGIN THERE
    driver.get('https://cdwtraders.com/wp-login.php')
    Username = driver.find_element_by_xpath('//*[@id="user_login"]')
    Username.click()
    Username.send_keys('Discord Bot Authenticator')
    Password = driver.find_element_by_xpath('//*[@id="user_pass"]')
    Password.send_keys('wK9Nf5&0Eg8yRx5He442V0gu')
    Login = driver.find_element_by_xpath('//*[@id="wp-submit"]')
    Login.click()
    await sleep(3)
    mem = {}
    # Get the PLUGIN ORDERS
    driver.get('https://cdwtraders.com/wp-admin/admin.php?page=ihc_manage&tab=users&ihc_limit=500')
    await sleep(1)
    response = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(response,'html.parser')
    app = soup.find_all('div',class_ = 'iump-rsp-table')
    try:
        for x in app:
            for y in x.find_all('tr'):
                for num,z in enumerate(y.find_all('td')):
                    if num == 0:
                        mem['1'] = {}
                        name = "".join(z.text.split())
                        name = name.replace('EditDelete','')
                        mem['1']['Name1'] = name
                    
                    if num == 1:
                        mem['1']['Name2'] = "".join(z.text.split())

                    if num == 3:                
                        a = "".join(z.text.split())
                        if 'ExpiredMembershipLevel1' in a:
                            for members in guild.members:
                                if not members.nick == None:
                                    nick = "".join(members.nick.split()) 
                                else:
                                    nick = 'None'
                                    
                                nm = "".join(members.name.split())
                                name = mem['1']['Name2']
                                if name in users:
                                    #! Basically need to check if 2 days are over?
                                    t3 = parser.parse(str(users[name]))
                                    t4 = parser.parse(str(datetime.datetime.now()))
                                    c = t3 - t4
                                    days = round(c.total_seconds() / 86400)

                                    if days <= 0:
                                        if mem['1']['Name1'] == nick or mem['1']['Name2'] == nick or mem['1']['Name2'] == nm or mem['1']['Name1'] == nm:
                                            embed=discord.Embed(color=0xff2e2e)
                                            embed.set_author(name=f"{name} has been removed from the group chat.", icon_url=members.avatar_url)
                                            embed.add_field(name=":notepad_spiral: Reason:", value="Membership Expired / Payment Not received.", inline=False)
                                            await channel.send(embed=embed)
                                            await members.kick(reason = 'Payment Not done within 2 days of the Notice!!')
                                            users.pop(mem['1']['Name2'])
                                            with open('Config/Users.json','w') as f:
                                                json.dump(users,f,indent = 3)
                                    else:
                                        continue

                                else:
                                    if mem['1']['Name1'] == nick or mem['1']['Name2'] == nick or mem['1']['Name2'] == nm or mem['1']['Name1'] == nm:
                                        embed=discord.Embed(description=f"Your payment is pending,\nPlease pay it within 2 days to avoid removal from the group chat.",color=0xff2e2e)
                                        embed.set_author(name=f"{mem['1']['Name1']} | Important Notification ", icon_url=members.avatar_url)
                                        await members.send(embed = embed)

                                        embed=discord.Embed(description=f"{mem['1']['Name1']} have a pending payment,\nThey have been given a Notice of 2 Days.",color=0xff2e2e)
                                        embed.set_author(name=f"{mem['1']['Name1']} | Notification Sent ", icon_url=members.avatar_url)
                                        await channel.send(embed = embed)
                                        users[mem['1']['Name2']] = str(datetime.datetime.now() + timedelta(days = 2))
                                        with open('Config/Users.json','w') as f:
                                            json.dump(users,f,indent = 3)      
                                

        # Close the Driver Window when finished
        driver.close()
    
    except exception as e:
        print(e)
        driver.close()
        pass
    

# Help Function
@bot.command()
async def help(ctx):
    embed=discord.Embed(color=0x875cff)
    embed.set_author(name="Commands Help")
    embed.add_field(name="setchannel", value="Change the channel of events.", inline=False)
    embed.add_field(name="stats", value="Check System Information", inline=False)
    await ctx.send(embed=embed)

# Stats Function
@bot.command()
async def stats(ctx):
    ram = f"{psutil.virtual_memory()[2]}%"
    cpu = f"{psutil.cpu_percent()}%"
    embed=discord.Embed(
        color=0x0ee2f1,
        description = f"`Version   :` 1.2\n\
            `System    :` Red Hat 7.3.1-6\n\
                `Ram Usage :` {ram}\n\
                    `CPU Usage :` {cpu}")

    embed.set_author(name="CDW Mod | System Info",icon_url='https://cdwtraders.com/wp-content/uploads/2019/12/2-logo-reglar-CDW.png"')
    await ctx.send(embed = embed)

# Channel Set Function
@has_permissions(administrator = True)   
@bot.command()
async def setchannel(ctx,channel:discord.TextChannel = None):
    if channel == None:
        await ctx.send(":information_source:  Command Usage: setchannel `#channel`")
        return

    else:
        with open('Config/settings.json') as f:
            settings = json.load(f)
        
        settings['Channel'] = channel.id
        with open('Config/settings.json','w') as f:
            json.dump(settings,f,indent = 3)

        await ctx.send(f':white_check_mark: Channel has been Changed to: {channel.mention}')

        
token = 'ODA4NTQ0NzY2MDgwOTc0ODQ4.YCIF_g.0vwdpJQXJRDmy-Z47q0EC0D2V1g'

bot.run(token)