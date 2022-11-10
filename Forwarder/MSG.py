import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix = '!')


@bot.event
async def on_ready():
    print('------- STARTED FORWARDING -------')


@bot.event
async def on_message(message):
    channels_data = {
        "951616970665635910": "https://discord.com/api/webhooks/965632281270190220/_HxjsliNO-rKZWN1uqe7xWTrZH4cLebZKBk1t59dSIRlNjkYHTagpQEBUs915a_9c24J", 
        "953375551219974165": "https://discord.com/api/webhooks/965632380993957958/NBUBwIT92QZBGpLL-nRg6MHw1rmfeGXI64ezq02Z371oCbo4Pf9ADwjIJuEHFjnlnuhK", 
        "960634867605991434": "https://discord.com/api/webhooks/965632457380614145/SKmDb-2SHKLCOkXmwzuTXBUosXWld4bxDW-GewehHDXaMR9fRHwCU5K6F55R422tXHkf",
        "957343292759101460": "https://discord.com/api/webhooks/965632543552577536/8agut9k6L2nDET9EVAO3vGpGK2BWReMKE-h6cyiUxky_N4eqIszxLdu6V0cBzdoSzlqK",
        "957119678470295582": "https://discord.com/api/webhooks/965603873786064916/wcPfsmx95de9AQhDhMCGThqafkM1SSI86E35Pgjb0SShrxp61eq7-4p3ZvU7DOCcRC1c", 
        "959113865453535232": "https://discord.com/api/webhooks/965632619452702830/657U-zetV0UeLaygKgel8D-CI_iud4OD3c8hhcQ4XAgg2J-7t40vNsNgRjiVzHfpf579"

    }

    if message.author == bot.user:
        return


    if str(message.channel.id) in channels_data:
        url = channels_data[str(message.channel.id)]
        content = message.content
        try:
            embed_dict = message.embeds[0].to_dict()
            embed = discord.Embed.from_dict(embed_dict)
            from discord import Webhook, RequestsWebhookAdapter
            webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
            webhook.send(embed = embed)

        except:
            pass

        if not content == '':
            files=[await attch.to_file() for attch in message.attachments]
            if not files == []:
                from discord import Webhook, RequestsWebhookAdapter
                webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
                webhook.send(content, files = files)
            else:
                from discord import Webhook, RequestsWebhookAdapter
                webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
                webhook.send(embed = embed)
                await webhook.send(content)
        

bot.run('OTM0NTExNjU0MTYxNTA2Mzc1.YjoXvQ.OaKF4H2_I7zVqTAUiFD-YQk7fR8', bot = False)