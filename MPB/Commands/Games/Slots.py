import discord
from discord.ext import commands
import json
import random
import asyncio
from Modules.Double_Coins import send_coin
from Modules.Fine import send_fine
from Modules.Cooldown import add_cooldown
from Modules.Cooldown import get_cooldown
class slots(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def init(self, bot):
        self.bot = bot
    

    @commands.command()
    async def slots(self,ctx, amount: int = None):
        author = str(ctx.author.id)
        command = 'slots'
        if not get_cooldown(command,author) == '':
            await ctx.send(get_cooldown(command,author))
            return
        with open('Config/prefixes.json','r') as f:
            pf = json.load(f)
            
        prefix = pf[str(ctx.guild.id)]['Prefix']           
        add_cooldown(command,author,6)
        try:

            with open("Config/data.json","r") as f:
                users = json.load(f)
            author2 = ctx.author.name
            author = str(ctx.author.id)
            slots = [':first_place:',":gem:",':dollar:', ':100:', ':moneybag:',':grey_question:']

            if not amount == None:
                if amount > users[author]["money"] or amount < 0:
                    await ctx.send("Make sure you have the required cash.")
                    return

            if amount == None:
                embed=discord.Embed(color=0xff95ff)
                embed.set_author(name=f"Slot Machine")
                embed.add_field(name="Winnnings", value=":first_place::first_place::grey_question: - 2X\n:100::100::grey_question: - 2X\n:gem::gem::grey_question: - 3X\n :first_place::first_place::first_place: - 5x\n :gem::gem::gem: - 5x\n:100::100::100: - 7x\n:dollar::dollar::dollar: - 7x\n:moneybag::moneybag::moneybag: - 9x", inline=False)
                embed.set_footer(text=f"To start the machine, Use: {prefix}slots <amount> ")
                await ctx.send(embed=embed)
            else:
                embed2=discord.Embed(color=0xff95ff)
                slot1 = random.choice(slots)
                slot2 = random.choice(slots)
                slot3 = random.choice(slots)
                embed=discord.Embed(title="Slot Machine ", color=0xff95ff)
                embed.set_author(name=f" Participant: {author2}")
                embed2=discord.Embed(title="Slot Machine ", color=0xff95ff)
                embed2.set_author(name=f" Participant: {author2}")
                slotOutput = '|\t{}\t|\t{}\t|\t{}\t|\n'.format(slot1, slot2, slot3)

                if slot1 == slots[0] and slot2 == slots[0]  or slot2 == slots[0] and slot3 == slots[0]: 
                    from Modules.Winp import win_percent
                    game = 'Slots'
                    value = 'win'
                    win_percent(author,game,value)
                    embed.add_field(name="Rolling.....", value="<a:slots:677086128263790612>|<a:slots:677086128263790612>|<a:slots:677086128263790612>", inline=False)
                    message = await ctx.send(embed = embed)
                    await asyncio.sleep(2)
                    embed2.add_field(name = 'Results:',value = f"{slotOutput}", inline=False)
                    amount = amount * 2 - amount
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed2.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount + profit - fine
                    else:
                        users[author]['money'] += amount + profit 
    
                    if not profit == 0:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} + ${profit} (Coins X) has been credited.", inline=False)
                    else:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} has been credited.", inline=False)
                    await message.edit(embed = embed2)
    

                elif slot1 == slots[1] and slot2 == slots[1] or slot2 == slots[1] and slot3 == slots[1]:
                    from Modules.Winp import win_percent
                    game = 'Slots'
                    value = 'win'
                    win_percent(author,game,value)
                    embed.add_field(name="Rolling.....", value="<a:slots:677086128263790612>|<a:slots:677086128263790612>|<a:slots:677086128263790612>", inline=False)
                    message = await ctx.send(embed = embed)
                    await asyncio.sleep(2)
                    embed2.add_field(name = 'Results:',value = f"{slotOutput}", inline=False)
                    amount = amount * 2 - amount
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed2.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount + profit - fine
                    else:
                        users[author]['money'] += amount + profit  
    
                    if not profit == 0:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} + ${profit} (Coins X) has been credited.", inline=False)
                    else:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} has been credited.", inline=False)
                    await message.edit(embed = embed2)

                elif slot2 == slots[3] and slot3 == slots[3] or slot1 == slots[3] and slot2 == slots[3]:
                    from Modules.Winp import win_percent
                    game = 'Slots'
                    value = 'win'
                    win_percent(author,game,value)
                    embed.add_field(name="Rolling.....", value="<a:slots:677086128263790612>|<a:slots:677086128263790612>|<a:slots:677086128263790612>", inline=False)
                    message = await ctx.send(embed = embed)
                    await asyncio.sleep(2)
                    embed2.add_field(name = 'Results:',value = f"{slotOutput}", inline=False)
                    amount = amount * 3 - amount
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed2.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount + profit - fine
                    else:
                        users[author]['money'] += amount + profit
    
                    if not profit == 0:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} + ${profit} (Coins X) has been credited.", inline=False)
                    else:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} has been credited.", inline=False)
                    await message.edit(embed = embed2)


                elif slot1 == slots[0] and slot2 == slots[0] and slot3 == slots[0]:
                    from Modules.Winp import win_percent
                    game = 'Slots'
                    value = 'win'
                    win_percent(author,game,value)
                    embed.add_field(name="Rolling.....", value="<a:slots:677086128263790612>|<a:slots:677086128263790612>|<a:slots:677086128263790612>", inline=False)
                    message = await ctx.send(embed = embed)
                    await asyncio.sleep(2)
                    embed2.add_field(name = 'Results:',value = f"{slotOutput}", inline=False)
                    amount = amount * 5 - amount
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed2.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount + profit - fine
                    else:
                        users[author]['money'] += amount + profit
    
                    if not profit == 0:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} + ${profit} (Coins X) has been credited.", inline=False)
                    else:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} has been credited.", inline=False)
                    await message.edit(embed = embed2)


                elif slot1 == slots[1] and slot2 == slots[1] and slot3 == slots[1]:
                    from Modules.Winp import win_percent
                    game = 'Slots'
                    value = 'win'
                    win_percent(author,game,value)
                    embed.add_field(name="Rolling.....", value="<a:slots:677086128263790612>|<a:slots:677086128263790612>|<a:slots:677086128263790612>", inline=False)
                    message = await ctx.send(embed = embed)
                    await asyncio.sleep(2)
                    embed2.add_field(name = 'Results:',value = f"{slotOutput}", inline=False)
                    amount = amount * 5 - amount
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed2.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount + profit - fine
                    else:
                        users[author]['money'] += amount + profit  
    
                    if not profit == 0:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} + ${profit} (Coins X) has been credited.", inline=False)
                    else:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} has been credited.", inline=False)
                    await message.edit(embed = embed2)


                elif slot1 == slots[2] and slot2 == slots[2] and slot3 == slots[2]:
                    from Modules.Winp import win_percent
                    game = 'Slots'
                    value = 'win'
                    win_percent(author,game,value)
                    embed.add_field(name="Rolling.....", value="<a:slots:677086128263790612>|<a:slots:677086128263790612>|<a:slots:677086128263790612>", inline=False)
                    message = await ctx.send(embed = embed)
                    await asyncio.sleep(2)
                    embed2.add_field(name = 'Results:',value = f"{slotOutput}", inline=False)
                    amount = amount * 7 - amount
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed2.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount + profit - fine
                    else:
                        users[author]['money'] += amount + profit  
    
                    if not profit == 0:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} + ${profit} (Coins X) has been credited.", inline=False)
                    else:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} has been credited.", inline=False)
                    await message.edit(embed = embed2)

                elif slot1 == slots[3] and slot2 == slots[3] and slot3 == slots[3]:
                    embed.add_field(name="Rolling.....", value="<a:slots:677086128263790612>|<a:slots:677086128263790612>|<a:slots:677086128263790612>", inline=False)
                    message = await ctx.send(embed = embed)
                    await asyncio.sleep(2)
                    from Modules.Winp import win_percent
                    game = 'Slots'
                    value = 'win'
                    win_percent(author,game,value)
                    embed2.add_field(name = 'Results:',value = f"{slotOutput}", inline=False)
                    amount = amount * 7 - amount
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed2.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount + profit - fine
                    else:
                        users[author]['money'] += amount + profit  
    
                    if not profit == 0:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} + ${profit} (Coins X) has been credited.", inline=False)
                    else:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} has been credited.", inline=False)
                    await message.edit(embed = embed2)
    
                elif slot1 == slots[4] and slot2 == slots[4] and slot3 == slots[4]:
                    await asyncio.sleep(2)
                    from Modules.Winp import win_percent
                    game = 'Slots'
                    value = 'win'
                    win_percent(author,game,value)
                    embed.add_field(name="Rolling.....", value="<a:slots:677086128263790612>|<a:slots:677086128263790612>|<a:slots:677086128263790612>", inline=False)
                    message = await ctx.send(embed = embed)
                    await asyncio.sleep(2)
                    embed2.add_field(name = 'Results:',value = f"{slotOutput}", inline=False)
                    amount = amount * 9 - amount
                    profit = send_coin(author,amount)
                    if not send_fine(author,amount) == 0:
                        fine = send_fine(author,amount)
                        with open('Config/data.json','r') as f:
                            users = json.load(f)
                        embed2.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                        users[author]['money'] += amount + profit - fine
                    else:
                        users[author]['money'] += amount + profit 
    
                    if not profit == 0:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} + ${profit} (Coins X) has been credited.", inline=False)
                    else:
                        embed2.add_field(name= 'Wonderful!',value= f"${amount} has been credited.", inline=False)
                    await message.edit(embed = embed2)


                else:
                    from Modules.Winp import win_percent
                    game = 'Slots'
                    value = 'lose'
                    win_percent(author,game,value)
                    embed.add_field(name="Rolling.....", value="<a:slots:677086128263790612>|<a:slots:677086128263790612>|<a:slots:677086128263790612>", inline=False)
                    message = await ctx.send(embed = embed)
                    await asyncio.sleep(2)
                    embed2.add_field(name = 'Results:',value = f"{slotOutput}", inline=False)
                    embed2.add_field(name= 'Loser!',value= f"${amount} has been Debited.", inline=False)
                    await message.edit(embed = embed2)
                    users[author]["money"] -= amount

                with open("Config/data.json","w") as f:
                    json.dump(users,f,indent = 3)
        
        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(slots(bot))
