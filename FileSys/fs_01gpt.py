import os
import shutil
from datetime import datetime

def copy_photos_by_date(source_directory, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    cnt =0
    for filename in os.listdir(source_directory):
        if filename.startswith("IMG_") and filename.endswith((".jpg", ".jpeg", ".png")):
            # Извлечение даты из имени файла
            date_str = filename.split('_')[1]
            try:
                date = datetime.strptime(date_str, "%Y%m%d")
            except ValueError:
                print(f"Ошибка при обработке файла {filename}: некорректный формат даты.")
                continue
            
            # Формирование имени целевой директории
            target_subdirectory = os.path.join(target_directory, f"{date.year}_{date.month:02d}")
            if not os.path.exists(target_subdirectory):
                os.makedirs(target_subdirectory)
            
            # Копирование файла
            source_file = os.path.join(source_directory, filename)
            destination_file = os.path.join(target_subdirectory, filename)
            shutil.copy2(source_file, destination_file)
            cnt += 1
            # print(f"Файл {filename} скопирован в {destination_file}")
    print(f"copied {cnt} files" )
    

# Пример использования
# source_directory = 'g:/test/'
# target_directory = 'g:/test2/'
source_directory = 'g:/photo/oneplus/photo/'
target_directory = 'e:/photo/oneplus/photo'
copy_photos_by_date(source_directory, target_directory)
