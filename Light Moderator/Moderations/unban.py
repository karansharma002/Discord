import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class unban(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def init(self, bot):
        self.bot = bot
    
    @has_permissions(kick_members =True,ban_members=True)
    @commands.command()
    async def unban(self,ctx,*,member = None):
        if member == None:
            embed=discord.Embed(description="Usage: unban `<user name>`",color=0xff8083)
            embed.set_author(name="Unban help", icon_url="https://i.imgur.com/wHD6EKK.jpg")
            embed.set_footer(text="Unban the user from the server.")
            await ctx.send(embed = embed)
            return
			
        else:
            banned_users = await ctx.guild.bans()
            if banned_users == []:
                user = 'None'
            
            else:
                for ban_entry in banned_users:
                    user = ban_entry.user
            try:
                if user == None:
                    await ctx.send('<a:alert_1:677763786664312860> (ERROR) Invalid User or User is not Banned.')
                else:
                    await ctx.guild.unban(user)
                    await ctx.send('<a:ln:678647491624960000> The user has been Unbanned.')
        
            except Exception as e:
                if e.startswith('local') or e.startswith("'str'"):
                    return
                else:
                    await ctx.send(f'<a:alert_1:677763786664312860> {e}')

    @unban.error
    async def unban_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> Oops You are missing the: `Ban Members` Permission.')

def setup(bot):
    bot.add_cog(unban(bot))
