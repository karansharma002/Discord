
import tweepy
import discord
from discord.ext import commands,tasks
from discord.ext.commands import has_permissions
import json

bot = commands.Bot(command_prefix='%')

@bot.event
async def on_ready():
    print('STARTED')
    await fetch_tw.start()
    
@tasks.loop(hours = 1)
async def fetch_tw():
    await bot.wait_until_ready()
    current = 0

    with open('ss.json') as f:
        settings = json.load(f)
    
    if not 'Keyword' in settings or not 'Amount' in settings or not 'Text' in settings:
        return

    keyword = settings['Keyword']
    amount = settings['Amount']
    amount = 2

    with open('Tweets.json') as f:
        twt = json.load(f)
    

    with open('Tokens.json') as f:
        tokens = json.load(f)
    
    Consumer_Key = tokens['Consumer Key']
    Consumer_Secret = tokens["Consumer Secret"]
    Access_Token = tokens['Access Token Key']
    Access_Token_Secret = tokens['Access Token Secret']

    auth = tweepy.OAuthHandler(Consumer_Key,Consumer_Secret)
    auth.set_access_token(Access_Token,Access_Token_Secret)
    api = tweepy.API(auth)
    fetched_tweets = api.search(keyword, count = 10000)

    for tweet in fetched_tweets:
        try:
            if not str(tweet.id) in twt:
                if current >= amount:
                    return
                
                api.update_status(status = settings['Text'], in_reply_to_status_id = tweet.id , auto_populate_reply_metadata=True)
                twt[str(tweet.id)] = 'Sent'
                current += 1
                channel = await bot.fetch_channel(settings['Channel'])
                await channel.send(f':white_check_mark: Replied to Tweet ID: {tweet.id}')
                with open('Tweets.json','w') as f:
                    json.dump(twt,f,indent = 3)
            else:
                continue
        except Exception as e:
            print(e)
            pass

@bot.command()
async def setup(ctx,channel:discord.TextChannel = None, amount:int = None,*,name:str = None):
    if not amount or not name or not channel:
        await ctx.send(':information_source: Command Usage: %setup `<#channel>` `<amount>` `<keyword>`')
        return
    
    with open('ss.json') as f:
        s = json.load(f)
    
    s['Keyword'] = name
    s['Amount'] = amount
    s['Channel'] = channel.id
    with open('ss.json','w') as f:
        json.dump(s,f,indent= 3)
    
    await ctx.send(':white_check_mark: Data has been saved and the Task has started.')

@bot.command()
async def settext(ctx,*,text:str = None):
    if not text:
        await ctx.send(':information_source: Command Usage: %settext `TWEET TEXT` ')
        return
    else:
        with open('ss.json') as f:
            s = json.load(f)
        
        s['Text'] = text
        await ctx.send(':white_check_mark: Tweet Data has been saved.')
        with open('ss.json','w') as f:
            json.dump(s,f,indent = 3)
        

bot.run('ODI1MDM1NTE5MzI2NjgzMTg2.YF4ENA.8Yz2oeGYvhU51SErDex-sgz8UgU')
    
        



