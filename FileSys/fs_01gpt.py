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

"""
Функция def copy_photos_by_date(source_directory, target_directory):
свою задачу выполняет! 
Хочу сделать ряд усовершенствованй.
1. В исходном каталоге ещё имеются видеофайлы  с расширением mp4 - включить их тоже в копирование.

2. Для больших каталогов функция работает долго 
a) сделать какую то простейшую визуализацию процесса обработки - например изменяющаяся цифра - счетчик обработанных файлов, желательно в одном месте экрана ( без громоздкой графики)  а рядом остаток необработанных файлов.

3. создавать какой то лог - файл с протоколом работы 
a) дата
b) пути - источник и целевой файл
c) количество переданных файлов ( фото и видео - раздельно)
d) осталось необработанных и где то выдать список ( не уверен что в лог - файле, нарушит структуру! - может просто на экран по итогу работы? )
e) время обработки
"""

"""
import os
import shutil
import datetime
import time

def copy_photos_by_date(source_directory, target_directory):
    # Фильтр файлов по расширениям
    extensions = ['.jpg', '.jpeg', '.png', '.mp4']
    
    # Подсчет всех файлов для обработки
    all_files = [f for f in os.listdir(source_directory) if os.path.splitext(f)[1].lower() in extensions]
    total_files = len(all_files)
    
    # Лог-файл
    log_file = 'copy_log.txt'
    with open(log_file, 'w') as log:
        log.write(f"Дата: {datetime.datetime.now()}\n")
        log.write(f"Источник: {source_directory}\n")
        log.write(f"Целевой каталог: {target_directory}\n")
        log.write(f"Всего файлов для копирования: {total_files}\n\n")
    
    processed_files = 0
    photo_count = 0
    video_count = 0

    start_time = time.time()
    
    for filename in all_files:
        ext = os.path.splitext(filename)[1].lower()
        source_path = os.path.join(source_directory, filename)
        
        # Определение целевого пути на основе даты создания файла
        creation_time = os.path.getctime(source_path)
        date_folder = datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')
        target_path = os.path.join(target_directory, date_folder, filename)
        
        # Создание целевой папки, если она не существует
        if not os.path.exists(os.path.dirname(target_path)):
            os.makedirs(os.path.dirname(target_path))
        
        # Копирование файла
        shutil.copy2(source_path, target_path)
        
        # Обновление счетчика
        processed_files += 1
        if ext in ['.jpg', '.jpeg', '.png']:
            photo_count += 1
        elif ext == '.mp4':
            video_count += 1
        
        # Обновление визуализации
        remaining_files = total_files - processed_files
        print(f"Обработано файлов: {processed_files}, Осталось: {remaining_files}", end='\r')
        
        # Запись в лог-файл
        with open(log_file, 'a') as log:
            log.write(f"Источник: {source_path}\n")
            log.write(f"Целевой файл: {target_path}\n")
            log.write(f"Дата создания: {datetime.datetime.fromtimestamp(creation_time)}\n\n")
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Итоговая запись в лог-файл
    with open(log_file, 'a') as log:
        log.write(f"Всего переданных фото: {photo_count}\n")
        log.write(f"Всего переданных видео: {video_count}\n")
        log.write(f"Осталось необработанных файлов: {remaining_files}\n")
        log.write(f"Время обработки: {processing_time:.2f} секунд\n")
    
    # Вывод итоговой информации на экран
    print(f"\nВсего переданных фото: {photo_count}")
    print(f"Всего переданных видео: {video_count}")
    print(f"Осталось необработанных файлов: {remaining_files}")
    print(f"Время обработки: {processing_time:.2f} секунд")

# Пример использования
source_directory = 'path_to_source_directory'
target_directory = 'path_to_target_directory'
copy_photos_by_date(source_directory, target_directory)

"""