import discord
from discord.ext import commands
import random
import json
import asyncio
from Modules.Fine import send_fine
from Modules.Double_Coins import send_coin
from Modules.Cooldown import add_cooldown
from Modules.Cooldown import get_cooldown
class russian_roulette(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(aliases = ['rr'])
    async def russianroulette(self,ctx,user:discord.User = None,bet:int = None):
        author = str(ctx.author.id)
        command = 'russianroulette'
        if not get_cooldown(command,author) == '':
            await ctx.send(get_cooldown(command,author))
            return
            
        add_cooldown(command,author,6)
        with open('Config/data.json','r') as f:
            data = json.load(f)
        
        def check(message):
            return message.author == user
        with open('Config/prefixes.json','r') as f:
            pf = json.load(f)
            
        prefix = pf[str(ctx.guild.id)]['Prefix']      
        if user == None or bet == None:
            embed=discord.Embed(color=0x785417)
            embed.set_author(name="Russian Roulette")
            embed.add_field(name="Information:", value="Both players has 1 bullet in the GUN.\nThe cylinder will be spinned.\nBoth person will point the trigger at their head.\nThe unluckiest person will DIE.", inline=True)
            embed.add_field(name="Usage:", value=f"{prefix}rr `<@user>` `<bet amount>`", inline=False)
            embed.set_footer(text="The player will have 20 seconds to accept the offer.")
            await ctx.send(embed = embed)
            return

        else:
            author2 = str(user.id)
            if ctx.author.id == user.id:
                await ctx.send('<a:alert:833301110587785267> You cannot play against yourself.')
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
                await ctx.send(f'{user.mention} Would you accept the Offer? `(Yes/No)` `(TIMEOUT in 20 Seconds)`')
                try:
                    msg = await self.bot.wait_for('message',check = check,timeout = 20)
                    if msg.content.lower() == 'yes':
                        pass

                    elif msg.content.lower() == 'no':
                        await ctx.send('The offer has been Cancelled.')
                        return
                    else:
                        await ctx.send('Invalid Reply, The offer has been cancelled.')
                        return

                except asyncio.TimeoutError:
                    await ctx.send(f'Offer Cancelled, {user.name} Failed to accept the within given time. ')
                    return

            embed=discord.Embed(color=0xfffa5c)
            embed.set_author(name=f"{ctx.author} VS {user}")
            embed.set_footer(text="Starting the Game in 5 Seconds.")
            a = await ctx.send(embed = embed)

            while True:
                await asyncio.sleep(5)
                if random.randint(1,100) >= 70:
                    from Modules.Winp import win_percent
                    game = 'Russian_Roulette'
                    value = 'win'
                    win_percent(author2,game,value)

                    game = 'Russian_Roulette'
                    value = 'lose'
                    win_percent(author,game,value)

                    msg = f'**{ctx.author.name}** `takes out the gun from a backpack and squeezes the trigger, and gets Hit.` :fire: :skull:'
                    embed = discord.Embed(description = msg,color = 0x00ff08)
                    
                    embed.set_author(name=f"{user} Won the Game", icon_url=user.avatar_url)

                    profit = send_coin(author2,bet)
                    if not send_fine(author2,bet) == 0:
                        fine = send_fine(author2,bet)
                        with open('Config/data.json','r') as f:
                            data = json.load(f)
                        embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        data[author2]['money'] += bet + profit - fine
                        data[author]['money'] -= bet
                    else:
                        data[author2]['money'] += bet + profit  
                        data[author]['money'] -= bet
                    if not profit == 0:
                        embed.add_field(name="Credited ", value=f"${bet*2} + {profit} (Coins X)", inline=False)
                    else:
                        embed.add_field(name="Credited:", value=f"${bet*2}", inline=False)

                    with open("Config/data.json","w") as f:
                        json.dump(data,f,indent = 3)

                    await a.edit(embed=embed)
                    return
 
                elif random.randint(1,100) >= 40 and random.randint(1,100) < 70:
                    from Modules.Winp import win_percent
                    game = 'Russian_Roulette'
                    value = 'win'
                    win_percent(author,game,value)

                    game = 'Russian_Roulette'
                    value = 'lose'
                    win_percent(author2,game,value)

                    msg = f'**{user.name}** `takes out the gun from a backpack and squeezes the trigger, and gets Hit.` :fire: :skull:'
                    embed = discord.Embed(description = msg,color = 0x00ff08)
                    embed.set_author(name=f"{ctx.author} Won the Game", icon_url=ctx.author.avatar_url)
                    profit = send_coin(author,bet)
                    if not send_fine(author,bet) == 0:
                        fine = send_fine(author,bet)
                        with open('Config/data.json','r') as f:
                            data = json.load(f)
                        embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        data[author]['money'] += bet + profit - fine
                        data[author2]['money'] -= bet
                    else:
                        data[author]['money'] += bet + profit 
                        data[author2]['money'] -= bet
                    if not profit == 0:
                        embed.add_field(name="Credited ", value=f"${bet*2} + {profit} (Coins X)", inline=False)
                    else:
                        embed.add_field(name="Credited:", value=f"${bet*2}", inline=False)

                    with open("Config/data.json","w") as f:
                        json.dump(data,f,indent = 3)

                    await a.edit(embed=embed)
                    return

                else:
                    msg = f'**{ctx.author.name}** `takes out the gun from a backpack and squeezes the trigger, and Survives.`\n**{user.name}** `takes out the gun from a backpack and squeezes the trigger, and Survives.`'
                    embed = discord.Embed(description = msg,color = 0x00ff08)  
                    embed = discord.Embed(description = msg,color = 0x00ff08)
                    embed.set_author(name=f"GAME DRAWN")
                    await a.edit(embed = embed)      
                    return   


def setup(bot):
    bot.add_cog(russian_roulette(bot))