from discord import Embed, TextChannel
from asyncio import sleep
from discord.ext import commands
import discord
import re
import random
import datetime
import requests
from datetime import timedelta

# GLOBAL DICT FOR STORING GIVEAWAY DETAILS
gw = {}

class giveaway(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    def convert(self,argument):
        time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d|w))+?")
        time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400,"w": 604800}
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(
                    f"{value} is an invalid time key! h|m|s|d are valid arguments"
                )
            except ValueError:
                raise commands.BadArgument(f"{key} is not a number!")
        return round(time)

    def sec_time(self, secs):
        days = secs//86400
        hours = (secs - days*86400)//3600
        minutes = (secs - days*86400 - hours*3600)//60
        seconds = secs - days*86400 - hours*3600 - minutes*60
        result = ("{0} day{1}, ".format(days, "s" if days!=1 else "") if days else "") + \
        ("{0} hour{1}, ".format(hours, "s" if hours!=1 else "") if hours else "") + \
        ("{0} minute{1}, ".format(minutes, "s" if minutes!=1 else "") if minutes else "") + \
        ("{0} second{1}".format(seconds, "s" if seconds!=1 else "") if seconds else "")
        return result
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        global gw
        guild = str(user.guild.id)
        try:
            if guild in gw:
                if reaction.emoji == '🎉' and reaction.message.id == gw[guild]['MSG ID']:
                    embed=discord.Embed(title = ':white_check_mark: Giveaway Entry Confirmed',\
                        description = f"Your entry for [this]({'https://discordapp.com/channels/{}/{}/{}'.format(user.guild.id,reaction.message.channel.id,reaction.message.id)}) has been confirmed.",color=0x2eff6d)
                    
                    await user.send(embed = embed)
        
        except Exception:
            pass


    @commands.guild_only()
    @commands.command(aliases = ['gstart'])
    @commands.has_permissions(administrator=True)
    async def giveaway(self,ctx,duration: str = None,limit:int = None,channel:str = None,*,prize = None):
        global gw
        if channel == None:
            guild = str(ctx.guild.id)
        else:
            channel = channel.replace("<","")
            channel = channel.replace(">","")
            channel = channel.replace("#","")
            channel = self.bot.get_channel(int(channel))
            guild = str(channel.guild.id)

        if duration == None:
            await ctx.send(':information_source: Usage: !giveaway `<duration (Example: 10S)>` `<Limit>` `<Channel>` `<Prize>`')
            return
        if limit <= 0 or limit > 3:
            await ctx.send('Winners Limit should be Between 1-3')
            return

        duration = re.sub(r"\s+", "", duration, flags=re.UNICODE)
        
        if guild in gw:
            await ctx.send(':exclamation: There is one Giveaway Active Already, End that first. `!gstop`')
            return
        else:
            gw[guild] = {}

        embed = Embed(title=prize,
                    description=f"**React with :tada: to enter!**\n"
                                f"Time Remaining: **{self.sec_time(self.convert(duration))}**\n"
                                f"Hosted by - {ctx.author.mention}",
                    color=ctx.guild.me.top_role.color,)

        embed.timestamp = datetime.datetime.utcnow() + timedelta(seconds = self.convert(duration))
        embed.set_footer(text = 'Ends at')
        
        if channel == None:
            msg = await ctx.channel.send(content=":tada: **GIVEAWAY** :tada:", embed=embed)
        else:
            msg = await channel.send(content=":tada: **GIVEAWAY** :tada:", embed=embed) 
        
        gw[guild]['MSG ID'] = msg.id
        await msg.add_reaction("🎉")
        Remaining = self.convert(duration)
        try:

            while Remaining:
                if not guild in gw:
                    return
                if Remaining <= 9:
                    break
                await sleep(10)
                if not guild in gw:
                    return
                Remaining-= 10
                embed.timestamp = datetime.datetime.utcnow() + timedelta(seconds = Remaining)
                embed.description = f"**React with :tada: to enter!**\nTime Remaining: **{self.sec_time(Remaining)}**\nHosted by - {ctx.author.mention}"
                await msg.edit(embed=embed)

            msg2 = await channel.fetch_message(msg.id)
            if msg2.reactions[0].count == 1:
                await channel.send('No users has participated Today.')
                embed = Embed(title = prize, description = f"Winner: None\nHosted By: {ctx.author}")
                await msg.edit(content = '**GIVEAWAY ENDED**',embed = embed)
                return
            
            a = []
            winners = ''
            winners2 = ''
            for reaction in msg2.reactions:
                print(reaction.users())
                async for user in reaction.users():
                    if not user.bot:
                        if user in ctx.guild.members:
                            a.append(user)
            try:
                if limit > len(a):
                    limit = len(a)
                if not len(a) == 1:
                    win1 = random.sample(a,limit)
                    for x in win1:
                        winners += f'{x.mention}\n'
                        winners2 += f'{x.mention} \u200b'

                else:
                    for x in a:
                        winners += f'{x.mention}\n'
                        winners2 += f'{x.mention} \u200b'
                        user = self.bot.get_user(x.id)
            
            except Exception as e:
                print(e)
            
            print(a)
            print(winners)
            print(winners2)
            embed = Embed(title = 'GIVEAWAY ENDED')
            embed.add_field(name = 'Winners:',value = f"{winners}",inline= False)
            embed.add_field(name = 'Hosted By:',value = f"{ctx.author}",inline = False)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text = 'Ended ')
            await msg.edit(content= 'GIVEAWAY ENDED',embed = embed)
            await channel.send(f':tada: Congratulations {winners2}, You have won the: **{prize}**')
            gw.pop(guild)
            return gw
        
        except Exception as e:
            import traceback
            traceback.print_exc() 

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def gstop(self,ctx):
        global gw
        guild = str(ctx.guild.id)
        if not guild in gw:
            await ctx.send('There are no giveaways ACTIVE')
            return
        else:
            gw.pop(guild)
        await ctx.send(':white_check_mark: Giveaway has been Ended.')
        return gw

    @giveaway.error
    async def gstart_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> Oops You are missing the: `Administrator` Permission.')

    @gstop.error
    async def gstop_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> Oops You are missing the: `Administrator` Permission.')

def setup(bot):
    bot.add_cog(giveaway(bot))