import discord
from discord.ext import commands
import json 
from dateutil import parser
import datetime
from datetime import timedelta
import random
import string
import asyncio
from Modules.date_converter import date_min

def rob_time(author):
    with open('Config/Cooldowns.json','r') as f:
        data = json.load(f)
    try:     
        t3 = parser.parse(data[author]['Rob'])
        t4 = parser.parse(str(datetime.datetime.now()))
        c = t3 - t4
        d = c.total_seconds()
        b = round(d/60)
        if b <= 0:
            data[author]['Rob'] = '0'
            with open('Config/Cooldowns.json','w') as f:
                json.dump(data,f,indent = 3)
            
            return 0
        else:
            return b

    except Exception:
        return 0

class rob(commands.Cog):
#@commands.Cog.listener() [EVENT]
#@commands.command() [COMMAND]
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def rob(self,ctx,user:discord.User = None):
        loss_words = ["You tried to ran away with the cash but the cop caught you around the corner. You had to pay `$650` in order to get away from the heat.",
        "You tried to run but unluckily, your clothes got stuck in the fence and you got caught. You had to return the purse and `$650` on the top of that.",
        "You tried to snatch the bag but the person was stronger than you and you got a really nasty punch on the face. The person not only saved his bag but also took `$650` from you. I feel pity on you.",
        "You got over smart and thought that you can do it but the person was a cop who caught you on the spot. You had to pay `$650` for the bail."]

        box = ['Police found you, To run away','The victim attacked at you, To resist','The money fell down from your hands, ']
        with open("Config/data.json","r") as f:
            data = json.load(f)
        author = str(ctx.author.id)
        
        def check(message):
            return message.author == ctx.author
        with open('Config/prefixes.json','r') as f:
            pf = json.load(f)
        
        with open('Config/Cooldowns.json','r') as f:
            cd = json.load(f)
        

        prefix = pf[str(ctx.guild.id)]['Prefix']            
        if user == None:
            await ctx.send(f'<:info:833301110835249163> **Usage:** {prefix}rob `<@player>`\n<:info:833301110835249163> **Requirement:** `$650 Money`\n<:info:833301110835249163> **Cooldown:** `5` Minutes')
            return

        else:
            author2 = str(user.id)
            if not author2 in data:
                await ctx.send(f'<a:alert:833301110587785267> `{user.name}` account has not been created yet.')
                return

        if author == author2:
            await ctx.send('<a:alert:833301110587785267> Hey, You cannot ROB Yourself. Please')
            return

        elif rob_time(author) > 0:
            await ctx.send(f"<a:alert:833301110587785267> You recently attempted the robbery, Wait for `{rob_time(author)}` Minutes.\n`(Prime Users has 2 minutes cooldown. (+donate) for more info)`")
            return
        
        elif data[author]['money'] < 650:
            await ctx.send('<a:alert:833301110587785267> You need minimum $650 Money before intitating the robbery.') 
            return
        
        elif not data[author2]['items']['Vault'] == '0':
            await ctx.send('<a:alert:833301110587785267> `Oops The victim has a Vault Setup, You cannot ROB Them.`')
            return

        elif data[author2]['money'] < 500:
            await ctx.send("<a:alert:833301110587785267> Victim doesn't have the required amount. ($500)")
            return
        else:
            if random.randint(1,100) > 50:
                if random.randint(1,100) > 50:
                    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 7))
                    code = str(code)
                    try:
                        try:
                            if data[author2]['Mine'] == 'Deployed':
                                a = round(data[author]['money'] * 0.7)
                                await ctx.send(f':sparkler: :sparkler: Oops, The Person had a (<:mine:737909491269501028> Remote Mine) Deployed, it Blasted. :sparkler: :sparkler:\n(:sparkler: :sparkler: `You lost ${a} Coins` :sparkler: :sparkler:)')
                                data[author]['money'] -= a
                                data[author2]['Mine'] = 'None'
                                with open('Config/data.json','w') as f:
                                    json.dump(data,f,indent = 3)
                                return

                        except KeyError:
                            pass

                        await ctx.send(f'{random.choice(box)}, **Type:** `{code}` in `10` Seconds.')
                        msg = await self.bot.wait_for('message',check = check,timeout = 10)
                        if str(msg.content.upper()) == code:
                            member = user.name
                            money = round(0.6 * data[author2]['money'])
                            data[author]['money'] += money
                            data[author2]['money'] -= money
                            if not author in cd:
                                cd[author] = {}
                            cd[author]['Rob'] = str(datetime.datetime.now() + timedelta(minutes = 5))
                            data[author2]['Last Robbery'] = str(datetime.datetime.now() + timedelta(seconds = 40))
                            data[author2]['Loss'] = money
                            a = random.randint(1,5)
                            if a == 1:
                                await ctx.send(f":tada: **Congratulations**, You've succesfully robbed the {member}. The purse had :moneybag: ${money} Money. Enjoy!!")
                            elif a == 2:
                                await ctx.send(f":tada: **Congrats**, You succesfully stolen :moneybag: ${money} Money. Buy some drinks now!")
                            elif a == 3:
                                await ctx.send(f"You've gotten away with the bag full of money. **Congrats,** You've robbed {member} and got :moneybag:  ${money} Money. Get some clothes now for god's sake.")
                            elif a == 4:
                                await ctx.send(f"You've quickly ran away dodging the cops behind you and succesfully stole :moneybag: ${money} cash from the {member}. Lay low for a while now!")
                            elif a == 5:
                                await ctx.send(f"You snatched the bag and found a bike and drove it quickly with the bag of money. Congrats, You've stolen :moneybag: ${money} cash from the {member}. Have fun with that!")

                        else:
                            data[author]['money'] -= 650
                            await ctx.send(random.choice(loss_words))
                            

                    except asyncio.TimeoutError:
                        data[author]['money'] -= 650
                        await ctx.send(random.choice(loss_words))
                        
                else:
                    try:
                        if data[author2]['Mine'] == 'Deployed':
                            a = round(data[author]['money'] * 0.7)
                            await ctx.send(f':sparkler: :sparkler: Oops, The Person had a (<:mine:737909491269501028> Remote Mine) Deployed, it Blasted. :sparkler: :sparkler:\n(:sparkler: :sparkler: `You lost ${a} Coins` :sparkler: :sparkler:)')
                            
                            data[author]['money'] -= a
                            data[author2]['Mine'] = 'None'
                            with open('Config/data.json','w') as f:
                                json.dump(data,f,indent = 3)
                            return
                            
                    except KeyError:
                        pass
                    member = user.name
                    money = round(0.6 * data[author2]['money'])
                    data[author]['money'] += money
                    data[author2]['money'] -= money
                    if not author in cd:
                        cd[author] = {}
                    cd[author]['Rob'] = str(datetime.datetime.now() + timedelta(minutes = 5))
                    data[author2]['Last Robbery'] = str(datetime.datetime.now() + timedelta(seconds = 40))
                    data[author2]['Loss'] = money
                    a = random.randint(1,5)
                    if a == 1:
                        await ctx.send(f":tada: **Congratulations**, You've succesfully robbed the {member}. The purse had :moneybag: ${money} Money. Enjoy!!")
                    elif a == 2:
                        await ctx.send(f":tada: **Congrats**, You succesfully stolen :moneybag: ${money} Money. Buy some drinks now!")
                    elif a == 3:
                        await ctx.send(f"You've gotten away with the bag full of money. **Congrats,** You've robbed {member} and got :moneybag: ${money} Money. Get some clothes now for god's sake.")
                    elif a == 4:
                        await ctx.send(f"You've quickly ran away dodging the cops behind you and succesfully stole :moneybag: ${money} cash from the {member}. Lay low for a while now!")
                    elif a == 5:
                        await ctx.send(f"You snatched the bag and found a bike and drove it quickly with the bag of money. Congrats, You've stolen :moneybag: ${money} cash from the {member}. Have fun with that!")


            else:
                data[author]['money'] -= 650
                if not author in cd:
                    cd[author] = {}
                cd[author]['Rob'] = str(datetime.datetime.now() + timedelta(minutes = 5))
                await ctx.send(random.choice(loss_words))

            with open('Config/data.json','w') as f:
                json.dump(data,f,indent = 3)
            
            with open('Config/Cooldowns.json','w') as f:
                json.dump(cd,f,indent = 3)

def setup(bot):
    bot.add_cog(rob(bot)) 