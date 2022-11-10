import discord
from discord.ext import commands
import json 
from dateutil import parser
import datetime
from datetime import timedelta
import random
import string
import asyncio


class rob(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def rob(self,ctx,user:discord.User = None):
        
        box = [':laughing: Police found you, Unlucky!',':laughing: The victim attacked at you, What a dumb!','face_with_monocle: The money fell down from your hands, Poor!']
        
        with open("Config/data.json","r") as f:
            data = json.load(f)

        author = str(ctx.author.id)
        

            
        if user == None:
            await ctx.send(':information_source: **Usage:** rob `<@player>`\n:information_source: **Requirement:** `$650 Money`')
            return

        else:
            author2 = str(user.id)
            if not author2 in data:
                await ctx.send(f':warning: `{user.name}` account has not been created yet.')
                return

        if author == author2:
            await ctx.send(':warning: Hey, You cannot ROB Yourself. Please')
            return

        
        elif data[author]['money'] < 650:
            await ctx.send(':warning: You need minimum $650 Money before intitating the robbery.') 
            return

        elif data[author2]['money'] < 500:
            await ctx.send(":warning: Victim doesn't have the required amount. ($500)")
            return

        else:
            if random.randrange(1,100) >= 50:
                amount = round(data[author2]['money'] * 0.7)
                await ctx.send(f':money_with_wings:  You managed to steal {amount} Money.')
                data[author]['money'] += amount
                data[author2]['money'] -= amount

                with open('Config/data.json','w') as f:
                    json.dump(data,f,indent = 3)
            
            else:
                data[author]['money'] -= 650
                await ctx.send(random.choice(box))
                with open('Config/data.json','w') as f:
                    json.dump(data,f,indent = 3)
def setup(bot):
    bot.add_cog(rob(bot)) 