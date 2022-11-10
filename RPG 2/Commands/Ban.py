import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
from datetime import datetime,timedelta
from dateutil import parser
class ban(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def ban(self,ctx,member: discord.Member = None,duration:int = None):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')

        if role1 in ctx.author.roles:
            pass

        elif role2 in ctx.author.roles:
            pass

        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        if role1 in member.roles or role2 in member.roles:
            await ctx.send(':warning: You cannot ban a Moderator')
            return
            
        if member == None or duration == None:
            embed=discord.Embed(description="Usage: =ban `<@user` `<DURATION IN HOURS>`",color=0xff8083)
            embed.set_author(name="Ban Help")
            embed.set_footer(text="Bans the Member from Using the BOT.")
            await ctx.send(embed = embed)
            return

        else:
            with open('Config/Bans.json') as f:
                bans = json.load(f)
            
            bans[str(member.id)] = str(datetime.now() + timedelta(hours = duration))
            with open('Config/Bans.json','w') as f:
                json.dump(bans,f,indent = 3)

            await ctx.send(f':white_check_mark: {member} **has been Banned for {duration} HOURS**.')



    @commands.command()
    async def unban(self,ctx,member:discord.Member = None):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')

        if role1 in ctx.author.roles:
            pass
        elif role2 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        if member == None:
            embed=discord.Embed(description="Usage: =unban `<user name>`",color=0xff8083)
            embed.set_author(name="Unban help")
            embed.set_footer(text="Unban the user from the BOT.")
            await ctx.send(embed = embed)
            return
			
        else:
            with open('Config/Bans.json') as f:
                bans = json.load(f)
            
            user = str(member.id)
            if not user in bans:
                await ctx.send(f':warning: {user.name} is not BANNED')
                return
            else:
                bans.pop(user)
                await ctx.send(':white_check_mark: The user has been Unbanned.')
                with open('Config/Bans.json','w') as f:
                    json.dump(bans,f,indent = 3)
    

    @commands.command()
    async def bans(self,ctx):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')

        if role1 in ctx.author.roles:
            pass
        elif role2 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        with open('Config/Bans.json') as f:
            bans = json.load(f)
        
        msg = ''
        for num,x in enumerate(bans):
            t1 = parser.parse(str(datetime.now()))
            t2 = parser.parse(str(bans[x]))
            t3 = t2 - t1
            seconds = round(t3.total_seconds() / 60)
            user = await self.bot.fetch_user(int(x))
            msg += f"**{num + 1}:** {user} - ({seconds} HOURS)\n"
        
        if msg == '':
            msg = 'The list is empty'

        embed = discord.Embed(title = 'BANS LIST',color = discord.Color.red(),description = msg)
        await ctx.send(embed = embed)

    @commands.command()
    async def banduration(self,ctx,duration:int = None):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        if role1 in ctx.author.roles:
            pass

        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        if not duration:
            await ctx.send('Usage: =banduration `<DURATION IN HOURS>`')
            return

        with open('Config/Settings.json') as f:
            settings = json.load(f)
        
        settings['Ban_Duration'] = duration
        with open('Config/Settings.json','w') as f:
            json.dump(settings,f,indent = 3)
        
        await ctx.send(':white_check_mark: Ban Duration has been Updated')

    @commands.command()
    async def autoban(self,ctx,num:int = None):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')


        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        if not num:
            await ctx.send('Usage: =autoban `<MAX WARNINGS FOR AUTO BAN [Example: 5]>`')
            return

        with open('Config/Settings.json') as f:
            settings = json.load(f)
        
        settings['Max_Warnings'] = num
        with open('Config/Settings.json','w') as f:
            json.dump(settings,f,indent = 3)
        
        await ctx.send(':white_check_mark: Auto Ban Max Warnings has been Updated')

def setup(bot):
    bot.add_cog(ban(bot))