import telegram
import json
import requests

tk = '1625980663:AAHMEd8vC1Zl0Muz5Fg7zDrh7dfc5jXTprY'
bot = telegram.Bot(token=tk)

from telegram.ext import Updater
updater = Updater(token=tk)
dispatcher = updater.dispatcher
def fetch(update, context):
    try:
        channel_id = update.channel_post.chat.id
        print(channel_id)
        return
        file_id = update.channel_post.photo[1].file_id
        file = context.bot.get_file(file_id)
        file.download('t23.jpg')
    except:
        pass

def sendImage():
    url = f"https://api.telegram.org/bot"+tk+"/sendPhoto"
    files = {'photo': open('YEEZY_BOOST_350_V2_ASH_PEARL_Left_Social_IG_1200x1200_ae743ecb-8cfa-459d-8612-e6b936add62e_1280x.jpg', 'rb')}
    data = {'chat_id' : "-1001529269261"}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

sendImage()
from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.photo,fetch)
dispatcher.add_handler(echo_handler)
updater.start_polling()

