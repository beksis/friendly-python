from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import sqlite3

# Определение стадий для ConversationHandler
NAME, PHONE_NUMBER, LOCATION = range(3)


# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Привет! Для регистрации введите ваше имя."
    )
    return NAME


# Функция для сохранения информации о пользователе в базу данных
def save_user_info(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    name = update.message.text
    context.user_data['name'] = name
    context.user_data['user_id'] = user.id

    # Сохраняем информацию в базу данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_id, name) VALUES (?, ?)", (user.id, name))
    conn.commit()
    conn.close()

    update.message.reply_text(
        f"Спасибо, {name}! Теперь введите ваш номер телефона."
    )
    return PHONE_NUMBER


# Функция для сохранения номера телефона пользователя
def save_phone_number(update: Update, context: CallbackContext) -> int:
    phone_number = update.message.text
    context.user_data['phone_number'] = phone_number

    # Обновляем информацию о пользователе в базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET phone_number = ? WHERE user_id = ?",
                   (phone_number, context.user_data['user_id']))
    conn.commit()
    conn.close()

    update.message.reply_text(
        "Теперь отправьте вашу локацию."
    )
    return LOCATION


# Функция для сохранения локации пользователя
def save_location(update: Update, context: CallbackContext) -> int:
    location = update.message.location
    context.user_data['location'] = location

    update.message.reply_text(
        "Спасибо! Все ваши данные сохранены."
    )
    return ConversationHandler.END


def main() -> None:
    updater = Updater("7065648023:AAF4daUy18TXNEmtWy1AYDf5Su2WH0Ql2aw")

    dispatcher = updater.dispatcher

    # Создаем таблицу пользователей в базе данных
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (user_id INTEGER PRIMARY KEY, name TEXT, phone_number TEXT, location TEXT)''')
    conn.commit()
    conn.close()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, save_user_info)],
            PHONE_NUMBER: [MessageHandler(Filters.text & ~Filters.command, save_phone_number)],
            LOCATION: [MessageHandler(Filters.location & ~Filters.command, save_location)],
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()