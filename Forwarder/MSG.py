import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix = '!', selfbot = True)


@bot.event
async def on_ready():
    print('------- STARTED FORWARDING -------')
    await bot.wait_until_ready()


@bot.event
async def on_message(message):
    with open('Config.json') as f:
        config = json.load(f)
    
    channels_data = config['MIRRORED_CHANNELS']
    channels_pings = config['PING_CHANNELS']

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
            try:
                channel = await bot.fetch_channel(965158944215535697)

                role = discord.utils.get(channel.guild.roles, name = channels_pings[str(message.channel.id)])
                webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
                webhook.send(f"<@&{role.id}>")

            except:
                pass

        except Exception as e:
            from discord import Webhook, RequestsWebhookAdapter
            webhook = Webhook.from_url('https://discord.com/api/webhooks/967307399209824296/ZEfPQPNRCXYb1ml30-TAuRTXOf0cMXz9IHhacNN7Sx9m4wDLwAlDrER7p8Ok90ETwSJ5', adapter=RequestsWebhookAdapter())
            webhook.send(e)         
            pass

        if not content == '':
            try:
                files=[await attch.to_file() for attch in message.attachments]
                if not files == []:
                    from discord import Webhook, RequestsWebhookAdapter
                    webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
                    webhook.send(content, files = files)
                    role = discord.utils.get(message.guild.roles, name = channels_pings[str(message.channel.id)])
                    channel = await bot.fetch_channel(965158944215535697)

                    role = discord.utils.get(channel.guild.roles, name = channels_pings[str(message.channel.id)])
                    webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
                    webhook.send(f"<@&{role.id}>")

                else:
                    from discord import Webhook, RequestsWebhookAdapter
                    webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
                    await webhook.send(content)

                    channel = await bot.fetch_channel(965158944215535697)

                    role = discord.utils.get(channel.guild.roles, name = channels_pings[str(message.channel.id)])
                    webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
                    webhook.send(f"<@&{role.id}>")

            except Exception  as e:
                from discord import Webhook, RequestsWebhookAdapter
                webhook = Webhook.from_url('https://discord.com/api/webhooks/967307399209824296/ZEfPQPNRCXYb1ml30-TAuRTXOf0cMXz9IHhacNN7Sx9m4wDLwAlDrER7p8Ok90ETwSJ5', adapter=RequestsWebhookAdapter())
                webhook.send(e)         
                
        

bot.run('OTM0NTExNjU0MTYxNTA2Mzc1.YjoXvQ.OaKF4H2_I7zVqTAUiFD-YQk7fR8')