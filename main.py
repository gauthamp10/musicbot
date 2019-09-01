#testing the bot api
import time
import getpass
import random
import telegram
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from modules import *



def start(bot,update):
    try:
        data=dict()
        global db,user,root
        chat_id = update.message.chat_id
        username=update.message.from_user.first_name
        timestamp=get_ist()
        bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=chat_id, text="Hai.. "+username+"\n\nI'm am Bulo98 Song bot. Lets get to bussiness. Ask me any song.")
        help_text=print_help()   
        time.sleep(2.0)
        bot.send_message(chat_id=chat_id, text=help_text) 
    except Exception as e:
        print("Error!: ",str(e))    


    


def not_command(bot,update):
    data=dict()
    global db,user,root
    chat_id = update.message.chat_id
    username=update.message.from_user.first_name
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    user_response=update.message.text
    user_response=user_response.lower()
    print(user_response)
    user_response=user_response.split(',')
    for item in user_response:
        response,thumbnail,video=get_song_data(item)
        print(response)
        if response:
            bot.send_photo(chat_id=update.message.chat_id, photo=thumbnail)
            bot.send_message(chat_id=update.message.chat_id, 
                    text='<b>'+response+': </b><a href="'+video+'">▶️ Play/Download</a>.', 
                    parse_mode=telegram.ParseMode.HTML)

        else:
            response=search(str(user_response))
            print(response)
            if response=="":
                no_result=["Sorry...I guess my 6th sense is down!","Sorry..there is something wrong with my systems.","I can't fetch you any infomation on that!","Pardon Me...I don't know.","I have no answers for that.","Sorry for dissappointing you..I'll be better."]
                response=str(random.choice(no_result))
                bot.send_message(chat_id=update.message.chat_id,text=str(response))
            else:
                bot.send_message(chat_id=update.message.chat_id,text=str(response))
    
        


def main():
    TOKEN = "YOUR_TELEGRAM-BOT-ID"
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    text_message_handler=MessageHandler(Filters.text,not_command)
    dp.add_handler(text_message_handler)
    dp.add_handler(CommandHandler('start',start))
    updater.start_polling(clean=True)
    updater.idle()
    

if __name__ == "__main__":
    main()

