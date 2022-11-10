import discord
from discord.ext import commands
import json
import random
import asyncio

class Join(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(aliases = ['j'])
    async def join(self,ctx):
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
            
        with open('Config/Bans.json') as f:
            bans = json.load(f)
        
        user = str(ctx.author.id)
        if user in bans:
            await ctx.send(f":warning: {ctx.author.mention} You don't have the access to use this command. **[BANNED]**")
            return
        with open('Config/Settings.json')  as f:
            settings = json.load(f)
        
        with open('Config/Cache.json') as f:
            cache = json.load(f)
        
        with open('Config/Queue.json') as f:
            queue = json.load(f)
        
        with open('Config/Maps.json') as f:
            maps = json.load(f)
        
        with open('Config/Data.json') as f:
            data = json.load(f)



        id_ = str(ctx.author.id)

        if not id_ in cache:
            await ctx.send(':warning: You are not registered currently. Please register using =register')
            return
        
        if 'Max_Players' in settings:
            max_players = settings['Max_Players']
        else:
            max_players = 4

        if not 'Game_Num' in cache:
            current_game = 1
        else:
            current_game = cache['Game_Num']                

        with open('Config/Games.json') as f:
            active_games = json.load(f)
        
        if not queue == {}:
            total_players = len(queue[str(current_game)])
        else:
            total_players = 0

        try:
            if not len(queue) == 0:
                    if int(id_) in queue[str(current_game)] and not len(queue[str(current_game)]) == max_players:
                        await ctx.send(f':warning: {ctx.author.mention} You already JOINED the queue. Use =leave to exit')
                        return
                    
                    if len(queue[str(current_game)]) == max_players:
                        if active_games[str(current_game)]['Status'] == 'PENDING':
                            await ctx.send(':warning: QUEUE is full. Wait for the current game picks to be finished.')
                            return
    
                    else:                   
                        queue[str(current_game)].append(int(id_))
                        total_players = len(queue[str(current_game)])
                        with open('Config/Queue.json','w') as f:
                            json.dump(queue,f,indent = 3)

                        msg = f'{total_players}/{max_players} - {ctx.author.mention} JOINED THE QUEUE'
                        embed = discord.Embed(color = discord.Color.dark_orange(),description = msg)
                        await ctx.send(embed = embed) 

                    if total_players == max_players:
                        while True:
                            if not active_games[str(current_game)]['Status'] == 'PENDING':
                                break
                        
                        await ctx.send('--- (Queue is full. Picking Teams) ---')

                        with open('Config/Queue.json') as f:
                            queue = json.load(f)
                        
                        if queue == {}:
                            return
                        
                        players = ''

                        temp_data = {}
                        for x in queue[str(current_game)]:
                            temp_data[str(x)] = data[str(x)]['Points']

                        captains_list = sorted(temp_data,key = temp_data.get,reverse = True)[:settings['Captain_%']]
                        Captain1 = int(random.choice(captains_list))
                        captains_list.remove(str(Captain1))
                        Captain2 = int(random.choice(captains_list))

                        queue[str(current_game)].remove(int(Captain1))
                        queue[str(current_game)].remove(int(Captain2))

                        for x in queue[str(current_game)]:
                            usr = await self.bot.fetch_user(x)
                            players += f"{usr.mention}\n"

                        active_games[str(current_game + 1)] = {}
                        active_games[str(current_game + 1)]['Map'] = list(maps)[settings['Current_Map']]
                        active_games[str(current_game + 1)]['Captain1'] = Captain1
                        active_games[str(current_game + 1)]['Captain2'] = Captain2
                        active_games[str(current_game + 1)]['Players'] = queue[str(current_game)]
                        queue.pop(str(current_game))
                        queue.pop('Channel')
                        queue.pop('Guild')
                        with open('Config/Queue.json','w') as f:
                            json.dump(queue,f,indent = 3)

                        active_games[str(current_game + 1)]['Status'] = 'PENDING'
                        active_games[str(current_game + 1)]['Pick_Amount'] = 1
                        active_games[str(current_game + 1)]['Pick_Turn'] = 'NAF'
                        Captain1 = await self.bot.fetch_user(Captain1)
                        Captain2 = await self.bot.fetch_user(Captain2)
                        active_games[str(current_game + 1)]['EDEN'] = []
                        active_games[str(current_game + 1)]['NAF'] = []
                        active_games[str(current_game + 1)]['Picked_EDEN'] = 0
                        active_games[str(current_game + 1)]['Picked_NAF'] = 0
                        with open('Config/Games.json','w') as f:
                            json.dump(active_games,f,indent = 3)
                        
                        await ctx.send(f':crown: {Captain1.mention} and :crown: {Captain2.mention} has been selected as a CAPTAIN for the GAME NUMBER: {current_game}')
                        await ctx.send(f'{Captain1.mention} turn to pick. **(PICKS LEFT: 1)**')
                        embed = discord.Embed(title = f"Game {current_game + 1} - Current Teams",color = discord.Color.green())
                        embed.add_field(name = 'Team1',value = f"Captain: {Captain1.mention}",inline=  False)
                        embed.add_field(name = 'Team2',value = f"Captain: {Captain2.mention}",inline=  False)
                        embed.add_field(name = 'Remaining Players',value = players)
                        await ctx.send(embed = embed)

                        cache['Game_Num'] += 1
                        with open('Config/Cache.json','w') as f:
                            json.dump(cache,f,indent = 3)    
                        
                        if settings['Current_Map'] + 1 >= len(maps):
                            settings['Current_Map'] = 0
                        else:
                            settings['Current_Map'] += 1
                            
                        with open("Config/Settings.json",'w') as f:
                            json.dump(settings,f,indent = 3)
                        
                        return
            else:                         
                queue[str(current_game)] = []
                queue[str(current_game)].append(int(id_))
                queue['Channel'] = ctx.channel.id
                queue['Guild'] = ctx.guild.id
                total_players = len(queue[str(current_game)])
                with open('Config/Queue.json','w') as f:
                    json.dump(queue,f,indent = 3)
                            
                msg = f'{total_players}/{max_players} - {ctx.author.mention} JOINED THE QUEUE'
                embed = discord.Embed(color = discord.Color.dark_orange(),description = msg)
                await ctx.send(embed = embed)   
                return
    
        except Exception:
            import traceback
            traceback.print_exc()
        
def setup(bot):
    bot.add_cog(Join(bot))