import os
import shutil
from datetime import datetime

def copy_photos_by_date(source_directory, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    cnt = 0
    for filename in os.listdir(source_directory):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            source_file = os.path.join(source_directory, filename)
            
            try:
                # Получение даты последней модификации файла
                timestamp = os.path.getmtime(source_file)
                date = datetime.fromtimestamp(timestamp)
            except Exception as e:
                print(f"Ошибка при обработке файла {filename}: {e}")
                continue
            
            # Формирование имени целевой директории
            target_subdirectory = os.path.join(target_directory, f"{date.year}_{date.month:02d}")
            if not os.path.exists(target_subdirectory):
                os.makedirs(target_subdirectory)
            
            # Копирование файла
            destination_file = os.path.join(target_subdirectory, filename)
            shutil.copy2(source_file, destination_file)
            cnt +=1
            
            # print(f"Файл {filename} скопирован в {destination_file}")
        print(f"copied {cnt} files" )

# Пример использования
source_directory = 'g:/test_meta_data/'
target_directory = 'g:/test_meta_data/Dest'
copy_photos_by_date(source_directory, target_directory)

