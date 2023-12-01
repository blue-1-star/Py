# test sqlite  Работа с SQLite в Python (для чайников)
# https://habr.com/ru/articles/754400/
import sqlite3
connection = sqlite3.connect('G:\\Programming\\Py\\SQLite\\Data\\my_dbase.db')
cursor = connection.cursor()
# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER
)
''')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users (email)')
# cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', ('newuser', 'newuser@example.com', 28))
# cursor.execute('INSERT INTO Users (username, email, age) VALUES (?, ?, ?)', ('barbos', 'barbos@example.com', 43))
# cursor.execute('UPDATE Users SET age = ? WHERE username = ?', (28, 'newuser'))
# cursor.execute('DELETE FROM Users WHERE username = ?', ('newuser',))
cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()
for user in users:
    print(user)
# print("Ot's OK")
# Применение операторов SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY
cursor.execute('SELECT username, age FROM Users WHERE age < ?', (25,))
results = cursor.fetchall()

for row in results:
    print(row)
connection.commit()
connection.close()

