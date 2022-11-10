import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
class setlogs(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def __init__(self, bot):
        self.bot = bot
    
    @has_permissions(administrator = True)
    @commands.command()
    async def setlogs(self,ctx,val2:str = None,val:int = None):
        def check(message):
            return message.author == ctx.author
        guild = str(ctx.guild.id)
        with open('Config/guildlogs.json','r') as f:
            data = json.load(f)
    
        if val == None:
            try:
                mute_logs = data[guild]['Mute Logs']
            except KeyError:
                data[guild]['Mute Logs'] = 'Disabled'
                mute_logs = 'Disabled'
                with open('Config/guildlogs.json','w') as f:
                    json.dump(data,f,indent = 3)    
            try:
                warning_logs = data[guild]['Warning Logs']
            except KeyError:
                data[guild]['Warning Logs'] = 'Disabled'
                warning_logs = 'Disabled'
            
                with open('Config/guildlogs.json','w') as f:
                    json.dump(data,f,indent = 3) 
            
            try:
                message_delete_logs = data[guild]['Message Delete']
            except KeyError:
                data[guild]['Message Delete'] = 'Disabled'
                message_delete_logs = 'Disabled'

                with open('Config/guildlogs.json','w') as f:
                    json.dump(data,f,indent = 3) 

            try:
                message_edit_logs = data[guild]['Message Edit']
            except KeyError:
                data[guild]['Message Edit'] = 'Disabled'
                message_edit_logs = 'Disabled'
                with open('Config/guildlogs.json','w') as f:
                    json.dump(data,f,indent = 3)       

            embed=discord.Embed(title=":gear: To Setup the Logs: Use +setlogs `<enable/disable>` `<number>`", color=0x70f0b4)
            embed.set_author(name="Logs Menu")
            embed.add_field(name="1: User Ban / Unban Logs:", value=f"Status: `{data[guild]['User Logs']}`", inline=False)
            embed.add_field(name="2: Role Create/Delete Logs:", value=f"Status: `{data[guild]['Role Logs']}`", inline=False)
            embed.add_field(name="3: Channel Create/Delete Logs:", value=f"Status: `{data[guild]['Channel Logs']}`", inline=False)
            embed.add_field(name="4: User Mute/Unmute Logs:", value=f"Status: `{mute_logs}`", inline=False)
            embed.add_field(name="5: User Warning Logs:", value=f"Status: `{warning_logs}`", inline=False)
            embed.add_field(name="6: Message Delete Logs:", value=f"Status: `{message_delete_logs}`", inline=False)
            embed.add_field(name="7: Message Edit Logs:", value=f"Status: `{message_edit_logs}`", inline=False)
            embed.set_footer(text = 'Note: Mute-Unmute / Warnings logs will only work with Fillory Command.')
            await ctx.send(embed = embed)
        
        elif val2.lower() == 'enable':
            if val == 1:
                if data[guild]['User Logs'] == 'Enabled':
                    await ctx.send('<a:alert_1:677763786664312860> User `Ban/Unban` Logs are already enabled.\nUse: +setlogs `disable` `2` To disable.')
                    return
                else:
                    await ctx.send(':tada: **Sweet, Specify the Channel ID (The logs should be sent to):**\n(`Mention The Channel)`')
                    msg = await self.bot.wait_for('message',check = check)
                    if msg.content.startswith('<#'):
                        a = msg.content
                        a = a.replace("<","")
                        a = a.replace(">","")
                        a = a.replace("#","")
                    else:
                        a = int(msg.content)
                    await ctx.send(f"<a:ln:678647491624960000> User `Ban/Unban` Logs have Enabled\n:information_source: Make sure I have the permission to Message in given channel.\n:information_source: To Disable **USE**: +setlogs disable 1")
                    data[guild]['User Logs'] = 'Enabled'
                    data[guild]['User ID'] = a
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)
            
            elif val == 2:
                if data[guild]['Role Logs'] == 'Enabled':
                    await ctx.send('<a:alert_1:677763786664312860> Role `Create/Delete` Logs are already enabled.\nUse: +setlogs <disable> <2> To disable.')
                    return
                else:
                    await ctx.send(':tada: **Sweet, Specify the Channel ID (The logs should be sent to):**\n(`Mention The Channel)`')
                    msg = await self.bot.wait_for('message',check = check)
                    if msg.content.startswith('<#'):
                        a = msg.content
                        a = a.replace("<","")
                        a = a.replace(">","")
                        a = a.replace("#","")
                    else:
                        a = int(msg.content)
                    await ctx.send(f"<a:ln:678647491624960000> Role `Create/Delete` Logs have Enabled\n:information_source: Make sure I have the permission to Message in given channel.\n:information_source: To Disable **USE**: +setlogs disable 2")
                    data[guild]['Role Logs'] = 'Enabled'
                    data[guild]['Role ID'] = a
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)

            elif val == 3:
                if data[guild]['Channel Logs'] == 'Enabled':
                    await ctx.send('<a:alert_1:677763786664312860> Channel `Create/Delete` Logs are already enabled.\nUse: +setlogs `disable` `3` To disable.')
                    return
                else:
                    await ctx.send(':tada: **Sweet, Specify the Channel ID (The logs should be sent to):**\n(`Mention The Channel)`')
                    msg = await self.bot.wait_for('message',check = check)
                    if msg.content.startswith('<#'):
                        a = msg.content
                        a = a.replace("<","")
                        a = a.replace(">","")
                        a = a.replace("#","")
                    else:
                        a = int(msg.content)
                    await ctx.send(f"<a:ln:678647491624960000> Channel `Create/Delete` Logs have Enabled\n:information_source: Make sure I have the permission to Message in given channel.\n:information_source: To Disable **USE**: +setlogs disable 3")
                    data[guild]['Channel Logs'] = 'Enabled'
                    data[guild]['Channel ID'] = a
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)

            elif val == 4:

                if data[guild]['Mute Logs'] == 'Enabled':
                    await ctx.send('<a:alert_1:677763786664312860> `User Mute/Unmute` Logs are already enabled.\nUse: +setlogs `disable` `4` To disable.')
                    return
   
                else:
                    await ctx.send(':tada: **Sweet, Specify the Channel ID (The logs should be sent to):**\n(`Mention The Channel)`')
                    msg = await self.bot.wait_for('message',check = check)
                    if msg.content.startswith('<#'):
                        a = msg.content
                        a = a.replace("<","")
                        a = a.replace(">","")
                        a = a.replace("#","")
                    else:
                        a = int(msg.content)
                    await ctx.send(f"<a:ln:678647491624960000>  `User Mute/Unmute` Logs have Enabled\n:information_source: Make sure I have the permission to Message in given channel.\n:information_source: To Disable **USE**: +setlogs disable 4")
                    data[guild]['Mute Logs'] = 'Enabled'
                    data[guild]['Mute ID'] = a
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)

            elif val == 5:
                if data[guild]['Warning Logs'] == 'Enabled':
                    await ctx.send('<a:alert_1:677763786664312860> `User Warning` Logs are already enabled.\nUse: +setlogs `disable` `5` To disable.')
                    return
                else:
                    await ctx.send(':tada: **Sweet, Specify the Channel ID (The logs should be sent to):**\n(`Mention The Channel)`')
                    msg = await self.bot.wait_for('message',check = check)
                    if msg.content.startswith('<#'):
                        a = msg.content
                        a = a.replace("<","")
                        a = a.replace(">","")
                        a = a.replace("#","")
                    else:
                        a = int(msg.content)
                    await ctx.send(f"<a:ln:678647491624960000> Channel `Create/Delete` Logs have Enabled\n:information_source: Make sure I have the permission to Message in given channel.\n:information_source: To Disable **USE**: +setlogs disable 5")
                    data[guild]['Warning Logs'] = 'Enabled'
                    data[guild]['Warning ID'] = a
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)


            elif val == 6:
                if data[guild]['Message Delete'] == 'Enabled':
                    await ctx.send('<a:alert_1:677763786664312860> `Message Delete` Logs are already enabled.\nUse: +setlogs `disable` `6` To disable.')
                    return
                else:
                    await ctx.send(':tada: **Sweet, Specify the Channel ID (The logs should be sent to):**\n(`Mention The Channel)`')
                    msg = await self.bot.wait_for('message',check = check)
                    if msg.content.startswith('<#'):
                        a = msg.content
                        a = a.replace("<","")
                        a = a.replace(">","")
                        a = a.replace("#","")
                    else:
                        a = int(msg.content)
                    await ctx.send(f"<a:ln:678647491624960000> Message `Delete` Logs have Enabled\n:information_source: Make sure I have the permission to Message in given channel.\n:information_source: To Disable **USE**: +setlogs disable 6")
                    data[guild]['Message Delete'] = 'Enabled'
                    data[guild]['Message Delete ID'] = a
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)

            elif val == 7:
                if data[guild]['Message Edit'] == 'Enabled':
                    await ctx.send('<a:alert_1:677763786664312860> `Message Edit` Logs are already enabled.\nUse: +setlogs `disable` `7` To disable.')
                    return
                else:
                    await ctx.send(':tada: **Sweet, Specify the Channel ID (The logs should be sent to):**\n(`Mention The Channel)`')
                    msg = await self.bot.wait_for('message',check = check)
                    if msg.content.startswith('<#'):
                        a = msg.content
                        a = a.replace("<","")
                        a = a.replace(">","")
                        a = a.replace("#","")
                    else:
                        a = int(msg.content)
                    await ctx.send(f"<a:ln:678647491624960000> Message `Edit` Logs have Enabled\n:information_source: Make sure I have the permission to Message in given channel.\n:information_source: To Disable **USE**: +setlogs disable 7")
                    data[guild]['Message Edit'] = 'Enabled'
                    data[guild]['Message Edit ID'] = a
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)
            else:
                await ctx.send('<a:alert_1:677763786664312860> Invalid Log Number. `(Use +setlogs and specify the correct one)`')

        elif val2.lower() == 'disable':
            if val == 1:
                if data[guild]['User Logs'] == 'Enabled':
                    await ctx.send(f"<a:ln:678647491624960000> This Feature has been Disabled.")
                    data[guild]['User Logs'] = 'Disabled'
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)
                    
                elif data[guild]['User Logs'] == 'Disabled':
                    await ctx.send(f"<a:alert_1:677763786664312860> This Feature is already Disabled.\n:information_source: To Enable **USE**: +setlogs <enable> 1")
                    return	

            elif val == 2:
                if data[guild]['Role Logs'] == 'Enabled':
                    await ctx.send(f"<a:ln:678647491624960000> This Feature has been Disabled.")
                    data[guild]['Role Logs'] = 'Disabled'
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)
                    
                elif data[guild]['Role Logs'] == 'Disabled':
                    await ctx.send(f"<a:alert_1:677763786664312860> This Feature is already Disabled.\n:information_source: To Enable **USE**: +setlogs <enable> 2")
                    return	

            elif val == 3:
                if data[guild]['Channel Logs'] == 'Enabled':
                    await ctx.send(f"<a:ln:678647491624960000> This Feature has been Disabled.")
                    data[guild]['Channel Logs'] = 'Disabled'
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)
                    
                elif data[guild]['Channel Logs'] == 'Disabled':
                    await ctx.send(f"<a:alert_1:677763786664312860> This Feature is already Disabled.\n:information_source: To Enable **USE**: +setlogs <enable> 3")
                    return	


            elif val == 4:
                if data[guild]['Mute Logs'] == 'Enabled':
                    await ctx.send(f"<a:ln:678647491624960000> This Feature has been Disabled.")
                    data[guild]['Mute Logs'] = 'Disabled'
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)
                    
                elif data[guild]['Mute Logs'] == 'Disabled':
                    await ctx.send(f"<a:alert_1:677763786664312860> This Feature is already Disabled.\n:information_source: To Enable **USE**: +setlogs <enable> 4")
                    return	


            elif val == 5:
                if data[guild]['Warning Logs'] == 'Enabled':
                    await ctx.send(f"<a:ln:678647491624960000> This Feature has been Disabled.")
                    data[guild]['Warning Logs'] = 'Disabled'
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)
                    
                elif data[guild]['Warning Logs'] == 'Disabled':
                    await ctx.send(f"<a:alert_1:677763786664312860> This Feature is already Disabled.\n:information_source: To Enable **USE**: +setlogs <enable> 6")
                    return	

            elif val == 6:
                if data[guild]['Message Delete'] == 'Enabled':
                    await ctx.send(f"<a:ln:678647491624960000> This Feature has been Disabled.")
                    data[guild]['Message Delete'] = 'Disabled'
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)
                    
                elif data[guild]['Message Delete'] == 'Disabled':
                    await ctx.send(f"<a:alert_1:677763786664312860> This Feature is already Disabled.\n:information_source: To Enable **USE**: +setlogs <enable> 6")
                    return	
            elif val == 7:
                if data[guild]['Message Edit'] == 'Enabled':
                    await ctx.send(f"<a:ln:678647491624960000> This Feature has been Disabled.")
                    data[guild]['Message Edit'] = 'Disabled'
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)
                    
                elif data[guild]['Message Edit'] == 'Disabled':
                    await ctx.send(f"<a:alert_1:677763786664312860> This Feature is already Disabled.\n:information_source: To Enable **USE**: +setlogs <enable> 7")
                    return	
            else:
                await ctx.send('<a:alert_1:677763786664312860> Invalid Log Number. `(Use +setlogs and specify the correct one)`')
    @setlogs.error
    async def setlogs_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> You are missing the: `Administrator` Permission.')
def setup(bot):
    bot.add_cog(setlogs(bot))
