import discord
from discord.ext import commands
import json

class shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def iteminfo(self,ctx,choice:str = None):
        if not choice:
            await ctx.send(':information_source: Usage: !iteminfo `<ITEM NAME>`')
            return

        else:
            author = str(ctx.author.id)

            with open('Config/Weapons.json') as f:
                weapons = json.load(f)
            
            with open('Config/Resources.json') as f:
                resources = json.load(f)

            with open('Config/Items.json') as f:
                items = json.load(f)
            
            choice = choice.lower()

            if choice in weapons:
                embed = discord.Embed(title = f"{choice.title()} | Info", color = discord.Color.green())
                embed.set_image(url = weapons[choice]['Image'])
                embed.add_field(name = 'Price', value = weapons[choice]['Price'], inline = False)
                embed.add_field(name = 'About', value = weapons[choice]['Description'], inline = False)
                await ctx.send(embed = embed)
            
            elif choice in resources:
                embed = discord.Embed(title = f"{choice.title()} | Info", color = discord.Color.green())
                embed.set_image(url = resources[choice]['Image'])
                embed.add_field(name = 'Price', value = resources[choice]['Price'], inline = False)
                embed.add_field(name = 'About', value = resources[choice]['Description'], inline = False)
                await ctx.send(embed = embed)


            elif choice in items:
                embed = discord.Embed(title = f"{choice.title()} | Info", color = discord.Color.green())
                embed.set_image(url = items[choice]['Image'])
                embed.add_field(name = 'Price', value = items[choice]['Price'], inline = False)
                embed.add_field(name = 'About', value = items[choice]['Description'], inline = False)
                await ctx.send(embed = embed)
            
            else:
                await ctx.send(':warning: Invalid Item')

    @commands.command()
    async def shop(self,ctx,choice:str = None,item:str = None, amount:int = None):
        if not choice:
            embed = discord.Embed(color = discord.Color.dark_green(), description = "**Weapons**\n**Resources**\n**Items**")
            embed.set_author(name = "SHOP", icon_url = ctx.author.avatar_url)
            embed.set_footer(text = 'Usage: !shop <category>')
            await ctx.send(embed = embed)
            return
        
        else:
            author = str(ctx.author.id)

            with open('Config/Weapons.json') as f:
                weapons = json.load(f)
            
            with open('Config/Resources.json') as f:
                resources = json.load(f)

            with open('Config/Items.json') as f:
                items = json.load(f)

            with open('Config/Data.json') as f:
                data = json.load(f)

            choice = choice.lower()
            if choice == 'resources':

                
                embed = discord.Embed(title = 'Resources Shop', color = discord.Color.blue())
                for x in resources:
                    description = resources[x]['Description']
                    price = resources[x]['Price']
                    emoji = resources[x]['Emoji']

                    embed.add_field(name = f"{emoji} {x.title()}", value = f"Info: {description}\nPrice: {price}", inline = False)
                
                embed.set_footer(text = f"To Buy: !shop buy <Name> <Quantity>")
                await ctx.send(embed = embed)

            elif choice == 'weapons':

                embed = discord.Embed(title = 'Weapons Shop', color = discord.Color.blue())
                for x in weapons:
                    description = weapons[x]['Description']
                    price = weapons[x]['Price']
                    dmg = weapons[x]['DMG']
                    type_ =  weapons[x]['Type']
                    aura = weapons[x]['Aura']
                    emoji = weapons[x]['Emoji']

                    embed.add_field(name = f"{emoji} {x.title()}", value = f"Info: {description}\nPrice: {price}\nDamage: {dmg}\nType: {type_}\n{aura}", inline = False)
                
                embed.set_footer(text = f"To Buy: !shop buy <Name> <Quantity>")
                await ctx.send(embed = embed)

            elif choice == 'items':                
                embed = discord.Embed(title = 'Items Shop', color = discord.Color.blue())
                for x in items:
                    description = items[x]['Description']
                    price = items[x]['Price']
                    type_ =  items[x]['Type']
                    stre = items[x]['STR']
                    intel = items[x]['INT']
                    agi = items[x]['AGI']
                    emoji = items[x]['Emoji']
                    embed.add_field(name = f"{emoji} {x.title()}", value = f"Info: {description}\nPrice: {price}\nType: {type_}\nAGI: {agi}\nINT: {intel}\nSTR: {stre}", inline = False)
              
                embed.set_footer(text = f"To Buy: !shop buy <Name> <Quantity>")
                await ctx.send(embed = embed)

            elif choice == 'buy':
                item = item.lower()

                if not item or  not amount:
                    await ctx.send(':warning: Missing Item name or Quantity')
                    return
                
                if not item in any(weapons, items, resources):
                    await ctx.send(':warning: Invalid Item Name')
                    return
                
                if amount < 0:
                    await ctx.send(':warning: Invalid Quantity')
                    return
                
                if amount == 0:
                    amount = 1
                
                if item in weapons:
                    coins = data[author]['Coins']
                    total_price = weapons[item]['Price'] * amount
                    if total_price < coins:
                        await ctx.send(':warning: Insufficient Balance')
                        return
                    
                    data[author]['Weapons'][item] = {}
                    data[author]['Coins'] -= total_price
                    with open('Config/Data.json','w') as f:
                        json.dump(data,f,indent = 3)

                    await ctx.send(f':white_check_mark: You have bought {item} for {total_price} COINS.')
                
                elif item in resources:
                    coins = data[author]['Coins']
                    total_price = resources[item]['Price'] * amount
                    if total_price < coins:
                        await ctx.send(':warning: Insufficient Balance')
                        return
                    
                    if not item in data[author]['Inventory']:
                        data[author]['Inventory'][item] = 0

                    data[author]['Inventory'][item] += amount
                    data[author]['Coins'] -= total_price
                    with open('Config/Data.json','w') as f:
                        json.dump(data,f,indent = 3)

                    await ctx.send(f':white_check_mark: You have bought {item} for {total_price} COINS.')

                elif item in items:
                    coins = data[author]['Coins']
                    total_price = items[item]['Price'] * amount
                    if total_price < coins:
                        await ctx.send(':warning: Insufficient Balance')
                        return
                    
                    data[author]['Items'][item] = {}
                    data[author]['Coins'] -= total_price
                    with open('Config/Data.json','w') as f:
                        json.dump(data,f,indent = 3)

                    await ctx.send(f':white_check_mark: You have bought {item} for {total_price} COINS.')
        
            elif choice == 'sell':
                item = item.lower()

                if not item or  not amount:
                    await ctx.send(':warning: Missing Item name or Quantity')
                    return
                
                if not item in any(weapons, items, resources):
                    await ctx.send(':warning: Invalid Item Name')
                    return
                
                if amount < 0:
                    await ctx.send(':warning: Invalid Quantity')
                    return
                
                if amount == 0:
                    amount = 1
                
                if item in weapons:
                    coins = data[author]['Coins']
                    total_price = weapons[item]['Price'] / 2
                    if not item in data[author]['Weapons']:
                        await ctx.send(':warning: Item not found in the inventory.')
                        return
                    
                    data[author]['Weapons'].pop(item)
                    data[author]['Coins'] += total_price

                    with open('Config/Data.json','w') as f:
                        json.dump(data,f,indent = 3)

                    await ctx.send(f':white_check_mark: You have sold {item} for {total_price} COINS.')
                
                elif item in resources:
                    coins = data[author]['Coins']
                    total_price = resources[item]['Price'] * amount / 2                    
                    if not item in data[author]['Inventory']:
                        await ctx.send(':warning: Item not found in the inventory.')
                        return
                    
                    elif data[author]['Inventory'][item] <= 0:
                        await ctx.send(':warning: Item not found in the inventory.')
                        return

                    data[author]['Inventory'][item] -= amount
                    data[author]['Coins'] += total_price

                    with open('Config/Data.json','w') as f:
                        json.dump(data,f,indent = 3)

                    await ctx.send(f':white_check_mark: You have sold {amount} {item} for {total_price} COINS.')

                elif item in items:
                    coins = data[author]['Coins']
                    total_price = items[item]['Price'] / 2
                    if not item in data[author]['Items']:
                        await ctx.send(':warning: Item not found in the inventory.')
                        return
                    
                    data[author]['Items'].pop(item)
                    data[author]['Coins'] += total_price

                    with open('Config/Data.json','w') as f:
                        json.dump(data,f,indent = 3)

                    await ctx.send(f':white_check_mark: You have sold {item} for {total_price} COINS.')

def setup(bot):
    bot.add_cog(shop(bot))

