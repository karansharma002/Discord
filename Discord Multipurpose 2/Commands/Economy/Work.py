import discord
from discord.ext import commands
import json
import random
import asyncio
import string
from Modules.date_converter import date_sec
from Modules.date_converter import date_min
import datetime
from datetime import timedelta
cooldown = {}
price = 31
fish_price = 42
class work(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def work(self,ctx,val:str = None,val2:str = None):
        author = str(ctx.author.id)
        global cooldown
        def check(message):
            return message.author == ctx.author

        if val == None:
            embed=discord.Embed(description = ':moneybag: Income:\n1: **Miner:** $31 / Stone\n2: **Guessword:** $350',title="To start working: +work `miner/guessword`", color=0x33c2e6)
            embed.set_author(name="Work Help")
            embed.add_field(name="1: Miner", value="Work as a miner and Mine the stones.", inline=False)
            embed.add_field(name ="2: Guessword",value = 'Guess What the word could be?')
            embed.set_footer(text="To start working: work <miner/fishing>")
            await ctx.send(embed= embed)
        
        elif val.lower() == 'guessword':
            with open('Config/data.json','r') as f:
                data = json.load(f)

            cool = 15

            if author in cooldown:
                if date_sec(cooldown[author]) > 0:
                    await ctx.send(f':warning: You recently worked, Try again after: `{date_sec(cooldown[author])}` Seconds.')
                    return
                else:
                    pass

            money = 350
            words = [line.strip() for line in open('Config/words.txt')]
            a = random.choice(words)
            import string_utils
            b = string_utils.shuffle(a)
            embed=discord.Embed(description = f'**Shuffled Word:** `{b.upper()}`',color=0x00ffee)
            embed.set_author(name="Guess it")
            embed.add_field(name="Attempts Left:", value="3/3", inline=False)
            embed.set_footer(text = f'Reply within {cool} Seconds.')
            ab = await ctx.send(embed = embed)
            with open('Config/data.json','r') as f:
                data = json.load(f)
            
            author = str(ctx.author.id)
            try:
                msg = await self.bot.wait_for('message',check = check,timeout = cool)
                if msg.content.lower() == a.lower():
                    embed=discord.Embed(description = f'**The Word Was:** {a}\nReceived: ${money}',color=0x40ff1a)
                    embed.set_author(name="Good Work")
                    #embed.add_field(name="Attempts Left:", value="3/3", inline=False)
                    #embed.set_footer(text = f'Reply within {cool} Seconds.')
                    await ab.edit(embed = embed)
                    data[author]['money'] += money
                    with open('Config/data.json','w') as f:
                        json.dump(data,f,indent = 3)
                    cooldown[author] = str(datetime.datetime.now() + timedelta(minutes = 1))
                    return cooldown

                elif not msg.content.lower() == a.lower():
                    embed=discord.Embed(description = f'**Shuffled Word:** `{b.upper()}`',color=0x00ffee)
                    embed.set_author(name="Wrong Word, Guess Again!")
                    embed.add_field(name="Attempts Left:", value="2/3", inline=False)
                    embed.set_footer(text = f'Reply within {cool} Seconds.')
                    await ab.edit(embed = embed)
                    try:

                        msg = await self.bot.wait_for('message',check = check,timeout = cool)

                    except asyncio.TimeoutError:
                        embed=discord.Embed(description = f'**The Word Was:** `{a.upper()}`',color=0xff1a1a)
                        embed.set_author(name="Timed Out Ya Lost!")
                        #embed.add_field(name="Attempts Left:", value="1/3", inline=False)
                        #embed.set_footer(text = f'Reply within {cool} Seconds.')       
                        await ab.edit(embed = embed) 
                        cooldown[author] = str(datetime.datetime.now() + timedelta(minutes = 1))
                        return cooldown

                    if msg.content.lower() == a.lower():
                        embed=discord.Embed(description = f'**The Word Was:** {a}\nReceived: ${money}',color=0x40ff1a)
                        embed.set_author(name="Good Work")
                        #embed.add_field(name="Attempts Left:", value="3/3", inline=False)
                        #embed.set_footer(text = f'Reply within {cool} Seconds.')
                        await ab.edit(embed = embed)
                        data[author]['money'] += money
                        with open('Config/data.json','w') as f:
                            json.dump(data,f,indent = 3)
                        cooldown[author] = str(datetime.datetime.now() + timedelta(minutes = 1))
                        return cooldown

                    elif not msg.content.lower() == a.lower():
                        embed=discord.Embed(description = f'**Shuffled Word:** `{b.upper()}`',color=0x00ffee)
                        embed.set_author(name="Wrong Word, Guess Again!")
                        embed.add_field(name="Attempts Left:", value="1/3", inline=False)
                        embed.set_footer(text = f'Reply within {cool} Seconds.')
                        await ab.edit(embed = embed)
                        try:
                            msg = await self.bot.wait_for('message',check = check,timeout = cool)
                        except asyncio.TimeoutError:
                            embed=discord.Embed(description = f'**The Word Was:** `{a.upper()}`',color=0xff1a1a)
                            embed.set_author(name="Timed Out Ya Lost!")
                            #embed.add_field(name="Attempts Left:", value="1/3", inline=False)
                            #embed.set_footer(text = f'Reply within {cool} Seconds.')       
                            await ab.edit(embed = embed) 
                            cooldown[author] = str(datetime.datetime.now() + timedelta(minutes = 1))
                            return cooldown

                        if msg.content.lower() == a.lower():
                            embed=discord.Embed(description = f'**The Word Was:** {a}\nReceived: ${money}',color=0x40ff1a)
                            embed.set_author(name="Good Work")
                            #embed.add_field(name="Attempts Left:", value="3/3", inline=False)
                            #embed.set_footer(text = f'Reply within {cool} Seconds.')
                            await ab.edit(embed = embed)
                            data[author]['money'] += money
                            with open('Config/data.json','w') as f:
                                json.dump(data,f,indent = 3)
                            cooldown[author] = str(datetime.datetime.now() + timedelta(minutes = 1))
                            return cooldown

                        else:
                            embed=discord.Embed(description = f'**The Word Was:** `{a.upper()}`',color=0xff1a1a)
                            embed.set_author(name="Poor Work, Ya Lost!")
                            #embed.add_field(name="Attempts Left:", value="1/3", inline=False)
                            cooldown[author] = str(datetime.datetime.now() + timedelta(minutes = 1))
                            return cooldown

            except asyncio.TimeoutError:
                embed=discord.Embed(description = f'**The Word Was:** `{a.upper()}`',color=0xff1a1a)
                embed.set_author(name="Timed Out Ya Lost!")
                #embed.add_field(name="Attempts Left:", value="1/3", inline=False)
                #embed.set_footer(text = f'Reply within {cool} Seconds.')       
                await ab.edit(embed = embed) 
                cooldown[author] = str(datetime.datetime.now() + timedelta(minutes = 1))
                return cooldown
            
 
        elif val.lower() == 'miner':
            global price
            guild = str(ctx.guild.id)
            with open('Config/data.json','r') as f:
                data = json.load(f)

            num = 0
            author = str(ctx.author.id)
            axe = 40
            stamina = 30
            

        
            N = 7
            guild = str(ctx.guild.id)

            if val2 == None:
                embed=discord.Embed(title="To Start Mining: +work `miner` `start`",color=0xc0c0c0)
                embed.set_author(name="Miner Job")
                embed.add_field(name="> **Information:**", value="> Your Stamina decreases each time you mine.\n> The more rocks, The more damage is done to your axe.\n> You can carry as much you want\n> Beware of Losing it due to Body Stability.", inline=False)
                embed.add_field(name="> **Payout:**", value=f"> **`{price} Coins` / Per Stone**", inline=False)
                await ctx.send(embed = embed)
                return

            elif val2.lower() == 'start':
                embed=discord.Embed(title="  Mining the Stones   ", color=0x460080)
                embed.add_field(name="> **Total Mined:**", value="> **`0` STONES**", inline=False)
                embed.add_field(name="> **Total Income:**", value="> **`0 Coins`**", inline=False)
                embed.add_field(name="> **Stamina Left:**", value=f"> **`{stamina}`**", inline=False)
                embed.add_field(name="> **Axe Health:**", value=f"> **`{axe}`**", inline=False)
                msg = await ctx.send(embed = embed)
                await asyncio.sleep(2)
                b = random.randint(1,4)
                num += b
                axe -= random.randint(5,20)
                stamina -= random.randint(7,20)
                msg1 = await ctx.send('**Type:** `mine` **To Mine some stones.**')
                vc = await self.bot.wait_for('message',check = check)
                dc = str(vc.content)
                await msg1.delete()
                await vc.delete()
                if dc.lower() == 'mine':
                    embed2=discord.Embed(title="  Mining the Stones   ", color=0x460080)
                    embed2.add_field(name="> **Total Mined:**", value=f"> **`{num}` STONES**", inline=False)
                    embed2.add_field(name="> **Total Income:**", value=f"> **`{num*price} Coins`**", inline=False)
                    embed2.add_field(name="> **Stamina Left:**", value=f"> **`{stamina}`**", inline=False)
                    embed2.add_field(name="> **Axe Health:**", value=f"> **`{axe}`**", inline=False)
                    await msg.edit(embed = embed2)
                    if stamina <= 0:
                        await ctx.send('You ran out of the Stamina, Thus you dropped all the rocks from your Hands.')
                        return
                    elif axe <= 0 :
                        
                        await ctx.send('Your Axe is damaged very badly, You cannot Mine any more rocks.')
                        return
                else:
                    await ctx.send(':warning: Invalid CODE Entered, Better Luck Next Time!')
                    return

                if random.randint(1,50) >= 25:
                    msg1 = await ctx.send(f"**Would you like to deliver the Stones?**\n**Don't wory, You can continue it at your own risk.**\n**Total Stones are: `{num}` **\n**Reply with: `yes/no`**")
                    msg2 = await self.bot.wait_for('message', check=check)
                    data1 = str(msg2.content)
                    await msg1.delete()
                    await msg2.delete()
                    if data1.lower() == 'yes':
                        await ctx.send(f":tada: **You have succesfully delivered `{num}` STONES.**:tada: \n:tada: **Your payout is: `{num*price} Coins` :tada:**")
                        data[author]['money'] += num*price
                        with open('Config/data.json','w') as f:
                            json.dump(data,f,indent = 4)

                    elif data1.lower() == 'no':
                        msg1 = await ctx.send(":warning: **BEWARE!!** You are on the risk of falling the `STONES` down from your hands. :warning:")
                        await asyncio.sleep(2)
                        await msg1.delete()
                        if random.randint(1,100) <= 50:
                            await ctx.send(":warning: **You Dropped all `STONES` Due to overweight. Better Luck Next time!**")
                            return

                        elif random.randint(1,100) > 50:
                            code = ''.join(random.choices(string.ascii_uppercase +string.digits, k = N)) 
                            code = str(code)
                            msg1 =await ctx.send(f":notepad_spiral: Enter The Following Code to continue the Mining: `{code}`")
                            user_input = await self.bot.wait_for("message",check = check)
                            data1 = str(user_input.content)
                            await msg1.delete()
                            await user_input.delete()           
                            if data1 == code:
                                b = num + random.randint(1,3)
                                stamina -= random.randint(7,20)
                                axe -= random.randint(5,20)
                                if b < 8:   
                                    embed3=discord.Embed(title="Miner Job", color=0xff0080)
                                    embed3=discord.Embed(title="  Mining the Stones   ", color=0x460080)
                                    embed3.add_field(name="> **Total Mined:**", value=f"> **`{num}` STONES**", inline=False)
                                    embed3.add_field(name="> **Total Income:**", value=f"> **`{num*price} Coins`**", inline=False)
                                    embed3.add_field(name="> **Stamina Left:**", value=f"> **`{stamina}`**", inline=False)
                                    embed3.add_field(name="> **Axe Health:**", value=f"> **`{axe}`**", inline=False)
                                    await msg.edit(embed = embed3)
                                    if stamina <= 0:
                                        await ctx.send('You ran out of the Stamina, Thus you dropped all the rocks from your Hands.')
                                        return

                                    elif axe <= 0 :
                                        
                                        await ctx.send('Your Axe is damaged very badly, You cannot Mine any more rocks.')
                                        return

                                    await asyncio.sleep(2)
                                    msg2 = await ctx.send(f":cry: You fallen down due to hitting the Rock with your feet\nType: `deliver` to deliver the STONES")
                                    v = await self.bot.wait_for("message",check = check)
                                    vc = str(v.content)
                                    await v.delete()
                                    await msg2.delete() 
                                    if vc.lower() == 'deliver':
                                        await ctx.send(f":tada: **You have succesfully delivered `{num}` STONES. **:tada: \n:tada: **Your payout is: `{num*price} Coins`**:tada: ")
                                        data[author]['money'] += num*price
                                        with open('Config/data.json','w') as f:
                                            json.dump(data,f,indent = 4)
                                        return
                                    else:
                                        await ctx.send(':warning: Invalid CODE Entered, Better Luck Next Time!')
                                        return

                                elif b > 7:
                                    await ctx.send(":warning: You Dropped all the Stones due to Overweight. Better Luck Next time.")
                                    return

                            elif data1 != code:
                                await ctx.send(':warning: Invalid CODE Entered, Better Luck Next Time!')
                                return

                    else:
                        await ctx.send(':warning: Invalid CODE Entered, Better Luck Next Time!')
                        return

                else:
                    b = random.randint(1,3)
                    num += b
                    ab = await ctx.send(' Mining the stones.')
                    embed4=discord.Embed(title="Miner Job", color=0xff0080)
                    embed4=discord.Embed(title="  Mining the Stones   ", color=0x460080)
                    embed4.add_field(name="> **Total Mined:**", value=f"> **`{num}` STONES**", inline=False)
                    embed4.add_field(name="> **Total Income:**", value=f"> **`{num*price} Coins`**", inline=False)
                    embed4.add_field(name="> **Stamina Left:**", value=f"> **`{stamina}`**", inline=False)
                    embed4.add_field(name="> **Axe Health:**", value=f"> **`{axe}`**", inline=False)
                    await msg.edit(embed = embed4)
                    if stamina <= 0:
                        await ctx.send('You ran out of the Stamina, Thus you dropped all the rocks from your Hands.')
                        return
                    elif axe <= 0 :
                        
                        await ctx.send('Your Axe is damaged very badly, You cannot Mine any more rocks.')
                        return
                    await asyncio.sleep(2)
                    await ab.delete()
                    code = ''.join(random.choices(string.ascii_uppercase +string.digits, k = N)) 
                    code = str(code)
                    ab = await ctx.send(f':notepad_spiral: Type The Following Code to Collect the STONES: `{code}`')
                    userinput = await self.bot.wait_for('message',check = check)
                    data1 = str(userinput.content)
                    await userinput.delete()
                    await ab.delete()
                    if data1 == code:
                        msg1 = await ctx.send(f"**Would you like to deliver the Stones?**\n**Don't wory, You can continue it at your own risk.**\n**Total Stones are: `{num}` **\n**Reply with: `yes/no`**")
                        msg2 = await self.bot.wait_for('message', check=check)
                        data1 = str(msg2.content)
                        await msg1.delete()
                        await msg2.delete()
                        c = random.randint(1,3)
                        if data1.lower() == 'yes':
                            await ctx.send(f":tada: **You have succesfully delivered `{num}` STONES.**:tada: \n:tada: **Your payout is: `{num*price} Coins` :tada:**")
                            data[author]['money'] += num*price
                            with open('Config/data.json','w') as f:
                                json.dump(data,f,indent = 4)
                            return
                        
                        elif data1.lower() == 'no':
                            msg1 = await ctx.send(":warning: **BEWARE!!** You are on the risk of falling the `STONES` down from your hands. :warning:")

                        await asyncio.sleep(2)

                        if random.randint(1,100) <= 50:
                            await ctx.send(":warning: You Dropped all the Stones due to Overweight. Better Luck Next time.")
                            return

                        elif random.randint(1,100) > 50:
                            b = random.randint(1,3)
                            num += b
                            stamina -= random.randint(7,20)
                            axe -= random.randint(5,20)
                            embed4=discord.Embed(title="Miner Job", color=0xff0080)
                            embed4=discord.Embed(title="  Mining the Stones   ", color=0x460080)
                            embed4.add_field(name="> **Total Mined:**", value=f"> **`{num}` STONES**", inline=False)
                            embed4.add_field(name="> **Total Income:**", value=f"> **`{num*price} Coins`**", inline=False)
                            embed4.add_field(name="> *Stamina Left:**", value=f"> **`{stamina}`**", inline=False)
                            embed4.add_field(name="> **Axe Health:**", value=f"> **`{axe}`**", inline=False)
                            await msg.edit(embed = embed4)
                            if axe <= 0 :
                                
                                await ctx.send('Your Axe is damaged very badly, You cannot Mine any more rocks.')
                                return
                            await asyncio.sleep(2)
                            if stamina <= 0:

                                msg2 = await ctx.send(f":cry: You ran out of Stamina. Type: `deliver` to deliver the STONES")
                                v = await self.bot.wait_for("message",check = check)
                                vc = str(v.content)
                                await v.delete()
                                await msg2.delete() 
                                if vc.lower() == 'deliver':
                                    await ctx.send(f":tada: **You have succesfully delivered `{num}` STONES.**:tada: \n:tada: **Your payout is: `{num*price} Coins` :tada:**") 
                                    data[author]['money'] += num*price
                                    with open('Config/data.json','w') as f:
                                        json.dump(data,f,indent = 4)
                                    return

                                else:
                                    await ctx.send(':warning: You failed to deliver in the right time, You earned nothing!')
                                    return
                            else:
                                b = num + random.randint(1,3)
                                axe -= random.randint(5,20)
                                if b < 8:   
                                    stamina = 0
                                    embed3=discord.Embed(title="Miner Job", color=0xff0080)
                                    embed3=discord.Embed(title="Mining the Stones   ", color=0x460080)
                                    embed3.add_field(name="> **Total Mined:**", value=f"> **`{num}` STONES**", inline=False)
                                    embed3.add_field(name="> **Total Income:**", value=f"> **`{num*price} Coins`**", inline=False)
                                    embed3.add_field(name="> **Stamina Left:**", value=f"> **`{stamina}`**", inline=False)
                                    embed3.add_field(name="> **Axe Health:**", value=f"> **`{axe}`**", inline=False)
                                    await msg.edit(embed = embed3)
                                    if axe <= 0 :
                                        
                                        await ctx.send('Your Axe is damaged very badly, You cannot Mine any more rocks.')
                                        return
                                    await ctx.send(f":tada: **You have succesfully delivered `{num}` STONES.**:tada: \n:tada: **Your payout is: `{num*price} Coins` :tada:**") 
                                    data[author]['money'] += num*price
                                    with open('Config/data.json','w') as f:
                                        json.dump(data,f,indent = 4)
                                    return

                    else:
                        await ctx.send(':warning: Invalid CODE Entered: Better Luck Next Time')
                        return
        
def setup(bot):
    bot.add_cog(work(bot))