import discord
from discord.ext import commands

class setname(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(aliases = ['setnick'])
    async def setname(self,ctx,member:discord.Member = None,*,val:str = None):
        if val == None or member == None:
            await ctx.send('<:info:722088058521911296> **Usage:** +setname `<@user>` `<name>` ')
  
        else:
            await member.edit(nick = val)
            await ctx.send(f'<a:ln:678647491624960000> `{member.name.upper()}` nick has been changed to: `{val}`')

def setup(bot):
    bot.add_cog(setname(bot))
