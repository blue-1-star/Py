import os
import ast
import datetime
import subprocess
import sys

# Путь к старой версии Python, укажите свой
OLD_PYTHON_PATH = r"C:\Python\python.exe"  # или путь к вашей старой версии

# Папка с проектами
BASE_DIR = r'G:\Programming\Py'
# Получаем папку, где запущен скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))

# Создаем папку Data внутри папки скрипта, если не существует
data_dir = os.path.join(script_dir, 'Data')
os.makedirs(data_dir, exist_ok=True)

# Создаем имя файла с датой
today_str = datetime.datetime.now().strftime('%d_%m_%Y')
diff_filename = os.path.join(data_dir, f'diff_lib_{today_str}.txt')


# Функция получения списка пакетов
def get_packages(python_path, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        subprocess.check_call([python_path, '-m', 'pip', 'freeze'], stdout=f)

# Получить списки
# old_req_file = 'old_requirements.txt'
# new_req_file = 'new_requirements.txt'
old_req_file =  os.path.join(data_dir, 'old_requirements.txt')
new_req_file = os.path.join(data_dir, 'new_requirements.txt')

print("Получение списка пакетов из старой версии Python...")
get_packages(OLD_PYTHON_PATH, old_req_file)

print("Получение списка пакетов из текущего окружения...")
get_packages(sys.executable, new_req_file)

# Читаем списки и вычисляем разность
with open(old_req_file, 'r', encoding='utf-8') as f:
    old_libs = set(line.strip() for line in f if line.strip())

with open(new_req_file, 'r', encoding='utf-8') as f:
    new_libs = set(line.strip() for line in f if line.strip())

libs_to_install = old_libs - new_libs

# Запись файла diff с датой
with open(diff_filename, 'w', encoding='utf-8') as f:
    for lib in sorted(libs_to_install):
        f.write(lib + '\n')

# print(f"Файл со списком разницы создан: {diff_filename}")

# Считаем количество строк в файле
with open(diff_filename, 'r', encoding='utf-8') as f:
    line_count = sum(1 for _ in f)

# Выводим сообщение с количеством строк
print(f"Файл со списком разницы создан: {diff_filename}, строк: {line_count}")


# Теперь используем этот файл для анализа использования библиотек в проектах
# (код из предыдущего сообщения)
# ...
