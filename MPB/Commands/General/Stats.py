
import discord
from discord.ext import commands,tasks
import json
import psutil

seconds = 0
minutes = 0
hours = 0
days = 0

@tasks.loop(seconds = 1)
async def uptime_calc():
    global seconds
    global minutes
    global hours
    global days

    if not seconds > 59:
        seconds += 1
    
    else:
        if not minutes > 59:
            seconds = 0
            minutes += 1
        elif not hours > 23:
            hours += 1
            seconds = 0
            minutes = 0
        else:
            hours = 0
            days += 1
        
    return days,hours,minutes,seconds 

uptime_calc.start()

class stats(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def stats(self,ctx):
        global days,hours,minutes,seconds
        ram = f"{psutil.virtual_memory()[2]}%"
        cpu = f"{psutil.cpu_percent()}%"
        if days == 0 and hours == 0:
            uptime = f'{minutes} Minutes {seconds} Seconds'
        elif days == 0 and not hours == 0:
            uptime = f'{hours} Hours {minutes} Minutes {seconds} Seconds'
        else:
            uptime = f'{days} Days {hours} Hours {minutes} Minutes {seconds} Seconds'
        embed=discord.Embed(color=0x0ee2f1)
        embed.add_field(name = ':alarm_clock: UPTIME', value = f'```\n{uptime}```',inline= False)
        embed.add_field(name = ':earth_americas: PING', value = f'```\n{round(self.bot.latency * 1000)} ms```',inline =False)


        #embed.set_author(name="Casino Queen",icon_url='https://i.imgur.com/izp9xAI.jpgg')
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(stats(bot))


