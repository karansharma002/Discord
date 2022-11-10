import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import datetime
class unmute(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @has_permissions(manage_messages = True)
    @commands.command()
    async def unmute(self,ctx,user:discord.User = None,*,reason:str = None):
        guild = str(ctx.guild.id)
        if user == None:
            embed=discord.Embed(description="Usage: unmute `<@user>` `<reason`",color=0xff8083)
            embed.set_author(name="Unmute Help")
            embed.set_footer(text="Unmutes the Muted Users.")
            await ctx.send(embed = embed)
            return
			
        else:
            role = discord.utils.get(ctx.guild.roles,name = 'Muted')
            member = ctx.guild.get_member(user.id)
            if not role in member.roles:
                await ctx.send(f'<a:alert_1:677763786664312860> {user.name} is not Muted.')
                return
            else:
                if reason == None:
                    reason = 'NONE'
                else:
                    reason = reason
                role = discord.utils.get(ctx.guild.roles, name='Muted')
                member = ctx.guild.get_member(user.id)
                await member.remove_roles(role)
                embed=discord.Embed(color=0x4dff00)
                embed.set_author(name=f"{user} | Unmuted")
                embed.add_field(name="Moderator:", value=f"{ctx.author}", inline=False)
                embed.add_field(name="Reason:", value=f"{reason}", inline=False)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
    
    @unmute.error
    async def unmute_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> Oops You are missing the: `Manage Messages` Permission.')

def setup(bot):
    bot.add_cog(unmute(bot))
