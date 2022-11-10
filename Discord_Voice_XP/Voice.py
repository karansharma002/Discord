import discord
import datetime
import json

from discord.ext import tasks

guild = 0

bot = discord.Bot(debug_guilds=[guild], command_prefix = '!')

@tasks.loop(minutes = 45)
async def extract_data():
    try:
        dta = datetime.datetime.now().strftime('%H:%M')
        if dta == '12:00':
            guild.voice_client.start_recording
            return
    
    except:
        pass
    
async def finished_callback(sink, ctx):
    print(sink.audio_data.items())
    print(sink.audio_data)
    recorded_users = [
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()

    ]
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]

    with open('Data.json') as f:
        data = json.load(f)

    for x in files:
        if not x in data:
            data[x] = {}
        
        data[x][files[x]['Duration']] = files[x]
    
    with open('Data.json', 'w') as f:
        json.dump(data,f,indent = 3)
        
        
@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        return

    if not before.channel and after.channel:
        try:
            await member.voice.channel.connect() 
            member.guild.voice_client.start_recording(discord.sinks.MP3Sink(), finished_callback, member.guild) 

        except:
            pass

bot.run('TOKEN_ID')

    
