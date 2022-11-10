import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json

class welcomemessage(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def __init__(self, bot):
        self.bot = bot
    
    @has_permissions(administrator = True)
    @commands.command()
    async def welcomemessage(self,ctx,val:str= None):
        with open('Config/guildlogs.json','r') as f:
            data = json.load(f)

            guild = str(ctx.guild.id)
            def check(message):
                return message.author == ctx.author
            if val == None:
                embed=discord.Embed(description="Usage: welcomemessage `<enable / disable>`",color=0xff8083)
                embed.set_author(name="Welcome Message Help")
                embed.set_footer(text="Delivers a Message when user Joins.")
                await ctx.send(embed = embed)
                return

        if val.lower() == 'enable':
            try:
                if data[guild]['Join_Message'] == 'Disabled':
                    await ctx.send(':tada: **Sweet, Specify the Channel ID:** (`Mention The Channel)`')
                    msg = await self.bot.wait_for('message',check = check)
                    if msg.content.startswith('<#'):
                        a = msg.content
                        a = a.replace("<","")
                        a = a.replace(">","")
                        a = a.replace("#","")
                    else:
                        a = int(msg.content)
                    
                    await ctx.send(f"<a:ln:678647491624960000> Welcome Messages are Enabled\n:information_source: Make sure I have the permission to Message in given channel.\n:information_source: To Disable **USE**: welcomemessage disable")
                    if not guild in data:
                        data[guild] = {}

                    data[guild]['Join_Message'] = 'Enabled'
                    data[guild]['Join ID'] = a
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)
            
            except KeyError:
                    await ctx.send(':tada: **Sweet, Specify the Channel ID:** (`Mention The Channel)`')
                    msg = await self.bot.wait_for('message',check = check)
                    if msg.content.startswith('<#'):
                        a = msg.content
                        a = a.replace("<","")
                        a = a.replace(">","")
                        a = a.replace("#","")
                    else:
                        a = int(msg.content)
                    
                    await ctx.send(f"<a:ln:678647491624960000> Welcome Messages are Enabled\n:information_source: Make sure I have the permission to Message in given channel.\n:information_source: To Disable **USE**: welcomemessage disable")
                    if not guild in data:
                        data[guild] = {}

                    data[guild]['Join_Message'] = 'Enabled'
                    data[guild]['Join ID'] = a
                    with open('Config/guildlogs.json','w') as f:
                        json.dump(data,f,indent = 4)               
            else:
                await ctx.send(f"<a:alert_1:677763786664312860> This Feature is already Enabled.\n:information_source: To Disable **USE**: welcomemessage <disable>")
                return
    
        elif val.lower() == 'disable':
            if data[guild]['Join_Message'] == 'Enabled':
                await ctx.send(f"<a:ln:678647491624960000> This Feature has been Disabled.")
                data[guild]['Join_Message'] = 'Disabled'
                with open('Config/guildlogs.json','w') as f:
                    json.dump(data,f,indent = 4)

            elif data[guild]['Join_Message'] == 'Disabled':
                await ctx.send(f"<a:alert_1:677763786664312860> This Feature is already Disabled.\n:information_source: To Enable **USE**: welcomemessage enable")
                return	
        

    @welcomemessage.error
    async def welcomemessage_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> You are missing the: `Administrator` Permission.')
    
    @has_permissions(administrator = True)
    @commands.command()
    async def usermessage(self,ctx,val:str = None):
        with open('Config/guildlogs.json') as f:
            data = json.load(f)
        
        guild = str(ctx.guild.id)

        if val == None:
            await ctx.send('Usage: usermessage `<enable/disable` `(Sends a Message to user on JOIN`')
            return
        else:
            if val.lower() == 'enable':
                try:
                    data[guild]['User_Message'] = 'Enabled'
                except KeyError:
                    data[guild] = {}
                    data[guild]['User_Message'] = 'Enabled'
                
                await ctx.send(':white_check_mark:  User Join Messages has been Enabled.')
            
            elif val.lower() == 'disable':
                try:
                    data[guild]['User_Message'] = 'Disabled'
                except KeyError:
                    data[guild] = {}
                    data[guild]['User_Message'] = 'Disabled'             
                
                await ctx.send(':white_check_mark:  User Join Messages has been Disabled.')
            
            with open('Config/guildlogs.json','w') as f:
                json.dump(data,f,indent = 3)

    @usermessage.error
    async def usermessage_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> You are missing the: `Administrator` Permission.')

def setup(bot):
    bot.add_cog(welcomemessage(bot))
