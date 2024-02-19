import sqlite3
from datetime import datetime, timedelta

# Создание базы данных SQLite3 и таблицы клиентов
def create_database():
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clients
                 (id INTEGER PRIMARY KEY, full_name TEXT, phone_number TEXT, balance REAL)''')
    conn.commit()
    conn.close()


# Регистрация нового клиента
def register_client(full_name, phone_number):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('''INSERT INTO clients (full_name, phone_number, balance) VALUES (?, ?, ?)''',
              (full_name, phone_number, 0))
    conn.commit()
    conn.close()


# Поиск клиента по ФИО или номеру телефона
def find_client(search_term):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM clients WHERE full_name LIKE ? OR phone_number LIKE ?''',
              (f'%{search_term}%', f'%{search_term}%'))
    clients = c.fetchall()
    conn.close()
    return clients


# Пополнение баланса клиента
def deposit(client_id, amount):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('''UPDATE clients SET balance = balance + ? WHERE id = ?''',
              (amount, client_id))
    conn.commit()
    conn.close()


# Снятие денег с баланса клиента
def withdraw(client_id, amount):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('''UPDATE clients SET balance = balance - ? WHERE id = ?''',
              (amount, client_id))
    conn.commit()
    conn.close()


# Просмотр баланса клиента
def check_balance(client_id):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute('''SELECT balance FROM clients WHERE id = ?''', (client_id,))
    balance = c.fetchone()[0]
    conn.close()
    return balance


# Подсчет вклада на указанный срок (12, 24 или 36 месяцев)
def calculate_deposit(client_id, amount, months):
    interest_rate = 0.05  # Процентная ставка в год
    total_amount = amount * (1 + interest_rate) ** (months / 12)
    deposit_end_date = datetime.now() + timedelta(days=30 * months)
    return total_amount, deposit_end_date


# Пример использования функций
create_database()
register_client("Каримов Ислам Абдуганиевич", "+998977106683")
register_client("Юсупов Ильхом Набиевич", "+998978086683")

# Поиск клиента по ФИО или номеру телефона
print(find_client("Каримов"))
print(find_client("Юсупов"))

# Пополнение баланса клиента
deposit(1, 10000)

# Снятие денег с баланса клиента
withdraw(1, 5000)

# Просмотр баланса клиента
print(check_balance(1))

# Подсчет вклада
amount = 100000
months = 12
total_amount, end_date = calculate_deposit(1, amount, months)
print(f"Сумма вклада через {months} месяцев: {total_amount}, до {end_date}")