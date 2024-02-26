import telebot
import buttons as bt
import database as db
from geopy import Nominatim

# Создаем объект бота
bot = telebot.TeleBot('7083271691:AAHuSNFe0DjFaDXgmGzZErtKgK8Y_IuO0pk')
# Работа с картами
geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
# id админа
admin_id = 6948762704
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
# Обработка команда /start

@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id ==admin_id:
        bot.send_message(admin_id, 'Добро пожаловать в админ-панель!',
                         reply_markup=bt.admin_buttons())
        # Переход на этап выбора команды
        bot.register_next_step_handler(message, admin_choice)
    else:
        bot.send_message(message.from_user.id, 'Вы не админ!\n'
                                                    'Нажмите /start')
# Этап выбора команды админом
def admin_choice(message):
    if message.text == 'Добавить продукт':
        bot.send_message(admin_id, 'Итак, давайте начнем! Введите название товара',
                          reply_markup=telebot.types.ReplyKeyboardRemove())
        #Переход на этап получения названия
        bot.register_next_step_handler(message, get_pr_name)
    elif message.text == 'Удалить продукт':
        pr_check = db.check_pr()
        if pr_check:
            bot.send_message(admin_id, 'Введите id товара')
            # Переход на этап получения id товара
            bot.register_next_step_handler(message, get_pr_to_del)
        else:
            bot.send_message(admin_id, 'Продуктов нет!')

    elif message.text == 'Изменить продукт':
       pr_check = db.check_pr()
       if pr_check:
            bot.send_message(admin_id, 'Введите id товара')
            # Переход на этап получения id товара
            bot.register_next_step_handler(message, get_pr_to_del)
       else:
            bot.send_message(admin_id, 'Продуктов нет!')

# Возвращаем на этап выбора команды
       bot.register_next_step_handler(message, admin_choice)

#Этап получения названия
def get_pr_name(message):
    pr_name = message.text
    bot.send_message(admin_id, 'Теперь придумайте описание товару!')
    #Переход на этап получения описания
    bot.register_next_step_handler(message, get_pr_description, pr_name)

#Этап получения описания
def get_pr_description(message, pr_name):
    pr_description = message.text
    bot.send_message(admin_id, 'Какое количество товара!')
    # Переход на этап получения количества
    bot.register_next_step_handler(message, get_pr_count, pr_name, pr_description)

# Этап получения количества
def get_pr_count(message, pr_name, pr_description):
    # Проверка на тип данных
    if message.text != int(message.text):
        bot.send_message(admin_id, 'Пишите только целые числа!')
        # Возвращаем на этап получения количества
        bot.register_next_step_handler(message, get_pr_count, pr_name, pr_description)
    else:
        pr_count = int(message.text)
        bot.send_message(admin_id, 'Какая цена у товара?')
        # Переход на этап получения цены
        bot.register_next_step_handler(message, get_pr_price, pr_name, pr_description, pr_count)

# Этап получения цены
def get_pr_price(message, pr_name, pr_description, pr_count):
    # Проверка на тип данных
    if message.text != float(message.text):
        bot.send_message(admin_id, 'Пишите только дробные числа!')
        # Возвращаем на этап получения количества
        bot.register_next_step_handler(message, get_pr_price, pr_name, pr_description, pr_count)
    else:
        pr_count = float(message.text)
        bot.send_message(admin_id, 'Последний этап, зайдите на сайт'
                                         'https://postimages.org/ и загрузите туда фото. \n'
                                        'Затем, отправьте мне прямую ссылку на фото!')

        # Переход на этап получения цены
        bot.register_next_step_handler(message, get_pr_photo, pr_name, pr_description, pr_count, pr_price)

# Этап получения фото
def get_pr_photo(message, pr_name, pr_description, pr_count, pr_price):
    pr_photo = message.text
    db.add_pr(pr_name, pr_description, pr_count, pr_price, pr_photo)
    bot.send_message(admin_id, 'Готово! Что-то еще?',
                     reply_markup=bt.admin_button())

    # Переход на этап выбора команды
    bot.register_next_step_handler(message, admin_choice)

# Изменение продукта
def get_pr_to_edit(message):
    # Проверка на тип данных
    if message.text != int(message.text):
        bot.send_message(admin_id, 'Пишите только целые числа!')
        # Возвращаем на этап получения id товара
        bot.register_next_step_handler(message, get_pr_to_edit)
    else:
        pr_id = int(message.text)
        bot.send_message(admin_id, 'Сколько товара прибыло?')
        # Переход на этап получения стока
        bot.register_next_step_handler(message, get_pr_stock, pr_id)

# Этап получения стока
def get_pr_stock(message, pr_id):
    if message.text != int(message.text):
        bot.send_message(admin_id, 'Пишите только целые числа!')
        # Возвращаем на этап получения id товара
        bot.register_next_step_handler(message, get_pr_stock, pr_id)
    else:
        pr_id = int(message.text)
        db.change_pr_count(pr_id, pr_stock)
        bot.send_message(admin_id, 'Количество товара успешно изменено!',
                         reply_markup=bt.admin_button())
        # Переход на этап получения выбора команды
        bot.register_next_step_handler(message, admin_choice)

# Удаление продукта
def get_pr_to_del(message):
    # Проверка на тип данных
    if message.text != int(message.text):
        bot.send_message(admin_id, 'Пишите только целые числа!')
        # Возвращаем на этап получения id товара
        bot.register_next_step_handler(message, get_pr_to_del)
    else:
        pr_id = int(message.text)
        db.del_pr(pr_id)
        bot.send_message(admin_id, 'Товар успешно удален!',
                         reply_markup=bt.admin_button())
        # Переход на этап получения выбора команды
        bot.register_next_step_handler(message, admin_choice)

        # Запуск и бота
bot.polling(non_stop=True)
