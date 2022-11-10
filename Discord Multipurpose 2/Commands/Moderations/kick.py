import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
class kick(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def init(self, bot):
        self.bot = bot
    
    @has_permissions(kick_members=True)
    @commands.command()
    async def kick(self,ctx,member: discord.Member = None,*,reason:str = None):
        if member == None:
            embed=discord.Embed(description="Usage: kick `<@user>` `<reason>`",color=0xff8083)
            embed.set_author(name="Kick Help")
            embed.set_footer(text="Kicks the user from the Server.")
            await ctx.send(embed = embed)
            return

        else:
            try:
                await member.kick(reason = reason)
                await ctx.send(f'<a:ln:678647491624960000> {member} **has been kicked**.')
            except Exception as e:
                await ctx.send(f'<a:alert_1:677763786664312860> {e}')

    @kick.error
    async def kick_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> You are missing the: `Kick Members` Permission.')


def setup(bot):
    bot.add_cog(kick(bot))