"""
project/
│
├── FileSys/            # Директория для библиотеки
│   ├── lib_files.py     # Модуль с функциями
│   
│
├── A/M/E                # Дерево поддиректорий со скриптом 
\u2500   ──
─
"""
def get_char_codes(s: str, start: int = 0, end: int = None) -> list:
    """
    Возвращает список кодов символов строки в указанном диапазоне.

    :param s: Входная строка.
    :param start: Начало среза (по умолчанию 0).
    :param end: Конец среза (по умолчанию None, что означает до конца строки).
    :return: Список кодов символов строки.
    """
    if end is None:
        end = len(s)
    return [ord(char) for char in s[start:end]]

# Пример использования
st = "├── main.py"               # Главный скрипт
string = "Привет, мир!"
# codes = get_char_codes(string, 0, 6)
codes = get_char_codes(st)
print(codes)  # [1055, 1088, 1080, 1074, 1077, 1090]
print('\u2500')
print('\u9500')

import sys
import os

# Получаем путь к корневой директории проекта
print(sys.path)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

# Добавляем этот путь в sys.path
sys.path.append(project_root)
print('----------------')
print(sys.path)

# Теперь можно импортировать
from FileSys.lib_files import get_full_file_path
