import discord
from discord.ext import commands
import json
import random
import asyncio
from Modules.Double_Coins import send_coin
from Modules.Fine import send_fine
from Modules.Cooldown import add_cooldown
from Modules.Cooldown import get_cooldown
class roulette(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def roulette(self,ctx,value:str = None,amount:int = None):
        author = str(ctx.author.id)
        command = 'roulette'
        if not get_cooldown(command,author) == '':
            await ctx.send(get_cooldown(command,author))
            return
            
        add_cooldown(command,author,6)
        with open('Config/data.json','r') as f:
            users = json.load(f)
        with open('Config/prefixes.json','r') as f:
            pf = json.load(f)
            
        prefix = pf[str(ctx.guild.id)]['Prefix']
        temp_var = ['black','red','green']
        author = str(ctx.author.id)
        author2 = ctx.author.name
        bk = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        rd = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        gn = [0]
        num_val = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
        embed=discord.Embed(title =f"To Start Playing: {prefix}roulette `<type>` `<bet amount>`" , color=0x0000ff)
        embed.set_author(name="Roulette Game")
        embed.add_field(name=":1234: **Bet Types:**", value="**`<black/red/green>` `<0-36>` `<high/low>` **", inline=False)
        embed.add_field(name=":notepad_spiral: **Information:**", value="**`Black/Red/Green` If bot rolls your color you win.**\n`0-36` **If bot rolls your number you win.**\n`High/Low` **Low = `1-18` | High = `19-36`**", inline=False)
        embed.add_field(name="**<a:bt:678920153563398146> Profit:**", value="**Black/Red - `2x`**\n**Green - `40x`**\n**0-36** `35x` \n**high/low** - `2x`", inline=False)
        embed.add_field(name=":1234: **Numbers:**", value="**Green:** `0`\n**Black:** `2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35`\n**Red:** `1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36`", inline=False)
        embed.set_footer(text = f'USAGE: {prefix}roulette <bet type> <amount>')
        embed2 = discord.Embed()
        embed2.set_author(name=f" Roulette !! {author2}")
        embed3 = discord.Embed()
        embed3.set_author(name=f" Roulette !! {author2}")

        if value is None and amount is None:
            await ctx.send(embed = embed)
            return
        
        elif amount is None:
            await ctx.send('<a:alert:833301110587785267> Specify the BET Amount.')
            return

        elif amount > users[author]['money']:
            await ctx.send(f"<a:alert:833301110587785267> Hey {ctx.author.mention} You don't have enough Coins. ")
            return   

        elif amount <= 0:
            await ctx.send("<a:alert:833301110587785267> The BET Amount should be greater than zero.")
            return

        value = value.lower() 
        if value.lower() == 'black':
            a = random.randint(1,36)
            #await ctx.send(f'*{ctx.author.mention} places his/her bet on the Number: `{value.upper()}` and start waiting for the `Fillory` to start the spin.*')
            #await asyncio.sleep(4)
            if a in bk:
                from Modules.Winp import win_percent
                game = 'Roulette'
                value = 'win'
                win_percent(author,game,value)
                if a in bk:
                    num = 'BLACK'
                elif a in rd:
                    num = 'RED'
                elif a in gn:
                    num = 'GREEN'
                #await ctx.send(f'**:tada: Congrulations, You Won! :tada:**\n**The Number Was: `BLACK {a}`**\n**<a:bt:678920153563398146> `${amount *2} Money` has been credited.**')
                embed=discord.Embed(description=f"The Number was: {num} `{a}`",color=0x00ff9f)
                embed.set_author(name="You Won!")
                profit = send_coin(author,amount)
                if not send_fine(author,amount) == 0:
                    fine = send_fine(author,amount)
                    with open('Config/data.json','r') as f:
                        users = json.load(f)
                    embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                    users[author]['money'] += amount + profit - fine
                else:
                    users[author]['money'] += amount + profit 
                if not profit == 0:
                    embed.add_field(name="Credited:", value=f"${amount*2} + {profit} (Coins X)", inline=False)
                else:
                    embed.add_field(name="Credited:", value=f"${amount*2}", inline=False)
                await ctx.send(embed = embed)
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)
        
            else:
                from Modules.Winp import win_percent
                game = 'Roulette'
                value = 'lose'
                win_percent(author,game,value)
                if a in bk:
                    num = 'BLACK'
                elif a in rd:
                    num = 'RED'
                elif a in gn:
                    num = 'GREEN'
                embed=discord.Embed(description = f"The Number Was: {num} `{a}`",color=0xff0000)
                embed.set_author(name="You Lost")
                embed.add_field(name = 'Debited',value = f'$ {amount}',inline = False)
                await ctx.send(embed = embed)
                #await ctx.send(f'**:frowning: Better Luck Next Time!**\n**<a:alert:833301110587785267>  The Number Was: `{num} {a}`**\n**<a:alert:833301110587785267> You lost the BET Amount.**')
                users[author]['money'] -= amount
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)

        elif value == 'red':
            #await ctx.send(f'*{ctx.author.mention} places his/her bet on the Number: `{value.upper()}` and start waiting for the `Fillory` to start the spin.*')
            #await asyncio.sleep(4)

            a = random.randint(1,36)
            if a in rd:
                from Modules.Winp import win_percent
                game = 'Roulette'
                value = 'win'
                win_percent(author,game,value)
                try:
                    if a in bk:
                        num = 'BLACK'
                    elif a in rd:
                        num = 'RED'
                    elif a in gn:
                        num = 'GREEN'
                    embed=discord.Embed(description=f"The Number was: {num} `{a}`",color=0x00ff9f)
                    embed.set_author(name="You Won!")
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount + profit - fine
                    else:
                        users[author]['money'] += amount + profit 
                    if not profit == 0:
                        embed.add_field(name="Credited:", value=f"${amount*2} + {profit} (Coins X)", inline=False)
                    else:
                        embed.add_field(name="Credited:", value=f"${amount*2}", inline=False)
                    await ctx.send(embed = embed)
                    with open("Config/data.json","w") as f:
                        json.dump(users,f,indent = 3)
                
                except Exception as e:
                    print(e)

            else:
                from Modules.Winp import win_percent
                game = 'Roulette'
                value = 'lose'
                win_percent(author,game,value)

                if a in bk:
                    num = 'BLACK'
                elif a in rd:
                    num = 'RED'
                elif a in gn:
                    num = 'GREEN'
                embed=discord.Embed(description = f"The Number Was: {num} `{a}`",color=0xff0000)
                embed.set_author(name="You Lost")
                embed.add_field(name = 'Debited',value = f'$ {amount}',inline = False)
                await ctx.send(embed = embed)
                users[author]['money'] -= amount
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)

        elif value == 'green':

            #await ctx.send(f'*{ctx.author.mention} places his/her bet on the Number: `{value.upper()}` and start waiting for the `Fillory` to start the spin.*')
            #await asyncio.sleep(4)

            a = random.randint(0,36)
            if a in gn:
                from Modules.Winp import win_percent
                game = 'Roulette'
                value = 'win'
                win_percent(author,game,value)
                if a in bk:
                    num = 'BLACK'
                elif a in rd:
                    num = 'RED'
                elif a in gn:
                    num = 'GREEN'
                amount = amount * 40 - amount
                embed=discord.Embed(description=f"The Number was: {num} `{a}`",color=0x00ff9f)
                embed.set_author(name="You Won!")
                profit = send_coin(author,amount)
                if not send_fine(author,amount) == 0:
                    fine = send_fine(author,amount)
                    with open('Config/data.json','r') as f:
                        users = json.load(f)
                    embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                    users[author]['money'] += amount + profit - fine
                else:
                    users[author]['money'] += amount + profit 
                if not profit == 0:
                    embed.add_field(name="Credited:", value=f"${amount*2} + {profit} (Coins X)", inline=False)
                else:
                    embed.add_field(name="Credited:", value=f"${amount*2}", inline=False)
                await ctx.send(embed = embed)
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)

            else:
                from Modules.Winp import win_percent
                game = 'Roulette'
                value = 'lose'
                win_percent(author,game,value)
                if a in bk:
                    num = 'BLACK'
                elif a in rd:
                    num = 'RED'
                embed=discord.Embed(description = f"The Number Was: {num} `{a}`",color=0xff0000)
                embed.set_author(name="You Lost")
                embed.add_field(name = 'Debited',value = f'$ {amount}',inline = False)
                await ctx.send(embed = embed)
                users[author]['money'] -= amount
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)

        elif value == 'high':

            a = random.randint(1,20)
            #await ctx.send(f'*{ctx.author.mention} places his/herbet on the Number: `{value.upper()}`and start waiting for the `Fillory` to start the spin.*')
            #await asyncio.sleep(4)
            if a > 10 and a < 21:
                from Modules.Winp import win_percent
                game = 'Roulette'
                value = 'win'
                win_percent(author,game,value)
                embed=discord.Embed(description=f"The Number was: `{a}`",color=0x00ff9f)
                embed.set_author(name="You Won!")
                profit = send_coin(author,amount)
                if not send_fine(author,amount) == 0:
                    fine = send_fine(author,amount)
                    with open('Config/data.json','r') as f:
                        users = json.load(f)
                    embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                    users[author]['money'] += amount + profit - fine
                else:
                    users[author]['money'] += amount + profit
                if not profit == 0:
                    embed.add_field(name="Credited:", value=f"${amount*2} + {profit} (Coins X)", inline=False)
                else:
                    embed.add_field(name="Credited:", value=f"${amount*2}", inline=False)
                await ctx.send(embed = embed)
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)
            else:
                from Modules.Winp import win_percent
                game = 'Roulette'
                value = 'lose'
                win_percent(author,game,value)
                embed=discord.Embed(description = f"The Number Was: {num} `{a}`",color=0xff0000)
                embed.set_author(name="You Lost")
                embed.add_field(name = 'Debited',value = f'$ {amount}',inline = False)
                await ctx.send(embed = embed)
                users[author]['money'] -= amount
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)

        elif value == 'low':


            a = random.randint(1,10)
            #await ctx.send(f'*{ctx.author.mention} places his/her bet on the Number: `{value.upper()}` and start waiting for the `Fillory` to start the spin.*')
            #await asyncio.sleep(4)
            if a < 11 and a > 0:
                from Modules.Winp import win_percent
                game = 'Roulette'
                value = 'win'
                win_percent(author,game,value)
                embed=discord.Embed(description=f"The Number was: `{a}`",color=0x00ff9f)
                embed.set_author(name="You Won!")
                profit = send_coin(author,amount)
                if not send_fine(author,amount) == 0:
                    fine = send_fine(author,amount)
                    with open('Config/data.json','r') as f:
                        users = json.load(f)
                    embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                    users[author]['money'] += amount + profit - fine
                else:
                    users[author]['money'] += amount + profit 
                if not profit == 0:
                    embed.add_field(name="Credited:", value=f"${amount*2} + {profit} (Coins X)", inline=False)
                else:
                    embed.add_field(name="Credited:", value=f"${amount*2}", inline=False)
                await ctx.send(embed = embed)
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)
            else:
                from Modules.Winp import win_percent
                game = 'Roulette'
                value = 'lose'
                win_percent(author,game,value)
                embed=discord.Embed(description = f"The Number Was: `{a}`",color=0xff0000)
                embed.set_author(name="You Lost")
                embed.add_field(name = 'Debited',value = f'$ {amount}',inline = False)
                await ctx.send(embed = embed)
                users[author]['money'] -= amount
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)

        elif int(value) in num_val:

            a = random.randint(1,36)
            value = int(value)
            #await ctx.send(f'*{ctx.author.mention} places his/herbet on the Number: `{value}`and start waiting for the `Fillory` to start the spin.*')
            #await asyncio.sleep(4)
            if value == a:
                from Modules.Winp import win_percent
                game = 'Roulette'
                value = 'win'
                win_percent(author,game,value)
                amount = amount * 35 - amount
                embed=discord.Embed(description=f"The Number was: `{a}`",color=0x00ff9f)
                embed.set_author(name="You Won!")
                profit = send_coin(author,amount)
                if not send_fine(author,amount) == 0:
                    fine = send_fine(author,amount)
                    with open('Config/data.json','r') as f:
                        users = json.load(f)
                    embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                    users[author]['money'] += amount + profit - fine
                else:
                    users[author]['money'] += amount + profit 
                if not profit == 0:
                    embed.add_field(name="Credited:", value=f"${amount*2} + {profit} (Coins X)", inline=False)
                else:
                    embed.add_field(name="Credited:", value=f"${amount*2}", inline=False)
                await ctx.send(embed = embed)
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)

            else:
                from Modules.Winp import win_percent
                game = 'Roulette'
                value = 'lose'
                win_percent(author,game,value)
                embed=discord.Embed(description = f"The Number Was: `{a}`",color=0xff0000)
                embed.set_author(name="You Lost")
                embed.add_field(name = 'Debited',value = f'$ {amount}',inline = False)
                await ctx.send(embed = embed)
                users[author]['money'] -= amount
                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)

        elif not value in num_val:
            await ctx.send("<a:alert:833301110587785267> Please choose the number between: `0 - 36`")
        
        else:
            await ctx.send('<a:alert:833301110587785267> Invalid Choice')
        


def setup(bot):
    bot.add_cog(roulette(bot))