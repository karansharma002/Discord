import discord
from discord.ext import commands
import json
import datetime


class Game(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def m(self,ctx,game_num:int = None):
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
            gm = json.load(f)
                
        with open('Config/Cache.json') as f:
            cache = json.load(f)
        
        with open('Config/Settings.json') as f:
            settings = json.load(f)

        if 'Win_Points' in settings:
            win_pts = settings['Win_Points']
        else:
            win_pts = 10

        if 'Lose_Points' in settings:
            lose_pts = settings['Lose_Points']
        else:
            lose_pts = 8

        if not game_num:
            game_num = str(int(cache['Game_Num']))
        else:
            game_num = str(game_num)

        if not str(game_num) in gm:
            await ctx.send(':warning: No games found with the given number')
            return

        if gm[game_num]['Status'] == 'REPORTED':
            winner_team = ''
            loser_team = ''
            winner = gm[str(game_num)]['WINNER']
            captain1 = await self.bot.fetch_user(gm[str(game_num)]['Captain1'])
            captain2 = await self.bot.fetch_user(gm[str(game_num)]['Captain2'])
            if winner == 'EDEN':
                team1 = 'EDEN'
                team2 = 'NAF'
                msg = f"{captain2.mention} (EDEN) has won against {captain1.mention} (NAF)"
            elif winner == 'NAF':
                team1 = 'NAF'
                team2 = 'EDEN'
                msg = f"{captain1.mention} (NAF) has won against {captain2.mention} (EDEN)"
            
            for x,y in zip(gm[game_num][team1],gm[game_num][team2]):
                x = await self.bot.fetch_user(int(x))
                y = await self.bot.fetch_user(int(y))
                winner_team += f"{x.mention}\n"
                loser_team += f"{y.mention}\n"
            
            if team1 == 'NAF':
                winner_team += f'{captain1.mention}'
                loser_team += f'{captain2.mention}'
            
            else:
                winner_team += f'{captain2.mention}'
                loser_team += f'{captain1.mention}'        

            embed = discord.Embed(color = discord.Color.dark_gold(),description = msg,title = f"Game #{game_num} | STATUS: {gm[game_num]['Status']}")
            embed.add_field(name = f'Winning_Points +{win_pts}',value = winner_team,inline = False)
            embed.add_field(name = f'Losing_Points -{lose_pts}',value = loser_team,inline= False)
            embed.add_field(name = 'Map Played',value = gm[game_num]['Map'])
            await ctx.send(embed = embed)
        
        else:
            naf_players = ''
            eden_players = ''

            for x,y in zip(gm[game_num]['NAF'],gm[game_num]['EDEN']):
                x = await self.bot.fetch_user(int(x))
                y = await self.bot.fetch_user(int(y))

                naf_players += f'{x.mention}\n'
                eden_players += f'{y.mention}\n'
                
            Captain1 = await self.bot.fetch_user(gm[game_num]['Captain1'])
            Captain2 = await self.bot.fetch_user(gm[game_num]['Captain2'])
            embed = discord.Embed(color = discord.Color.green(),title = f"Game #{game_num} | STATUS: {gm[game_num]['Status']}")
            embed.add_field(name = F'Team NAF: {Captain1}',value = naf_players,inline = False)
            embed.add_field(name = F'Team EDEN: {Captain2}',value = eden_players,inline = False)
            embed.add_field(name = 'Map Played',value = gm[game_num]['Map'])
            await ctx.send(embed = embed)

    @commands.command()
    async def cancel(self,ctx,num:int = None):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        role2 = discord.utils.get(ctx.guild.roles,name = 'Moderator')

        if role1 in ctx.author.roles:
            pass
        elif role2 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        if not num:
            await ctx.send(':information_source: Usage: =cancel `<GAME NUMBER>`')
            return
        
        with open('Config/Games.json') as f:
            gm = json.load(f)
        
        if not str(num) in gm:
            await ctx.send(f':warning: No active games found with the Game Number: {num}')
            return
        else:
            gm[str(num)]['Status'] = 'CANCELLED'
            
            with open('Config/Games.json','w') as f:
                json.dump(gm,f,indent = 3)
            
            await ctx.send(f':white_check_mark: Game Number `{num}` has been CANCELLED')
    
    @commands.command()
    async def captain(self,ctx,val:int = None):

        role1 = discord.utils.get(ctx.guild.roles,name = 'Admin')
        if role1 in ctx.author.roles:
            pass
        else:
            await ctx.send(":tools: You don't have the sufficient permissions for using this command.")
            return

        if not val:
            await ctx.send(':information_source: Usage: =captain `<Number of Players to Pick from>')
            return
        
        with open('Config/Settings.json') as f:
            settings = json.load(f)
        
        settings['Captain_%'] = val

        with open('Config/Settings.json','w') as f:
            json.dump(settings,f,indent = 3)
        
        await ctx.send(':white_check_mark: Settings has been SAVED')
    
    @commands.command(aliases = ['p'])
    async def pick(self,ctx,user2:discord.User = None):
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
            
        channel = str(ctx.channel.id)

        with open('Config/Games.json') as f:
            gm = json.load(f)
        
        with open('Config/Data.json') as f:
            data = json.load(f)
        
        with open('Config/Cache.json') as f:
            cache = json.load(f)
        
        with open('Config/Settings.json') as f:
            settings = json.load(f)
        
        try:
                
            max_players = settings['Max_Players']
            id_ = ctx.author.id
            game_num = ''
            turn = ''
            for x in gm:
                if id_ == gm[x]['Captain1'] and gm[x]['Status'] == 'PENDING':
                    game_num = x
                    break 
                elif  id_ == gm[x]['Captain2'] and gm[x]['Status'] == 'PENDING':
                    game_num = x
                    break 

            if not user and not game_num == '':
                await ctx.send(':information_source: Usage: =pick `<@user>`')
                return

            if game_num == '':
                await ctx.send(":warning: You don't have the permissions to use this COMMAND")
                return
            

            print(gm[game_num]['Status'])

            if gm[game_num]['Status'] != 'PENDING':
                await ctx.send(':warning: This game is either CONFIRMED or Not Authorised')
                return
            
            Pick_Turn = gm[game_num]['Pick_Turn']
            Pick_Amount = gm[game_num]['Pick_Amount']
            Picked_EDEN = gm[game_num]['Picked_EDEN']
            Picked_NAF = gm[game_num]['Picked_NAF']
            if gm[game_num]['Pick_Turn'] == 'NAF' and not id_ == gm[game_num]['Captain1']:
                if Pick_Turn == 'EDEN':
                    available_amount = Pick_Amount - Picked_EDEN
                
                else:
                    available_amount = Picked_EDEN - Picked_NAF

                await ctx.send(f":warning: It's Team {Pick_Turn} turn to PICK The player. `(Turns: {available_amount})`")
                return
            
            elif gm[game_num]['Pick_Turn'] == 'EDEN' and not id_ == gm[game_num]['Captain2']:
                if Pick_Turn == 'EDEN':
                    available_amount = Pick_Amount - Picked_EDEN
                
                else:
                    available_amount = Picked_EDEN - Picked_NAF

                await ctx.send(f":warning: It's Team {Pick_Turn} turn to PICK The player. `(Turns: {available_amount})`")
                return   

            else:
                if Pick_Amount == 1 and Pick_Turn == 'NAF':
                    if not user2.id in gm[game_num]['Players']:
                        await ctx.send(':warning: The mentioned player is not in the QUEUE')
                        return
                    
                    if user2.id in gm[game_num]['EDEN'] or user2.id in gm[game_num]['NAF']:
                        await ctx.send(':warning: This player is already PICKED.')
                        return

                    gm[game_num]['Pick_Amount'] = 2
                    gm[game_num]['Pick_Turn'] = 'EDEN'
                    gm[game_num]['Players'].remove(user2.id)
                    gm[game_num][Pick_Turn].append(user2.id)
                    await ctx.send(f"> {ctx.author.mention} has PICKED `({user2})`")
                    captain2 = await self.bot.fetch_user(gm[game_num]['Captain2'])
                    if not len(gm[game_num]['Players']) == 1:
                        await ctx.send(f'{captain2.mention} TURN to pick the player. **(TURNS: 2)**')
                    with open('Config/Games.json','w') as f:
                        json.dump(gm,f,indent = 3)

                    with open('Config/Games.json','w') as f:
                        json.dump(gm,f,indent = 3)
                        
                    with open('Config/Games.json','r') as f:
                        gm = json.load(f)
                    
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
                    
                    if not len(gm[game_num]['Players']) == 1:
                        Captain1 = await self.bot.fetch_user(gm[game_num]['Captain1'])
                        Captain2 = await self.bot.fetch_user(gm[game_num]['Captain2'])
                        embed = discord.Embed(color = discord.Color.green(),title = f"Game #{game_num}")
                        embed.add_field(name = F'Team NAF: {Captain1}',value = naf_players,inline = False)
                        embed.add_field(name = F'Team EDEN: {Captain2}',value = eden_players,inline = False)
                        embed.add_field(name = F'Remaining Players',value = remaining_players,inline = False)
                        await ctx.send(embed = embed)
                        return

                    else:
                        await ctx.send('------ `(Finalizing the game)` ------')

                        # len(gm[game_num]['Players']) == 1:
                        len1 = len(gm[game_num]['EDEN'])
                        len2 = len(gm[game_num]['NAF'])
                        player_to_move = gm[game_num]['Players'][0]
                        if len1 > len2:
                            gm[game_num]['NAF'].append(player_to_move)
                        
                        else:
                            gm[game_num]['EDEN'].append(player_to_move)

                        gm[game_num]['Players'].remove(player_to_move)
                        with open('Config/Games.json','w') as f:
                            json.dump(gm,f,indent = 3)
                        
                        with open('Config/Games.json','r') as f:
                            gm = json.load(f)
                        

                        EU_Players = 0
                        NA_Players = 0
                        SA_Players = 0 
                        EDENPLAYERS = ''
                        NAFPLAYERS = ''

                        ct1 = gm[game_num]['Captain1']
                        ct2 = gm[game_num]['Captain2']
                        ct1 = cache[str(ct1)]
                        ct2 = cache[str(ct2)]

                        players_region = {}
                        if data[ct1]['Region'] in players_region:
                            players_region[data[ct1]['Region']] += 1
                        else:
                            players_region[data[ct1]['Region']] = 1

                        if data[ct2]['Region'] in players_region:
                            players_region[data[ct2]['Region']] += 1
                        else:
                            players_region[data[ct2]['Region']] = 1

                        for x in gm[game_num]['EDEN']:
                            username = cache[str(x)]
                            region = data[username]['Region']
                            if not region in players_region:
                                players_region[region] = 1
                            
                            else:
                                players_region[region] += 1

                            
                            usr = await self.bot.fetch_user(x)
                            EDENPLAYERS += f"{usr.mention}\n"
                        
                        for x in gm[game_num]['NAF']:
                            username = cache[str(x)]
                            region = data[username]['Region']
                            if not region in players_region:
                                players_region[region] = 1
                            
                            else:
                                players_region[region] += 1

                            usr = await self.bot.fetch_user(x)
                            NAFPLAYERS += f"{usr.mention}\n"                   

                            
                        Captain1 = await self.bot.fetch_user(gm[game_num]['Captain1'])
                        Captain2 = await self.bot.fetch_user(gm[game_num]['Captain2'])
                        embed = discord.Embed(color = discord.Color.green(),title = f"Game #{game_num}")
                        embed.add_field(name = F'Team NAF: {Captain1}',value = NAFPLAYERS,inline = False)
                        embed.add_field(name = F'Team EDEN: {Captain2}',value = EDENPLAYERS,inline = False)
                        for x in players_region:
                            embed.add_field(name = x + ' Players',value = players_region[x],inline = False)
                        embed.add_field(name = 'Room',value = 'IA PUGS',inline = False)
                        embed.add_field(name = 'Password',value = 'MOM',inline = False)
                        embed.add_field(name = 'Lobby Size',value = len(gm[game_num]['EDEN']) + len(gm[game_num]['NAF']) + 2,inline = False)
                        embed.add_field(name = 'Map',value = gm[game_num]['Map'])
                        await ctx.send(embed = embed)
                        gm[game_num]['Status'] = 'CONFIRMED'
                        with open('Config/Games.json','w') as f:
                            json.dump(gm,f,indent = 3)
                        
                        
                        with open('Config/Cache.json','w') as f:
                            json.dump(cache,f,indent = 3)
                        
                        return

                else:
                    if Pick_Turn == 'EDEN':
                        if not user2.id in gm[game_num]['Players']:
                            await ctx.send(':warning: The mentioned player is not in the QUEUE')
                            return
                        
                        if user2.id in gm[game_num]['EDEN'] or user2.id in gm[game_num]['NAF']:
                            await ctx.send(':warning: This player is already PICKED.')
                            return
                        gm[game_num]['Picked_EDEN'] += 1
                        gm[game_num]['Players'].remove(user2.id)
                        gm[game_num][Pick_Turn].append(user2.id)
                        player = await self.bot.fetch_user(user2.id)
                        await ctx.send(f"> {ctx.author.mention} has PICKED `({player})`")
                        Captain1 = await self.bot.fetch_user(gm[game_num]['Captain1'])
                        Captain2 = await self.bot.fetch_user(gm[game_num]['Captain2'])
                        if Pick_Amount == gm[game_num]['Picked_EDEN']:
                            gm[game_num]['Pick_Turn'] = 'NAF'
                            gm[game_num]['Picked_EDEN'] = 0
                            Captain1 = await self.bot.fetch_user(gm[game_num]['Captain1'])
                            if not len(gm[game_num]['Players']) == 1:
                                await ctx.send(f"It's {Captain1.mention} turn to PICK now. **(PICKS LEFT: 2)**")
                        else:
                            if not len(gm[game_num]['Players']) == 1:
                                await ctx.send(f"It's {Captain2.mention} turn to PICK now. **(PICKS LEFT: 1)**")

                        with open('Config/Games.json','w') as f:
                            json.dump(gm,f,indent = 3)
                        
                        with open('Config/Games.json','r') as f:
                            gm = json.load(f)
                        
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

                        if not len(gm[game_num]['Players']) == 1:
                            Captain1 = await self.bot.fetch_user(gm[game_num]['Captain1'])
                            Captain2 = await self.bot.fetch_user(gm[game_num]['Captain2'])
                            embed = discord.Embed(color = discord.Color.green(),title = f"Game #{game_num}")
                            embed.add_field(name = F'Team NAF: {Captain1}',value = naf_players,inline = False)
                            embed.add_field(name = F'Team EDEN: {Captain2}',value = eden_players,inline = False)
                            embed.add_field(name = F'Remaining Players',value = remaining_players,inline = False)
                            await ctx.send(embed = embed)
                            return

                        else:# len(gm[game_num]['Players']) == 1:
                            await ctx.send('------ `(Finalizing the game)` ------')
                            len1 = len(gm[game_num]['EDEN'])
                            len2 = len(gm[game_num]['NAF'])
                            player_to_move = gm[game_num]['Players'][0]
                            if len1 > len2:
                                gm[game_num]['NAF'].append(player_to_move)
                            
                            else:
                                gm[game_num]['EDEN'].append(player_to_move)
                            gm[game_num]['Players'].remove(player_to_move)
                            with open('Config/Games.json','w') as f:
                                json.dump(gm,f,indent = 3)
                            
                            with open('Config/Games.json','r') as f:
                                gm = json.load(f)
                            

                            EDENPLAYERS = ''
                            NAFPLAYERS = ''
                            ct1 = gm[game_num]['Captain1']
                            ct2 = gm[game_num]['Captain2']
                            ct1 = cache[str(ct1)]
                            ct2 = cache[str(ct2)]

                            players_region = {}
                            if data[ct1]['Region'] in players_region:
                                players_region[data[ct1]['Region']] += 1
                            else:
                                players_region[data[ct1]['Region']] = 1

                            if data[ct2]['Region'] in players_region:
                                players_region[data[ct2]['Region']] += 1
                            else:
                                players_region[data[ct2]['Region']] = 1
                                
                            for x in gm[game_num]['EDEN']:
                                username = cache[str(x)]
                                region = data[username]['Region']
                                if not region in players_region:
                                    players_region[region] = 1
                                
                                else:
                                    players_region[region] += 1
                                    
                                usr = await self.bot.fetch_user(x)
                                EDENPLAYERS += f"{usr.mention}\n"
                            
                            for x in gm[game_num]['NAF']:
                                username = cache[str(x)]
                                region = data[username]['Region']
                                if not region in players_region:
                                    players_region[region] = 1
                                
                                else:
                                    players_region[region] += 1
                                

                                usr = await self.bot.fetch_user(x)
                                NAFPLAYERS += f"{usr.mention}\n"                   

                                
                            
                            Captain1 = await self.bot.fetch_user(gm[game_num]['Captain1'])
                            Captain2 = await self.bot.fetch_user(gm[game_num]['Captain2'])
                            embed = discord.Embed(color = discord.Color.green(),title = f"Game #{game_num}")
                            embed.add_field(name = F'Team NAF: {Captain1}',value = NAFPLAYERS,inline = False)
                            embed.add_field(name = F'Team EDEN: {Captain2}',value = EDENPLAYERS,inline = False)
                            for x in players_region:
                                embed.add_field(name = x + ' Players',value = players_region[x],inline = False)
                            embed.add_field(name = 'Room',value = 'IA PUGS',inline = False)
                            embed.add_field(name = 'Password',value = 'MOM',inline = False)
                            embed.add_field(name = 'Lobby Size',value = len(gm[game_num]['EDEN']) + len(gm[game_num]['NAF']) + 2,inline = False)
                            embed.add_field(name = 'Map',value = gm[game_num]['Map'])
                            await ctx.send(embed = embed)
                            gm[game_num]['Status'] = 'CONFIRMED'
                            with open('Config/Games.json','w') as f:
                                json.dump(gm,f,indent = 3)
                            
                            
                            with open('Config/Cache.json','w') as f:
                                json.dump(cache,f,indent = 3)
                            
                            return
                                
                    elif Pick_Turn == 'NAF':
                        if not user2.id in gm[game_num]['Players']:
                            await ctx.send(':warning: The mentioned player is not in the QUEUE')
                            return
                        
                        if user2.id in gm[game_num]['EDEN'] or user2.id in gm[game_num]['NAF']:
                            await ctx.send(':warning: This player is already PICKED.')
                            return
                        if not user2.id in gm[game_num]['Players']:
                            await ctx.send(':warning: The mentioned player is not in the QUEUE')
                            return
                        
                        if user2.id in gm[game_num]['EDEN'] or user2.id in gm[game_num]['NAF']:
                            await ctx.send(':warning: This player is already PICKED.')
                            return

                        gm[game_num]['Picked_NAF'] += 1
                        gm[game_num]['Players'].remove(user2.id)
                        gm[game_num][Pick_Turn].append(user2.id)
                        player = await self.bot.fetch_user(user2.id)
                        await ctx.send(f"> {ctx.author.mention} has PICKED `({player})`")
                        Captain1 = await self.bot.fetch_user(gm[game_num]['Captain1'])
                        Captain2 = await self.bot.fetch_user(gm[game_num]['Captain2'])
                        if Pick_Amount == gm[game_num]['Picked_NAF']:
                            gm[game_num]['Pick_Turn'] = 'EDEN'
                            gm[game_num]['Picked_NAF'] = 0
                            Captain2 = await self.bot.fetch_user(gm[game_num]['Captain2'])
                            if not len(gm[game_num]['Players']) == 1:
                                await ctx.send(f"It's {Captain2.mention} turn to PICK now. **(PICKS LEFT: 2)**")
                        else:
                            if not len(gm[game_num]['Players']) == 1:
                                await ctx.send(f"It's {Captain1.mention} turn to PICK now. **(PICKS LEFT: 1)**")

                        with open('Config/Games.json','w') as f:
                            json.dump(gm,f,indent = 3)
                        with open('Config/Games.json','r') as f:
                            gm = json.load(f)
                        
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
                        
                        if not len(gm[game_num]['Players']) == 1:
                            Captain1 = await self.bot.fetch_user(gm[game_num]['Captain1'])
                            Captain2 = await self.bot.fetch_user(gm[game_num]['Captain2'])
                            embed = discord.Embed(color = discord.Color.green(),title = f"Game #{game_num}")
                            embed.add_field(name = F'Team NAF: {Captain1}',value = naf_players,inline = False)
                            embed.add_field(name = F'Team EDEN: {Captain2}',value = eden_players,inline = False)
                            embed.add_field(name = F'Remaining Players',value = remaining_players,inline = False)
                            await ctx.send(embed = embed)
                            return

                        else:# len(gm[game_num]['Players']) == 1:
                            await ctx.send('------ `(Finalizing the game)` ------')
                            len1 = len(gm[game_num]['EDEN'])
                            len2 = len(gm[game_num]['NAF'])
                            player_to_move = gm[game_num]['Players'][0]
                            if len1 > len2:
                                gm[game_num]['NAF'].append(player_to_move)
                            
                            else:
                                gm[game_num]['EDEN'].append(player_to_move)
                            gm[game_num]['Players'].remove(player_to_move)
                            with open('Config/Games.json','w') as f:
                                json.dump(gm,f,indent = 3)
                            
                            with open('Config/Games.json','r') as f:
                                gm = json.load(f)
                            
                            EDENPLAYERS = ''
                            NAFPLAYERS = ''

                            ct1 = gm[game_num]['Captain1']
                            ct2 = gm[game_num]['Captain2']
                            ct1 = cache[str(ct1)]
                            ct2 = cache[str(ct2)]

                            players_region = {}
                            if data[ct1]['Region'] in players_region:
                                players_region[data[ct1]['Region']] += 1
                            else:
                                players_region[data[ct1]['Region']] = 1

                            if data[ct2]['Region'] in players_region:
                                players_region[data[ct2]['Region']] += 1
                            else:
                                players_region[data[ct2]['Region']] = 1

                            for x in gm[game_num]['EDEN']:
                                username = cache[str(x)]
                                region = data[username]['Region']
                                if not region in players_region:
                                    players_region[region] = 1
                                
                                else:
                                    players_region[region] += 1
                                
                                
                                usr = await self.bot.fetch_user(x)
                                EDENPLAYERS += f"{usr.mention}\n"
                            
                            for x in gm[game_num]['NAF']:
                                username = cache[str(x)]
                                region = data[username]['Region']
                                if not region in players_region:
                                    players_region[region] = 1
                                
                                else:
                                    players_region[region] += 1
                                

                                usr = await self.bot.fetch_user(x)
                                NAFPLAYERS += f"{usr.mention}\n"                   

                                
                            
                            Captain1 = await self.bot.fetch_user(gm[game_num]['Captain1'])
                            Captain2 = await self.bot.fetch_user(gm[game_num]['Captain2'])
                            embed = discord.Embed(color = discord.Color.green(),title = f"Game #{game_num}")
                            embed.add_field(name = F'Team NAF: {Captain1}',value = NAFPLAYERS,inline = False)
                            embed.add_field(name = F'Team EDEN: {Captain2}',value = EDENPLAYERS,inline = False)
                            for x in players_region:
                                embed.add_field(name = x + ' Players',value = players_region[x],inline = False)
                            embed.add_field(name = 'Room',value = 'IA PUGS',inline = False)
                            embed.add_field(name = 'Password',value = 'MOM',inline = False)
                            embed.add_field(name = 'Lobby Size',value = len(gm[game_num]['EDEN']) + len(gm[game_num]['NAF']) + 2,inline = False)
                            embed.add_field(name = 'Map',value = gm[game_num]['Map'])
                            await ctx.send(embed = embed)
                            gm[game_num]['Status'] = 'CONFIRMED'
                            with open('Config/Games.json','w') as f:
                                json.dump(gm,f,indent = 3)  

                            
                            with open('Config/Cache.json','w') as f:
                                json.dump(cache,f,indent = 3)
                            
                            return

                    else:

                        if not user2.id in gm[game_num]['Players']:
                            await ctx.send(':warning: The mentioned player is not in the QUEUE')
                            return
                        
                        if user2.id in gm[game_num]['EDEN'] or user2.id in gm[game_num]['NAF']:
                            await ctx.send(':warning: This player is already PICKED.')
                            return
                        if len(gm[game_num]['Players']) == 1:
                            await ctx.send('------ `(Finalizing the game)` ------')
                            len1 = len(gm[game_num]['EDEN'])
                            len2 = len(gm[game_num]['NAF'])
                            player_to_move = gm[game_num]['Players'][0]
                            if len1 > len2:
                                gm[game_num]['NAF'].append(player_to_move)
                            
                            else:
                                gm[game_num]['EDEN'].append(player_to_move)
                            
                            gm[game_num]['Players'].remove(player_to_move)
                            
                            with open('Config/Games.json','w') as f:
                                json.dump(gm,f,indent = 3)
                            
                            with open('Config/Games.json','r') as f:
                                gm = json.load(f)
                            

                            EU_Players = 0
                            NA_Players = 0
                            SA_Players = 0 
                            EDENPLAYERS = ''
                            NAFPLAYERS = ''
                            ct1 = gm[game_num]['Captain1']
                            ct2 = gm[game_num]['Captain2']
                            ct1 = cache[str(ct1)]
                            ct2 = cache[str(ct2)]
                            players_region = {}
                            if data[ct1]['Region'] in players_region:
                                players_region[data[ct1]['Region']] += 1
                            else:
                                players_region[data[ct1]['Region']] = 1

                            if data[ct2]['Region'] in players_region:
                                players_region[data[ct2]['Region']] += 1
                            else:
                                players_region[data[ct2]['Region']] = 1

                            for x in gm[game_num]['EDEN']:
                                username = cache[str(x)]
                                region = data[username]['Region']
                                if not region in players_region:
                                    players_region[region] = 1
                                
                                else:
                                    players_region[region] += 1
                                
                                
                                usr = await self.bot.fetch_user(x)
                                EDENPLAYERS += f"{usr.mention}\n"
                            
                            for x in gm[game_num]['NAF']:
                                username = cache[str(x)]
                                region = data[username]['Region']
                                if not region in players_region:
                                    players_region[region] = 1
                                
                                else:
                                    players_region[region] += 1
                                
                                usr = await self.bot.fetch_user(x)
                                NAFPLAYERS += f"{usr.mention}\n"                   

                                
                            
                            Captain1 = await self.bot.fetch_user(gm[game_num]['Captain1'])
                            Captain2 = await self.bot.fetch_user(gm[game_num]['Captain2'])
                            embed = discord.Embed(color = discord.Color.green(),title = f"Game #{game_num}")
                            embed.add_field(name = F'Team NAF: {Captain1}',value = NAFPLAYERS,inline = False)
                            embed.add_field(name = F'Team EDEN: {Captain2}',value = EDENPLAYERS,inline = False)
                            for x in players_region:
                                embed.add_field(name = x + ' Players',value = players_region[x],inline = False)
                            embed.add_field(name = 'Room',value = 'IA PUGS',inline = False)
                            embed.add_field(name = 'Password',value = 'MOM',inline = False)
                            embed.add_field(name = 'Lobby Size',value = len(gm[game_num]['EDEN']) + len(gm[game_num]['NAF']) + 2,inline = False)
                            embed.add_field(name = 'Map',value = gm[game_num]['Map'])
                            await ctx.send(embed = embed)
                            gm[game_num]['Status'] = 'CONFIRMED'
                            
                            with open('Config/Games.json','w') as f:
                                json.dump(gm,f,indent = 3)
                            
                            
                            with open('Config/Cache.json','w') as f:
                                json.dump(cache,f,indent = 3)
        except Exception:
            import traceback
            traceback.print_exc()
    
def setup(bot):
    bot.add_cog(Game(bot))