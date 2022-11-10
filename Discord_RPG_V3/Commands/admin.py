import discord
from discord.ext import commands
import json
import random

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator = True)
    @commands.command()
    async def mines(self, ctx,param:str = None, value:str = None):
        if not param or not value:
            await ctx.send(':information_source: Command Usage: !mines `<#PARAMETER>` `<#VALUE>`')
            return
        
        with open('Config/Settings.json') as f:
            settings = json.load(f)
        
        if not param.lower() in ('digcooldown', 'digxp',' digcoin', 'orehp',' orehit', 'minecooldown', 'minexp',' minecoin',\
            'stone', 'iron', 'sword', 'crown', 'gem'):

            await ctx.send(':warning: Invalid Choice')
            return
        
        settings[param.lower()] = value

        with open('Config/Settings.json', 'w') as f:
            json.dump(settings,f,indent = 3)
        
        await ctx.send(f':white_check_mark: {param} value modified.')
        
    @commands.command()
    async def makeres(self, ctx,name:str = None, emoji:str = None, price:int = None,*, desc:str = None):
        if not name or not emoji or not price or not desc:
            await ctx.send(':information_source: Command Usage: !makeres `<NAME [SPACE AS _]>` `<EMOJI>` `<PRICE>` `<DESCRIPTION>`')
            return
        
        with open('Config/Resources.json') as f:
            assets = json.load(f)
        
        name = name.lower()

        if name in assets:
            await ctx.send(':warning: Resource already exists.')
            return

        assets[name] = {}
        assets[name]['Emoji'] = emoji
        assets[name]['Price'] = price
        assets[name]['Description'] = desc

        with open('Config/Resources.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: {name} Added.')


    @commands.command()
    async def editres(self, ctx,name:str = None, emoji:str = None, price:int = None,*, desc:str = None):
        if not name or not emoji or not price or not desc:
            await ctx.send(':information_source: Command Usage: !editres `<NAME [SPACE AS _]>` `<EMOJI>` `<PRICE>` `<DESCRIPTION>`')
            return
        
        with open('Config/Resources.json') as f:
            assets = json.load(f)
        
        name = name.lower()
        if not name in assets:
            await ctx.send(':warning: Resource not exist.')
            return

        assets[name]['Emoji'] = emoji
        assets[name]['Price'] = price
        assets[name]['Description'] = desc

        with open('Config/Resources.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: {name} Edited.')


    @commands.command()
    async def deleteres(self, ctx, name:str = None):
        if not name:
            await ctx.send(':information_source: Command Usage: !deleteres `<NAME [SPACE AS _]>` ')
            return
        
        with open('Config/Resources.json') as f:
            assets = json.load(f)
        
        name = name.lower()
        if not name in assets:
            await ctx.send(':warning: Resource not exist.')
            return

        assets.pop(name)

        with open('Config/Resources.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: {name} Removed.')

    @commands.command()
    async def spawnres(self, ctx, name:str = None, user:discord.User = None, amount:int = None):
        if not name or not user or not amount:
            await ctx.send(':information_source: Command Usage: !spawnres `<NAME [SPACE AS _]>` `<@USER>` `<AMOUNT>`')
            return
        
        with open('Config/Resources.json') as f:
            assets = json.load(f)

        with open('Config/Data.json') as f:
            config = json.load(f)

        name = name.lower()
        author = str(user.id)

        if not name in assets:
            await ctx.send(':warning: Resource not exist.')
            return

        if not author in config:
            await ctx.send(':warning: User not found!')
            return

        if not name in config[author]['Inventory']:
            config[author]['Inventory'][name] = 0

        config[author]['Inventory'][name] += 1

        with open('Config/Resources.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: Added `{amount}` of {name} to {user}')

    @commands.command()
    async def removeres(self, ctx, name:str = None, user:discord.User = None, amount:int = None):
        if not name or not user or not amount:
            await ctx.send(':information_source: Command Usage: !removeres `<NAME [SPACE AS _]>` `<@USER>` `<AMOUNT>`')
            return
        
        with open('Config/Resources.json') as f:
            assets = json.load(f)
        
        with open('Config/Data.json') as f:
            config = json.load(f)

        name = name.lower()
        author = str(user.id)

        if not name in assets:
            await ctx.send(':warning: Resource not exist.')
            return

        if not author in config:
            await ctx.send(':warning: User not found!')
            return

        if not name in config[author]['Inventory']:
            config[author]['Inventory'][name] = 0

        else:
            if config[author]['Inventory'][name] - amount <= 0:
                config[author]['Inventory'][name] -= amount
            else:
                config[author]['Inventory'][name] = 0

        with open('Config/Resources.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: Removed `{amount}` of {name} from {user}')

    @commands.command()
    async def makeweapon(self, ctx,name:str = None,type_:str = None,emoji:str = None,dmg:str = None,aura:str = None, price:int = None,*, desc:str = None):
        if not name or not emoji or not price or not desc or not dmg or not aura or not type_:
            await ctx.send(':information_source: Command Usage: !makeweapon `<NAME [SPACE AS _]>` <`TYPE>` `<EMOJI>` `<DMG>` `<AGI/STR/INT>` `<PRICE>` `<DESCRIPTION>`')
            return
        
        with open('Config/Weapons.json') as f:
            assets = json.load(f)
        
        name = name.lower()

        if name in assets:
            await ctx.send(':warning: Weapon already exists.')
            return

        assets[name] = {}
        assets[name]['Emoji'] = emoji
        assets[name]['Price'] = price
        assets[name]['Description'] = desc
        assets[name]['DMG'] = dmg
        assets[name]['Type'] = type_
        assets[name]['Aura'] = aura

        with open('Config/Weapons.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: {name} Added.')


    @commands.command()
    async def editweapon(self, ctx,name:str = None,type_:str = None,emoji:str = None,dmg:str = None,aura:str = None, price:int = None,*, desc:str = None):
        if not name or not emoji or not price or not desc or not dmg or not aura or not type_:
            await ctx.send(':information_source: Command Usage: !makeweapon `<NAME [SPACE AS _]>` <`TYPE>` `<EMOJI>` `<DMG>` `<AGI/STR/INT>` `<PRICE>` `<DESCRIPTION>`')
            return            
        
        with open('Config/Weapons.json') as f:
            assets = json.load(f)
        
        name = name.lower()

        if not name in assets:
            await ctx.send(':warning: Weapon not found!')
            return

        assets[name]['Emoji'] = emoji
        assets[name]['Price'] = price
        assets[name]['Description'] = desc
        assets[name]['DMG'] = dmg
        assets[name]['Type'] = type_
        assets[name]['Aura'] = aura

        with open('Config/Weapons.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: {name} Edited.')


    @commands.command()
    async def deleteweapon(self, ctx, name:str = None):
        if not name:
            await ctx.send(':information_source: Command Usage: !deleteweapon `<NAME [SPACE AS _]>` `<REFUND AMOUNT [OPTIONAL]>`')
            return
        
        with open('Config/Weapons.json') as f:
            assets = json.load(f)
        
        name = name.lower()
        if not name in assets:
            await ctx.send(':warning: Weapon not exist.')
            return

        assets.pop(name)

        with open('Config/Weapons.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: {name} Removed.')

    @commands.command()
    async def spawnweapon(self, ctx, name:str = None, user:discord.User = None, amount:int = None):
        if not name or not user or not amount:
            await ctx.send(':information_source: Command Usage: !spawnweapon `<NAME [SPACE AS _]>` `<@USER>`')
            return
        
        with open('Config/Weapons.json') as f:
            assets = json.load(f)

        with open('Config/Data.json') as f:
            config = json.load(f)

        name = name.lower()
        author = str(user.id)

        if not name in assets:
            await ctx.send(':warning: Weapon not exist.')
            return

        if not author in config:
            await ctx.send(':warning: User not found!')
            return

        config[author]['Weapons'][name] = {}
        
        with open('Config/Weapons.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: Spawned {name} to {user}')

    @commands.command()
    async def removeweapon(self, ctx, name:str = None, user:discord.User = None):
        if not name or not user:
            await ctx.send(':information_source: Command Usage: !removeweapon `<NAME [SPACE AS _]>` `<@USER>` ')
            return
        
        with open('Config/Weapons.json') as f:
            assets = json.load(f)
        
        with open('Config/Data.json') as f:
            config = json.load(f)

        name = name.lower()
        author = str(user.id)

        if not name in assets:
            await ctx.send(':warning: Weapon not exist.')
            return

        if not author in config:
            await ctx.send(':warning: User not found!')
            return

        if not name in config[author]['Weapons']:
            pass
        else:
            config[author]['Weapons'].pop(name)

        with open('Config/Weapons.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: Removed {name} from {user}')

    @commands.command()
    async def makeitem(self, ctx,name:str = None,type_:str = None,emoji:str = None,stre:str = None,intel:str = None,agi:str = None, price:int = None,*, desc:str = None):
        if not name or not emoji or not price or not desc or not stre or not intel or not agi or not type_:
            await ctx.send(':information_source: Command Usage: !makeitem `<NAME [SPACES AS _]>` <`TYPE (PASSIVE/ACTIVE)>` `<EMOJI>` `<STR AMOUNT>` `<INT AMOUNT>` `<AGI AMOUNT>` `<PRICE>` `<AGI/STR/INT>` `<DESCRIPTION>`')
            return
        
        with open('Config/Items.json') as f:
            assets = json.load(f)
        
        name = name.lower()

        if name in assets:
            await ctx.send(':warning: Item already exists.')
            return

        assets[name] = {}
        assets[name]['Emoji'] = emoji
        assets[name]['Price'] = price
        assets[name]['Description'] = desc
        assets[name]['Type'] = type_
        assets[name]['STR'] = stre
        assets[name]['INT'] = intel
        assets[name]['AGI'] = agi
        with open('Config/Items.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: {name} Added.')

    @commands.command()
    async def edititem(self, ctx,name:str = None,type_:str = None,emoji:str = None,dmg:str = None,stre:str = None,intel:str = None,agi:str = None, price:int = None,*, desc:str = None):
        if not name or not emoji or not price or not desc or not dmg or not stre or not intel or not agi or not type_:
            await ctx.send(':information_source: Command Usage: !edititem `<NAME [SPACES AS _]>` <`TYPE (PASSIVE/ACTIVE)>` `<EMOJI>` `<STR AMOUNT>` `<INT AMOUNT>` `<AGI AMOUNT>` `<PRICE>` `<AGI/STR/INT>` `<DESCRIPTION>`')
            return
        
        with open('Config/Items.json') as f:
            assets = json.load(f)
        
        name = name.lower()

        if not name in assets:
            await ctx.send(':warning: Item not found!!')
            return

        assets[name]['Emoji'] = emoji
        assets[name]['Price'] = price
        assets[name]['Description'] = desc
        assets[name]['Type'] = type_
        assets[name]['STR'] = stre
        assets[name]['INT'] = intel
        assets[name]['AGI'] = agi
        with open('Config/Items.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: {name} Edited.')


    @commands.command()
    async def deleteitem(self, ctx, name:str = None):
        if not name:
            await ctx.send(':information_source: Command Usage: !deleteitem `<NAME [SPACE AS _]>` `<REFUND AMOUNT [OPTIONAL]>`')
            return
        
        with open('Config/Items.json') as f:
            assets = json.load(f)
        
        name = name.lower()
        if not name in assets:
            await ctx.send(':warning: Item not exist.')
            return

        assets.pop(name)

        with open('Config/Items.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: {name} Removed.')

    @commands.command()
    async def spawnitem(self, ctx, name:str = None, user:discord.User = None):
        if not name or not user:
            await ctx.send(':information_source: Command Usage: !spawnitem `<NAME [SPACE AS _]>` `<@USER>`')
            return
        
        with open('Config/Items.json') as f:
            assets = json.load(f)

        with open('Config/Data.json') as f:
            config = json.load(f)

        name = name.lower()
        author = str(user.id)

        if not name in assets:
            await ctx.send(':warning: Item not exist.')
            return

        if not author in config:
            await ctx.send(':warning: User not found!')
            return
        
        if not name in config[author]['Items']:
            config[author]['Items'][name] = {}

        with open('Config/Items.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: Spawned {name} to {user}')

    @commands.command()
    async def removeitem(self, ctx, name:str = None, user:discord.User = None):
        if not name or not user:
            await ctx.send(':information_source: Command Usage: !removeitem `<NAME [SPACE AS _]>` `<@USER>` ')
            return
        
        with open('Config/Items.json') as f:
            assets = json.load(f)
        
        with open('Config/Data.json') as f:
            config = json.load(f)

        name = name.lower()
        author = str(user.id)

        if not name in assets:
            await ctx.send(':warning: Item not exist.')
            return

        if not author in config:
            await ctx.send(':warning: User not found!')
            return

        if not name in config[author]['Items']:
            pass
        else:
            config[author]['Items'].pop(name)

        with open('Config/Items.json','w') as f:
            json.dump(assets,f,indent = 3)
        
        await ctx.send(f':white_check_mark: Removed {name} from {user}')

    @commands.command()
    async def spawndemon(self, ctx, name:str = None,emoji:str = None, channel:discord.TextChannel = None, hp:str = None,steal:str = None, hunt:str = None, items:str = None):
        if not name or not channel or not hp or not steal or not hunt or not items or not emoji:
            await ctx.send(':information_source: Usage: !spawndemon `<NAME>` `<EMOJI>` `<#channel>` `<HP>` `<STEAL>` `<HUNT [0] to disable>` `<ITEMS>`')
            return
        
        with open('Config/Demons.json') as f:
            demons = json.load(f)
        

        await ctx.send(':white_check_mark: Demon Spawned')

        embed = discord.Embed(title = f'{name} has Spawned', color = discord.Color.red())
        embed.add_field(name = 'HP Left', value = hp, inline = False)
        embed.set_emoji(url = emoji)
        msg = await channel.send(embed = embed)

        ch = str(channel.id)
        demons[str(channel.id)] = {}
        demons[ch]['Name'] = name
        demons[ch]['HP'] = hp
        demons[ch]['Steal'] = steal
        if not hunt == '0':
            demons[ch]['Hunt'] = hunt
        
        demons[ch]['Items'] = items
        demons[ch]['Emoji'] = emoji
        demons[ch]['Logs'] = ''
        demons[ch]['MSG'] = msg.id
        with open('Config/Demons.json','w') as f:
            json.dump(demons,f,indent = 3)

        
def setup(bot):
    bot.add_cog(admin(bot))
