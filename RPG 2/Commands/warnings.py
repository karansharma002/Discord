import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
from datetime import datetime,timedelta

class Warnings(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def clearwarnlist(self,ctx):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')

        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        with open('Config/warnings.json','r') as f:
            data = json.load(f)
        

        def check(m):
            return m.author == ctx.author

        with open('Config/warnings.json','r') as f:
            data = json.load(f)
        
        try:
            try:
                await ctx.send('Are you sure about this:question: (REPLY WITH `Yes/NO`)')
                confirmation = await self.bot.wait_for('message',check = check,timeout = 20)
                if confirmation.content.lower() in ('yes','y'):
                    data = {}
                    with open('Config/warnings.json','w') as f:
                        json.dump(data,f,indent = 3)
                    
                    await ctx.send(':white_check_mark: Warnings List has been CLEARED')
                    return

                else:
                    await ctx.send(':white_check_mark: (Action REVERTED)')
                    return
            
            except Exception as e:
                print(e)

        except asyncio.TimeoutError:
            await ctx.send(':warning: Request TIMED OUT. Retry!')

    @commands.command()
    async def unwarn(self,ctx,user2:discord.User = None,amount:int = None):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')

        if role1 in ctx.author.roles:
            pass
        elif role2 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        if not user2 or not amount:
            await ctx.send(':information_source: Usage: =unwarn `<@user>` `<NUM OF WARNS TO REMOVE>`')
            return

        with open('Config/warnings.json','r') as f:
            data = json.load(f)
        
        user = str(user2.id)
        if not user in data:
            await ctx.send(':warning: User has no active warnings.')
            return
        
        else:
            if data[user]['Warnings'] - amount <= 0:
                data.pop(user)
            else:
                data[user]['Warnings'] -= amount

            with open('Config/warnings.json','w') as f:
                json.dump(data,f,indent = 3)
            
            await ctx.send(f':white_check_mark: Removed {amount} of warnings from {user2}')
            return

    @commands.command()
    async def warn(self,ctx,member:discord.Member = None,*,reason = None):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')

        if role1 in ctx.author.roles:
            pass
        elif role2 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        with open('Config/warnings.json','r') as f:
            data = json.load(f)
        
        with open('Config/Settings.json') as f:
            settings = json.load(f)

        if member == None or reason == None:
            embed=discord.Embed(description="Usage: =warn `<@user` `<reason>`",color=0xff8083)
            embed.set_author(name="Warn Help", icon_url=self.bot.user.avatar_url)
            embed.set_footer(text="Gives a Warning to the User.")
            await ctx.send(embed = embed)
            return
			

        else:
            try:

                author = str(member.id)

                if not author in data:
                    data[author] = {}
                    data[author]['Warnings'] = 1
                    data[author]['Reason'] = [reason]
                    with open('Config/warnings.json','w') as f:
                        json.dump(data,f,indent = 3) 
                else:
                    data[author]['Warnings'] += 1
                    data[author]['Reason'].append(reason)
                    with open('Config/warnings.json','w') as f:
                        json.dump(data,f,indent = 3) 

                with open('Config/warnings.json','r') as f:
                    data = json.load(f)
                
                warning = data[author]['Warnings']
                if 'Max_Warnings' in settings:
                    max_warnings = settings['Max_Warnings']
                else:
                    await ctx.send(':warning: MAX Warnings for the auto ban is not set. Use: =autoban to set')
                    return

                if warning >= max_warnings:                
                    data.pop(author)
                    
                    with open('Config/warnings.json','w') as f:
                        json.dump(data,f,indent = 4)
                    
                    with open('Config/Bans.json') as f:
                        bans = json.load(f)
                                    
                    if 'Ban_Duration' in settings:
                        duration = settings['Ban_Duration']
                    else:
                        duration = 10
                    
                    bans[str(member.id)] = str(datetime.now() + timedelta(hours = duration))
                    with open('Config/Bans.json','w') as f:
                        json.dump(bans,f,indent = 3)

                    embed=discord.Embed(color=0xf9231f)
                    embed.set_author(name=f"{member} | Banned ({warning}/{max_warnings}) WARNINGS")
                    embed.add_field(name=f"Moderator:", value=f"{ctx.author}", inline=False)
                    embed.add_field(name=f"Reason:", value=f"{reason}", inline=False)
                    embed.add_field(name=f"Duration:", value=f"{duration} Hours", inline=False)
                    await ctx.send(embed = embed)
                    await member.send(f':warning: You have been BANNED from using the bot for {duration} HOURS.')
                
                else:
                    embed=discord.Embed(color=0xec8e8e)
                    embed.set_author(name=f"{member} | Warned ({warning}/{max_warnings})")
                    embed.add_field(name=f"Moderator:", value=f"{ctx.author}", inline=False)
                    embed.add_field(name=f"Reason:", value=f"{reason}", inline=False)
                    await ctx.send(embed = embed)

            except Exception as e:
                print(e)


    @commands.command()
    async def warns(self,ctx):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')

        if role1 in ctx.author.roles:
            pass
        elif role2 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return
            
        with open('Config/warnings.json','r') as f:
            data = json.load(f)

        msg = ''
        embed = discord.Embed(title = 'WARNINGS LIST',color = discord.Color.red(),description = msg)
        for num,x in enumerate(data):
            reason = ''
            user = await self.bot.fetch_user(int(x))
            for num2,y in enumerate(data[x]['Reason']):
                reason += f"{num2 + 1}: {y}\n"
            embed.add_field(name = f"**{num + 1}:** {user} - (**Warnings**: {data[x]['Warnings']})",value = reason,inline = False)
        
        if msg == '':
            msg = 'The list is empty'

        await ctx.send(embed = embed)           

def setup(bot):
    bot.add_cog(Warnings(bot))

