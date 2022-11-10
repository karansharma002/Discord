import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import datetime

class removewarn(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @has_permissions(ban_members = True)
    @commands.command()
    async def removewarn(self,ctx,user:discord.User=None,reason:str = None):
        with open('Config/warnings.json','r') as f:
            data = json.load(f)
        
        if user == None or reason == None:
            embed=discord.Embed(description="Usage: removewarn `<@user>` `<reason>`",color=0xff8083)
            embed.set_author(name="Removewarn Help", icon_url="https://i.imgur.com/wHD6EKK.jpg")
            embed.set_footer(text="Removes 1 Warning from the User.")
            await ctx.send(embed = embed)
            return
        
        else:
            guild = str(ctx.guild.id)
            with open('Config/warnings.json','r') as f:
                data = json.load(f)

            author = str(user.id)
            if not guild in data:
                await ctx.send('<a:alert_1:677763786664312860> No Logs found for this GUILD.')
                return
                
            if not author in data[guild]:
                await ctx.send("<a:alert_1:677763786664312860> This user doesn't have any warnings.")
                return

            elif data[guild][author]['Warnings'] == 0:
                await ctx.send("<a:alert_1:677763786664312860> This user doesn't have any warnings.")
                return

            else:
                data[guild][author]['Warnings'] -= 1
                warning = data[guild][author]['Warnings'] - 1
                with open('Config/guildlogs.json','r') as f:
                    rv = json.load(f)
                try:

                    if rv[guild]['warning Logs'] == 'Enabled':
                        channel = self.bot.get_channel(int(rv[guild]['warning ID']))
                        embed=discord.Embed(color=0x99ff00)
                        embed.set_author(name=f"{user} | 1 warning Removed")
                        embed.add_field(name="Moderator:", value=f"{ctx.author}", inline=False)
                        embed.add_field(name="Reason:", value=f"{reason}", inline=False)
                        embed.add_field(name="Active warnings:", value=f"{warning}", inline=False)
                        await channel.send(embed = embed)
                    else:
                        embed=discord.Embed(color=0x99ff00)
                        embed.set_author(name=f"{user} | 1 warning Removed")
                        embed.add_field(name="Moderator:", value=f"{ctx.author}", inline=False)
                        embed.add_field(name="Reason:", value=f"{reason}", inline=False)
                        embed.add_field(name="Active warnings:", value=f"{warning}", inline=False)
                        await ctx.send(embed = embed)
                
                except KeyError:
                    embed=discord.Embed(color=0x99ff00)
                    embed.set_author(name=f"{user} | 1 warning Removed")
                    embed.add_field(name="Moderator:", value=f"{ctx.author}", inline=False)
                    embed.add_field(name="Reason:", value=f"{reason}", inline=False)
                    embed.add_field(name="Active warnings:", value=f"{warning}", inline=False)
                    await ctx.send(embed = embed)
                with open('Config/warnings.json','w') as f:
                    json.dump(data,f,indent = 3)


    @removewarn.error
    async def removewarn_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> Oops You are missing the: `Ban Members` Permission.')

def setup(bot):
    bot.add_cog(removewarn(bot))