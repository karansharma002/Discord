import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class ban(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def __init__(self, bot):
        self.bot = bot
    
    @has_permissions(ban_members=True)
    @commands.command()
    async def ban(self,ctx,member: discord.Member = None,*,reason:str = None):
        if member == None or reason == None:
            embed=discord.Embed(description="Usage: ban `<@user` `<reason>`",color=0xff8083)
            embed.set_author(name="Ban Help")
            embed.set_footer(text="Bans the Member from Server.")
            await ctx.send(embed = embed)
            return
        else:
            try:	
                #await member.ban(reason = reason,days = days)	
                await member.ban(reason = reason)
                await ctx.send(f'<a:ln:678647491624960000> {member} **has been Banned**.')
            except Exception as e:
                await ctx.send(f'<a:alert_1:677763786664312860> {e}')

    @ban.error
    async def ban_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> Oops You are missing the: `Ban Members` Permission.')

def setup(bot):
    bot.add_cog(ban(bot))