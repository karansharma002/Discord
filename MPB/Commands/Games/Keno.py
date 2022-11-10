import discord
from discord.ext import commands
import json
import random
import asyncio
from Modules.Fine import send_fine
from Modules.Double_Coins import send_coin
from Modules.Cooldown import add_cooldown
from Modules.Cooldown import get_cooldown
class keno(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def init(self, bot):
        self.bot = bot
    

    @commands.command()
    async def keno(self,ctx,bet: int = None,num1: int = None,num2: int = None,num3: int = None, num4: int = None ,num5: int = None):
        author = str(ctx.author.id)
        command = 'keno'
        if not get_cooldown(command,author) == '':
            await ctx.send(get_cooldown(command,author))
            return
            
        add_cooldown(command,author,6)
        with open('Config/data.json','r') as f:
            users = json.load(f)
        with open('Config/prefixes.json','r') as f:
            pf = json.load(f)
            
        prefix = pf[str(ctx.guild.id)]['Prefix']
        if bet == None and num1 == None and num2 == None and num3 == None and num4 == None and num5 == None:
            embed=discord.Embed(color=0x0080ff)
            embed.set_author(name="Keno Game || Documentation")
            embed.add_field(name=":page_facing_up: Info: ", value="• There are 40 numbers in the CARD.\n• You have to choose 5 numbers.\n• Fillory will generate 5 random numbers.\n • Profit will be multiplied if two numbers got Matched.\n • Your money will be refunded if one number got Matched \n • Additional Profit 2X if Lucky Number Comes.\n• The game will be lost if none of the numbers are matched. ", inline=False)
            embed.add_field(name=":money_with_wings: Profit: ", value="`1.5X` - Per 2 Numbers\n`2X`- Lucky Number", inline=False)
            embed.set_footer(text=f"Usage: {prefix}keno <BET Amount> <num1> <num2> <num3> <num4> <num5>")
            await ctx.send(embed=embed)
            return
        
        if not bet == None and num1 == None or num2 == None or num3 == None or num4 == None or num5 == None:
            await ctx.send('Provide all the 5 numbers to continue.')
            return
            
        if bet > users[author]["money"]:
            await ctx.send(" Make sure you have the required money.")
            return

        elif bet <= 0:
            await ctx.send("The amount should be greater than 0")
            return

        elif num1 <= 0 or num2 <= 0 or num3 <= 0 or num4 <= 0 or num5 <= 0:
            await ctx.send("Invalid Numbers Chosen.")
            return

        elif num1 > 40 or num2 > 40 or num3 > 40 or num4 > 40 or num5 > 40:
            await ctx.send("Invalid Numbers Chosen.")
            return

        elif num1 == num2 or num2 == num3 or num3 == num4 or num4 == num5 or num5 == num1:
            await ctx.send("You can't choose same numbers.")
            return

        elif num1 == num3 or num3 == num5 or num5 == num2 or num5 == num3:

            await ctx.send("You can't choose same numbers.")
            return

        else:
            msg = ''
            msg += '{} {} {} {} {}'.format(num1,num2,num3,num4,num5)
            msg2 = ''
            b1 = random.randint(1,40)
            b2 = random.randint(1,40)
            b3 = random.randint(1,40)
            b4 = random.randint(1,40)
            b5 = random.randint(1,40)
            b6 = random.randint(1,40)

            if b1 == b2 or b1 == b3 or b1 == b4 or b1 == b5:
                b1 = random.randint(1,40)
                
            elif b2 == b1 or b2 == b3 or b2 == b4 or b2 == b5:
                b2 = random.randint(1,40)
                
            elif b3 == b1 or b3 == b2 or b3 == b4 or b3 == b5:
                b3 = random.randint(1,40)
                
            elif b4 == b1 or b4 == b2 or b4 == b3 or b4 == b5:
                b4 = random.randint(1,40)
                #i = i + 1
            elif b5 == b1 or b5 == b2 or b5 == b3 or b5 == b4:
                b5 = random.randint(1,40)
                
            msg2 += '{} {} {} {} {}'.format(b1,b2,b3,b4,b5)
            matched_num = 0
            embed2=discord.Embed(color=0x8080c0)
            embed2.set_author(name="Fillory Is Generating Numbers:")
            embed2.add_field(name="|<a:Loading_1:677762614603939880> | <a:Loading_1:677762614603939880>|<a:Loading_1:677762614603939880>|<a:Loading_1:677762614603939880> | <a:Loading_1:677762614603939880>| <a:Loading_1:677762614603939880>", value="\u200b", inline=False)
            embed2.add_field(name="Your Numbers: ", value=f"{msg}", inline=False)
            message = await ctx.send(embed = embed2)
            await asyncio.sleep(5)

            if b1 == num1 or b1 == num2 or b1 == num3 or b1 == num4 or b1 == num5:
                matched_num += 1

            if b2 == num1 or b2 == num2 or b2 == num3 or b2 == num4 or b2 == num5:
                matched_num += 1

            if b3 == num1 or b3 == num2 or b3 == num3 or b3 == num4 or b3 == num5:
                matched_num += 1
            
            if b4 == num4 or b4 == num2 or b4 == num3 or b4 == num4 or b4 == num5:
                matched_num += 1
            
            if b5 == num1 or b5 == num2 or b5 == num3 or b5 == num4 or b5 == num5:
                matched_num += 1

            if matched_num == 0:
                from Modules.Winp import win_percent
                game = 'Keno'
                value = 'lose'
                win_percent(author,game,value)
                embed=discord.Embed(color=0xff0000)
                embed.set_author(name="Loser!! ")
                embed.add_field(name="Fillory Generated: ", value=f"{msg2}", inline=False)
                embed.add_field(name="Your Numbers: ", value=f"{msg}", inline=False)
                embed.add_field(name="Numbers Matched:", value=f"{matched_num}", inline=False)
                embed.add_field(name="Debited:", value=f"{bet}", inline=False)
                await message.edit(embed = embed)
                users[author]["money"] -= bet
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)


            elif matched_num == 1:
                from Modules.Winp import win_percent
                game = 'Keno'
                value = 'lose'
                win_percent(author,game,value)
                embed=discord.Embed(color=0xff0000)
                embed.set_author(name="Better luck next time!")
                embed.add_field(name="Fillory Generated: ", value=f"{msg2}", inline=False)
                embed.add_field(name="Your Numbers: ", value=f"{msg}", inline=False)
                embed.add_field(name="Numbers Matched:", value=f"{matched_num}", inline=False)
                embed.add_field(name="Money: ", value="Refunded", inline=False)
                await message.edit(embed = embed)

            elif matched_num == 2:
                from Modules.Winp import win_percent
                game = 'Keno'
                value = 'win'
                win_percent(author,game,value)
                if b6 == 26:
                    z = ['<a:ln:678647491624960000>']
                    bet = bet * 2
                elif not b6 == 26:
                    z = 'None'
                    bet = round(bet * 1.5) - bet

                embed=discord.Embed(color=0x80ff00)
                embed.set_author(name="Congrats || You WON")
                embed.add_field(name="Fillory Generated: ", value=f"{msg2}", inline=False)
                embed.add_field(name="Your Numbers: ", value=f"{msg}", inline=False)
                embed.add_field(name="Numbers Matched:", value=f"{matched_num}", inline=False)
                embed.add_field(name="Lucky Number: ", value=f"{z}", inline=False)
                embed.add_field(name="Profit:", value="1.2X", inline=False)

                profit = send_coin(author,bet)
                if not send_fine(author,bet) == 0:
                    fine = send_fine(author,bet)
                    with open('Config/data.json','r') as f:
                        users = json.load(f)
                    embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                    users[author]['money'] += bet + profit - fine
                else:
                    users[author]['money'] += bet + profit
                if not profit == 0:
                    embed.add_field(name="Credited ", value=f"${bet} + {profit} (Coins X)", inline=False)
                else:
                    embed.add_field(name="Credited:", value=f"${bet}", inline=False)

                await message.edit(embed = embed)
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)

            elif matched_num == 3:
                from Modules.Winp import win_percent
                game = 'Keno'
                value = 'win'
                win_percent(author,game,value)
                if b6 == 26:
                    z = ['<a:ln:678647491624960000>']
                    bet = bet * 8
                elif not b6 == 26:
                    z = 'None'
                    bet = round(bet * 1.5 - bet) * 3

                embed=discord.Embed(color=0x80ff00)
                embed.set_author(name="Congrats || You WON")
                embed.add_field(name="Fillory Generated: ", value=f"{msg2}", inline=False)
                embed.add_field(name="Your Numbers: ", value=f"{msg}", inline=False)
                embed.add_field(name="Numbers Matched:", value=f"{matched_num}", inline=False)
                embed.add_field(name="Lucky Number: ", value=f"{z}", inline=False)
                embed.add_field(name="Profit:", value="3X", inline=False)
                profit = send_coin(author,bet)
                if not send_fine(author,bet) == 0:
                    fine = send_fine(author,bet)
                    with open('Config/data.json','r') as f:
                        users = json.load(f)
                    embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                    users[author]['money'] += bet + profit - fine
                else:
                    users[author]['money'] += bet + profit  
                if not profit == 0:
                    embed.add_field(name="Credited ", value=f"${bet} + {profit} (Coins X)", inline=False)
                else:
                    embed.add_field(name="Credited:", value=f"${bet}", inline=False)
                    
                await message.edit(embed = embed)
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)


            elif matched_num == 4:
                from Modules.Winp import win_percent
                game = 'Keno'
                value = 'win'
                win_percent(author,game,value)

                if b6 == 26:
                    z = ['<a:ln:678647491624960000>']
                    bet = bet * 9
                elif not b6 == 26:
                    z = 'None'
                    bet = round(bet * 1.5 - bet) * 4

                embed=discord.Embed(color=0x80ff00)
                embed.set_author(name="Congrats || You WON")
                embed.add_field(name="Fillory Generated: ", value=f"{msg2}", inline=False)
                embed.add_field(name="Your Numbers: ", value=f"{msg}", inline=False)
                embed.add_field(name="Numbers Matched:", value=f"{matched_num}", inline=False)
                embed.add_field(name="Lucky Number: ", value=f"{z}", inline=False)
                embed.add_field(name="Profit:", value="4X", inline=False)
                profit = send_coin(author,bet)
                if not send_fine(author,bet) == 0:
                    fine = send_fine(author,bet)
                    with open('Config/data.json','r') as f:
                        users = json.load(f)
                    embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                    users[author]['money'] += bet + profit - fine
                else:
                    users[author]['money'] += bet + profit 
                if not profit == 0:
                    embed.add_field(name="Credited ", value=f"${bet} + {profit} (Coins X)", inline=False)
                else:
                    embed.add_field(name="Credited:", value=f"${bet}", inline=False)
                    
                await message.edit(embed = embed)
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)
        

            elif matched_num == 5:
                from Modules.Winp import win_percent
                game = 'Keno'
                value = 'win'
                win_percent(author,game,value)
                users[author]["money"] -= bet
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)
                if b6 == 26:
                    z = ['<a:ln:678647491624960000>']
                    bet = bet * 10
                elif not b6 == 26:
                    z = 'None'
                    bet = round(bet * 1.5 - bet) * 5
                    
                embed=discord.Embed(color=0x80ff00)
                embed.set_author(name="Congrats || You WON")
                embed.add_field(name="Fillory Generated: ", value=f"{msg2}", inline=False)
                embed.add_field(name="Your Numbers: ", value=f"{msg}", inline=False)
                embed.add_field(name="Numbers Matched:", value=f"{matched_num}", inline=False)
                embed.add_field(name="Lucky Number: ", value=f"{z}", inline=False)
                embed.add_field(name="Profit:", value="5X", inline=False)
                profit = send_coin(author,bet)
                if not send_fine(author,bet) == 0:
                    fine = send_fine(author,bet)
                    with open('Config/data.json','r') as f:
                        users = json.load(f)
                    embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                    users[author]['money'] += bet + profit - fine
                else:
                    users[author]['money'] += bet + profit
                if not profit == 0:
                    embed.add_field(name="Credited ", value=f"${bet} + {profit} (Coins X)", inline=False)
                else:
                    embed.add_field(name="Credited:", value=f"${bet}", inline=False)
                    
                await message.edit(embed = embed)
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)


def setup(bot):
    bot.add_cog(keno(bot))