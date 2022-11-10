import telegram

from googleapiclient.discovery import build
from google.oauth2 import service_account

import datetime

row_id = 250

tk = '5121924028:AAF_iZ_erQBlEt0XhPgXVmGvV9m00MTvxcQ'
bot = telegram.Bot(token=tk)

from telegram.ext import Updater
updater = Updater(token=tk)
dispatcher = updater.dispatcher
def fetch(update, context):
    global row_id

    text = update.message.text
    if 'twitter' in text and 'http' in text or 'twitter' in text and 'https' in text:
        user = update.message.from_user
        user = user['username']
        sent_at = datetime.datetime.now().strftime("%d/%m/%Y")

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

        SERVICE_ACCOUNT_FILE = 'keys.json'

        creds = None
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        vall = []
        vall = [[sent_at, user, text]]

        SERVICE_ACCOUNT_FILE = 'keys.json'
        credentials = None
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        SAMPLE_SPREADSHEET_ID = '1eYcm-2CFZ9mATkzGJDEJGEBMCB3BhAWEcb8Smp7g3xs'
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        value_range_body = {
            'majorDimension': 'ROWS',
            'values': vall}

        request = sheet.values().update(spreadsheetId = SAMPLE_SPREADSHEET_ID,range = f"Shill Sheet!B{row_id}",valueInputOption = "USER_ENTERED", body = {"values":vall}).execute()
        row_id += 1

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.all,fetch)
dispatcher.add_handler(echo_handler)
updater.start_polling()


