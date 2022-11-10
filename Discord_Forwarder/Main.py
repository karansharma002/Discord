from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands
import json
import aiohttp
bot = commands.Bot(command_prefix='!', self_bot=True)

@bot.event
async def on_ready():
    print('---SERVER STARTED----')
    await bot.wait_until_ready()
    ch = await bot.fetch_channel(554177170180669470)
    print(ch)

@bot.event
async def on_message(message):
    with open('Data.json') as f:
        data = json.load(f)
    
    ch = str(message.channel.id)
    if ch in data:
        webhook = Webhook.from_url(data[ch], adapter=RequestsWebhookAdapter())
        if str(message.embeds[0]) != '[]':
            webhook.send(embed = message.embeds[0])
        else:
            webhook.send(content = message.content, tts=message.tts, files=[await attch.to_file() for attch in message.attachments])
        
        print('sent')
        print(message.content)

bot.run("mfa.NPg4-9iirkxJx7OLZnJwGSg-vHeEs9afOMk6rEv0wOIa4e8hluXEvyGdg6iei2jdq8czbV_2s9kxwpSRC16J")