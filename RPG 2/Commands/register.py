import discord
from discord.ext import commands
import json

class Register(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def unregister(self,ctx):
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

        with open('Config/Settings.json') as f:
            settings = json.load(f)
        

        if 'Register_Channel' in settings:
            if not ctx.channel.id == settings['Register_Channel']:
                return
        else:
            await ctx.send(':warning: Default Registration channel is not SET.')
            return

        with open('Config/Data.json') as f:
            data = json.load(f)
        
        with open('Config/Cache.json') as f:
            cache = json.load(f)
        
        id_ = str(ctx.author.id)

        if not id_ in cache:
            await ctx.send(':warning: You are not registered.')
            return
        
        else:
            data.pop(id_)
            with open('Config/Data.json','w') as f:
                json.dump(data,f,indent = 3)
            
            cache.pop(id_)
            with open('Config/Cache.json','w') as f:
                json.dump(cache,f,indent = 3)
            
            await ctx.send(':white_check_mark: You have been unregistered')
            await ctx.author.edit(nick = ctx.author.name)

    @commands.command()
    async def register(self,ctx,region:str = None,*,username:str = None):
        with open('Config/Settings.json') as f:
            settings = json.load(f)

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')
        if role1 in ctx.author.roles or role2 in ctx.author.roles:
            pass

        elif 'Register_Channel' in settings:
            if not ctx.channel.id == settings['Register_Channel']:
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
        
        id_ = str(ctx.author.id)

        if id_ in cache:
            await ctx.send(':warning: Account is already registered. For modifying the name, Use: `=rename`') 
            return

        if not region or not username:
            await ctx.send(':information_source: Usage:  =register `<region>` `<username>`')
            return
        
        if username in data:
            await ctx.send(':warning: This username is already taken, Please select another one!')
            return
        
        regions = ''
        for x in settings['Region']:
            regions += f"{x} - "

        if not region.upper() in settings['Region']:
            await ctx.send(f':warning: The region should match any of this: ({regions})')
            return
        
        cache[id_] = username
        data[id_] = {}
        data[id_]['Points'] = 0
        data[id_]['Region'] = region.upper()
        data[id_]['Wins'] = 0
        data[id_]['Loss'] = 0
        data[id_]['Best_Maps'] = 'None'
        data[id_]['ID'] = ctx.author.id
        data[id_]['Username'] = username

        with open('Config/Data.json','w') as f:
            json.dump(data,f,indent = 3)
        
        with open('Config/Cache.json','w') as f:
            json.dump(cache,f,indent = 2)
        
        await ctx.send(f':white_check_mark: ({username}) has been registered.')
        role = discord.utils.get(ctx.guild.roles,name = 'Member')
        await ctx.author.add_roles(role)
        await ctx.author.edit(nick = f'[0] {username} ({region.upper()})')

def setup(bot):
    bot.add_cog(Register(bot))