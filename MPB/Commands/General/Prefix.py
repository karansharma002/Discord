import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json

class prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @has_permissions(manage_guild = True)
    @commands.command()
    async def prefix(self,ctx,*,val:str = None):
        with open('Config/prefixes.json','r') as f:
            data = json.load(f)

        if val == None:
            try:
                a = data[str(ctx.guild.id)]['Prefix']
            except KeyError:
                a = "!"
            await ctx.send(f':information_source: (`{ctx.guild})` **Prefix is:** (`{a})`\n:information_source: **Use:** **prefix** `<newprefix>` **to change.**')

        elif not val == None:
            guild = str(ctx.guild.id)
            if not guild in data:
                data[guild] = {}
            data[str(ctx.guild.id)]['Prefix'] = val
            await ctx.send(f'<a:ln:678647491624960000> ** Server Prefix Has been Changed**\n<a:ln:678647491624960000> **Your New Prefix Is:** (`{val}`)')
            with open('Config/prefixes.json','w') as f:
                json.dump(data,f,indent = 4)

    @prefix.error
    async def prefix_error(self,ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('<a:alert_1:677763786664312860> You are missing the: `Manage Server` Permission.')



def setup(bot):
    bot.add_cog(prefix(bot))

