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

        with open('Config/guildlogs.json','r') as f:
            logs = json.load(f)
        
        if member == None or reason == None:
            embed=discord.Embed(description="Usage: warn `<@user` `<reason>`",color=0xff8083)
            embed.set_author(name="Warn Help")
            if guild in logs:
                if 'Max Warnings' in logs[guild]:
                    max_warnings = logs[guild]['Max Warnings']
                else:
                    max_warnings = 3
            else:
                max_warnings = 3
            embed.set_footer(text=f"Gives a Warning to the User. ({max_warnings} / {max_warnings}) = KICK")
            await ctx.send(embed = embed)
            return

        else:
            author = str(member.id)
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
            if guild in logs:
                if 'Max Warnings' in logs[guild]:
                    max_warnings = logs[guild]['Max Warnings']
                else:
                    max_warnings = 3
            else:
                max_warnings = 3

            if warning >= max_warnings:
                if warning > max_warnings:
                    warning = max_warnings
                else:
                    warning = warning
                
                data[guild][author]['Warnings'] = 0
                await member.kick(reason = '3/3 Warnings')
                with open('Config/warnings.json','w') as f:
                    json.dump(data,f,indent = 4)
                
                embed=discord.Embed(color=0xf9231f)
                embed.set_author(name=f"{member} | Kicked ({warning}/{max_warnings})")
                embed.add_field(name=f"Moderator:", value=f"{ctx.author}", inline=False)
                embed.add_field(name=f"Reason:", value=f"3 Warnings", inline=False)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed = embed)
        
            else:
                embed=discord.Embed(color=0xec8e8e)
                embed.set_author(name=f"{member} | Warned ({warning}/ {max_warnings})")
                embed.add_field(name=f"Moderator:", value=f"{ctx.author}", inline=False)
                embed.add_field(name=f"Reason:", value=f"{reason}", inline=False)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed = embed)
    
    @has_permissions(ban_members = True)
    @commands.command()
    async def setwarn(self,ctx,val:int = None):
        with open('Config/guildlogs.json','r') as f:
            data = json.load(f)
        
        if val == None:
            await ctx.send(':information_source: Usage: setwarn `<Max Warnings = Kick>`')
            return

        guild = str(ctx.guild.id)
        if not guild in data:
            data[guild] = {}
            
        data[guild]['Max Warnings'] = val
        await ctx.send(f':white_check_mark: Max Warnings has been changed to: {val}')
        with open('Config/guildlogs.json','w') as f:
            json.dump(data,f,indent = 3)
    @warn.error
    async def warn_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> Oops You are missing the: `Ban Members` Permission.')

def setup(bot):
    bot.add_cog(warn(bot))