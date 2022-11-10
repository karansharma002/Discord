import discord
from discord.ext import commands

class Lock(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.has_permissions(manage_channels = True)
    @commands.command()
    async def lock(self,ctx,*,text = None):
        if text == None:
            await ctx.send(':info: Usage: !lock `<text>`')
            return
        else:
            channel = ctx.channel
            await channel.set_permissions(ctx.guild.default_role, send_messages = False)
            await ctx.channel.purge(limit = 1)
            await ctx.send(f'```diff\n- {text}```')
            #await ctx.send(f':white_check_mark: {channel.mention} has been Locked.')
    
    @commands.has_permissions(manage_channels = True)
    @commands.command()
    async def unlock(self,ctx, channel : discord.TextChannel= None):
        await ctx.channel.purge(limit = 1)
        channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages = True)
        await ctx.send(f'```css\n- Chat Enabled```')
    
    @lock.error
    async def lock_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> Oops You are missing the: `Manage Channels` Permission.')

    @unlock.error
    async def unlock_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> Oops You are missing the: `Manage Channels` Permission.')

def setup(bot):
    bot.add_cog(Lock(bot))