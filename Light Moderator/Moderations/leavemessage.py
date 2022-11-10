import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
class leavemessage(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def __init__(self, bot):
        self.bot = bot
    
    @has_permissions(administrator = True)
    @commands.command()
    async def leavemessage(self,ctx,val:str= None):
        guild = str(ctx.guild.id)
        with open('Config/prefixes.json','r') as f:
            data = json.load(f)

        def check(message):
            return message.author == ctx.author
        if val == None:
                embed=discord.Embed(description="Usage: leavemessage `<enable / disable>`",color=0xff8083)
                embed.set_author(name="Leavemessage Help", icon_url="https://i.imgur.com/wHD6EKK.jpg")
                embed.set_footer(text="Delivers a Message when user Leaves.")
                await ctx.send(embed = embed)
                return

        if val.lower() == 'enable':
            if data[guild]['Leave_Message'] == 'Disabled':				
                await ctx.send(':tada: **Sweet, Specify the Channel ID:** (`Mention The Channel)`')
                msg = await self.bot.wait_for('message',check = check)
                if msg.content.startswith('<#'):
                    a = msg.content
                    a = a.replace("<","")
                    a = a.replace(">","")
                    a = a.replace("#","")
                else:
                    a = int(msg.content)
                
                await ctx.send(f"<a:ln:678647491624960000> User Leave Messages are Enabled\n:information_source: Make sure I have the permission to Message in given channel.\n:information_source: To Disable **USE**: +leavemessage <disable>")
                data[guild]['Leave_Message'] = 'Enabled'
                data[guild]['Leave ID'] = a
                with open('Config/prefixes.json','w') as f:
                    json.dump(data,f,indent = 4)
            else:
                await ctx.send(f"<a:alert_1:677763786664312860> This Feature is already Enabled.\n:information_source: To Disable **USE**: +leavemessage <disable>")
                return
        
        elif val.lower() == 'disable':
            if data[guild]['Leave_Message'] == 'Enabled':
                await ctx.send(f"<a:ln:678647491624960000> This Feature has been Disabled.")
                data[guild]['Leave_Message'] = 'Disabled'
                with open('Config/prefixes.json','w') as f:
                    json.dump(data,f,indent = 4)
                
            elif data[guild]['Leave_Message'] == 'Disabled':
                await ctx.send(f"<a:alert_1:677763786664312860> This Feature is already Disabled.\n:information_source: To Enable **USE**: +leavemessage <enable>")
                return	

    @leavemessage.error
    async def leavemessage_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> You are missing the: `Administrator` Permission.')

def setup(bot):
    bot.add_cog(leavemessage(bot))
