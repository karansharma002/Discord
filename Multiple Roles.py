# bot.py
import os
import random
import discord
from discord.ext import commands
from discord.ext.commands.core import command
from fuzzywuzzy import fuzz

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('ODI0NzA3ODYyNDc0MzkxNTcy.YFzTDA.VnQU7s6YvJg_10bfEXdeipVBr_s')


bot = commands.Bot(command_prefix= '?')

@bot.event
async def on_ready():
    print('--- BOT INSTANCE STARTED ---')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # List to store the possible Roles
    roles = ['ok','Test']

    
    for num, x in enumerate(roles):
        num = num+1

        # Fetching the roles from the GUILD
        role = discord.utils.get(message.guild.roles, name=x)

        # Checking if the User has the role?, If not, Return back.

        if role in message.author.roles:
            # Break and Pass
            break

        else:
            # Do nothing and return
            if num == len(roles):
                return


    #Here, Brooklyn_99_quotes and Care Messages are a list of the responses. I have used external LIST for a better understanding

    brooklyn_99_quotes = ["I'm the human form of the 💯 emoji.","Bingpot!","Cool. Cool. Cool, cool, cool, cool, cool, cool..","No doubt, no doubt, no doubt, no doubt.."]
    care_messages = ["She does not care."]

    # Creating a dictionary instead of LIST which can store the One word and The answer.
    # Example: "I care" (Is a key or The Word which should be matched) : "She Doesnt Not care" (This is the response) without multiple words
    # Example: I care : ["She Doesn't Care", "She Cares"] Similar to above, We have passed list as the responses.

    words = {"99!":brooklyn_99_quotes,"I care": care_messages}
    
    # Iterating through the WORDS Dictionary and fetching the Keys [IE - Our Words which needs to be matched]
    for key in words:

        # Match the Ratio of the sentences.
        ratio = fuzz.ratio(str(message.content), key)

        # If the ratio is greater than 55 or equal, We send the message and break.
        if ratio >= 55:
            response = random.choice(words[key])
            await message.channel.send(f"{message.author.mention} {response}")
            break

bot.run(TOKEN)

