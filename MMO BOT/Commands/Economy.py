import discord
from discord.ext import commands
import random
import json
import asyncio 
from Modules.Currency import currency

class Economy(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases = ['setcurrency'])
    async def set_currency(self,ctx, symbol:str = None):
        with open('Config.json') as f:
            config = json.load(f)
        
        if not 'Currency' in config:
            cc = ':coin:'
        else:
            cc = config['Currency']

        if not symbol:
            msg = f'The currency symbol for this server is {cc}\n\nUsage: set_currency `<symbol>`'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return

        config['Currency'] = symbol
        
        with open('Config.json', 'w') as f:
            json.dump(config,f,indent = 3)
        
        msg = f':white_check_mark: The currency symbol has been updated.'
        embed = discord.Embed(color = discord.Color.green(), description = msg)
        embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['startbalance'])
    async def set_start_balance(self,ctx, bal:str = None):
        with open('Config.json') as f:
            config = json.load(f)
        
        if not 'Currency' in config:
            cc = ':coin:'
        else:
            cc = config['Currency']
        
        start_balance = 0 if not 'Start_Balance' in config else config['Start_Balance']

        if not bal:
            msg = f'The starting balance for new members is set to: {cc}{start_balance}\n\nUsage: set_start_balance <amount>'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return

        config['Start_Balance'] = bal
        
        with open('Config.json', 'w') as f:
            json.dump(config,f,indent = 3)
        
        msg = f':white_check_mark: The starting balance for new members has been set to:  {cc}{start_balance}'
        embed = discord.Embed(color = discord.Color.green(), description = msg)
        embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
        await ctx.send(embed = embed)


    @commands.command(aliases = ['addmoneyrole'])
    async def add_money_role(self,ctx, role:discord.Role,points:int, type_:str = None):
        with open('Config/data.json') as f:
            data = json.load(f)
        
        if not role or not points:
            msg = f'Usage: add_money_role <role> <amount> [cash | bank]'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return
        
        if not type_:
            msg = f':warning: [cash | bank] not provided\n\nUsage: add_money_role <role> <amount> [cash | bank]'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return  

        if not type_.lower() in ('bank', 'cash'):
            msg = f':warning: Invalid Type: Allowed [cash | bank]'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return    

        num = 0
        for user in role.members:
            num += 1
            author = str(user.id)        
            if not author in data:
                data[author] = {}
                data[author]['Points'] = 0
                data[author]['Bank'] = 0
            
            if type_.lower() == 'bank':
                data[author]['Bank'] += points
            
            else:
                data[author]['Points'] += points
            

        with open('Config/data.json', 'w') as f:
            json.dump(data,f,indent = 3)


        msg = f':white_check_mark: Added **{points}{currency()}** to {len(role.members)} member(s) with the {role.mention} role.'
        embed = discord.Embed(color = discord.Color.green(), description = msg)
        embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['addmoney'])
    async def add_money(self,ctx, user:discord.User,points:int, type_:str = None):
        with open('Config/data.json') as f:
            data = json.load(f)
        
        if not user or not points:
            msg = f'Usage: add_money <user> <amount> [cash | bank]'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return
        
        if not type_:
            msg = f':warning: [cash | bank] not provided\n\nUsage: add_money <user> <amount> [cash | bank]'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return  

        if not type_.lower() in ('bank', 'cash'):
            msg = f':warning: Invalid Type: Allowed [cash | bank]'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return    

        author = str(user.id)     
        if not author in data:
            data[author] = {}
            data[author]['Points'] = 0
            data[author]['Bank'] = 0
        
        if type_.lower() == 'bank':
            data[author]['Bank'] += points
        
        else:
            data[author]['Points'] += points
            
        with open('Config/data.json', 'w') as f:
            json.dump(data,f,indent = 3)


        msg = f':white_check_mark: Added **{points}{currency()}** to {user}'
        embed = discord.Embed(color = discord.Color.green(), description = msg)
        embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['removemoneyrole'])
    async def remove_money_role(self,ctx, role:discord.Role,points:int, type_:str = None):
        with open('Config/data.json') as f:
            data = json.load(f)
        
        if not role or not points:
            msg = f'Usage: remove_money_role <role> <amount> [cash | bank]'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return
        
        if not type_:
            msg = f':warning: [cash | bank] not provided\n\nUsage: remove_money_role <role> <amount> [cash | bank]'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return  

        if not type_.lower() in ('bank', 'cash'):
            msg = f':warning: Invalid Type: Allowed [cash | bank]'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return    

        num = 0
        for user in role.members:
            num += 1
            author = str(user.id)        
            if not author in data:
                data[author] = {}
                data[author]['Points'] = 0
                data[author]['Bank'] = 0
            
            if type_.lower() == 'bank':
                if not data[author]['Bank'] - points < 0:
                    data[author]['Bank'] -= points
                else:
                    data[author]['Bank'] = 0
            
            else:
                if not data[author]['Points'] - points < 0:
                    data[author]['Points'] -= points
                else:
                    data[author]['Points'] = 0
            

        with open('Config/data.json', 'w') as f:
            json.dump(data,f,indent = 3)


        msg = f':white_check_mark: Removed **{points}{currency()}** from {len(role.members)} member(s) with the {role.mention} role.'
        embed = discord.Embed(color = discord.Color.green(), description = msg)
        embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['removemoney'])
    async def remove_money(self,ctx, user:discord.User,points:int, type_:str = None):
        with open('Config/data.json') as f:
            data = json.load(f)
        
        if not user or not points:
            msg = f'Usage: remove_money <user> <amount> [cash | bank]'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return
        
        if not type_:
            msg = f':warning: [cash | bank] not provided\n\nUsage: remove_money <user> <amount> [cash | bank]'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return  

        if not type_.lower() in ('bank', 'cash'):
            msg = f':warning: Invalid Type: Allowed [cash | bank]'
            embed = discord.Embed(color = discord.Color.red(), description = msg)
            embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
            return    

        author = str(user.id)     
        if not author in data:
            data[author] = {}
            data[author]['Points'] = 0
            data[author]['Bank'] = 0
        
        if type_.lower() == 'bank':
            if not data[author]['Bank'] - points < 0:
                data[author]['Bank'] -= points
            else:
                data[author]['Bank'] = 0
        
        else:
            if not data[author]['Points'] - points < 0:
                data[author]['Points'] -= points
            else:
                data[author]['Points'] = 0
            
        with open('Config/data.json', 'w') as f:
            json.dump(data,f,indent = 3)


        msg = f':white_check_mark: Removed **{points}{currency()}** from {user}'
        embed = discord.Embed(color = discord.Color.green(), description = msg)
        embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['givemoney'])
    async def give_money(self,ctx,user:discord.User = None,val:int = None):
        with open('Config/data.json') as f:
            data = json.load(f)

        author = str(ctx.author.id)
        if user == None or val == None:
            await ctx.send(f'<:info:833301110835249163> **Usage:** pay `<@user`> `<amount>`')
            return
        
        elif user == None and not val == None:
            await ctx.send('<:info:833301110835249163> Specify the Amount you want to transfer!')
            return
        
        elif val <= 0:
            await ctx.send('<:info:833301110835249163> The amount should be greater than Zero')
            return
            
        elif val > data[author]['Points']:
            await ctx.send("<:info:833301110835249163> You don't have enough Money to transfer.")
            return
        
        else:
            author2 = str(user.id)
            if not author2 in data:
                data[author2] = {}
                data[author2]['Points'] = 0
                data[author2]['Bank'] = 0

            gold = data[author]['Points']
            await ctx.send(f':white_check_mark:**{val}{currency()}** has been transferred to **{user}**\n `(Your remaining Balance is:)` **`${gold - val}`**{currency()}')
            data[author]['Points'] -= val
            data[str(author2)]['Points'] += val
            with open('Config/data.json','w') as f:
                json.dump(data,f,indent = 4)

    @commands.command()
    async def deposit(self,ctx,amount = None):
        with open('Config/prefixes.json','r') as f:
            data = json.load(f)
            
        try:
            author2 = ctx.author.name
            author = str(ctx.author.id)
            with open("Config/data.json","r") as f:
                data = json.load(f)
            bank = data[author]["Bank"]
            money = data[author]["Points"]
            
            if amount == None:
                await ctx.send(f'<:info:833301110835249163> **Usage:** deposit `<amount>`\n**In Hand:** `({money}){currency()}`')
                return
            
            elif not amount == None:
                if int(amount) <= 0:
                    await ctx.send('<:info:833301110835249163> `The amount should greater than ZERO`')
                    return

                elif int(amount) > money:
                    await ctx.send("<:info:833301110835249163> `You don't have the Given Amount.`")
                    return
    
                else:
                    data[author]["Bank"] += int(amount)
                    data[author]["Points"] -= int(amount)
                    await ctx.send(f":white_check_mark: `{int(amount)}`{currency()} has been deposited")
                    with open("Config/data.json","w") as f:
                        json.dump(data,f,indent = 3)
            
        except Exception as e:
            print(e)

    @commands.command()
    async def withdraw(self,ctx,amount = None):
        try:
            author = str(ctx.author.id)
            with open("Config/data.json","r") as f:
                data = json.load(f)

            bank = data[author]["Bank"]
            money = data[author]["Points"]
            
            if amount == None:
                await ctx.send(f'<:info:833301110835249163> **Usage:** withdraw `<amount>`\n**In Bank:** `({bank}){currency()}`')
                return
            
            elif not amount == None:
                if int(amount) <= 0:
                    await ctx.send('<:info:833301110835249163> `The amount should greater than ZERO`')
                    return

                elif int(amount) > bank:
                    await ctx.send("<:info:833301110835249163> `You don't have the Given Amount.`")
                    return
    
                else:
                    data[author]["Bank"] -= int(amount)
                    data[author]["Points"] += int(amount)
                    await ctx.send(f":white_check_mark: `{int(amount)}`{currency()} has been Withdrawn")
                    with open("Config/data.json","w") as f:
                        json.dump(data,f,indent = 3)
            
        except Exception as e:
            print(e)

    @commands.command()
    async def money(self,ctx):
        author = str(ctx.author.id)
        with open("Config/data.json","r") as f:
            data = json.load(f)
        
        bank = data[author]["Bank"]
        money = data[author]["Points"]

        embed = discord.Embed(color = discord.Color.orange())
        embed.set_author(name = ctx.author, url = ctx.author.avatar_url)
        embed.add_field(name = 'Cash', amount = f"{money} {currency()}")
        embed.add_field(name = 'Bank', amount = f"{bank} {currency()}")
        embed.add_field(name = 'Total', amount = f"{money + bank} {currency()}")

        await ctx.send(embed = embed)
    
    @commands.command()
    async def income(self,ctx, role:discord.Role, points:int = None, max:int = None):
        if not role or not points or not max:
            await ctx.send(':information_source: Command Usage: !income <role> <points> <max points per day>')
            return
        
        await ctx.send(':white_check_mark: INCOME Modified.')

def setup(bot):
    bot.add_cog(Economy(bot))