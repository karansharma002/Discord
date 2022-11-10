import discord
from discord.ext import commands
import json
from discord.ext.commands import has_permissions

class leaderboard(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def leaderboard(self,ctx):
        with open('Config/Winners.json','r') as f:
            users = json.load(f)

        high_score_list1 = sorted(users, key=lambda x : users[x].get('Games Won', 0), reverse=True)
        msg1 = ''
        for number,user in enumerate(high_score_list1):
            msg1 += '**‣ {0}**. {1} - Games Won: **{2}** \n'.format(number+1,user, users[user].get('Games Won', 0))
            number += 1
            if number == 11:
                break
            else:
                number += 1
        
        embed = discord.Embed(
            title= ":crown: Top Winners",
            color= 0x05ffda,
            description= msg1
            )
        
        await ctx.send(embed = embed)
    
    @has_permissions(administrator = True)
    @commands.command()
    async def getwinnersfile(self,ctx):
        await ctx.send(file = discord.File('Config/Winners.json'))


def setup(bot):
    bot.add_cog(leaderboard(bot))


