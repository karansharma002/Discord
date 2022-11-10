import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import typing

class clear(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def __init__(self, bot):
        self.bot = bot
    
    @has_permissions(manage_channels = True)
    @commands.command(aliases = ['Prune'])
    async def clear(self,ctx,val:int = None,user: discord.User = None):
        
        if val == None:
            embed=discord.Embed(description="Usage: clear `amount` `<@user`",color=0xff8083)
            embed.set_author(name="Clear Help")
            embed.set_footer(text="Clears / Deletes the Amount of Messages.")
            await ctx.send(embed = embed)
            return
        else:
            def is_user_message(message):
                return message.author.id == user.id
                
            if not user == None:
                await ctx.channel.purge(limit=val, check=is_user_message,before = None)
                msg = await ctx.send(f'<a:ln:678647491624960000> **Cleared** `{val}` **messages by {user}**\n`(This message will be auto deleted after 5 Secs)`')
                await asyncio.sleep(5)
                await msg.delete()
                return
            else:
                await ctx.channel.purge(limit = val)
                msg = await ctx.send(f'<a:ln:678647491624960000> **Cleared** `{val}` **messages.**\n`(This message will be auto deleted after 5 Secs)`')
                await asyncio.sleep(5)
                await msg.delete()

    @clear.error
    async def clear_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> You are missing the: `Manage Channels` Permission.')
    
def setup(bot):
    bot.add_cog(clear(bot))
