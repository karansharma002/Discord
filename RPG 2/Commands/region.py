import discord
from discord.ext import commands
import json

class Region(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def addregion(self,ctx,*,val:str = None):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')

        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        with open('Config/Settings.json') as f:
            m = json.load(f)
        
        if not val:
            await ctx.send(':information_source: Usage: =addregion `<REGION NAME>`')
            return
        
        val = val.upper()
        
        if val in m['Region']:
            await ctx.send(f':warning: `{val}` REGION Already exists.')
            return
        
        m['Region'].append(val)

        with open('Config/Settings.json','w') as f:
            json.dump(m,f,indent = 3)
        
        await ctx.send(':white_check_mark: REGION has been added')


    @commands.command()
    async def delregion(self,ctx,*,val:str = None):
        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')

        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return
            
        with open('Config/Settings.json') as f:
            m = json.load(f)
        
        if not val:
            await ctx.send(':information_source: Usage: =delregion `<REGION NAME>`')
            return
        
        val = val.upper()

        if not val in m['Region']:
            await ctx.send(f':warning: `{val}` REGION NOT FOUND')
            return
        
        m['Region'].remove(val)

        with open('Config/Settings.json','w') as f:
            json.dump(m,f,indent = 3)
        
        await ctx.send(':white_check_mark: REGION has been removed')

    @commands.command()
    async def region(self,ctx,rg:str = None):
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
        with open('Config/Data.json') as f:
            data = json.load(f)

        with open('Config/Cache.json') as f:
            cache = json.load(f)
        
        with open('Config/Settings.json') as f:
            settings = json.load(f)
        
        regions = ''
        for x in settings['Region']:
            regions += f"{x} - "

        if not rg:
            await ctx.send(f':information_source: Usage: =region `<NEW REGION (ALLOWED: {regions})`')
            return

        id_ = str(ctx.author.id)

        if not id_ in cache:
            await ctx.send(':warning: Account doesnt exist. Register a new one using: =register')
            return

        if not rg.upper() in settings['Region']:
            await ctx.send(f':warning: The region should match any of this: ({regions})')
            return
        
        rg = rg.upper()
        username = id_
        data[username]['Region'] = rg
        await ctx.send(':white_check_mark: Region has been CHANGED')
        
        with open('Config/Data.json','w') as f:
            json.dump(data,f,indent = 3)
        
            
        await ctx.author.edit(nick = f"[{data[username]['Points']}] {data[username]['Username']} ({data[username]['Region']})")


def setup(bot):
    bot.add_cog(Region(bot))