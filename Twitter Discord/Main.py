
import tweepy
import discord
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions
import json

auth = tweepy.OAuthHandler('AzJPweX8l37Iv7oFJC7PXmmvc', 'VTTuF3RhE1lDpg14GixWCp8KPIBeipZkm33B68MZrNyJHs43Mv')
auth.set_access_token('1163016022644760576-6fWjkADGMXW6ag035oV7wrrT3dFzuQ', 'vPH5MU6pUX6KEjQh4ae1MVF9JPyfgOtbCFN0JMXjuuYXH')
api = tweepy.API(auth)
fetched_tweets = api.search('Sofia', count = 2)
# parsing tweets one by one
print(len(fetched_tweets))

for tweet in fetched_tweets:
    print('------')
    print(tweet.text)
    print(tweet.id)
    print('-----')
    try:
        api.update_status(status = 'Testing', in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)
    
    except Exception as e:
        print(e)
        pass
input()
bot = commands.Bot(command_prefix='$')

OLD = []

@bot.event
async def on_ready():
    print('STARTED')
    await fetch_tw.start()

@tasks.loop(seconds = 60)
async def fetch_tw():
    global OLD
    
    with open('ST.json') as f:
        s = json.load(f)
    
    tweets = api.user_timeline(screen_name = 'fxvitali')
    for tweet in tweets:
        tw = tweet.text
        if tw in OLD:
            continue
        else:
            OLD.append(tw)
            if not 'Channel' in s:
                return

            ch = await bot.fetch_channel(s['Channel'])
            embed = discord.Embed(description = tw,color = discord.Colour.blue())
            if 'media' in tweet.entities:
                for x in tweet.entities['media']:
                    embed.set_image(url=x['media_url_https'])
            
            await ch.send(embed = embed)

@has_permissions(administrator = True)
@bot.command()
async def setchannel(ctx,channel:discord.TextChannel = None):
    if not channel:
        return
    
    with open('ST.json') as f:
        s = json.load(f)
    
    s['Channel'] = channel.id
    with open('ST.json','w') as f:
        json.dump(s,f,indent = 3)
    
    await ctx.send(':white_check_mark: Channel has been marked as Active!')

@has_permissions(administrator = True)
@bot.command()
async def clear(ctx,amount:int = None):
    if amount == None:
        amount = 1
    await ctx.channel.purge(limit = amount)

bot.run('ODI1MDM1NTE5MzI2NjgzMTg2.YF4ENA.8Yz2oeGYvhU51SErDex-sgz8UgU')
    
        



