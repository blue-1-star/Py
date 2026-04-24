import sqlite3
import pandas as pd
import shutil
import os

# Тот самый путь, который мы нашли
DB_PATH = "/Users/san/Library/Application Support/ViberPC/380978987352/viber.db"
# Временная копия, чтобы не мешать работе Viber
TEMP_DB = "viber_copy.db"

def collect_viber_stats():
    # Копируем файл базы
    shutil.copy2(DB_PATH, TEMP_DB)
    
    # Подключаемся к копии
    conn = sqlite3.connect(TEMP_DB)
    
    # SQL-запрос для сбора статистики:
    # Считаем количество сообщений от каждого участника
    query = """
    SELECT 
        Contact.Name, 
        Contact.Number,
        COUNT(Messages.MessageID) as total_messages
    FROM Messages
    JOIN Contact ON Messages.ContactID = Contact.ContactID
    WHERE Messages.ChatID IS NOT NULL
    GROUP BY Contact.ContactID
    ORDER BY total_messages DESC
    """
    
    try:
        df = pd.read_sql_query(query, conn)
        return df
    finally:
        conn.close()
        # Удаляем временный файл после работы
        if os.path.exists(TEMP_DB):
            os.remove(TEMP_DB)

# Запуск
stats = collect_viber_stats()
# print(stats)
print(stats.head(10))
