import discord
from discord.ext import commands
import json
import asyncio

class Lobby(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def max_players(self,ctx,val:int = None):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')

        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        if not val:
            await ctx.send(':information_source: Usage: =max_players `<TOTAL PLAYERS ALLOWED PER LOBBY>`')
            return
        
        with open('Config/Settings.json') as f:
            settings = json.load(f)
        
        settings['Max_Players'] = val

        with open('Config/Settings.json','w') as f:
            json.dump(settings,f,indent = 3)
        
        await ctx.send(f':white_check_mark: Max Players have been changed to: {val}')
    
    @commands.command()
    async def lobby(self, ctx):
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

        with open('Config/Games.json','r') as f:
            gm = json.load(f)
        
        game_num = ''
        for x in gm:
            if gm[x]['Status'] == 'PENDING':
                game_num = x
        
        if game_num == '':
            await ctx.send(':warning: No active games found.')
            return
            
        eden_players= ''
        naf_players = ''
        remaining_players = ''

        for x in gm[game_num]['EDEN']:                         
            usr = await self.bot.fetch_user(x)
            eden_players += f"{usr.mention}\n"
        
        for x in gm[game_num]['NAF']:
            usr = await self.bot.fetch_user(x)
            naf_players += f"{usr.mention}\n"   

        for x in gm[game_num]['Players']:
            usr = await self.bot.fetch_user(x)
            remaining_players += f"{usr.mention}\n"
        
        if eden_players == '':
            eden_players = 'NONE'
        
        if naf_players == '':
            naf_players = 'NONE'
        
        Captain1 = await self.bot.fetch_user(gm[game_num]['Captain1'])
        Captain2 = await self.bot.fetch_user(gm[game_num]['Captain2'])
        embed = discord.Embed(color = discord.Color.green(),title = f"Game #{game_num}")
        embed.add_field(name = F'Team NAF: {Captain1}',value = naf_players,inline = False)
        embed.add_field(name = F'Team EDEN: {Captain2}',value = eden_players,inline = False)
        embed.add_field(name = F'Remaining Players',value = remaining_players,inline = False)
        await ctx.send(embed = embed)
        
    @commands.command()
    async def scorechannel(self,ctx,channel:discord.TextChannel = None):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')

        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        if not channel:
            await ctx.send(':information_source: Usage: =scorechannel `<#channel>`')
            return
        
        with open('Config/Settings.json') as f:
            settings = json.load(f)
        
        settings['Score_Channel'] = channel.id

        with open('Config/Settings.json','w') as f:
            json.dump(settings,f,indent = 3)
        
        await ctx.send(f':white_check_mark: {channel.mention} has been marked as RESULTS Channel')

    @commands.command()
    async def noresult(self,ctx):
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
            
        with open('Config/Games.json') as f:
            games = json.load(f)
        
        msg = ''
        for x in games:
            if games[x]['Status'] == 'PENDING' or games[x]['Status'] == 'CONFIRMED':
                if games[x]['Status'] == 'PENDING':
                    Captain1 = await self.bot.fetch_user(games[x]['Captain1'])
                    Captain2 = await self.bot.fetch_user(games[x]['Captain2'])
                    msg += f"**Game Number:** `{x}` | **Status** - **PENDING PICKS** | **Captains:** `{Captain1}` | `{Captain2}`\n"
                else:
                    Captain1 = await self.bot.fetch_user(games[x]['Captain1'])
                    Captain2 = await self.bot.fetch_user(games[x]['Captain2'])
                    msg += f"**Game Number:** `{x}` | **Status** - **READY** | **Captains:** `{Captain1}` | `{Captain2}`\n"
                
        if not msg == '':
            embed = discord.Embed(color = discord.Color.green(),title = 'Pending Games',description = msg)
            await ctx.send(embed = embed)
        else:
            await ctx.send(':warning: No Pending GAMES Found')


    @commands.command(aliases = ['r'])
    async def report(self,ctx,game:str = None,*,team:str = None):
        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')
        role3 = discord.utils.get(ctx.guild.roles,name = 'Score Reporter')

        if role1 in ctx.author.roles:
            pass
        elif role2 in ctx.author.roles:
            pass
        elif role3 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        try:

            def check(message):
                return message.author == ctx.author
            
            msg = ''

            with open('Config/Games.json') as f:
                gm = json.load(f)
            
            with open('Config/Settings.json') as f:
                settings = json.load(f)
            
            with open('Config/Data.json') as f:
                data = json.load(f)
            
            with open('Config/Cache.json') as f:
                cache = json.load(f)

            if 'Win_Points' in settings:
                win_pts = settings['Win_Points']
            else:
                win_pts = 10

            if 'Lose_Points' in settings:
                lose_pts = settings['Lose_Points']
            else:
                lose_pts = 8

            if not game and not team:
                await ctx.send(':information_source: Usage: =r `<GAME NUMBER>` `<TEAM NAME>`')
                return

            else:
                if game in gm:
                    if not 'Score_Channel' in settings:
                        await ctx.send(':warning: Score Channel is not SET. Please set using ==scorechannel')
                        return

                    if gm[game]['Status'] == 'CONFIRMED' or gm[game]['Status'] == 'REPORTED':
                        if gm[game]['Status'] == 'REPORTED':
                            captain1 = await self.bot.fetch_user(gm[game]['Captain1'])
                            captain2 = await self.bot.fetch_user(gm[game]['Captain2'])
                            winner = gm[game]['WINNER']
                            if winner == 'EDEN':
                                team1 = 'EDEN'
                                team2 = 'NAF'
                                msg = f"{captain1.mention} (EDEN) has won against {captain2.mention} (NAF)"
                            elif winner == 'NAF':
                                team1 = 'NAF'
                                team2 = 'EDEN'
                                msg = f"{captain2.mention} (NAF) has won against {captain1.mention} (EDEN)"
                                
                            await ctx.send(msg)
                            await ctx.send('Would you like to change the RESULT? Reply with `yes/no` in the chat')
                            confirmation = await self.bot.wait_for('message',check = check)
                            if confirmation.content.lower() == 'yes':
                                if winner.upper() == 'EDEN':
                                    team1 = 'EDEN'
                                    team2 = 'NAF'
                                    msg = f"{captain2} (EDEN) has won against {captain1} (NAF)"
                                elif winner.upper() == 'NAF':
                                    team1 = 'NAF'
                                    team2 = 'EDEN'
                                    msg = f"{captain1} (NAF) has won against {captain2} (EDEN)"
                                else:
                                    await ctx.send(':warning: Invalid TEAM')
                                    return

                                for user1,user2 in zip(gm[game][team1],gm[game][team2]):
                                    username1 = str(user1) 
                                    username2 = str(user2)
                                    if not data[username1]['Points'] - win_pts < 0:
                                        data[username1]['Points'] -= win_pts
                                    else:
                                        data[username1]['Points'] = 0

                                    if not data[username1]['Wins'] - 1 < 0:
                                        data[username1]['Wins'] -= 1
                                    else:
                                        data[username1]['Wins'] = 0
                                    
                                    if not data[username2]['Points'] == 0:
                                        data[username2]['Points'] += lose_pts
                                    else:
                                        data[username2]['Points'] = 0
                                    
                                    if not data[username2]['Loss'] - 1 < 0:
                                        data[username2]['Loss'] -= 1
                                    else:
                                        data[username2]['Loss'] = 0

                                    with open('Config/Data.json','w') as f:
                                        json.dump(data,f,indent = 3)

                                with open('Config/Data.json','r') as f:
                                    data= json.load(f)
                            
                                if team1 == 'NAF':
                                    username1 = cache[str(gm[game]['Captain1'])]
                                    username2 = cache[str(gm[game]['Captain2'])]
                                else:
                                    username1 = cache[str(gm[game]['Captain2'])]
                                    username2 = cache[str(gm[game]['Captain1'])]  
                                
                                if not data[username1]['Points'] - win_pts < 0:
                                    data[username1]['Points'] -= win_pts
                                else:
                                    data[username1]['Points'] = 0


                                if not data[username1]['Wins'] - 1 < 0:
                                    data[username1]['Wins'] -= 1
                                else:
                                    data[username1]['Wins'] = 0                                
                                
                                if not data[username2]['Points'] == 0:
                                    data[username2]['Points'] += lose_pts
                                else:
                                    data[username2]['Points'] = 0 
                                    
                                if not data[username2]['Loss'] - 1 < 0:
                                    data[username2]['Loss'] -= 1
                                else:
                                    data[username2]['Loss'] = 0

                                with open('Config/Data.json','w') as f:
                                    json.dump(data,f,indent = 3)

                            else:
                                await ctx.send('-- Changes has been REVERTED -- ')
                                return
                        
                        channel = await self.bot.fetch_channel(settings['Score_Channel'])
                        captain1 = await self.bot.fetch_user(gm[game]['Captain1'])
                        captain2 = await self.bot.fetch_user(gm[game]['Captain2'])

                        with open('Config/Data.json','r') as f:
                            data= json.load(f)
                            
                        if team.upper() == 'EDEN':
                            team1 = 'EDEN'
                            team2 = 'NAF'
                            msg = f"Game Num: {game}| {captain2} (EDEN) has won against {captain1} (NAF)"
                        elif team.upper() == 'NAF':
                            team1 = 'NAF'
                            team2 = 'EDEN'
                            msg = f"Game Num: {game} | {captain1} (NAF) has won against {captain2} (EDEN)"
                        else:
                            await ctx.send(':warning: Invalid TEAM')
                            return
                    

                        winner_team = ''
                        loser_team = ''

                        for user1,user2 in zip(gm[game][team1],gm[game][team2]):
                            username1 = str(user1) 
                            username2 = str(user2)
                            usr = await self.bot.fetch_user(int(user1))
                            winner_team += f"{usr.mention}\n"
                            try:
                                await usr.edit(nick = f"[{data[username1]['Points'] + win_pts}] {username1} ({data[username1]['Region']})")
                            except Exception:
                                pass
                            data[username1]['Points'] += win_pts
                            data[username1]['Wins'] += 1
                            
                            usr2 = await self.bot.fetch_user(int(user2))
                            loser_team += f"{usr2.mention}\n"
                            if not data[username2]['Points'] - lose_pts < 0:
                                try:
                                    await usr2.edit(nick = f"[{data[username2]['Points'] - lose_pts}] {username2} ({data[username2]['Region']})")
                                except Exception:
                                    pass
                                data[username2]['Points'] -= lose_pts
                                data[username2]['Loss'] += 1
                            else:
                                try:
                                    await usr2.edit(nick = f"[0] {username2} ({data[username2]['Region']})")
                                except Exception:
                                    pass
                                    
                                data[username2]['Points'] = 0
                                data[username2]['Loss'] += 1
                        
                        if team1 == 'NAF':
                            username1 = cache[str(gm[game]['Captain1'])]
                            username2 = cache[str(gm[game]['Captain2'])]
                            usr = await self.bot.fetch_user(int(gm[game]['Captain1']))
                            usr2 = await self.bot.fetch_user(int(gm[game]['Captain2']))          
            
                        else:
                            username1 = cache[str(gm[game]['Captain2'])]
                            username2 = cache[str(gm[game]['Captain1'])]  
                            usr = await self.bot.fetch_user(int(gm[game]['Captain2']))
                            usr2 = await self.bot.fetch_user(int(gm[game]['Captain1']))          

                        try:
                            await usr.edit(nick = f"[{data[username1]['Points'] + win_pts}] {username1} ({data[username1]['Region']})")
                        except Exception:
                            pass

                        data[username1]['Points'] += win_pts
                        data[username1]['Wins'] += 1
                        
                        if not data[username2]['Points'] - lose_pts < 0:
                            try:
                                await usr2.edit(nick = f"[{data[username2]['Points'] - lose_pts}] {username2} ({data[username2]['Region']})")   
                            except Exception:
                                pass
                            data[username2]['Points'] -= lose_pts
                            data[username2]['Loss'] += 1
                        else:
                            try:
                                await usr2.edit(nick = f"[0] {username2} ({data[username2]['Region']})")
                            except Exception:
                                pass        
                            data[username2]['Points'] = 0     
                            data[username2]['Loss'] += 1 
                                   
                        with open('Config/Data.json','w') as f:
                            json.dump(data,f,indent = 3)
                        

                        embed = discord.Embed(color = discord.Color.dark_gold(),title = msg)
                        embed.add_field(name = f'Winning_Points +{win_pts}',value = winner_team,inline = False)
                        embed.add_field(name = f'Losing_Points -{lose_pts}',value = loser_team,inline= False)
                        await channel.send(embed = embed)
                        with open('Config/Games.json','r') as f:
                            gm = json.load(f)
                            
                        gm[game]['WINNER'] = team.upper()
                        gm[game]['Status'] = 'REPORTED'

                        await ctx.send(':white_check_mark: Result has been Announced')
                        await asyncio.sleep(1.5)
                        with open('Config/Games.json','w') as f:
                            json.dump(gm,f,indent = 3)

                    elif gm[game]['Status'] == 'CANCELLED':
                        await ctx.send(':information_source: This game is CANCELLED Already')
                        return
                else:
                    await ctx.send(':warning: Invalid Game Number')    
    
        except Exception:
            import traceback
            print(traceback.print_exc())



def setup(bot):
    bot.add_cog(Lobby(bot))