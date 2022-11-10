import discord
from discord.ext import commands
import json

class Rename(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def rename(self,ctx,*,username:str = None):
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
        if not username:
            await ctx.send(':information_source: Usage: =rename `<NEW USERNAME>`')
            return
        with open('Config/Data.json') as f:
            data = json.load(f)
        
        with open('Config/Cache.json') as f:
            cache = json.load(f)
        
        id_ = str(ctx.author.id)
        
        if not id_ in cache:
            await ctx.send(':warning: Account is not registered. Use: `=register` to register your account')
            return
        
        data[id_]['Username'] = username
        cache[id_] = username

        with open('Config/Data.json','w') as f:
            json.dump(data,f,indent = 3)
        
        with open('Config/Cache.json','w') as f:
            json.dump(cache,f,indent = 2)
        
        with open('Config/Data.json') as f:
            data = json.load(f)
        
        await ctx.send(f':white_check_mark: Username has been changed to: ({username})') 
        await ctx.author.edit(nick = f"[{data[username]['Points']}] {username} ({data[username]['Region']})")

def setup(bot):
    bot.add_cog(Rename(bot))