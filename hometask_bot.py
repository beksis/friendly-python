import telebot
from telebot import types

# Создание бота по YouTube

token = '7182378741:AAGWDWoMASuM7MbXqTt_NM1ShAf1jzLo-Jo'
my_id = 6948762704

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton(text='Услуги')
    button2 = types.KeyboardButton(text='О нас')
    button3 = types.KeyboardButton(text='Оставить заявку')
    keyboard.add(button1, button2, button3)
    bot.send_message(message.chat.id, 'Добро пожаловать', reply_markup=keyboard)


@bot.message_handler(commands=['info'])
def test(message):
    keyboard = types.InlineKeyboardMarkup()
    url = types.InlineKeyboardButton(text='Ссылка на наш сайт', url='https://www.typingtest.com/')
    keyboard.add(url)
    bot.send_message(message.chat.id, 'Информация о нас ', reply_markup=keyboard)


def send_request(message):
    mes = f'Заявка: {message.text}'
    bot.send_message(my_id, mes)
    bot.send_message(message.chat.id, 'Спасибо за обращение! Наши специалисты свяжутся с вами')


def send_service(message):
    bot.send_message(message.chat.id, '1. Сделать годовой отчет')
    bot.send_message(message.chat.id, '2. Заплатить за TOO')
    bot.send_message(message.chat.id, '3. Подсчет бюджетных средств')


@bot.message_handler(content_types=['text'])
def repeat_all(message):
    if message.text.lower() == 'о нас':
        test(message)
    elif message.text.lower() == 'оставить заявку':
        bot.send_message(message.chat.id, 'Мы будем рады обслужить вас')
        bot.register_next_step_handler(message, send_request)
    elif message.text.lower() == 'услуги':
        send_service(message)


bot.polling(non_stop=True)