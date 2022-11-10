import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import datetime
class mute(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @has_permissions(manage_messages = True)
    @commands.command()
    async def mute(self,ctx,user:discord.User = None,*,reason:str = None):
        guild = str(ctx.guild.id)
        if user == None or reason == None:
            embed=discord.Embed(description="Usage: mute `<@user>` `<reason>`",color=0xff8083)
            embed.set_author(name="Mute Help", icon_url="https://i.imgur.com/wHD6EKK.jpg")
            embed.set_footer(text="Mutes the User from replying anywhere.")
            await ctx.send(embed = embed)
            return
        
        else:
            date = datetime.datetime.today().strftime("%A, %B %d %Y @ %H:%M:%S %p")
            role = discord.utils.get(ctx.guild.roles,name = 'Muted')
            if role == None:
                try:
                    muted = await ctx.guild.create_role(name = 'Muted')
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(muted,send_messages=False)

                    role = discord.utils.get(ctx.guild.roles,name = 'Muted')
                    member = ctx.guild.get_member(user.id)
                    if role in member.roles:
                        await ctx.send(f'<a:alert_1:677763786664312860> `{user.name}`` is already Muted.')
                        return

                    member = ctx.guild.get_member(user.id)
                    role = discord.utils.get(ctx.guild.roles, name='Muted')
                    await member.add_roles(role)
                    embed=discord.Embed(color=0xff0000)
                    embed.set_author(name=f"{user} Has been muted.")
                    embed.add_field(name="Moderator:", value=f"{ctx.author}", inline=False)
                    embed.add_field(name="Reason:", value=f"{reason}", inline=False)
                    embed.set_footer(text=f"{date}")
                    await ctx.send(embed = embed)

                except Exception as e:
                    await ctx.send(f'<a:alert_1:677763786664312860> ERROR: `{e}`')
            else:
                try:
                    role = discord.utils.get(ctx.guild.roles,name = 'Muted')
                    member = ctx.guild.get_member(user.id)
                    if role in member.roles:
                        await ctx.send(f'<a:alert_1:677763786664312860> `{user.name}` is already Muted.')
                        return

                    member = ctx.guild.get_member(user.id)
                    role = discord.utils.get(ctx.guild.roles, name='Muted')
                    await member.add_roles(role)
                    with open('Config/guildlogs.json','r') as f:
                        data = json.load(f)
                    try:
                        if data[guild]['Mute Logs'] == 'Enabled':
                            av = int(data[guild]['Mute ID'])
                            channel = self.bot.get_channel(av)
                            embed=discord.Embed(color=0xff0000)
                            embed.set_author(name=f"{user} Has been muted.")
                            embed.add_field(name="Moderator:", value=f"{ctx.author}", inline=False)
                            embed.add_field(name="Reason:", value=f"{reason}", inline=False)
                            embed.set_footer(text=f"{date}")
                            await channel.send(embed = embed)

                        else:
                            embed=discord.Embed(color=0xff0000)
                            embed.set_author(name=f"{user} Has been muted.")
                            embed.add_field(name="Moderator:", value=f"{ctx.author}", inline=False)
                            embed.add_field(name="Reason:", value=f"{reason}", inline=False)
                            embed.set_footer(text=f"{date}")
                            await ctx.send(embed = embed)	

                    except KeyError:
                            embed=discord.Embed(color=0xff0000)
                            embed.set_author(name=f"{user} Has been muted.")
                            embed.add_field(name="Moderator:", value=f"{ctx.author}", inline=False)
                            embed.add_field(name="Reason:", value=f"{reason}", inline=False)
                            embed.set_footer(text=f"{date}")
                            await channel.send(embed = embed)			

                except Exception:
                    await ctx.send(f'<a:alert_1:677763786664312860> ERROR: `{e}`')
    @mute.error
    async def unmute_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> Oops You are missing the: `Manage Messages` Permission.')

def setup(bot):
    bot.add_cog(mute(bot))
