

import telegram
import json

tk = '1761859355:AAER1tcBldUd5UOxvbrjzh9Oq6CT8tQU_hA'
bot = telegram.Bot(token=tk)

from telegram.ext import Updater
updater = Updater(token=tk)
dispatcher = updater.dispatcher
def fetch(update, context):
    try:
        channel_id = update.channel_post.sender_chat.id
        print(channel_id)
        file_id = update.channel_post.document.file_id
        file = context.bot.get_file(file_id)
        file.download()
    except:
        pass

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.all,fetch)
dispatcher.add_handler(echo_handler)
updater.start_polling()