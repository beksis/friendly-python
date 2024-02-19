import sqlite3

def create_database():
    conn = sqlite3.connect("mydatabase.db")
    conn.close()

# Создание таблицы "students"
def create_table():
    conn = sqlite3.connect("mydatabase.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, grade TEXT)''')
    conn.commit()
    conn.close()

def insert_student(name, age, grade):
    conn = sqlite3.connect("mydatabase.db")
    c = conn.cursor()
    c.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", (name, age, grade))
    conn.commit()
    conn.close()

def get_student_by_name(name):
    conn = sqlite3.connect("mydatabase.db")
    c = conn.cursor()
    c.execute("SELECT name, age, grade FROM students WHERE name=?", (name,))
    student_info = c.fetchone()
    conn.close()
    return student_info

def update_student_grade(name, new_grade):
    conn = sqlite3.connect("mydatabase.db")
    c = conn.cursor()
    c.execute("UPDATE students SET grade=? WHERE name=?", (new_grade, name))
    conn.commit()
    conn.close()

def delete_student(name):
    conn = sqlite3.connect("mydatabase.db")
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE name=?", (name,))
    conn.commit()
    conn.close()

# Создание базы данных и таблицы
create_database()
create_table()

insert_student("Юсуф", 20, "A")
insert_student("Малика", 22, "B")
insert_student("Бобур", 21, "C")

student_info = get_student_by_name("Юсуф")
if student_info:
    print("Student Info:", student_info)
else:
    print("Student not found")

update_student_grade("Юсуф", "B")

student_info = get_student_by_name("Юсуф")
if student_info:
    print("Updated Student Info:", student_info)
else:
    print("Student not found")

# Удаление студента
delete_student("Бобур")