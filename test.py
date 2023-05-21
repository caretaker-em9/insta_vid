import telebot

bot_token = '6172233153:AAE2yZFTGz_TOiR-c9RQ9yfbQoMIRqbJ5-Y'

bot = telebot.TeleBot(bot_token)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global chat_id
    chat_id=message.chat.id
    global msg
    msg=message.text
    if "https://www.instagram.com" in msg:
      bot.send_message(chat_id,"downloading...")
    elif "https://www.instagram.com" not in msg:
      bot.send_message(chat_id,"send a valid link")
    _url = msg.split("?")
    _url=_url[0]
    

bot.polling()
