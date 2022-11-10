import discord
from discord.ext import commands
import random
import json
import asyncio
from Modules.Fine import send_fine
from Modules.Double_Coins import send_coin
from Modules.Cooldown import add_cooldown
from Modules.Cooldown import get_cooldown
class baccarat(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def init(self, bot):
        self.bot = bot
    

    @commands.command()
    async def baccarat(self,ctx,value: str = None,amount:int = None):
        author = str(ctx.author.id)
        command = 'baccarat'
        if not get_cooldown(command,author) == '':
            await ctx.send(get_cooldown(command,author))
            return
            
        add_cooldown(command,author,6)
        values = ['player','banker','tie']

        author = str(ctx.author.id)
        author2 = ctx.author.name
        with open('Config/data.json','r') as f:
            users = json.load(f)

        money = users[author]['money']
        with open('Config/prefixes.json','r') as f:
            pf = json.load(f)
            
        prefix = pf[str(ctx.guild.id)]['Prefix']

        if value == None and amount == None:
            embed=discord.Embed(color=0x800080)
            embed.set_author(name="Baccarat Game || Documentation")
            embed.add_field(name=":page_facing_up: Information", value="1: In Baccarat, every user has three options: [Player, Tie, and Banker].\n2: Upon placing the bet, 2 Cards are dealt to each user.\n3: The card types are: Banker Hand and Player Hand.\n4: The winning hand would be the higher of the 2 and anyone who placed a corresponding bet wins.", inline=False)
            embed.add_field(name=":dollar: Profits:", value="Player: 2x \n Banker: 2x \n Tie: 9x", inline=False)
            embed.add_field(name=":page_facing_up: Minimum BET: ", value="$100", inline=False)
            embed.add_field(name=":alarm_clock: Total Time", value="20 Seconds", inline=False)
            embed.set_footer(text=f"To Start The Game: {prefix}baccarat <choice (banker/tie/player)> <bet>")
            await ctx.send(embed = embed)
            return

        if amount > users[author]['money']:
            await ctx.send('Make sure you have the required amount.')
            return

        elif amount <= 0:
            await ctx.send('The amount should be greater than zero.')
            return

        elif amount < 100:
            await ctx.send('The minimum bet amount is: $100')
            return

        player1 = random.randint(1,9)
        player2 = random.randint(1,9)
        banker1 = random.randint(1,9)
        banker2 = random.randint(1,9)
        

        if not value in values:
            await ctx.send('Please choose the correct CHOICE: (Allowed Terms: `player/banker/tie`)')
            return

        else:
            embed=discord.Embed(color=0x800080)
            embed.set_author(name="Baccarat Game ")
            embed.add_field(name="Initializing the Game", value="|<a:Loading_1:677762614603939880> | <a:Loading_1:677762614603939880>|<a:Loading_1:677762614603939880>|<a:Loading_1:677762614603939880> | <a:Loading_1:677762614603939880>| <a:Loading_1:677762614603939880>", inline=False)
            embed.add_field(name="You Chosen:", value=f"{value}", inline=False)
            message = await ctx.send(embed = embed)
            turn = random.randint(1,2)

        if turn == 1:
            await asyncio.sleep(5)
            embed10=discord.Embed(color=0x800080)
            embed10.add_field(name="|DEALING THE CARDS|", value="| <a:spin_1:677761066087874580> | <a:spin_1:677761066087874580> | <a:spin_1:677761066087874580> | <a:spin_1:677761066087874580> |", inline=False)
            await message.edit(embed = embed10)
            #banker turn
            await asyncio.sleep(6)
            #embed here of banker generating numbers
            total2 = banker1 + banker2 

            embed2=discord.Embed(color=0x800080)
            embed2.set_author(name="Banker Turn ")
            embed2.add_field(name="Banker Hand Numbers: ", value=f"{banker1} and {banker2}", inline=False)
            embed2.add_field(name="Total: ", value=f"{total2}", inline=False)
            await message.edit(embed = embed2)
            
            #player turn
            total1 = player1 + player2
            await asyncio.sleep(5)
            embed3=discord.Embed(color=0x0080c0)
            embed3.set_author(name="Player Turn")
            embed3.add_field(name="Player Hand Numbers: ", value=f"{player1} and {player2}", inline=False)
            embed3.add_field(name="Total: ", value=f"{total1}", inline=False)
            await message.edit(embed = embed3)

            if total1 >= 10:
                total1 -= 10

            elif total2 >= 10:
                total2 -= 10

            if value == 'player':
                await asyncio.sleep(5)

                if total1 > total2:
                    from Modules.Winp import win_percent
                    game = 'Baccarat'
                    value = 'win'
                    win_percent(author,game,value)
                    embed4=discord.Embed(color=0x00ff80)
                    embed4.set_author(name=" Congratulations, You Won")
                    embed4.add_field(name="Banker Total:", value=f"{total2}", inline=False)
                    embed4.add_field(name="Player Total:", value=f"{total1}", inline=False)
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed4.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount + profit - fine
                    else:
                        users[author]['money'] += amount + profit 
                    
                    if not profit == 0:
                        embed4.add_field(name="Profit", value=f"{amount*2} + {profit} (Coins X)", inline=False)
                    else:
                        embed4.add_field(name="Profit", value=f"{amount*2}", inline=False)
                
                    embed4.add_field(name="Money in Hand: ", value=f"{money+amount}", inline=False)
                    await message.edit(embed=embed4)

                else:
                    from Modules.Winp import win_percent
                    game = 'Baccarat'
                    value = 'lose'
                    win_percent(author,game,value)
                    embed4=discord.Embed(color=0xff0000)
                    embed4.set_author(name="Well Deserved, The game is lost!")
                    embed4.add_field(name="Banker Total:", value=f"{total2}", inline=False)
                    embed4.add_field(name="Player Total:", value=f"{total1}", inline=False)
                    embed4.add_field(name="Deducted: ", value=f"{amount}", inline=False)
                    embed4.add_field(name="Money in Hand: ", value=f"{money - amount}", inline=False)
                    await message.edit(embed=embed4)
                    users[author]['money'] -= amount
    
            elif value == 'banker':
                await asyncio.sleep(5)

                if total2 > total1:
                    from Modules.Winp import win_percent
                    game = 'Baccarat'
                    value = 'win'
                    win_percent(author,game,value)
                    embed4=discord.Embed(color=0x00ff80)
                    embed4.set_author(name=" Congratulations, You Won")
                    embed4.add_field(name="Banker Total:", value=f"{total2}", inline=False)
                    embed4.add_field(name="Player Total:", value=f"{total1}", inline=False)
                    embed4.add_field(name="Profit: ", value=f"{amount}", inline=False)
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed4.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount + profit - fine
                    else:
                        users[author]['money'] += amount + profit 
                    
                    if not profit == 0:
                        embed4.add_field(name="Profit", value=f"{amount*2} + {profit} (Coins X)", inline=False)
                    else:
                        embed4.add_field(name="Profit", value=f"{amount*2}", inline=False)
                
                    embed4.add_field(name="Money in Hand: ", value=f"{money+amount}", inline=False)
                    await message.edit(embed=embed4)

                else:
                    from Modules.Winp import win_percent
                    game = 'Baccarat'
                    value = 'lose'
                    win_percent(author,game,value)
                    embed4=discord.Embed(color=0xff0000)
                    embed4.set_author(name="You've lost your control,You've lost the game.")
                    embed4.add_field(name="Banker Total:", value=f"{total2}", inline=False)
                    embed4.add_field(name="Player Total:", value=f"{total1}", inline=False)
                    embed4.add_field(name="Deducted:", value=f"{amount}", inline=False)
                    embed4.add_field(name="Money in Hand: ", value=f"{money-amount}", inline=False)
                    await message.edit(embed=embed4)
                    users[author]['money'] -= amount

            elif value == 'tie':
                await asyncio.sleep(5)

                if total1 == total2:
                    from Modules.Winp import win_percent
                    game = 'Baccarat'
                    value = 'win'
                    win_percent(author,game,value)
                    embed4=discord.Embed(color=0x00ff80)
                    embed4.set_author(name=" Congratulations, You Won")
                    embed4.add_field(name="Banker Total:", value=f"{total2}", inline=False)
                    embed4.add_field(name="Player Total:", value=f"{total1}", inline=False)
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed4.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount * 9 - amount + profit - fine
                    else:
                        users[author]['money'] += amount * 9 - amount + profit 
                    
                    if not profit == 0:
                        embed4.add_field(name="Profit", value=f"{amount*9} + {profit} (Coins X)", inline=False)
                    else:
                        embed4.add_field(name="Profit", value=f"{amount*9}", inline=False)
                
                    embed4.add_field(name="Money in Hand: ", value=f"{money+amount}", inline=False)
                    await message.edit(embed=embed4)


                else:
                    from Modules.Winp import win_percent
                    game = 'Baccarat'
                    value = 'lose'
                    win_percent(author,game,value)
                    embed4=discord.Embed(color=0xff0000)
                    embed4.set_author(name="You lost, Damn!")
                    embed4.add_field(name="Banker Total:", value=f"{total2}", inline=False)
                    embed4.add_field(name="Player Total:", value=f"{total1}", inline=False)
                    embed4.add_field(name="Deducted: ", value=f"{amount * 2}", inline=False)
                    embed4.add_field(name="Money in Hand: ", value=f"{money-amount}", inline=False)
                    await message.edit(embed=embed4)
                    users[author]['money'] -= amount

        with open('Config/data.json','w') as f:
            json.dump(users,f,indent = 3)
            
        if turn == 2:
            await asyncio.sleep(5)
            embed10=discord.Embed(color=0x800080)
            embed10.add_field(name="DEALING THE CARDS", value="| <a:spin_1:677761066087874580> | <a:spin_1:677761066087874580> | <a:spin_1:677761066087874580> | <a:spin_1:677761066087874580> |", inline=False)
            await message.edit(embed = embed10)
            #banker turn
            await asyncio.sleep(6)
            #embed here of banker generating numbers
            total2 = banker1 + banker2 

            embed2=discord.Embed(color=0x800080)
            embed2.set_author(name="Banker Turn ")
            embed2.add_field(name="Banker Hand Numbers: ", value=f"{banker1} and {banker2}", inline=False)
            embed2.add_field(name="Total: ", value=f"{total2}", inline=False)
            await message.edit(embed = embed2)
            
            #player turn
            total1 = player1 + player2
            await asyncio.sleep(5)
            embed3=discord.Embed(color=0x0080c0)
            embed3.set_author(name="Player Turn")
            embed3.add_field(name="Player Hand Numbers: ", value=f"{player1} and {player2}", inline=False)
            embed3.add_field(name="Total: ", value=f"{total1}", inline=False)
            await message.edit(embed = embed3)

            if total1 > 10:
                total1 -= 10

            elif total2 > 10:
                total2 -= 10

            if value == 'player':
                await asyncio.sleep(5)

                if total1 > total2:
                    from Modules.Winp import win_percent
                    game = 'Baccarat'
                    value = 'win'
                    win_percent(author,game,value)
                    embed4=discord.Embed(color=0x00ff80)
                    embed4.set_author(name=" Congratulations, You Won")
                    embed4.add_field(name="Banker Total:", value=f"{total2}", inline=False)
                    embed4.add_field(name="Player Total:", value=f"{total1}", inline=False)
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed4.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount  + profit - fine
                    else:
                        users[author]['money'] += amount  + profit  
                    
                    if not profit == 0:
                        embed4.add_field(name="Profit", value=f"{amount*2} + {profit} (Coins X)", inline=False)
                    else:
                        embed4.add_field(name="Profit", value=f"{amount*2}", inline=False)
                
                    embed4.add_field(name="Money in Hand: ", value=f"{money+amount}", inline=False)
                    await message.edit(embed=embed4)


                else:
                    from Modules.Winp import win_percent
                    game = 'Baccarat'
                    value = 'lose'
                    win_percent(author,game,value)
                    embed4=discord.Embed(color=0xff0000)
                    embed4.set_author(name="You've lost it!")
                    embed4.add_field(name="Banker Total:", value=f"{total2}", inline=False)
                    embed4.add_field(name="Player Total:", value=f"{total1}", inline=False)
                    embed4.add_field(name="Deducted: ", value=f"{amount}", inline=False)
                    embed4.add_field(name="Money in Hand: ", value=f"{money-amount}", inline=False)
                    await message.edit(embed=embed4)
                    users[author]['money'] -= amount

            elif value == 'banker':
                await asyncio.sleep(5)

                if total2 > total1:
                    from Modules.Winp import win_percent
                    game = 'Baccarat'
                    value = 'win'
                    win_percent(author,game,value)
                    embed4=discord.Embed(color=0x00ff80)
                    embed4.set_author(name=" Congratulations, You Won")
                    embed4.add_field(name="Banker Total:", value=f"{total2}", inline=False)
                    embed4.add_field(name="Player Total:", value=f"{total1}", inline=False)
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed4.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount  + profit - fine
                    else:
                        users[author]['money'] += amount  + profit  
                    
                    if not profit == 0:
                        embed4.add_field(name="Profit", value=f"{amount*2} + {profit} (Coins X)", inline=False)
                    else:
                        embed4.add_field(name="Profit", value=f"{amount*2}", inline=False)
                
                    embed4.add_field(name="Money in Hand: ", value=f"{money+amount}", inline=False)
                    await message.edit(embed=embed4)

                else:
                    from Modules.Winp import win_percent
                    game = 'Baccarat'
                    value = 'lose'
                    win_percent(author,game,value)
                    embed4=discord.Embed(color=0xff0000)
                    embed4.set_author(name="Never smoke and Drink, You lost.")
                    embed4.add_field(name="Banker Total:", value=f"{total2}", inline=False)
                    embed4.add_field(name="Player Total:", value=f"{total1}", inline=False)
                    embed4.add_field(name="Deducted:", value=f"{amount}", inline=False)
                    embed4.add_field(name="Money in Hand: ", value=f"{money-amount}", inline=False)
                    await message.edit(embed=embed4)
                    users[author]['money'] -= amount


            elif value == 'tie':
                await asyncio.sleep(5)

                if total1 == total2:
                    from Modules.Winp import win_percent
                    game = 'Baccarat'
                    value = 'win'
                    win_percent(author,game,value)
                    embed4=discord.Embed(color=0x00ff80)
                    embed4.set_author(name=" Congratulations, You Won")
                    embed4.add_field(name="Banker Total:", value=f"{total2}", inline=False)
                    embed4.add_field(name="Player Total:", value=f"{total1}", inline=False)
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed4.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount  + profit - fine
                    else:
                        users[author]['money'] += amount  + profit  
                    
                    if not profit == 0:
                        embed4.add_field(name="Profit", value=f"{amount*2} + {profit} (Coins X)", inline=False)
                    else:
                        embed4.add_field(name="Profit", value=f"{amount*2}", inline=False)
                
                    embed4.add_field(name="Money in Hand: ", value=f"{money+amount}", inline=False)
                    await message.edit(embed=embed4)

                else:
                    from Modules.Winp import win_percent
                    game = 'Baccarat'
                    value = 'lose'
                    win_percent(author,game,value)
                    embed4=discord.Embed(color=0xff0000)
                    embed4.set_author(name="You lost, Damn!")
                    embed4.add_field(name="Banker Total:", value=f"{total2}", inline=False)
                    embed4.add_field(name="Player Total:", value=f"{total1}", inline=False)
                    embed4.add_field(name="Deducted: ", value=f"{amount}", inline=False)
                    embed4.add_field(name="Money in Hand: ", value=f"{money-amount}", inline=False)
                    await message.edit(embed=embed4)

                    users[author]['money'] -= amount
            
        with open('Config/data.json','w') as f:
            json.dump(users,f,indent = 3)



def setup(bot):
    bot.add_cog(baccarat(bot))