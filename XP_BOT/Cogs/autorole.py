import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
import json
class autorole(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def __init__(self, bot):
        self.bot = bot
    
    @has_permissions(manage_roles = True)
    @commands.command()
    async def autorole(self,ctx,*,val:str = None):
        with open('Config/prefixes.json','r') as f:
            data = json.load(f)
        guild = str(ctx.guild.id)
        if val == None:
            embed=discord.Embed(description="Usage: autorole `<role name>`",color=0xff8083)
            embed.set_author(name="Autorole Help", icon_url="https://i.imgur.com/wHD6EKK.jpg")
            embed.set_footer(text="Enable Autorole | To Disable Use: autorole <disable>")
            await ctx.send(embed = embed)
            return
        
        elif val.lower() == 'disable':
            if data[guild]['Autorole'] == 'Disabled':
                await ctx.send('<a:alert_1:677763786664312860> This Feature is already Disabled.')
                return

            data[guild]['Autorole'] = 'Disabled'
            with open('Config/prefixes.json','w') as f:
                json.dump(data,f,indent = 4)
            
            await ctx.send('<a:ln:678647491624960000> **Autorole** has been Disabled')
            return

        else:
            if get(ctx.guild.roles,name = val):
                if not guild in data:
                    data[guild] = {}
                else:
                    data[guild]['Autorole'] = val
                    with open('Config/prefixes.json','w') as f:
                        json.dump(data,f,indent = 4)
            #PASS JSON DOCUMENT HERE AND D UMP THE ROLE.
                    await ctx.send(f'<a:ln:678647491624960000> **Autorole** has been enabled\n<a:ln:678647491624960000> **Users** now will receive the role upon joining.\n:information_source: **Make sure My Role is Above than** `{val}` **Role**.\n:information_source: To **DISABLE** Use: +autorole `<disable>`')
            else:
                await ctx.send(':warning: Role not Found!')
                return

    @autorole.error
    async def autorole_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> You are missing the: `Manage Roles` Permission.')

def setup(bot):
    bot.add_cog(autorole(bot))
