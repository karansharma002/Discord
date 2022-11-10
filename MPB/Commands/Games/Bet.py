import discord
from discord.ext import commands
import json
import random
from Modules.Double_Coins import send_coin
from Modules.Fine import send_fine
from Modules.Cooldown import add_cooldown
from Modules.Cooldown import get_cooldown
class bet(commands.Cog):
    #@commands.Cog.listener() [EVENT]
    #@commands.command() [COMMAND]
    def init(self, bot):
        self.bot = bot

    #@commands.cooldown(1, 6,commands.BucketType.user)
    @commands.command(alises =['gamble','dicebet'])
    async def bet(self,ctx, amount: int = None):
        author = str(ctx.author.id)
        command = 'bet'
        if not get_cooldown(command,author) == '':
            await ctx.send(get_cooldown(command,author))
            return
            
        add_cooldown(command,author,6)

        author2 = ctx.author.name
        with open('Config/data.json','r') as f:
            users = json.load(f)

        if amount == None:
            embed=discord.Embed(color=0x0080ff)
            embed.set_author(name="Dice Bet")
            embed.add_field(name="Profit: ", value="2X", inline=False)
            embed.add_field(name="Usage: ", value="bet <amount>", inline=False)
            embed.add_field(name="Cooldown: ", value="5 Seconds", inline=False)
            embed.add_field(name ='Aliases:',value = '`dicebet` `gamble`')
            await ctx.send(embed = embed)
            return

        if amount > users[author]["money"]:
            await ctx.send(f"Hey, {author2}, You don't have enough cash.")
            return

        if amount <= 0:
            await ctx.send("The amount should be greater than ZERO.")
            return

        num1 = random.randint(1, 12)
        num2 = random.randint(1, 12)
        
        if num1 > num2:
            from Modules.Winp import win_percent
            game = 'Bet'
            value = 'win'
            win_percent(author,game,value)
            embed=discord.Embed(color=0x80ff00)
            embed.set_author(name=f'Congratulations, You won the Bet.')
            embed.add_field(name=f"{ctx.author.name}", value=f"𝗥𝗼𝗹𝗹𝗲𝗱: {num1}", inline=False)
            embed.add_field(name="Alien", value=f"𝗥𝗼𝗹𝗹𝗲𝗱: {num2}", inline=False)
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
    
            with open("Config/data.json","w") as f:
                json.dump(users,f,indent = 3)
            await ctx.send(embed=embed)

        elif num1 < num2:
            from Modules.Winp import win_percent
            game = 'Bet'
            value = 'lose'
            win_percent(author,game,value)
            embed=discord.Embed(color=0xff0000)
            embed.set_author(name="You lost!!")
            embed.add_field(name=f"{author2}", value=f"𝗥𝗼𝗹𝗹𝗲𝗱: {num1}", inline=False)
            embed.add_field(name="Alien", value=f"𝗥𝗼𝗹𝗹𝗲𝗱: {num2}", inline=False)
            embed.add_field(name="Debited", value=f"${amount}", inline=False)
            await ctx.send(embed=embed)
            users[author]["money"] -= amount
            with open("Config/data.json","w") as f:
                json.dump(users,f,indent = 3)

        else:
            embed=discord.Embed(color=0xffe74d)
            embed.set_author(name="Match Tied")
            embed.add_field(name=f"{author2}", value=f"𝗥𝗼𝗹𝗹𝗲𝗱: {num1}", inline=False)
            embed.add_field(name="Alien", value=f"𝗥𝗼𝗹𝗹𝗲𝗱: {num2}", inline=False)
            await ctx.send(embed = embed)
'''
    @bet.error
    async def bet_error(self,ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            await ctx.send(f"<a:alert_1:677763786664312860> You are on Cooldown, Wait `{int(error.retry_after)}` Seconds.\n`(Prime Users has 3 Seconds Cooldown. `**+donate**` for more info.)`")
            return
'''
def setup(bot):
    bot.add_cog(bet(bot))