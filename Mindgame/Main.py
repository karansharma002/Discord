import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
import json
import random
import datetime
from dateutil import parser
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component
import asyncio

import urllib.request


import requests

#! yes done

from discord_slash.context import ComponentContext

bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

participants = []

current_question = 0
current_list = []


@bot.event
async def on_ready():

    print('------ GAMES BOT HAS STARTED -------')
    await bot.wait_until_ready()

participants = []

current_question = 0
current_list = []
game_data = {}

def return_board(type_):
    board = [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]
    number_list = [":one:",":two:",":three:",":four:",":five:"]

    for x in range(5):
        if x == 0:
            board[0][0] = ':red_square:'        
            board[0][1] = '🇦'
            board[0][2] = '🇧'
            board[0][3] = '🇨'
            board[0][4] = '🇩'
            continue

        for y in range(5):
            board[x][y] = random.choice('⬜')

    board[1][0] = number_list[0]
    board[2][0] = number_list[1]
    board[3][0] = number_list[2]
    board[4][0] = number_list[3]

    desc = ''
    for y in board:
        desc += f"\u200b {y[0]} \u200b {y[1]} \u200b {y[2]}\u200b {y[3]}\u200b {y[4]}\n"

    if type_ == 'desc':
        return desc
    else:
        return board

@bot.event
async def on_component(ctx: ComponentContext):
    global game_data
    label = ctx.component['label']
    #! VERIFY FOLLOWING

    if label == "🟢 START THE GAME":
        try:
            author = str(ctx.author.id)
            
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and author in game_data

            if author in game_data:
                await ctx.send(':warning: You are already in a game.')
                return

            words = ['<:5_:959346269149593600>', '<:4_:959346270739238962>', '<:9_:959346270772789258>', '<:1_:959346271288713276>', '<:16:959346271733288981>', '<:7_:959346271745884160>', '<:14:959346272161116210>', '<:2_:959346272366628864>', '<:13:959346273289375744>', '<:11:959346273494896661>', '<:10:959346273520058398>', '<:3_:959346273847222323>', '<:8_:959346274157625444>', '<:12:959346274627366962>', '<:6_:959346274765791242>', '<:15:959346275021639720>']
            board = [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]
            number_list = [":one:",":two:",":three:",":four:",":five:"]
            for x in range(5):
                if x == 0:
                    board[0][0] = ':red_square:'        
                    board[0][1] = '🇦'
                    board[0][2] = '🇧'
                    board[0][3] = '🇨'
                    board[0][4] = '🇩'
                    continue

                for y in range(5):
                    board[x][y] = random.choice(words)

            board[1][0] = number_list[0]
            board[2][0] = number_list[1]
            board[3][0] = number_list[2]
            board[4][0] = number_list[3]

            desc = ''
            for y in board:
                desc += f"\u200b {y[0]} \u200b {y[1]} \u200b {y[2]}\u200b {y[3]}\u200b {y[4]}\n"

            game_data[author] = {}
            game_data[author]['Board1'] = board

            board = [['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', '']]
            number_list = [":one:",":two:",":three:",":four:",":five:"]

            for x in range(5):
                if x == 0:
                    board[0][0] = ':red_square:'        
                    board[0][1] = '🇦'
                    board[0][2] = '🇧'
                    board[0][3] = '🇨'
                    board[0][4] = '🇩'
                    continue

                for y in range(5):
                    board[x][y] = random.choice('⬜')

            board[1][0] = number_list[0]
            board[2][0] = number_list[1]
            board[3][0] = number_list[2]
            board[4][0] = number_list[3]

            desc = ''
            for y in board:
                desc += f"\u200b {y[0]} \u200b {y[1]} \u200b {y[2]}\u200b {y[3]}\u200b {y[4]}\n"

            game_data[author]['Board2'] = board
            game_data[author]['Board3'] = board
            game_data[author]['Points'] = 0

            embed = discord.Embed(color = discord.Color.blue(), title = 'To End the Game: Type: !exit', description = desc)
            embed.set_author(name = f'{ctx.author} | Board', icon_url = ctx.author.avatar_url)
            embed.add_field(name = ':small_red_triangle: Points Earned', value = '0', inline = False)
            embed.add_field(name = ':hourglass_flowing_sand: Chance Left', value = '5', inline = False)
            embed.set_footer(text = "Reply with Keys to Choose your Option")
            msg = await ctx.send(embed = embed)
            
            game_data[author]['MSG'] = msg.id
            game_data[author]['Turns'] = 5

            while True:
                try:
                    KEYS = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
                    move3 = await bot.wait_for('message', check = check, timeout = 60)
                    move1 = move3.content.upper()
                    await move3.delete()

                    key1 = move1[0]
                    if not key1 in KEYS:
                        print('TRUE')
                        await ctx.send('-------------- INVALID OPTION ----------------', delete_after = 5)
                        continue
                    
                    key1 = KEYS[key1]
                    key2 = move1[1]
                    key2 = int(key2)

                    if not key2 in (1,2,3,4):
                        print('FALSE')
                        await ctx.send('-------------- INVALID OPTION ----------------', delete_after = 5)
                        continue

                    game_data[author]['Board2'][key2][key1] = game_data[author]['Board1'][key2][key1] 
                    emoji1 = game_data[author]['Board1'][key2][key1]

                    desc = ''

                    for y in game_data[author]['Board2']:
                        desc += f"\u200b {y[0]} \u200b {y[1]} \u200b {y[2]}\u200b {y[3]}\u200b {y[4]}\n"

                    embed = discord.Embed(color = discord.Color.blue(), title = 'To End the Game: Type: !exit', description = desc)
                    embed.set_author(name = f'{ctx.author} | Board', icon_url = ctx.author.avatar_url)
                    embed.add_field(name = ':small_red_triangle: Points Earned', value = game_data[author]['Points'], inline = False)
                    embed.add_field(name = ':hourglass_flowing_sand: Chance Left', value = game_data[author]['Turns'], inline = False)
                    embed.set_footer(text = "Reply with Keys to Choose your Option")
                    await msg.edit(embed = embed)

                    print(key1,key2)
                    move3 = await bot.wait_for('message', check = check, timeout = 60)
                    move2 = move3.content.upper()
                    await move3.delete()
                    key1 = move2[0]
                    if not key1 in KEYS:
                        await ctx.send(':warning: `-------------- INVALID OPTION ----------------`', delete_after = 5)
                        continue
                    
                    key1 = KEYS[key1]
                    key2 = move2[1]
                    key2 = int(key2)
                    if not key2 in (1,2,3,4):
                        await ctx.send(':warning: `-------------- INVALID OPTION ----------------`', delete_after = 5)
                        continue
                    
                    game_data[author]['Board2'][key2][key1] = game_data[author]['Board1'][key2][key1] 
                    emoji2 = game_data[author]['Board1'][key2][key1]

                    if emoji1 == emoji2:
                        desc = ''
                        for y in game_data[author]['Board2']:
                            desc += f"\u200b {y[0]} \u200b {y[1]} \u200b {y[2]}\u200b {y[3]}\u200b {y[4]}\n"

                        game_data[author]['Points'] += 5
                        embed = discord.Embed(color = discord.Color.green(), description = desc)
                        embed.set_author(name = f'CHANCES EXCEEDED | GAME ENDED', icon_url = ctx.author.avatar_url)
                        embed.add_field(name = ':small_red_triangle: Points Earned', value = game_data[author]['Points'], inline = False)
                        embed.add_field(name = ':hourglass_flowing_sand: Chance Left', value = game_data[author]['Turns'], inline = False)
                        embed.set_footer(text = "Reply with Keys to Choose your Option")
                        await msg.edit(embed = embed)
                        continue

                    else:
                        game_data[author]['Turns'] -= 1

                        desc = ''
                        for y in game_data[author]['Board2']:
                            desc += f"\u200b {y[0]} \u200b {y[1]} \u200b {y[2]}\u200b {y[3]}\u200b {y[4]}\n"

                        embed = discord.Embed(color = discord.Color.red(), title = 'To End the Game: Type: !exit', description = desc)
                        embed.set_author(name = f'{ctx.author} | Board', icon_url = ctx.author.avatar_url)
                        embed.add_field(name = ':small_red_triangle: Points Earned', value = game_data[author]['Points'], inline = False)
                        embed.add_field(name = ':hourglass_flowing_sand: Chance Left', value = game_data[author]['Turns'], inline = False)
                        embed.set_footer(text = "Reply with Keys to Choose your Option")
                        await msg.edit(embed = embed)

                        game_data[author]['Board2'] = return_board('clean')

                        await asyncio.sleep(0.5)
                        
                        embed = discord.Embed(color = discord.Color.red(), title = 'To End the Game: Type: !exit', description = return_board('desc'))
                        embed.set_author(name = f'{ctx.author} | Board', icon_url = ctx.author.avatar_url)
                        embed.add_field(name = ':small_red_triangle: Points Earned', value = game_data[author]['Points'], inline = False)
                        embed.add_field(name = ':hourglass_flowing_sand: Chance Left', value = game_data[author]['Turns'], inline = False)
                        embed.set_footer(text = "Reply with Keys to Choose your Option")
                        await msg.edit(embed = embed)
                        

                    if game_data[author]['Turns'] <= 0:
                        desc = ''
                        for y in game_data[author]['Board1']:
                            desc += f"\u200b {y[0]} \u200b {y[1]} \u200b {y[2]}\u200b {y[3]}\u200b {y[4]}\n"

                        embed = discord.Embed(color = discord.Color.green(), title = f'Chances Exceeded | Game Ended', description = desc)
                        embed.add_field(name = ':small_red_triangle: Points Earned', value = game_data[author]['Points'], inline = False)
                        embed.add_field(name = ':hourglass_flowing_sand: Chance Left', value = game_data[author]['Turns'], inline = False)
                        await msg.edit(embed = embed)
            
                except asyncio.TimeoutError:
                        desc = ''
                        for y in game_data[author]['Board1']:
                            desc += f"\u200b {y[0]} \u200b {y[1]} \u200b {y[2]}\u200b {y[3]}\u200b {y[4]}\n"

                        embed = discord.Embed(color = discord.Color.red(), title = f'TIMEDOUT | Game Ended', description = desc)
                        embed.add_field(name = ':small_red_triangle: Points Earned', value = game_data[author]['Points'], inline = False)
                        embed.add_field(name = ':hourglass_flowing_sand: Chance Left', value = game_data[author]['Turns'], inline = False)
                        await ctx.send('https://cdn.discordapp.com/attachments/866656591133802517/959368075432583188/gameFile.png')
                        await msg.edit(embed = embed)      
                        game_data.pop(author)   
                        return
        
        except KeyError:
            try:
                await msg.delete()
            except:
                return
            return



@bot.command(aliases = ['mmr'])
async def memory(ctx):
    desc = '''

**1:** In the Memory game, you have to remember the previous chars.
**2:** The Game resets the board after two attempts.
**3:** The Game ends when the chances left as zero.
**4:** For each match, 5 Points are earned.
**5:** __**Usage:**__ Reply with KEY: Example: A1 B2 C4    
    '''
    embed = discord.Embed(color = discord.Color.magenta(), description = desc)
    embed.set_author(name = 'GAME INSTRUCTIONS', icon_url = bot.user.avatar_url)
    embed.set_image(url = 'https://i.imgur.com/JOv8Goq.png')

    from discord_slash.utils.manage_components import create_button, create_actionrow
    from discord_slash.model import ButtonStyle

    buttons = [
        create_button(style=ButtonStyle.green, label="🟢 START THE GAME")
    ]

    action_row = create_actionrow(*buttons)

    msg = await ctx.send(embed = embed, components=[action_row])

@bot.command()
async def exit(ctx):
    author = str(ctx.author.id)
    if author in game_data:
        game_data.pop(author) 
        await ctx.send(':white_check_mark: You have left the game.')

    else:
        await ctx.send(':information_source: You are not in a game.')

bot.run('ODIxMDIzNTUyNDMzNTUzNDQ5.YE9rxA.ZZxvshhAuM-69hkBd4EQ8QQ6beo')