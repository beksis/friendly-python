import telebot
import buttons as bt
import database as db
from geopy import Nominatim

# Создаем объект бота
bot = telebot.TeleBot('7083271691:AAHuSNFe0DjFaDXgmGzZErtKgK8Y_IuO0pk')
# Работа с картами
geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')

# Обработчик команды /start

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    check = db.check_user(user_id)
    if check:
        bot.send_message(user_id, 'Добро пожаловать в наш магазин!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Здравствуйте! '
                                        'Давайте проведем регистрацию!\n'
                                        'Напишите свое имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())

        # Переход на этап получения имени
        bot.register_next_step_handler(message, get_name)

# Этап получения номера
def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Супер, а теперь отправьте номер!',
                     reply_markup=bt.num_button())
    # Переход на этап получения номера
    bot.register_next_step_handler(message, get_number,user_name)

# Этап получения номера
def get_number(message, user_name):
    user_id = message.from_user.id
    # Если user отправил номер по кнопке
    if message.contact:
        user_number = message.contact.phone_number
        bot.send_message(user_id, 'А теперь локацию!',
                         reply_markup=bt.loc_button())
        # Переход на этап получения локации
        bot.register_next_step_handler(message, get_location,
                                       user_name, user_number)
    # Если user отправил номер не по кнопке

    else:
        bot.send_message(user_id, 'Отправьте номер по кнопке!',
                         reply_markup=bt.num_button())
        # Возврат на этап получения номера
        bot.register_next_step_handler(message, get_number, user_name)

# Этап получения локации
def get_location(message, user_name, user_number):
    user_id = message.from_user.id
    # Если user отправил локацию по кнопке
    if message.location:
        user_location = geolocator.reverse(f'{message.location.latitude}, '
                                           f'{message.location.longitude}')
        db.register(user_id, user_name, user_number, str(user_location))
        bot.send_message(user_id, 'Регистрация прошла успешна!')
    # Если user отправил не по кнопке
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку!',
                         reply_markup=bt.loc_button())
        # Возврат на этап получения локации
        bot.register_next_step_handler(message, get_location,
                                       user_name, user_number)

#

# Запуск и бота
bot.polling(non_stop=True)
