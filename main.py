import os
import telebot
from telebot import types
import config
bot = telebot.TeleBot(config.TELEGRAM_API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b_info = types.KeyboardButton("О чат боте")
    b_search = types.KeyboardButton("Поиск")
    markup.add(b_info, b_search)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот".format(message.from_user), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def func(message):
    if(message.text == "О чат боте"):
        bot.send_message(message.chat.id, text="Чат бот создан для поиска произведений студентом Д. Команенко")
    elif(message.text == "Поиск"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b_word_search = types.KeyboardButton("Поиск по слову")
        b_name_search = types.KeyboardButton("Поиск по названию")
        b_back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(b_word_search, b_name_search, b_back)
        bot.send_message(message.chat.id, text="Выберите тип поиска", reply_markup=markup)
    
    elif(message.text == "Поиск по слову"):
        bot.send_message(message.chat.id, "Введите слово: ")
        bot.register_next_step_handler(message, word_search)
    
    elif message.text == "Поиск по названию":
        bot.send_message(message.chat.id, "Введите название: ")
        bot.register_next_step_handler(message, name_search)
    
    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b_info = types.KeyboardButton("О чат боте")
        b_search = types.KeyboardButton("Поиск")
        markup.add(b_info, b_search)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="Ошибка")

    
def word_search(message):
    for file in os.scandir('database'):
        file_open=open('database//'+file.name,'r')
        text=file_open.read()
        print(text)
        if message.text in text:
            bot.send_message(message.chat.id, text=file.name)
        else:
            bot.send_message(message.chat.id, text="Не найдено!")
        os.scandir('database').close()

def name_search(message):
    path = 'database//'+message.text
    if os.path.exists(path+'.txt'):
        bot.send_message(message.chat.id, text=message.text+' - произведение найдено!')
        if os.path.exists(path+'.png'):
            bot.send_photo(message.chat.id, 'https://pytba.readthedocs.io/ru/latest/_static/logo2.png')
        else:
            f = open(path+'.txt')
            str_te = f.read(30)
            bot.send_message(message.chat.id, str_te)

bot.infinity_polling()
