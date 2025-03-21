import os
from pathlib import Path

import os
from pathlib import Path

def add_suffix_to_files(folder_path, suffix="_d0"):
    """
    Добавляет суффикс к именам всех файлов *.jpg в каталоге, если имя файла не заканчивается на этот суффикс.
    
    :param folder_path: Путь к каталогу с файлами.
    :param suffix: Суффикс, который нужно добавить (по умолчанию "_d0").
    """
    # Проверяем, существует ли каталог
    if not os.path.exists(folder_path):
        print(f"Каталог {folder_path} не существует.")
        return
    
    # Получаем список всех файлов *.jpg в каталоге
    jpg_files = list(Path(folder_path).glob("*.jpg"))
    
    # Переименовываем файлы
    for file_path in jpg_files:
        file_name = file_path.name  # Имя файла с расширением
        file_stem = file_path.stem  # Имя файла без расширения
        
        # Проверяем, заканчивается ли имя файла на суффикс
        if not file_stem.endswith(suffix):
            # Формируем новое имя файла
            new_file_name = f"{file_stem}{suffix}.jpg"
            new_file_path = file_path.with_name(new_file_name)
            
            # Переименовываем файл
            file_path.rename(new_file_path)
            print(f"Файл {file_name} переименован в {new_file_name}.")
        else:
            print(f"Файл {file_name} уже содержит суффикс {suffix}. Переименование не требуется.")

# Пример использования
folder_path = r"G:\My\sov\extract\plant_d14"
add_suffix_to_files(folder_path, suffix="_d0")


def remove_suffix_from_files(folder_path, suffix="_d0"):
    """
    Удаляет суффикс из имен всех файлов *.jpg в каталоге, если имя файла заканчивается на этот суффикс.
    
    :param folder_path: Путь к каталогу с файлами.
    :param suffix: Суффикс, который нужно удалить (по умолчанию "_d0").
    """
    # Проверяем, существует ли каталог
    if not os.path.exists(folder_path):
        print(f"Каталог {folder_path} не существует.")
        return
    
    # Получаем список всех файлов *.jpg в каталоге
    jpg_files = list(Path(folder_path).glob("*.jpg"))
    
    # Переименовываем файлы
    for file_path in jpg_files:
        file_name = file_path.name  # Имя файла с расширением
        file_stem = file_path.stem  # Имя файла без расширения
        
        # Проверяем, заканчивается ли имя файла на суффикс
        if file_stem.endswith(suffix):
            # Удаляем суффикс из имени файла
            new_file_stem = file_stem[:-len(suffix)]  # Убираем суффикс
            new_file_name = f"{new_file_stem}.jpg"
            new_file_path = file_path.with_name(new_file_name)
            
            # Переименовываем файл
            file_path.rename(new_file_path)
            print(f"Файл {file_name} переименован в {new_file_name}.")
        else:
            print(f"Файл {file_name} не содержит суффикс {suffix} в конце. Переименование не требуется.")

# Пример использования
folder_path = r"G:\My\sov\extract\plant_d0"
# remove_suffix_from_files(folder_path, suffix="_d0")

# Пример использования
add_suffix_to_files(folder_path, suffix="_d0")
