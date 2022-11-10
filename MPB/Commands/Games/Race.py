import discord
from discord.ext import commands
import random
import json
import asyncio
from Modules.Double_Coins import send_coin
from Modules.Fine import send_fine
from Modules.Cooldown import add_cooldown
from Modules.Cooldown import get_cooldown
import secrets

# GLOBAL DICTIONARY TO STORE THE DATA INDIVIDUALLY FOR THE GUILDS INSTEAD OF THE LOCAL VARIABLES
# FOR MORE PERSONALISED EXPERIENCE.

users_data = {}
def send_road(num):
    if num == 6:
        return ':arrow_left: :arrow_left: :arrow_left: :arrow_left: :arrow_left: :arrow_left: '
    elif num == 5:
        return ':arrow_left: :arrow_left: :arrow_left: :arrow_left: :arrow_left: '

    elif num == 4:
        return ':arrow_left: :arrow_left: :arrow_left: :arrow_left: '
    elif num == 3:
        return ':arrow_left: :arrow_left: :arrow_left: '
    elif num == 2:
        return ':arrow_left: :arrow_left: '
    elif num == 1:
        return ':arrow_left:'

class race(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def race(self,ctx,user:discord.User = None,bet:int= None):

        guild = str(ctx.guild.id)

        if not guild in users_data:
            users_data[guild] = {}
        author = str(ctx.author.id)
        command = 'race'
        if not get_cooldown(command,author) == '':
            print(get_cooldown(command,author))
            await ctx.send(get_cooldown(command,author))
            return
            
        add_cooldown(command,author,6)
        def check(message):
            return message.author == user

        with open('Config/data.json','r') as f:
            data = json.load(f)
        with open('Config/prefixes.json','r') as f:
            pf = json.load(f)
            
        prefix = pf[str(ctx.guild.id)]['Prefix']
        if user == None or bet== None:
            embed=discord.Embed(color=0xadb0f5)
            embed.set_author(name="Car Race")
            embed.add_field(name="Info:", value="Challenge your friends in the car racing.", inline=False)
            embed.add_field(name="Usage:", value=f"{prefix}race `<@user>` `<bet amount>`", inline=False)
            embed.set_footer(text="The game will begin once opponent accepts your offer.")
            await ctx.send(embed = embed)
        
        else:
            amount = bet
            author = str(ctx.author.id)
            author2 = str(user.id)
            if author in users_data[guild] or author2 in users_data[guild]:
                await ctx.send('<:info:833301110835249163> There is an active GAME already. Wait for it to finish!!')
                return

            if not author2 in data:
                await ctx.send("<a:alert:833301110587785267> The opponent isn't a registered user")
                return

            if ctx.author.id == user.id:
                await ctx.send('<a:alert:833301110587785267> You cannot race against yourself.')
                return
            
            elif not user in ctx.guild.members:
                await ctx.send('<a:alert:833301110587785267> That player is not part of this server.')
                return

            elif bet > data[author]['money']:
                await ctx.send("<a:alert:833301110587785267> You don't have the required money")
                return

            elif bet > data[author2]['money']:
                await ctx.send("<a:alert:833301110587785267> The opponent doesn't have the required amount")
                return

            elif bet <= 0:
                await ctx.send('<a:alert:833301110587785267> The bet amount should be greater than ZERO.')
                return
            
            else:
                await ctx.send(f'{user.mention} Would you accept the Race Duel? `(Yes/No)` `(TIMEOUT in 20 Seconds)`')
                try:
                    msg = await self.bot.wait_for('message',check = check,timeout = 20)
                    if msg.content.lower() == 'yes':
                        pass

                    elif msg.content.lower() == 'no':
                        await ctx.send('Race Cancelled.')
                        return
                    else:
                        await ctx.send('Invalid Reply, The Race has been cancelled.')
                        return

                except asyncio.TimeoutError:
                    await ctx.send(f'Race Cancelled, {user.name} Failed to accept the duel. ')
                    return

            
            users_data[guild][author] = 6
            users_data[guild][author2] = 6
    
            msg = f'**Ground:**\n\n:checkered_flag: {send_road(users_data[guild][author])} :red_car:\n:checkered_flag: {send_road(users_data[guild][author2])} :blue_car:\n'
            embed=discord.Embed(description = msg,color=0xfffa5c)
            embed.set_author(name=f"{ctx.author.name} VS {user.name}")
            embed.add_field(name = f'{ctx.author.name}',value = '**Red Car** :red_car:')
            embed.add_field(name = f'{user.name}',value = '**Blue Car** :blue_car:')
            a = await ctx.send(embed = embed)
            while True:
                await asyncio.sleep(1)
                chn = secrets.randbelow(100)
                if chn < 50:
                    users_data[guild][author] -= 1

                elif chn > 50:              
                    users_data[guild][author2] -= 1

                elif chn == 50:
                    users_data[guild][author] -= 1
                    users_data[guild][author2] -= 1
            
                if users_data[guild][author] <= 0 and users_data[guild][author2] > 0:
                    from Modules.Winp import win_percent
                    game = 'Race'
                    value = 'win'
                    win_percent(author,game,value)

                    game = 'Race'
                    value = 'lose'
                    win_percent(author2,game,value)

                    msg = f'**Ground:**\n\n:checkered_flag: :red_car:\n:checkered_flag: {send_road(users_data[guild][author2])} :blue_car:\n'
                    embed2=discord.Embed(description = msg,color=0x00ff6e)
                    embed2.set_author(name=f"{ctx.author} Won the Game", icon_url=ctx.author.avatar_url)
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            data = json.load(f)
                        embed2.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        data[author]['money'] += amount + profit - fine
                        data[author2]['money'] -= amount
                    else:
                        data[author]['money'] += amount + profit 
                        data[author2]['money'] -= amount
                    if not profit == 0:
                        embed2.add_field(name="Credited ", value=f"${amount * 2} + {profit} (Coins X)", inline=False)
                    else:
                        embed2.add_field(name="Credited:", value=f"${amount * 2}", inline=False)
                    
                    await a.edit(embed = embed2)
                    with open("Config/data.json","w") as f:
                        json.dump(data,f,indent = 3)
                    
                    break

                elif users_data[guild][author2] <= 0 and users_data[guild][author] > 0:

                    from Modules.Winp import win_percent
                    game = 'Race'
                    value = 'win'
                    win_percent(author2,game,value)

                    game = 'Race'
                    value = 'lose'
                    win_percent(author,game,value)

                    msg = f'**Ground:**\n\n:checkered_flag: {send_road(users_data[guild][author])} :red_car:\n:checkered_flag: :blue_car:\n'
                    embed2=discord.Embed(description = msg,color=0x00ff6e)
                    embed2.set_author(name=f"{user} Won the Game", icon_url=user.avatar_url)
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            data = json.load(f)
                        embed2.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        data[author2]['money'] += amount + profit - fine
                        data[author]['money'] -= amount
                    else:
                        data[author2]['money'] += amount + profit 
                        data[author]['money'] -= amount
                    if not profit == 0:
                        embed2.add_field(name="Credited ", value=f"${amount * 2} + {profit} (Coins X)", inline=False)
                    else:
                        embed2.add_field(name="Credited:", value=f"${amount * 2}", inline=False)
                    
                    await a.edit(embed = embed2)
                    with open("Config/data.json","w") as f:
                        json.dump(data,f,indent = 3)
                    break

                else:                  
                    msg = f'**Ground:**\n\n:checkered_flag: {send_road(users_data[guild][author])} :red_car:\n:checkered_flag: {send_road(users_data[guild][author2])} :blue_car:\n'
                    embed2=discord.Embed(description = msg,color=0xfffa5c)
                    embed2.set_author(name=f"{ctx.author.name} VS {user.name}")
                    embed2.add_field(name = f'{ctx.author.name}',value = '**Red Car** :red_car:')
                    embed2.add_field(name = f'{user.name}',value = '**Blue Car** :blue_car:')
                    await a.edit(embed = embed2)
                    
            users_data[guild].pop(author)
            users_data[guild].pop(author2)

def setup(bot):
    bot.add_cog(race(bot))
