from telebot import types


#Кнопка отправки номера
def num_button():
    #Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #Создаем сами кнопки
    number = types.KeyboardButton('Отправить номер', request_contact=True)
    #Добавляем кнопку в пространство
    kb.add(number)
    return kb

# Кнопка отправки локации
def loc_button():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем сами кнопки
    location = types.KeyboardButton('Отправить локацию', request_location=True)
    #Добавляем кнопку в пространство
    kb.add(location)
    return kb


#Кнопки для админ-панели
def admin_buttons():
    #Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #Создаем сами кнопки
    add_pr = types.KeyboardButton('Добавить продукт')
    del_pr = types.KeyboardButton('Удалить продукт')
    edit_pr = types.KeyboardButton('Изменить количество продукта')
    to_menu = types.KeyboardButton('На главную')
    #Объединяем кнопки с пространством
    kb.add(add_pr, edit_pr, del_pr)
    kb.row(to_menu)
    return kb

    #
