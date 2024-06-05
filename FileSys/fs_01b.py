import os
import shutil
import datetime
import time
# import subprocess
from lib_photos import get_creation_date, get_video_creation_date

def copy_photos_by_date(source_directory, target_directory):
    # Фильтр файлов по расширениям
    extensions = ['.jpg', '.jpeg', '.png', '.mp4']
    
    # Подсчет всех файлов для обработки
    all_files = [f for f in os.listdir(source_directory) if os.path.splitext(f)[1].lower() in extensions]
    total_files = len(all_files)
    
    # Лог-файл
    dtt = datetime.datetime.now()
    name = dtt.strftime('%d_%m_%Y')
    log_file = os.path.join('g:/test', f'copy_log_{name}.txt')
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
        if ext in ['.jpg', '.jpeg', '.png']:
            creation_date = get_creation_date(source_path)
        elif ext == '.mp4':
            creation_date = get_video_creation_date(source_path)
        else:
            continue
        
        if creation_date is None:
            print(f"Не удалось получить дату создания для {source_path}")
            continue
        
        date_folder = creation_date.strftime('%Y_%m')
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
            log.write(f"Дата создания: {creation_date}\n\n")
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Итоговая запись в лог-файл
    with open(log_file, 'a') as log:
        log.write(f"Всего переданных фото: {photo_count}\n")
        log.write(f"Всего переданных видео: {video_count}\n")
        log.write(f"Осталось необработанных файлов: {total_files - processed_files}\n")
        log.write(f"Время обработки: {processing_time:.2f} секунд\n")
    
    # Вывод итоговой информации на экран
    print(f"\nВсего переданных фото: {photo_count}")
    print(f"Всего переданных видео: {video_count}")
    print(f"Осталось необработанных файлов: {total_files - processed_files}")
    print(f"Время обработки: {processing_time:.2f} секунд")

# Пример использования
source_directory = 'g:/test'
target_directory = 'g:/test/imvers'
copy_photos_by_date(source_directory, target_directory)
