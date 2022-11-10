import discord
from discord.ext import commands
import random
import json
import asyncio 

class Economy(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.cooldown(1, 300, commands.BucketType.user)
    @commands.command()
    async def crime(self,ctx):
        author = str(ctx.author.id)
        with open('Config/data.json','r') as f:
            data = json.load(f)
        if random.randint(1,100) <= 70:
            money = random.randint(60,300)
            a = [f"You searched your room and your foot got on the top of some metallic item. Congrats, You've found **${money}** underneath your shoe.",
            f"You went out of the house and you've seen something shining in the grass. You came closer and found that it's a penny worth of **${money}**. You felt happy :relieved:",
            f"While sitting in your room, you scratched your head thinking about money & you found one coin stuck in your hairs. You've found **${money}**",
            f"You wished the falling star for some money and when you turned back, then you found a bag. You've opened it and find trash inside with **${money}** bucks. Congrats :tada:",
            f"You went out searching for some money. You saw a beggar there and sat with him, peoples came and thought you're a beggar too and they gave you some money. You've got **${money}** bucks.",
            f"You went to a friend's house and opened the fridge to drink water but you saw that there are **${money}** worth of cash hidden inside. You took it immediately and ran away. \n[PS: He is still searching for his money] ",
            f"You went out in the street and you saw a blind beggar. You slowly sat near him and stole all the money from his bucket and ran away with **${money}**. Shame on you!!"]
            await ctx.send(random.choice(a))
            data[author]['money'] += money

        else:
            money = random.randint(1,25)
            a = [f"You went out in the street and you saw a blind beggar. You slowly sat near him and stole all the money from his bucket and ran away with **${money}**. Shame on you!!",
            f"You were walking in the street and you again found a blind beggar, Your devin mind told you to stole & while you were stealing from his bucket, the beggar grabs your hand. You had to return him the money and gave **${money}** on the top of that.\n[PS: The beggar was acting blind]",
            f"You found some cash on the street. When you tried to pick it up, it got flied away with air. You ran behind and came in the middle of the road. You just paid **${money}** as hospital charges.",
            f"You tried to become over-smart and started acting like a beggar in the street with new branded clothes. Police caught you on the spot. You have to pay **${money}** for the bail."]
            await ctx.send(random.choice(a))
            if data[author]['money'] - money < 0:
                data[author]['money'] = 0
            else:
                data[author]['money'] -= money
        
        with open('Config/data.json','w') as f:
            json.dump(data,f,indent = 3)

def setup(bot):
    bot.add_cog(Economy(bot))
