import os
def get_full_file_path(filename):
    """
    Возвращает полный путь к файлу данных, находящемуся в той же директории,
    что и текущий скрипт, или в указанной поддиректории.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Путь к директории скрипта
    return os.path.join(script_dir, filename)

script_dir = os.path.dirname(os.path.abspath(__file__))  # Путь к директории скрипта
print(os.path.dirname(os.path.abspath(__file__)))    
# 
# import os
import shutil

import os
import shutil

def process_files(directory, operation):
    """
    Выполняет указанную операцию над файлами в каталоге с именами, содержащими "- Copy".

    :param directory: Путь к каталогу
    :param operation: Операция ("rename", "delete", "copy")
    """
    if not os.path.isdir(directory):
        print(f"Каталог {directory} не существует.")
        return

    count = 0
    for filename in os.listdir(directory):
        if "- Copy" in filename:
            old_path = os.path.join(directory, filename)
            if operation == "rename":
                new_filename = filename.replace(" - Copy", "")
                new_path = os.path.join(directory, new_filename)
                os.rename(old_path, new_path)
                count += 1
                print(f"{new_filename} | Переименовано файлов: {count}", end="\r")
            elif operation == "delete":
                os.remove(old_path)
                count += 1
                print(f"{filename} | Удалено файлов: {count}", end="\r")
            elif operation == "copy":
                new_filename = filename.replace(" - Copy", "")
                new_path = os.path.join(directory, new_filename)
                shutil.copy2(old_path, new_path)
                count += 1
                print(f"{new_filename} | Скопировано файлов: {count}", end="\r")
            else:
                print(f"Неизвестная операция: {operation}")
                return

    print(f"\nОперация '{operation}' завершена. Всего обработано файлов: {count}")

# Пример использования
# Замените путь к каталогу на нужный


# Пример использования
# Замените путь к каталогу на нужный
# directory_path = "путь/к/вашему/каталогу"
# directory_path = "G:/test"
directory_path = r"G:\Photo\OnePlus\Photo"

operation = "rename"  # Возможные значения: "rename", "delete", "copy"
process_files(directory_path, operation)
