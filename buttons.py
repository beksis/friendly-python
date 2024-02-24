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