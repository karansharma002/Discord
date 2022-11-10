from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import discord
from discord.ext import commands,tasks
import json
import asyncio
from telethon import TelegramClient, sync
from telethon import functions, types
from telethon import errors
from telethon.errors.rpcerrorlist import UsernameInvalidError

id = 14982672
hash = 'f3a69e82a5584256663ffc2abe631cd1'

client = TelegramClient('Checker', id, hash)
client.start()


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1x2g2ztLB2Pv7Opt26u6LMP_muNq3gCOzQttvBuCrS4A'
SAMPLE_RANGE_NAME = 'Sheet1!A1:G'
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        

gnum = 2
'''
for num, x in enumerate(values[1:]):
    name = x[1]
    tele = x[2]
    account = tele
    try:
        result = client(functions.account.CheckUsernameRequest(username=account))
    except UsernameInvalidError:
        print('Invalid Name', tele)
        continue

    if name in values_data or tele in values_data or x[3] in values_data or x[4] in values_data or x[5] in values_data or x[6] in values_data:
        print('Exists Already',name)
        continue

    vall.append([x[0], x[1], x[2], x[3], x[4], x[5], x[6]])
    values_data.append(x[0])
    values_data.append(name)
    values_data.append(tele)
    values_data.append(x[3])
    values_data.append(x[4])
    values_data.append(x[5])
    values_data.append(x[6])
    print('Added', name)
    print(num)

'''

msg = ''
vall = []

'''
for x in reversed(values):        
    id = 0

    for y,z in zip(x,values[0]):
        if 'Discord ID (case-sensitive) – e.g., DiscordUser#1234' in z:
            id = y
            break
    
    
    #settings['FORM_2'].append(x[1])
    #with open('ST2.json','w') as f:
    #    json.dump(settings,f,indent = 3)


    try:
        guild = bot.get_guild(858977700260478976)
        role = discord.utils.get(guild.roles, name = '🧑‍🔬Testers')
        if '#' in str(id):
            id = id.split('#')
            user = discord.utils.get(guild.members, name=id[0], discriminator=id[1])
        else:
            user = await bot.fetch_user(id)

        if user in guild.members:                
            if not role in user.roles:
                await user.add_roles(role)
                print(user)
            
            vall.append([x[0], x[1], x[2], x[3], x[4]])

        print('EXISTS ALREADY.')

    except Exception as e:
        continue

'''


with open('Data.json') as f:
    da = json.load(f)

vall = da['Data']
print('WE ARE AT THE END')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'
credentials = None
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SAMPLE_SPREADSHEET_ID = '1x2g2ztLB2Pv7Opt26u6LMP_muNq3gCOzQttvBuCrS4A'
SAMPLE_RANGE_NAME = f'Sheet1!A{gnum}'
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

value_range_body = {
    'majorDimension': 'ROWS',
    'values': vall}

request = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID,range = f"Sheet1!A{gnum}",valueInputOption = "USER_ENTERED", body = {"values":vall}).execute()

number = 62

bot = commands.Bot(command_prefix = '!', intents = discord.Intents.all())

@bot.event
async def on_ready():
    print('-------- SERVER HAS STARTED -----------')
    await bot.wait_until_ready()
    fetch_form_2.start()
    await asyncio.sleep(10)
    #fetch_form_1.start()

@tasks.loop(seconds = 50000)
async def fetch_form_1():
    try:
        with open('ST1.json') as f:
            settings = json.load(f)
        
        if not 'Channel_1' in settings:
            return

        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1aq9FHNnXJVVgFfXCL00tDHWhgnYoZ6itJXQ2H-yUByo'
        SAMPLE_RANGE_NAME = 'Form responses 1!A1:G'
        from google.oauth2 import service_account

        SERVICE_ACCOUNT_FILE = 'keys.json'

        creds = None
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
                

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            return
        
        else:
            msg = ''
            for num,x in enumerate(values[4:]):
                
                global number

                embed = discord.Embed(color = discord.Color.blue(), title = 'New Bug Report')
                for y,z in zip(x,values[0]):
                    if 'Email ID' in z:
                        continue
                    
                    if 'Timestamp' in z:
                        continue

                    if y == '':
                        y = 'N/A'

                    embed.add_field(name = z,value = y,inline = False)
                    msg = 'ADDED\n'
                
                if not msg == '':
                    try:
                        url = 'https://discord.com/api/webhooks/945351916228055110/ORSzfSArUQXkz8SuIEiWYL2wv30ZCAyhmVWUVWjgwfGZ0cvoKA4QS8E6XPhfWPg0Bln1'  
                        from discord import Webhook, RequestsWebhookAdapter   
                        webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())              
                        webhook.send(embed = embed
                        )
                        settings['FORM_1'].append(x[0])
                        settings[str(number)] = msg.id
                        with open('ST1.json','w') as f:
                            json.dump(settings,f,indent = 3)

                        msg = ''
                        number += 1
                    
                    except:
                        msg = ''
                        pass
    except Exception as e:
        print(e)
        return

@bot.command()
async def status(ctx, num:str = None, type_:str = None):
    role1 = discord.utils.get(ctx.guild.roles, name = 'Developers')
    role2 = discord.utils.get(ctx.guild.roles, name = 'Administrators')
    role3 = discord.utils.get(ctx.guild.roles, name = 'Owners')

    if role1 in ctx.author.roles:
        pass
    
    elif role2 in ctx.author.roles:
        pass

    elif role3 in ctx.author.roles:
        pass

    else:
        await ctx.send(':warning: Missing permissions')
        return
        
    if not num or not type_:
        await ctx.send(':information_source: Usage: !status `<REPORT NUMBER>` <`Status Name> `[Accepted/Rejected/Processing/Fixed]`')
        return
    
    keys_ = {'accepted': "⚪", 'rejected': '🔴', 'processing': '🔵', 'fixed': '✅'}

    with open('ST1.json') as f:
        settings = json.load(f)
    
    if not num in settings:
        await ctx.send(':warning: Invalid Report Number')
        return
    
    type_ = type_.lower()
    
    if not type_ in  keys_:
        await ctx.send(':warning: Invalid Status Name')
        return
    
    ch = await bot.fetch_channel(909714201294028810)
    msg = await ch.fetch_message(settings[num])
    await msg.clear_reactions()
    await msg.add_reaction(keys_[type_])
    await ctx.message.add_reaction('✅')

values_data = []
@tasks.loop(hours = 6)
async def fetch_form_2():
    vall = []
    gnum = 2
    try:
        with open('ST2.json') as f:
            settings = json.load(f)
        
        if not 'Channel_2' in settings:
            return

        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1x2g2ztLB2Pv7Opt26u6LMP_muNq3gCOzQttvBuCrS4A'
        SAMPLE_RANGE_NAME = 'Sheet1!A1:G'
        from google.oauth2 import service_account

        SERVICE_ACCOUNT_FILE = 'keys.json'

        creds = None
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
                

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            return
        
        else:
            '''
            for num, x in enumerate(values[1:]):
                name = x[1]
                tele = x[2]
                account = tele
                try:
                    result = client(functions.account.CheckUsernameRequest(username=account))
                except UsernameInvalidError:
                    print('Invalid Name', tele)
                    continue

                if name in values_data or tele in values_data or x[3] in values_data or x[4] in values_data or x[5] in values_data or x[6] in values_data:
                    print('Exists Already',name)
                    continue

                vall.append([x[0], x[1], x[2], x[3], x[4], x[5], x[6]])
                values_data.append(x[0])
                values_data.append(name)
                values_data.append(tele)
                values_data.append(x[3])
                values_data.append(x[4])
                values_data.append(x[5])
                values_data.append(x[6])
                print('Added', name)
                print(num)

            '''

            msg = ''
            vall = []

            '''
            for x in reversed(values):        
                id = 0

                for y,z in zip(x,values[0]):
                    if 'Discord ID (case-sensitive) – e.g., DiscordUser#1234' in z:
                        id = y
                        break
                
                
                #settings['FORM_2'].append(x[1])
                #with open('ST2.json','w') as f:
                #    json.dump(settings,f,indent = 3)


                try:
                    guild = bot.get_guild(858977700260478976)
                    role = discord.utils.get(guild.roles, name = '🧑‍🔬Testers')
                    if '#' in str(id):
                        id = id.split('#')
                        user = discord.utils.get(guild.members, name=id[0], discriminator=id[1])
                    else:
                        user = await bot.fetch_user(id)

                    if user in guild.members:                
                        if not role in user.roles:
                            await user.add_roles(role)
                            print(user)
                        
                        vall.append([x[0], x[1], x[2], x[3], x[4]])

                    print('EXISTS ALREADY.')

                except Exception as e:
                    continue
            
            '''


            with open('Data.json') as f:
                da = json.load(f)
            
            vall = da['Data']
            print('WE ARE AT THE END')
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            SERVICE_ACCOUNT_FILE = 'keys.json'
            credentials = None
            credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            SAMPLE_SPREADSHEET_ID = '1x2g2ztLB2Pv7Opt26u6LMP_muNq3gCOzQttvBuCrS4A'
            SAMPLE_RANGE_NAME = f'Sheet1!A{gnum}'
            service = build('sheets', 'v4', credentials=credentials)
            sheet = service.spreadsheets()

            value_range_body = {
                'majorDimension': 'ROWS',
                'values': vall}
            
            request = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID,range = f"Sheet1!A{gnum}",valueInputOption = "USER_ENTERED", body = {"values":vall}).execute()

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)
        return


@bot.command()
async def setchannel_1(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Command Usage: !setchannel_1 `<CHANNEL WHERE FORMS ARE SENT>`')
        return
    
    with open('ST1.json') as f:
        settings = json.load(f)
    
    settings['Channel_1'] = channel.id
    with open('ST1.json','w') as f:
        json.dump(settings,f,indent = 2)
    
    await ctx.send(':white_check_mark: Channel has been Added')

@bot.command()
async def setchannel_2(ctx,channel:discord.TextChannel = None):
    if not channel:
        await ctx.send(':information_source: Command Usage: !setchannel_2 `<CHANNEL WHERE FORMS ARE SENT>`')
        return
    
    with open('ST2.json') as f:
        settings = json.load(f)
    
    settings['Channel_2'] = channel.id
    with open('ST2.json','w') as f:
        json.dump(settings,f,indent = 2)
    
    await ctx.send(':white_check_mark: Channel has been Added')

TOKEN = 'ODcwMTY4ODk3Mjg5MDkzMTMw.YQI18A.A54QOxCE34YBbXTlSCUpPi8gwHI'
bot.run(TOKEN)

