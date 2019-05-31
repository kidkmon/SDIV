import telebot
import emoji
token = "838657777:AAHvnc3nRR9uNjUm0g4NcmdiNPcjYATwcw4"

bot = telebot.TeleBot(token)
chat_id = '385861650'

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Your user code is: " + str(chat_id))

@bot.message_handler(commands=['fogo'])
def send_tpfb(message):
    photo = open('faustao_fogo.gif', 'rb')
    chat_id = message.chat.id
    bot.send_document(chat_id, photo)
    

bot.polling()