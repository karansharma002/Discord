import discord
from discord.ext import commands
import json
import random

from random import choice as rchoice

import datetime

from discord_components import Button, Select, SelectOption, ComponentsBot

cooldowns = {}


classes = {"Fighter": {"Strength": 20, "Agility": 12, "Intellect": 10},\
    "Assassin": {"Strength": 10, "Agility": 20, "Intellect": 12},\
        "Cleric": {"Strength": 12, "Agility": 10, "Intellect": 20}}

class player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx):
        with open('Config/Data.json') as f:
            data = json.load(f)
        
        author = str(ctx.author.id)
        embed = discord.Embed(color = discord.Color.red())
        embed.set_author(name = f'{ctx.author} | Profile', icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)
        embed.add_field(name = 'Class', value = data[author]['Class'], inline = True)
        embed.add_field(name = 'XP', value = data[author]['XP'], inline = True)
        embed.add_field(name = 'Level', value = data[author]['Level'], inline = True)
        embed.add_field(name = 'Weapons', value = len(data[author]['Weapons']), inline = True)
        embed.add_field(name = 'Items', value = len(data[author]['Items']), inline = True)
        embed.add_field(name = 'Coins', value = data[author]['Coins'], inline = True)
        embed.add_field(name = 'Skill Points', value = data[author]['Points'], inline = True)
        await ctx.send(embed = embed)

    @commands.command()
    async def stats(self, ctx):
        with open('Config/Data.json') as f:
            data = json.load(f)
        
        author = str(ctx.author.id)

        embed = discord.Embed()
        embed.set_author(name = f"{ctx.author} | STATS", icon_url = ctx.author.avatar_url)
        embed.add_field(name = 'Strength', value = data[author]['Strength'], inline = True)
        embed.add_field(name = 'Agility', value = data[author]['Agility'], inline = True)
        embed.add_field(name = 'Intellect', value = data[author]['Intellect'], inline = True)
        await ctx.send(embed = embed)

    @commands.command()
    async def equip(self, ctx, val:str = None):
        if not val:
            await ctx.send(':information_source: Usage: !equip `<WEAPON Name>`')
            return
        
        val = val.lower()

        with open('Config/Data.json') as f:
            data = json.load(f)
        
        author = str(ctx.author.id)

        if not val in data[author]['Weapons']:
            await ctx.send(':warning: Invalid Weapon or You dont own it!!')
            return
        
        with open('Config/Weapons.json') as f:
            weapons = json.load(f)
        
        for x in weapons:
            if x == val:
                data[author]['Damage'] = weapons[x]['DMG']
                with open('Config/Data.json') as f:
                    json.dump(data,f,indent = 3)
            
                await ctx.send(f':white_check_mark: {val.title()} Equipped!')
                return

    @commands.command()
    async def distribute(self, ctx, choice:str = None):
        with open('Config/Data.json') as f:
            data = json.load(f)
        
        author = str(ctx.author.id)

        points = data[author]['Points']

        if not points:
            await ctx.send(":warning: You don't have any skill points to distribute.")
            return
        
        else:
            if not choice:
                await ctx.send(':information_source: Usage: !distribute `<# SKILL NAME [ONE PER TIME (Agility / Strength / Intellect)]>`')
                return
            
            choice = choice.lower()
            if not choice in ('strength', 'agility', 'intellect'):
                await ctx.send(':warning: Invalid Skill Name')
                return
            
            data[author][choice.title()] += 1
            data[author]['Points'] -= 1

            with open('Config/Data.json','w') as f:
                json.dump(data,f,indent = 3)
            
            await ctx.send(f':white_check_mark: Added +1 to {choice.title()}')
        
    @commands.command()
    async def register(self, ctx, choice:str = None):
        with open('Config/Data.json') as f:
            config = json.load(f)
        
        author = str(ctx.author.id)

        if author in config:
            await ctx.send(':warning: You are already registered.')
            return
        
        else:
            embed = discord.Embed(color = discord.Color.blurple())
            embed.set_image(url = 'https://images-ext-2.discordapp.net/external/1gy-xAsxBk37idaTzW_Wsy7ffMzHjSFxME3AI6UB8h4/https/i.imgur.com/noWbiml.png?width=500&height=290')
            await ctx.send(embed = embed,
                components=[
                    Select(
                        placeholder="Select the class",
                        options=[
                            SelectOption(label="Class: Fighter", value="Fighter"),
                            SelectOption(label="Class: Assassin", value="Assassin"),
                            SelectOption(label="Class: Cleric", value="Cleric"),
                        ],
                        custom_id="select1",
                    )
                ],
            )

            interaction = await self.bot.wait_for(
                "select_option", check=lambda inter: inter.custom_id == "select1" and inter.author == ctx.author
            )

            choice = interaction.values[0]
            await interaction.send(content=f':white_check_mark: You have registered as {choice}\n:information_source: You have received 3 skills POINTS. Use: `!distribute` to use them.')
            
            print(choice)
            config[author] = {}
            config[author]['Class'] = choice
            config[author]['XP'] = 0
            config[author]['Level'] = 1
            config[author]['Inventory'] = {}
            config[author]['Items'] = {}
            config[author]['Weapons'] = {}
            config[author]['Coins'] = 200
            config[author]['Points'] = 3

            for x in classes[choice]:
                config[author][x] = classes[choice][x]
            
            with open('Config/Data.json', 'w') as f:
                json.dump(config,f, indent = 3)
            
    @commands.command()
    async def inventory(self, ctx):
        author = str(ctx.author.id)
        
        with open('Config/Data.json') as f:
            config = json.load(f)
        
        msg = ''

        for x in config[author]['Inventory']:
            msg += f"{x}: {config[author]['Inventory'][x]}"

        if msg == '':
            msg = 'Inventory is Empty'

        embed = discord.Embed(color = discord.Color.orange(), title = f'{ctx.author} | Inventory', description = msg)
        await ctx.send(embed = embed)

    @commands.command()
    async def dig(self, ctx):
        with open('Config/Data.json', 'r') as f:
            config = json.load(f)

        author = str(ctx.author.id)

        player_class = config[author]['Class']

        bonus_xp = config[author]['Intellect'] / 5
        with open('Config/Settings.json') as f:
            settings = json.load(f)
        
        if 'digxp' in settings:
            xp = settings['digxp']
        else:
            xp = 10
        
        xp = round(bonus_xp / 100 * xp) + xp

        if 'digcoin' in settings:
            digcoin = settings['digcoin']
        else:
            digcoin = 1
        
        if 'orehp' in settings:
            orehp = settings['orehp']
        else:
            orehp = random.randint(100,200)

        if 'ORE' in config[author]:
            await ctx.send(":warning: There's an ORE waiting for you. Type: !mine to continue mining it.")
            return

        config[author]['XP'] += xp
        config[author]['Coins'] += digcoin

        await ctx.send(f"{ctx.author}, You have gained 10 XP and 1 Coin.")

        if random.randrange(100) < 20:
            embed = discord.Embed(description = "You have found an ORE. (Type: !mine to mine it)")
            await ctx.send(embed = embed)

            config[author]['ORE'] = orehp
        
        with open('Config/Data.json','w') as f:
            json.dump(config,f,indent = 3)
        
    @commands.command()
    async def mine(self, ctx):
    
        #! PENDING ITEM DROPS

        with open('Config/Data.json', 'r') as f:
            config = json.load(f)

        author = str(ctx.author.id)

        if not 'ORE' in config[author]:
            await ctx.send(':warning: Nothing to MINE!!')
            return

        with open('Config/Settings.json') as f:
            settings = json.load(f)
        
        if 'minexp' in settings:
            xp = settings['minexp']
        else:
            xp = 10
        
        if 'minecoin' in settings:
            minecoin = settings['minecoin']
        else:
            minecoin = 1

        if 'stone' in settings:
            stone = settings['stone']
        else:
            stone = 0

        if 'iron' in settings:
            iron = settings['iron']
        else:
            iron = 0


        config[author]['XP'] += xp
        config[author]['Coins'] += minecoin

        gained = ''

        if random.randrange(100) < stone:
            config[author]['Inventory']['Stone'] += 1
            gained += "1 Stone"
        
        if random.randrange(100) < iron:
            gained = 1
            config[author]['Inventory']['Iron'] += 1
            gained += ", 1 Iron"

        if not config[author]['ORE'] - 20 <= 0:
            bonus_dmg = config[author]['Strength'] / 1
            bonus_dmg = round(bonus_dmg / 100 * 20) + 20
            config[author]['ORE'] -= bonus_dmg 
            hp_left = config[author]['ORE']
            
        else:
            config[author].pop('ORE')
            hp_left = 0
        
        embed = discord.Embed(description = f'You have gained {xp} XP, {minecoin} Coins {gained}')
        embed.add_field(name = 'Ore HP', value = hp_left, inline = False)
        await ctx.send(embed = embed)
        
        with open('Config/Data.json','w') as f:
            json.dump(config,f,indent = 3)
        
    @commands.command()
    async def spy(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        with open('Config/Data.json', 'r') as f:
            config = json.load(f)

        author = str(ctx.author.id)

        words = {'Words1': ('were inspecting fields all day when you saw','were checking mill barns and noticed','were at your observation spot when spotted','didn"t expect anything special on farms this day when you suddenly detected'),
        'Words2':  ('small group','bunch','weird company'),
        'Words3': ('suspicious','anxious','scared','wounded'),
        'Words4': ('citizens','strangers','drunkards','peasants','guards','adventurers'),
        "Words5": ('carefully','lurking','quietly','sneaking','hiding','wandering randomly','resting','fighting','eating meat chunks'),
        "Words6": ('high grass','a shady bush','shady trees','a shallow pond','crop fields','an old shack','a barn','a mill')
        }
        
        
        description = "YOU {} a {} of {} {} {} in {}".format(rchoice(words['Words1']),rchoice(words['Words2']),rchoice(words['Words3']),rchoice(words['Words4']), rchoice(words['Words5']), rchoice(words['Words6']))
        description += "\n\n__You want to come closer to see whats going on there?__"
        
        await ctx.send(description,
            components=[
                Select(
                    placeholder="Select the Option",
                    options=[
                        SelectOption(label="No, call for help", value="no"),
                        SelectOption(label="Yes, come closer", value="yes"),
                    ],
                    custom_id="select1",
                )
            ],
        )

        interaction = await self.bot.wait_for(
            "select_option", check=lambda inter: inter.custom_id == "select1" and inter.author == ctx.author
        )

        choice = interaction.values[0]
        if choice == 'no':
            config[author]['XP'] += 10
            config[author]['Coins'] += 10
            await ctx.send(f"You called for help but a guardian couldnt catch them. Garnison captain gave you reward for the information (+10XP + 10 Coins")
            with open('Config/Data.json','w') as f:
                json.dump(config, f,indent = 3)
            
            return
        
        else:
            chance = 50
            if not random.randrange(100) < chance:
                await ctx.send('*They noticed you and ran away in opposite directions*')
                return

            words = {
            "Word1": ('somehow feel','get closer carefully and realize','are not sure but it looks like','think','noticed they have dark spots all over their skin and suppose','guess they can"t see properly and maybe','hear them making weird noises and winder if'),

            "Word2": ('charmed','bewitched','under a spell','poisoned') ,
            "Word3": ('look','stare','move'),
            "Word4": ('Wait, there is somebody else there among them!','There must be somebody controlling them','This must be some kind of evil magic',' You almost fell off your observation spot, but managed to hold onto a branch',' Your senses tell you theres something wrong in here, something unusual and maybe dangerous',' Oh no! You think they noticed you! Cover! It"s fine, they are just staring unfocused')}
            description = "You {} they are all {} because of the way they {} {}".format(rchoice(words['Word1']), rchoice(words['Word2']), rchoice(words['Word3']), rchoice(words['Word4']))
            description += "\n\n__Do you want to approach them?__"

            await ctx.send(description,
                components=[
                    Select(
                        placeholder="Select the Option",
                        options=[
                            SelectOption(label="Yes, carefully.", value="yes"),
                            SelectOption(label="No, call for guards help!", value="no"),
                        ],
                        custom_id="select1",
                    )
                ],
            )

            interaction = await self.bot.wait_for(
                "select_option", check=lambda inter: inter.custom_id == "select1" and inter.author == ctx.author
            )

            choice = interaction.values[0]

            if choice == 'no':
                config[author]['XP'] += 30
                config[author]['Coins'] += 5
                await ctx.send(f"You and two guards managed to catch one. Garnison captain gave you reward for the job. (30 XP and 20 Coins)")
                with open('Config/Data.json','w') as f:
                    json.dump(config, f,indent = 3)
                
                return
                
            chance = 40
            if not random.randrange(100) < chance:
                await ctx.send('*They noticed you and ran away in opposite directions*')
                return
            

            words = {"Word1": ('What is it? One of them fell on the ground and stopped breathing!',' Look at that fat one! Those eyes look demonic and skin is all in wounds!','You approached them and can clearly feel strong rotting flesh smell. The big one is eating bones now'),
            "Word2": ('You see a tall figure in a grey robe',' You noticed a mage',' You realized theres a man in a robe','You can see a warlock now','Theres a sorcerer','There is a suspicious man in mages robe'),
            "Word3": ('moving hands in the air','burning a bunch of wooden dolls','whispering spells',' casting spells around him','slowly cutting a rooster','standing in centre of pentagram','talking to a skull'),
            "Word4": ('You want to distract him first and throw a small rock in opposite direction','You are now ready to attack the stranger','Seems like thats the one who controls the whole group. You have to stop him now!',' This mage has to be caught! You are getting ready for attack',' The warlock must die before he noticed you!')}
    
            description = "{} {} {} {}".format(rchoice(words['Word1']), rchoice(words['Word2']), rchoice(words['Word3']), rchoice(words['Word4']))
            description += "\n\n__Attack or report details to the guards?__"

            await ctx.send(description,
                components=[
                    Select(
                        placeholder="Select the Option",
                        options=[
                            SelectOption(label="Attack!", value="attack"),
                            SelectOption(label="Report", value="report"),
                        ],
                        custom_id="select1",
                    )
                ],
            )

            interaction = await self.bot.wait_for(
                "select_option", check=lambda inter: inter.custom_id == "select1" and inter.author == ctx.author
            )

            choice = interaction.values[0]

            if 'report' in choice:
                config[author]['XP'] += 180
                config[author]['Coins'] += 90

                await ctx.send('*You almost got him! At least guards know his appearance and details now. Garnison  captain gave you reward for the information""(+180XP  +90 coins)*')
                with open('Config/Data.json','w') as f:
                    json.dump(config, f,indent = 3)
                
                return
            
            else:
                if not random.randrange(100) < 30:
                    await ctx.send('*He noticed that and managed to freeze you with a weak paralyze spell. Then the whole group ran away in opposite directions.*')
                    return
                else:
                    await ctx.send('Attack! (Success) - It happened in a second. You smashed him from behind with a massive kick and pushed him to the ground. The whole group suddenly fell too. You brought the warlock to Garnison captain. He took him to jail straight away and rewarded you generously. (+80XP  +40 coins)')
                    return

    @commands.command()
    async def attack(self, ctx):
        global cooldowns

        with open('Config/Data.json') as f:
            data = json.load(f)
        
        with open('Config/Demons.json') as f:
            demon = json.load(f)
        
        author = str(ctx.author.id)

        if author in cooldowns:
            from dateutil import parser
            
            t1 = parser.parse(str(cooldowns[author]['TM']))
            t2 = parser.parse(str(datetime.datetime.now()))
            t3 = t2 - t1
            t4 = round(t3.total_seconds())

            if not t4 <= 0:
                await ctx.send(f':warning: You are on cooldown. [SECONDS LEFT - {t4}')
                return

        ch = str(ctx.channel.id)

        if not ch in demon:
            await ctx.send(':warning: There is no Demon to attack.')
            return
        
        if demon['Turn'] == 'attack':
            msg = data[ch]['Logs']
            tm = datetime.datetime.today().strftime('%H:%M:%S')

            if random.randrange(100) < 50:
                msg += f'{tm}:\n!attack\n{tm}: {ctx.author} missed (your attack cooldown is 10 sec\n'
                cooldowns[author] = str(datetime.datetime.now() + datetime.timedelta(seconds = 10))

            else:
                damage = data[author]['Damage']
                demon[ch]['HP'] -= damage
                msg += f'{tm}: {ctx.author} hits Demon {damage} damage!\n'

            hp = demon[ch]['HP']

            msg += f'{tm}: Demon attacks! {hp}HP type: !dodge\n'
            embed = discord.Embed(description = msg, color = discord.Color.red())
            embed.add_field(name = 'HP Left', value = hp, inline = False)
            embed.set_image(url = data[ch]['Image'])
            message = await ctx.channel.fetch_message(data[ch]['MSG'])
            await message.edit(embed = embed)
            demon[ch]['Logs'] = msg
            demon[ch]['Turn'] = 'dodge'
            with open('Config/Demons.json', 'w') as f:
                json.dump(demon, f, indent = 3)

        else:
            msg = data[ch]['Logs']
            tm = datetime.datetime.today().strftime('%H:%M:%S')
            msg += f'{tm}:\n{ctx.author} !dodge\n'
            hp = demon[ch]['HP']
            embed = discord.Embed(description = msg, color = discord.Color.red())
            embed.add_field(name = 'HP Left', value = hp, inline = False)
            embed.set_image(url = data[ch]['Image'])
            message = ctx.channel.fetch_message(data[ch]['MSG'])
            await message.edit(embed = embed) 

            cooldowns[author] = str(datetime.datetime.now() + datetime.timedelta(minutes = 1))
        
    @commands.command()
    async def dodge(self, ctx):
        global cooldowns
        
        with open('Config/Data.json') as f:
            data = json.load(f)
        
        with open('Config/Demons.json') as f:
            demon = json.load(f)
        
        author = str(ctx.author.id)

        if author in cooldowns:
            from dateutil import parser
            
            t1 = parser.parse(str(cooldowns[author]['TM']))
            t2 = parser.parse(str(datetime.datetime.now()))
            t3 = t2 - t1
            t4 = round(t3.total_seconds())

            if not t4 <= 0:
                await ctx.send(f':warning: You are on cooldown. [SECONDS LEFT - {t4}')
                return

        ch = str(ctx.channel.id)

        if not ch in demon:
            await ctx.send(':warning: There is no Demon to attack.')
            return
        
        if demon['Turn'] == 'dodge':        
            msg = data[ch]['Logs']
            tm = datetime.datetime.today().strftime('%H:%M:%S')
            msg += f'{tm}:\n{ctx.author} dodge\n{tm}: Demon hits Nobody! Nice Move!\n'
            hp = demon[ch]['HP']
            embed = discord.Embed(description = msg, color = discord.Color.red())
            embed.add_field(name = 'HP Left', value = hp, inline = False)
            embed.set_image(url = data[ch]['Image'])
            message = await ctx.channel.fetch_message(data[ch]['MSG'])
            await message.edit(embed = embed)
            demon[ch]['Logs'] = msg
            demon[ch]['Turn'] = 'attack'
            with open('Config/Demons.json', 'w') as f:
                json.dump(demon, f, indent = 3)
        
        else:
            msg = data[ch]['Logs']
            tm = datetime.datetime.today().strftime('%H:%M:%S')
            msg += f'{tm}:\n{ctx.author} !attack\n'
            hp = demon[ch]['HP']
            embed = discord.Embed(description = msg, color = discord.Color.red())
            embed.add_field(name = 'HP Left', value = hp, inline = False)
            embed.set_image(url = data[ch]['Image'])
            message = ctx.channel.fetch_message(data[ch]['MSG'])
            await message.edit(embed = embed)
            cooldowns[author] = str(datetime.datetime.now() + datetime.timedelta(minutes = 1))

    @commands.command()
    async def hunt(self, ctx):    
        with open('Config/Demons.json') as f:
            demons = json.load(f)
        
        await ctx.send(':warning: No demon to hunt!!')
    

def setup(bot):
    bot.add_cog(player(bot))
