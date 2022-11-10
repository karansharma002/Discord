import discord
from discord.ext import commands
import random
import json
import asyncio 
from Modules.Fine import send_fine
from Modules.Double_Coins import send_coin
from Modules.Cooldown import add_cooldown
from Modules.Cooldown import get_cooldown

class duelbet(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    

    @commands.command()
    async def duelbet(self,ctx,user:discord.User = None,bet:int = None):
        author = str(ctx.author.id)
        command = 'duelbet'
        if not get_cooldown(command,author) == '':
            await ctx.send(get_cooldown(command,author))
            return
            
        add_cooldown(command,author,6)
        try:
                
            def check(message):
                return message.author == user

            with open('Config/data.json','r') as f:
                data = json.load(f)
            with open('Config/prefixes.json','r') as f:
                pf = json.load(f)
                
            prefix = pf[str(ctx.guild.id)]['Prefix']

            if bet == None or user == None:
                print('yes?')
                embed=discord.Embed(title=f"To Place a Bet: Use: {prefix}duelbet `<@user>` `<bet amount>`", color=0x575cff)
                embed.set_author(name="Duel Bet")
                embed.add_field(name="Info:", value="Challenge your friends by placing the bets.", inline=False)
                embed.add_field(name="Cooldown:", value="Non Prime: `6 Seconds`\nPrime: `3 Seconds`", inline=False)
                embed.set_footer(text = 'The player will have 20 seconds to accept the bet.')
                await ctx.send(embed = embed)
            
            else:
                amount = bet
                author = str(ctx.author.id)
                author2 = str(user.id)
                if ctx.author.id == user.id:
                    await ctx.send('<a:alert:833301110587785267> You cannot duel yourself.')
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
                    await ctx.send(f'{user.mention} Would you accept the Duel? `(Yes/No)` `(TIMEOUT in 20 Seconds)`')
                    try:
                        msg = await self.bot.wait_for('message',check = check,timeout = 20)
                        if msg.content.lower() == 'yes':
                            pass

                        elif msg.content.lower() == 'no':
                            await ctx.send('Duel Cancelled.')
                            return
                            
                        else:
                            await ctx.send('Invalid Reply, The Duel has been cancelled.')
                            return

                    except asyncio.TimeoutError:
                        await ctx.send(f'Duel Cancelled, {user.name} Failed to accept the duel. ')
                        return

                    num1 = random.randint(1, 12)
                    num2 = random.randint(1, 12)
                    if num1 > num2:
                        from Modules.Winp import win_percent
                        game = 'Duelbet'
                        value = 'win'
                        win_percent(author,game,value)

                        game = 'Duelbet'
                        value = 'lose'
                        win_percent(author2,game,value)

                        embed=discord.Embed(color=0x80ff00)
                        embed.set_author(name=f'{ctx.author} Won the Bet.',icon_url=ctx.author.avatar_url)
                        embed.add_field(name=f"{ctx.author.name}", value=f"𝗥𝗼𝗹𝗹𝗲𝗱: {num1}", inline=False)
                        embed.add_field(name=f"{user.name}", value=f"𝗥𝗼𝗹𝗹𝗲𝗱: {num2}", inline=False)
                        profit = send_coin(author,amount)
                        if not send_fine(author,amount) == 0:
                            fine = send_fine(author,amount)
                            with open('Config/data.json','r') as f:
                                data = json.load(f)
                            embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                            data[author]['money'] += amount + profit - fine
                            data[author2]['money'] -= amount
                        else:
                            data[author]['money'] += amount + profit 
                            data[author2]['money'] -= amount

                        if not profit == 0:
                            embed.add_field(name="Credited:", value=f"${amount*2} + {profit} (Coins X)", inline=False)
                        else:
                            embed.add_field(name="Credited:", value=f"${amount*2}", inline=False)
                        
                        await ctx.send(embed = embed)
                        with open("Config/data.json","w") as f:
                            json.dump(data,f,indent = 3)

        
                    elif num2 > num1:
                        from Modules.Winp import win_percent
                        game = 'Duelbet'
                        value = 'win'
                        win_percent(author2,game,value)

                        game = 'Duelbet'
                        value = 'lose'
                        win_percent(author,game,value)

                        embed=discord.Embed(color=0x80ff00)
                        embed.set_author(name=f"{user} Won the Bet.",icon_url=user.avatar_url)
                        embed.add_field(name=f"{ctx.author.name}", value=f"𝗥𝗼𝗹𝗹𝗲𝗱: {num1}", inline=False)
                        embed.add_field(name=f"{user.name}", value=f"𝗥𝗼𝗹𝗹𝗲𝗱: {num2}", inline=False)
                        profit = send_coin(author2,amount)
                        if not send_fine(author2,amount) == 0:
                            fine = send_fine(author2,amount)
                            with open('Config/data.json','r') as f:
                                data = json.load(f)
                            embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                            data[author2]['money'] += amount + profit - fine
                            data[author]['money'] -= amount
                        else:
                            data[author2]['money'] += amount + profit 
                            data[author]['money'] -= amount

                        if not profit == 0:
                            embed.add_field(name="Credited:", value=f"${amount*2} + {profit} (Coins X)", inline=False)
                        else:
                            embed.add_field(name="Credited:", value=f"${amount*2}", inline=False)
                        
                        await ctx.send(embed = embed)
                        with open("Config/data.json","w") as f:
                            json.dump(data,f,indent = 3)

                    else:
                        embed=discord.Embed(color=0xffe74d)
                        embed.set_author(name="Match Tied (Have a cup of Coffee)")
                        embed.add_field(name=f"{ctx.author.name}", value=f"𝗥𝗼𝗹𝗹𝗲𝗱: {num1}", inline=False)
                        embed.add_field(name=f"{user.name}", value=f"𝗥𝗼𝗹𝗹𝗲𝗱: {num2}", inline=False)
                        await ctx.send(embed = embed)
        
        except Exception as  e:
            print(e)
        


def setup(bot):
    bot.add_cog(duelbet(bot))