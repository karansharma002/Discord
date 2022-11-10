import warnings
from discord.ext.commands import has_permissions
from discord.ext import commands,tasks
import discord
import os
import json
import asyncio
import datetime

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print('----- SERVER STARTED -----')

@has_permissions(administrator = True)
@bot.command()
async def nuke(ctx, channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Command Usage: !nuke `#channel`')
        return

    if channel is not None:
        await channel.clone(reason="Has been nuked")
        await channel.delete()

@nuke.error
async def nuke_error(ctx,error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(':warning:  Oops You are missing the: `Administrator` Permission.')

@bot.command()
async def build(ctx):
    if not ctx.channel.id == 802991970720940043:
        return
    user = ctx.author.name
    file_name = f'-{user}_loader.lua'
    os.rename('Test.lua',file_name)
    embed=discord.Embed(title="Sending you your latest semirage build!", description="Please make sure to rename the file to start with ! instead of -\nIf you don't get a download link within two minutes, please contact the admin.", color=0xff8000)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text = 'Build Date')
    await ctx.author.send(embed=embed)
    await asyncio.sleep(1)
    await ctx.author.send(file = discord.File(file_name))
    await ctx.message.add_reaction('✅')
    os.rename(file_name,'Test.lua')
    embed=discord.Embed(title="There you go, have fun!", description="Please make sure to rename the file to start with ! instead of -\nIf you have troubles loading the lua, please contact the admin.", color=0x70FF00)
    await ctx.author.send(embed = embed)


@has_permissions(manage_channels = True)
@bot.command(aliases = ['Prune','Purge'])
async def clear(ctx,val:int = None):
    if val == None:
        embed=discord.Embed(description="Usage: clear `amount`",color=0xff8083)
        embed.set_author(name="Clear Help")
        embed.set_footer(text="Clears / Deletes the Amount of Messages.")
        await ctx.send(embed = embed)
        return

    else:
        await ctx.channel.purge(limit = val)
        msg = await ctx.send(f':white_check_mark: **Cleared** `{val}` **messages.**\n`(This message will be auto deleted after 5 Secs)`')
        await asyncio.sleep(5)
        await msg.delete()

@clear.error
async def clear_error(ctx,error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(':warning:  Oops You are missing the: `Manage Channels` Permission.')

@has_permissions(ban_members = True)
@bot.command()
async def warn(ctx,member:discord.Member = None,*,reason = None):
    guild = str(ctx.guild.id)
    with open('Config/warnings.json','r') as f:
        data = json.load(f)

    if member == None or reason == None:
        embed=discord.Embed(description="Usage: warn `<@user` `<reason>`",color=0xff8083)
        embed.set_author(name="Warn Help")
        max_warnings = 3
        embed.set_footer(text=f"Gives a Warning to the User. ({max_warnings} / {max_warnings}) = KICK")
        await ctx.send(embed = embed)
        return

    else:
        if 'Channel' in data:
            channel = await bot.fetch_channel(data['Channel'])
        
        else:
            channel = 'None'

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
        max_warnings = 5

        if warning >= max_warnings:
            if warning > max_warnings:
                warning = max_warnings
            else:
                warning = warning
            
            msg = await ctx.send(':information_source: User has reached the Max Warnings, Would you like to Proceed with Ban?')
            await msg.add_reaction('✅')
            await msg.add_reaction('🔴')
            valid_reactions = ['🔴','✅']
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in valid_reactions

            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            if reaction.emoji == '✅':
                pass

            elif reaction.emoji == '🔴':
                await ctx.send(':white_check_mark: No actions were taken')
                return

            data[guild][author]['Warnings'] = 0
            await member.ban(reason = '5/5 Warnings')
            with open('Config/warnings.json','w') as f:
                json.dump(data,f,indent = 4)
            
            embed=discord.Embed(color=0xf9231f)
            embed.set_author(name=f"{member} | Banned ({warning}/{max_warnings})")
            embed.add_field(name=f"Moderator:", value=f"{ctx.author}", inline=False)
            embed.add_field(name=f"Reason:", value=f"5 Warnings", inline=False)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)
    
        else:
            embed=discord.Embed(color=0xec8e8e)
            embed.set_author(name=f"{member} | Warned ({warning}/ {max_warnings})")
            embed.add_field(name=f"Moderator:", value=f"{ctx.author}", inline=False)
            embed.add_field(name=f"Reason:", value=f"{reason}", inline=False)
            embed.timestamp = datetime.datetime.utcnow()
            if not channel == 'None':
                await channel.send(embed = embed)
            else:
                await ctx.send(embed = embed)
            
            await ctx.message.add_reaction('✅')

        
@warn.error
async def warn_error(ctx,error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(':warning:  Oops You are missing the: `Ban Members` Permission.')

@bot.command()
async def removewarn(ctx,user:discord.User=None,*,reason:str = None):
    if user == None or reason == None:
        embed=discord.Embed(description="Usage: removewarn `<@user>` `<reason>`",color=0xff8083)
        embed.set_author(name="Removewarn Help")
        embed.set_footer(text="Removes 1 Warning from the User.")
        await ctx.send(embed = embed)
        return
    
    else:
        guild = str(ctx.guild.id)
        with open('Config/warnings.json','r') as f:
            data = json.load(f)
            
        if 'Channel' in data:
            channel = await bot.fetch_channel(data['Channel'])
        else:
            channel = 'None'

        author = str(user.id)
        if not guild in data:
            await ctx.send(':warning:  No Logs found for this GUILD.')
            return
            
        if not author in data[guild]:
            await ctx.send(":warning:  This user doesn't have any warnings.")
            return

        elif data[guild][author]['Warnings'] == 0:
            await ctx.send(":warning:  This user doesn't have any warnings.")
            return

        else:
            data[guild][author]['Warnings'] -= 1
            warning = data[guild][author]['Warnings'] - 1
            if warning == -1:
                wg = 0

            embed=discord.Embed(color=0x99ff00)
            embed.set_author(name=f"{user} | 1 warning Removed")
            embed.add_field(name="Moderator:", value=f"{ctx.author}", inline=False)
            embed.add_field(name="Reason:", value=f"{reason}", inline=False)
            embed.add_field(name="Active warnings:", value=f"{wg}", inline=False)
            embed.timestamp = datetime.datetime.utcnow()
            if not channel == 'None':
                await channel.send(embed = embed)
            else:
                await ctx.send(embed = embed)
            
        with open('Config/warnings.json','w') as f:
            json.dump(data,f,indent = 3)
        
        await ctx.message.add_reaction('✅')

@removewarn.error
async def removewarn_error(ctx,error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(':warning:  Oops You are missing the: `Ban Members` Permission.')

@bot.command()
async def setchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Command Usage: !setchannel `#channel (To Forward the Logs)`')
        return
    
    with open('Config/warnings.json') as f:
        w = json.load(f)
    
    w['Channel'] = channel.id
    with open('Config/warnings.json','w') as f:
        json.dump(w,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel Saved')

@has_permissions(manage_channels = True)
@bot.command(aliases = ['message'])
async def announce(ctx,channel:discord.TextChannel = None,*,msg:str = None):
    if not channel or not msg:
        await ctx.send(':information_source: Command Usage: !announce `#channel` `message`')
        return

    else:
        await channel.send(msg)
        await ctx.message.add_reaction('✅')
    

@has_permissions(ban_members=True)
@bot.command()
async def ban(ctx,member: discord.Member = None,*,reason:str = None):
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
            await ctx.send(f':warning: {member} **has been Banned**.')
        except Exception as e:
            await ctx.send(f':warning: {e}')
        
        with open('Config/warnings.json') as f:
            w = json.load(f)
        
        if not 'Channel' in w:
            return 
        else:
            channel = await bot.fetch_channel(w['Channel'])
            embed=discord.Embed(title=f"Member Banned",color=0xfc0303)
            embed.add_field(name="Member Name", value=f"{member}", inline=False)
            embed.add_field(name="Member ID", value=f"{member.id}", inline=False)
            embed.add_field(name= 'Moderator:',value = ctx.author)
            embed.timestamp = datetime.datetime.utcnow()
            await channel.send(embed = embed)

@has_permissions(kick_members=True)
@bot.command()
async def kick(ctx,member: discord.Member = None,*,reason:str = None):
    if member == None:
        embed=discord.Embed(description="Usage: kick `<@user>` `<reason>`",color=0xff8083)
        embed.set_author(name="Kick Help")
        embed.set_footer(text="Kicks the user from the Server.")
        await ctx.send(embed = embed)
        return

    else:
        try:
            await member.kick(reason = reason)
            await ctx.send(f':warning: {member} **has been kicked**.')
        except Exception as e:
            await ctx.send(f':warning: {e}')

        with open('Config/warnings.json') as f:
            w = json.load(f)

        if not 'Channel' in w:
            return 
        else:
            channel = await bot.fetch_channel(w['Channel'])
            embed=discord.Embed(title=f"Member Kicked",color=0xfc0303)
            embed.add_field(name="Member Name", value=f"{member}", inline=False)
            embed.add_field(name="Member ID", value=f"{member.id}", inline=False)
            embed.add_field(name= 'Moderator:',value = ctx.author)
            embed.timestamp = datetime.datetime.utcnow()
            await channel.send(embed = embed)

with open('Config/Token.json') as f:
    TOKEN = json.load(f)

bot.run(TOKEN['Token'])