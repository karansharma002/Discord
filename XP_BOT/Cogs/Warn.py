import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import datetime

class warn(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @has_permissions(ban_members = True)
    @commands.command()
    async def warn(self,ctx,member:discord.Member = None,*,reason = None):
        guild = str(ctx.guild.id)
        with open('Config/warnings.json','r') as f:
            data = json.load(f)

        if member == None or reason == None:
            embed=discord.Embed(description="Usage: warn `<@user` `<reason>`",color=0xff8083)
            embed.set_author(name="Warn Help", icon_url="https://i.imgur.com/wHD6EKK.jpg")
            embed.set_footer(text="Gives a Warning to the User. (3/3) = BAN")
            await ctx.send(embed = embed)
            return
			

        else:
            author = str(member.id)
            date = datetime.datetime.today().strftime("%A, %B %d %Y @ %H:%M:%S %p")
            if not guild in data:
                data[guild] = {}
                with open('Config/warnings.json','w') as f:
                    json.dump(data,f,indent = 3) 
            
            if not author in data[guild]:
                data[guild][author] = {}
                data[guild][author]['Warnings'] = 1
                data[guild][author]['Reason'] = reason
                with open('Config/warnings.json','w') as f:
                    json.dump(data,f,indent = 3) 
            else:
                data[guild][author]['Warnings'] += 1
                data[guild][author]['Reason'] = reason
                with open('Config/warnings.json','w') as f:
                    json.dump(data,f,indent = 3) 

            with open('Config/warnings.json','r') as f:
                data = json.load(f)
            
            warning = data[guild][author]['Warnings']
            if warning >= 3:
                if warning > 3:
                    warning = 3
                else:
                    warning = warning
                
                data[guild][author]['Warnings'] = 0
                await member.ban(reason = '3/3 Warnings')
                with open('Config/warnings.json','w') as f:
                    json.dump(data,f,indent = 4)
                
                with open('Config/guildlogs.json','r') as f:
                    data1 = json.load(f)
                
                try:
                    if data1[guild]['Warning Logs'] == 'Enabled':
                        channel = self.bot.get_channel(int(data1[guild]['Warning ID']))
                        embed=discord.Embed(color=0xf9231f)
                        embed.set_author(name=f"{member} | Banned ({warning}/3)")
                        embed.add_field(name=f"Moderator:", value=f"{ctx.author}", inline=False)
                        embed.add_field(name=f"Reason:", value=f"3 Warnings", inline=False)
                        embed.set_footer(text=f"{date}")
                        await channel.send(embed = embed)
                    else:
                        embed=discord.Embed(color=0xf9231f)
                        embed.set_author(name=f"{member} | Banned ({warning}/3)")
                        embed.add_field(name=f"Moderator:", value=f"{ctx.author}", inline=False)
                        embed.add_field(name=f"Reason:", value=f"3 Warnings", inline=False)
                        embed.set_footer(text=f"{date}")
                        await ctx.send(embed = embed)
                
                except KeyError:
                    embed=discord.Embed(color=0xf9231f)
                    embed.set_author(name=f"{member} | Banned ({warning}/3)")
                    embed.add_field(name=f"Moderator:", value=f"{ctx.author}", inline=False)
                    embed.add_field(name=f"Reason:", value=f"3 Warnings", inline=False)
                    embed.set_footer(text=f"{date}")
                    await ctx.send(embed = embed)
            
            else:

                with open('Config/guildlogs.json','r') as f:
                    data1 = json.load(f)
                try:
                    if data1[guild]['Warning Logs'] == 'Enabled':
                        channel = self.bot.get_channel(int(data1[guild]['Warning ID']))
                        embed=discord.Embed(color=0xec8e8e)
                        embed.set_author(name=f"{member} | Warned ({warning}/3)")
                        embed.add_field(name=f"Moderator:", value=f"{ctx.author}", inline=False)
                        embed.add_field(name=f"Reason:", value=f"{reason}", inline=False)
                        embed.set_footer(text=f"{date}")
                        await channel.send(embed = embed)
                    else:
                        embed=discord.Embed(color=0xec8e8e)
                        embed.set_author(name=f"{member} | Warned ({warning}/3)")
                        embed.add_field(name=f"Moderator:", value=f"{ctx.author}", inline=False)
                        embed.add_field(name=f"Reason:", value=f"{reason}", inline=False)
                        embed.set_footer(text=f"{date}")
                        await ctx.send(embed = embed)
                
                except KeyError:
                    embed=discord.Embed(color=0xec8e8e)
                    embed.set_author(name=f"{member} | Warned ({warning}/3)")
                    embed.add_field(name=f"Moderator:", value=f"{ctx.author}", inline=False)
                    embed.add_field(name=f"Reason:", value=f"{reason}", inline=False)
                    embed.set_footer(text=f"{date}")
                    await ctx.send(embed = embed)

    @warn.error
    async def warn_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> Oops You are missing the: `Ban Members` Permission.')

def setup(bot):
    bot.add_cog(warn(bot))