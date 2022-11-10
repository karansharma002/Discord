import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class Tickets(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def setup_ticket(self, ctx,channel:discord.TextChannel = None):
        pass


def setup(bot):
    bot.add_cog(Tickets(bot))
