import discord
from discord.ext import commands
import json

class leaderboard(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def leaderboard(self,ctx):
        try:

            with open('Config/data.json','r') as f:
                users = json.load(f)

            high_score_list1 = sorted(users, key=lambda x : users[x].get('money', 0), reverse=True)
            msg1 = ''
            msg2 = ''
            for number,user in enumerate(high_score_list1):
                author = await self.bot.fetch_user(int(user))
                number += 1
                xp = users[user]['experience']
                level = users[user]['level']
                msg1 += f"**‣ {number}**. {author} ⁃\nLevel: **{level}** | XP: **{xp}** | Money: $**{users[user]['money']}**\n\n"
                if number == 8:
                    break
                    #msg2 += f"**‣ {number}**. {author} ⁃\nLevel: **{level}** | XP: **{xp}** | Money: **{users[user].get('money', 0)}**\n\n"
                else:
                    number += 1

            embed = discord.Embed(
                title= ":money_with_wings: Global Leaderboard ",
                color= 0x05ffda,
                description= msg1
                )
            
            with open('Test.txt','w') as f:
                f.write(msg1)
                
            await ctx.send(embed = embed)
        
        except Exception as e:
            await ctx.send(str(e))

def setup(bot):
    bot.add_cog(leaderboard(bot))


