import discord
from discord.ext import commands
import json
import random
from Modules.Double_Coins import send_coin
from Modules.Fine import send_fine
from Modules.Cooldown import add_cooldown
from Modules.Cooldown import get_cooldown
class highlow(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def init(self, bot):
        self.bot = bot

    @commands.command(aliases = ['hl'])
    async def highlow(self,ctx,guess = None, amount: int = None ):
        author = str(ctx.author.id)
        command = 'highlow'
        if not get_cooldown(command,author) == '':
            await ctx.send(get_cooldown(command,author))
            return
        with open('Config/prefixes.json','r') as f:
            pf = json.load(f)
            
        prefix = pf[str(ctx.guild.id)]['Prefix']           
        add_cooldown(command,author,6)
        if guess == None and amount == None:
            embed=discord.Embed(color=0x0080ff)
            embed.set_author(name="High Low || Documentation")
            embed.add_field(name="Profit: ", value="1.5X", inline=False)
            embed.add_field(name="Information: ", value="(`1-5`) Low\n(`6`) Draw\n(`7-10`) High", inline=False)
            embed.add_field(name="Cooldown: ", value="10 Seconds", inline=False)
            embed.add_field(name ='Aliases:',value = '`hl`',inline = False)
            embed.set_footer(text=f"Use: {prefix}highlow <option> <bet>")
            await ctx.send(embed = embed)
            return

        author = str(ctx.author.id)
        author2 = ctx.author.name
        num = random.randint(1,10)
        with open("Config/data.json","r") as f:
            users = json.load(f)
        guess = guess.lower()

        if amount > users[author]["money"]:
            await ctx.send(f"Ey {author2} , You don't have the required money.")
            return

        elif amount <= 0:
            await ctx.send("The amount should be greater than 0")
            return
        
        a = amount
        temp_guess = ['low','high']
        embed=discord.Embed(color=0x80ff00)
        embed.set_author(name=f"HIGHLOW !! Documentation")
        embed.add_field(name="Correct", value=f"Number was: {num}", inline=False)

        embed2=discord.Embed(color=0xff0000)
        embed2.set_author(name=f"HIGHLOW !! {author2}")
        embed2.add_field(name="Wrong", value=f"Number was: {num}", inline=False)
        embed2.add_field(name="Debited", value=f"{a}", inline=False)

        if guess not in temp_guess:
            await ctx.send("Invalid Choice! Allowed Options are: <high> or <low>")
            return

        elif guess.lower() == 'low' and num < 6:
            a = round(amount * 1.5) - amount
            profit = send_coin(author,a)
            if not send_fine(author,a) == 0:
                fine = send_fine(author,a)
                with open('Config/data.json','r') as f:
                    users = json.load(f)
                embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                users[author]['money'] += a + profit - fine
            else:
                users[author]['money'] += a + profit 
            if not profit == 0:
                embed.add_field(name="Credited ", value=f"${a*2} + {profit} (Coins X)", inline=False)
            else:
                embed.add_field(name="Credited:", value=f"${a*2}", inline=False)
    
            with open("Config/data.json","w") as f:
                json.dump(users,f,indent = 3)
                
            await ctx.send(embed = embed)
            with open("Config/data.json","w") as f:
                json.dump(users,f,indent = 3)


        elif guess.lower() == "high" and num > 6:
            from Modules.Winp import win_percent
            game = 'Highlow'
            value = 'win'
            win_percent(author,game,value)

            a = round(amount * 1.5) - amount
            profit = send_coin(author,a)
            if not send_fine(author,a) == 0:
                fine = send_fine(author,a)
                with open('Config/data.json','r') as f:
                    users = json.load(f)
                embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                users[author]['money'] += a + profit - fine
            else:
                users[author]['money'] += a + profit  
            if not profit == 0:
                embed.add_field(name="Credited ", value=f"${a*2} + {profit} (Coins X)", inline=False)
            else:
                embed.add_field(name="Credited:", value=f"${a*2}", inline=False)
    
            with open("Config/data.json","w") as f:
                json.dump(users,f,indent = 3)
                
            await ctx.send(embed = embed)
            with open("Config/data.json","w") as f:
                json.dump(users,f,indent = 3)
        
        elif guess.lower() == 'draw' and num == 6:
            from Modules.Winp import win_percent
            game = 'Highlow'
            value = 'win'
            win_percent(author,game,value)
            a = round(amount * 1.5) - amount
            profit = send_coin(author,a)
            if not send_fine(author,a) == 0:
                fine = send_fine(author,a)
                with open('Config/data.json','r') as f:
                    users = json.load(f)
                embed.set_footer(text =f'Hacking Device Caused: -$ {fine} Fine ')
                users[author]['money'] += a + profit - fine
            else:
                users[author]['money'] += a + profit  
            if not profit == 0:
                embed.add_field(name="Credited ", value=f"${a*2} + {profit} (Coins X)", inline=False)
            else:
                embed.add_field(name="Credited:", value=f"${a*2}", inline=False)
    
            with open("Config/data.json","w") as f:
                json.dump(users,f,indent = 3)
                
            await ctx.send(embed = embed)
            with open("Config/data.json","w") as f:
                json.dump(users,f,indent = 3)

        else:
            from Modules.Winp import win_percent
            game = 'Highlow'
            value = 'lose'
            win_percent(author,game,value)
            users[author]["money"] -= amount
            with open("Config/data.json","w") as f:
                json.dump(users,f,indent = 3)
            await ctx.send(embed = embed2)
    

def setup(bot):
    bot.add_cog(highlow(bot))
