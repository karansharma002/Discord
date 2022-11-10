import asyncio
import discord
from discord.ext import commands
import json

page = {}
class leaderboard(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def leaderboard(self,ctx):
        with open('Config/Settings.json') as f:
            settings = json.load(f)
        

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')

        if role1 in ctx.author.roles or role2 in ctx.author.roles:
            pass

        elif 'Bot_Channel' in settings:
            if not ctx.channel.id == settings['Bot_Channel']:
                return
        else:
            await ctx.channel.send(':warning: Default BOT channel is not SET.')
            return

        global page
        
        with open('Config/Bans.json') as f:
            bans = json.load(f)
        
        user = str(ctx.author.id)
        if user in bans:
            await ctx.send(f":warning: {ctx.author.mention} You don't have the access to use this command. **[BANNED]**")
            return
        try:
            with open('Config/Data.json','r') as f:
                data = json.load(f)

            msg = ''
            high_score_list1 = sorted(data, key=lambda x : data[x].get('Points', 0), reverse=True)
            data_1 = []
            num = 1
            for i in range(0, len(high_score_list1), 10):
                for user in high_score_list1[i:i+10]:
                    usr = data[user]['Username']
                    wins = data[user]['Wins']
                    loss = data[user]['Loss']
                    points = data[user]['Points']
                    if loss == 0 and wins == 0:
                        win_rate = '0%'
                    else:
                        total_games = int(wins) + int(loss)
                        win_rate = round(int(wins) / int(total_games) * 100)
                        win_rate = str(win_rate) + '%' 

                    msg += f"**{num}:** {usr} - **Points:** {points} | **Wins**: {wins} | **Losses**: {loss} | **WIN RATE**: {win_rate}\n\n"
                    num += 1
                   
                data_1.append(msg)
                msg = ''
            
            
            page[str(ctx.author.id)] = 0
            embed = discord.Embed(
                title= ":crown: Global Leaderboard ",
                color= discord.Color.dark_orange(),
                description= data_1[page[str(ctx.author.id)]]
                )
            embed.set_footer(text = f'Showing Page: 1 of {len(data_1)}')
            
            sent_m = await ctx.send(embed = embed)
            await sent_m.add_reaction('⏮️')
            await sent_m.add_reaction('⬅️')
            await sent_m.add_reaction('➡️')
            await sent_m.add_reaction('⏭️')
            page[str(ctx.author.id)] = 0
            def check(reaction, user):
                return str(reaction.emoji) in ('⏮️','⬅️','➡️','⏭️') and str(user.id) in page

            while True:
                try:
                    reaction,user = await self.bot.wait_for('reaction_add',check = check,timeout = 40)
                except asyncio.TimeoutError:
                    print('timedout')
                    page.pop(str(ctx.author.id))
                    return
                if reaction.emoji == '⏮️':
                    await sent_m.remove_reaction(member = ctx.author,emoji = '⏮️')
                    if page[str(user.id)] == 0:
                        continue
                    else:
                        page[str(user.id)] = 0 
                        embed = discord.Embed(
                            title= ":crown: Global Leaderboard ",
                            color= discord.Color.dark_orange(),
                            description= data_1[page[str(user.id)]]
                            )
                        embed.set_footer(text = f'Showing Page: 1 of {len(data_1)}')
                        await sent_m.edit(embed = embed)
                
                elif reaction.emoji == '⏭️':
                    await sent_m.remove_reaction(member = ctx.author,emoji = '⏭️')
                    if page[str(user.id)] == len(data_1) - 1:
                        continue
                    else:
                        page[str(user.id)] = len(data_1) - 1
                        embed = discord.Embed(
                            title= ":crown: Global Leaderboard ",
                            color= discord.Color.dark_orange(),
                            description= data_1[page[str(user.id)]]
                            )
                        embed.set_footer(text = f'Showing Page: {len(data_1)} of {len(data_1)}')
                        await sent_m.edit(embed = embed)
                        

                elif reaction.emoji == '⬅️':
                    await sent_m.remove_reaction(member = ctx.author,emoji = '⬅️')
                    if page[str(user.id)] == 0:
                        continue

                    else:
                        
                        page[str(user.id)] -= 1
                        embed = discord.Embed(
                            title= ":crown: Global Leaderboard ",
                            color= discord.Color.dark_orange(),
                            description= data_1[page[str(user.id)]]
                            )
                        embed.set_footer(text = f'Showing Page: {page[str(user.id)] + 1} of {len(data_1)}')
                        await sent_m.edit(embed = embed)

                elif reaction.emoji == '➡️':
                    await sent_m.remove_reaction(member = ctx.author,emoji = '➡️')
                    if page[str(user.id)] == len(data_1) - 1:
                        continue
                    else:
                        page[str(user.id)] += 1
                        embed = discord.Embed(
                            title= ":crown: Global Leaderboard ",
                            color= discord.Color.dark_orange(),
                            description= data_1[page[str(user.id)]]
                            )
                        embed.set_footer(text = f'Showing Page: {page[str(user.id)] + 1} of {len(data_1)}')
                        await sent_m.edit(embed = embed)


        except:
            import traceback
            traceback.print_exc()

def setup(bot):
    bot.add_cog(leaderboard(bot))


