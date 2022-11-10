import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio

class clear(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def __init__(self, bot):
        self.bot = bot
    
    @has_permissions(manage_channels = True)
    @commands.command(aliases = ['Prune'])
    async def clear(self,ctx,val:int = None):
        if val == None:
            embed=discord.Embed(description="Usage: clear `amount``",color=0xff8083)
            embed.set_author(name="Clear Help", icon_url="https://i.imgur.com/wHD6EKK.jpg")
            embed.set_footer(text="Clears / Deletes the Amount of Messages.")
            await ctx.send(embed = embed)
            return
        else:
            await ctx.channel.purge(limit = val)
            msg = await ctx.send(f':white_check_mark: **Cleared** `{val}` **messages.**\n`(This message will be auto deleted after 5 Secs)`')
            await asyncio.sleep(5)
            await msg.delete()

    @clear.error
    async def clear_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> You are missing the: `Manage Channels` Permission.')
    
    @clear.error
    async def clear_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> You are missing the: `Manage Channels` Permission.')
def setup(bot):
    bot.add_cog(clear(bot))
