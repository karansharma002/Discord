import discord
from discord.ext import commands
import json
import random

class Map(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def addmap(self,ctx,*,val:str = None):
        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        with open('Config/Maps.json') as f:
            m = json.load(f)
        
        if not val:
            await ctx.send(':information_source: Usage: =addmap `<MAP NAME>`')
            return
        
        if val in m:
            await ctx.send(f':warning: `{val}` MAP Already exists.')
            return
        
        m[val] = 'Active'

        with open('Config/Maps.json','w') as f:
            json.dump(m,f,indent = 3)
        
        await ctx.send(':white_check_mark: MAP has been added')


    @commands.command()
    async def removemap(self,ctx,*,val:str = None):
        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return
        with open('Config/Maps.json') as f:
            m = json.load(f)
        
        if not val:
            await ctx.send(':information_source: Usage: =removemap `<MAP NAME>`')
            return

        if not val in m:
            await ctx.send(f':warning: `{val}` MAP NOT FOUND')
            return
        
        m.pop(val)

        with open('Config/Maps.json','w') as f:
            json.dump(m,f,indent = 3)
        
        await ctx.send(':white_check_mark: MAP has been removed')

    @commands.command()
    async def maps(self,ctx):
        with open('Config/Settings.json') as f:
            settings = json.load(f)

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')
        if role1 in ctx.author.roles or role2 in ctx.author.roles:
            pass

        elif 'Bot_Channel' in settings:
            if not ctx.channel.id == settings['Bot_Channel']:
                return
        else:
            await ctx.channel.send(':warning: Default BOT channel is not SET.')
            return

        with open('Config/Maps.json') as f:
            m = json.load(f)
        
        msg = ''
        for num,x in enumerate(m):
            msg += f"{num+1} - **{x}**\n"
        
        if msg == '':
            msg = 'Oops, No maps found'
        await ctx.send(msg)
    
    @commands.command()
    async def map(self,ctx,num:int = None,*,map_name:str = None):
        with open('Config/Settings.json') as f:
            settings = json.load(f)

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')
        if role1 in ctx.author.roles or role2 in ctx.author.roles:
            pass

        elif 'Bot_Channel' in settings:
            if not ctx.channel.id == settings['Bot_Channel']:
                return
        else:
            await ctx.channel.send(':warning: Default BOT channel is not SET.')
            return
            
        with open('Config/Bans.json') as f:
            bans = json.load(f)
        
        user = str(ctx.author.id)
        if user in bans:
            await ctx.send(f":warning: {ctx.author.mention} You don't have the access to use this command. **[BANNED]**")
            return

        with open('Config/Maps.json') as f:
            maps = json.load(f)

        if not num and not map_name:
            choose_from = list(maps)
            await ctx.send(f'**Map Name:** {random.choice(choose_from)}')
            return

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')

        if role1 in ctx.author.roles:
            pass
        elif role2 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return
        
        with open('Config/Games.json') as f:
            gm = json.load(f)
        
        if not map_name in maps:
            await ctx.send(":warning: This map doesn't exists")
            return
        
        if not str(num) in gm:
            await ctx.send(f':warning: No active game found for the number: {num}')
            return
        
        gm[str(num)]['Map'] = map_name
        with open('Config/Games.json','w') as f:
            json.dump(gm,f,indent = 3)
        
        await ctx.send(f':white_check_mark: Map has been changed.')

    
def setup(bot):
    bot.add_cog(Map(bot))