import discord
from discord.ext import commands, tasks
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
import datetime
bot = commands.Bot(command_prefix = '!')



@bot.event
async def on_ready():
    print('----- GOOGLE FORMS FORWARDING HAS STARTED -----')
    await bot.wait_until_ready()
    fetch_form1.start()

@tasks.loop(seconds = 30)
async def fetch_form1():
    try:
        with open('Data.json') as f:
            settings = json.load(f)
        
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1yYztCS8Ju2a99QNNzbdmbKBUkSQl_ZAEyEaqzVDkVlg'
        SAMPLE_RANGE_NAME = '⭐️!A1:U'
        

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
            for num,x in enumerate(reversed(values)):
                if x[0] in settings['SENT_FORMS']:
                    continue
                
                title = x[2]
                title = f"AVIS {title.upper()}"
                client = x[1]
                Message_Client = x[5] if not x[5] == '' else x[14]
                graphiste = x[4] if not x[4] == '' else x[13]
                field1 = x[3] if not x[3] == '' else x[12]
                field2 = x[6] if not x[6] == '' else x[15]
                field3 = x[7] if not x[7] == '' else x[16]
                field4 = x[8] if not x[8] == '' else x[17]
                field5 = x[9] if not x[9] == '' else x[18]
                field6 = x[10] if not x[10] == '' else x[19]
                field7 = x[11] if not x[11] == '' else x[20]
                
                msg = f'''> <:MC_Personne:906936886755491870> ⁝ INFORMATIONS CLIENT :
                ```
• Client : {client}

• Avis du client : {Message_Client}```
                > <:MC_Coche:906936886424133713>  ⁝ PERSONNE EN CHARGE DU TICKET:
                ```
• {graphiste}```
                > <:MC_Livraison:906936886596108368> ⁝ NOTATION:
                ```
• Note generale : {field1}

• Professionnalisme : {field2}
• Attente : {field3}
• Rapidite : {field4}
• Savoir-Faire : {field5}
• Sympathie : {field6}
• Suivi : {field7}```
                '''
                CUSTOM_COLOR = discord.Color.from_rgb(34,34,34) 
                embed = discord.Embed(color = CUSTOM_COLOR, title = title, description = msg)

                formatted_date = datetime.date.strftime(datetime.datetime.now(), "%H:%M:%S %b %d %Y")
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text = f"Merci d'avoir fait confiance en Mistia.")
                embed.set_image(url = 'https://zupimages.net/up/22/04/b758.png')
                if 'serveur' in x[2]:
                    channel = await bot.fetch_channel(906672017791676427)
                else:
                    channel = await bot.fetch_channel(906671990079885322 )

                await channel.send(embed = embed)

                with open('Data.json') as f:
                    data = json.load(f)
                
                data['SENT_FORMS'].append(x[0])

                with open('Data.json', 'w') as f:
                    json.dump(data,f,indent = 2)
                
                if num == 5:
                    return

    except Exception as e:
        print(e)
        return

    
bot.run('OTQxMzI3NjE0NjU0NjkzNDE4.YgUVqA.oZCtrnqpGCOKCQS9Xx7l7aWYWWQ')