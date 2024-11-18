from PIL import Image
from PIL.ExifTags import TAGS
import os
import datetime
import subprocess
import shutil
import time
import pytz

def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    if not exif_data:
        return None

    exif = {
        TAGS.get(tag): value
        for tag, value in exif_data.items()
        if tag in TAGS
    }
    return exif

def get_creation_date(image_path):
    exif_data = get_exif_data(image_path)
    if not exif_data:
        return None

    creation_date = exif_data.get('DateTimeOriginal')
    if not creation_date:
        return None

    return datetime.datetime.strptime(creation_date, '%Y:%m:%d %H:%M:%S')


    
 


# -------- 18.11.2024 version GPT

def get_video_creation_date(video_path):
    """Определяет дату создания видеофайла с использованием exiftool."""
    try:
        # Запуск exiftool для получения даты создания
        result = subprocess.run(
            ['G:/Soft/PORTABLE/exiftool', '-CreateDate', '-d', '%Y-%m-%d %H:%M:%S', video_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Ошибка при вызове exiftool: {result.stderr}")
            return None

        output = result.stdout.strip()
        if not output:
            print(f"Пустой результат exiftool для файла: {video_path}")
            return None

        # Извлечение строки даты из вывода
        try:
            creation_date_str = output.split(':', 1)[1].strip()
            # Парсинг даты
            creation_date = datetime.datetime.strptime(creation_date_str, '%Y-%m-%d %H:%M:%S')
            # Установка временной зоны UTC
            creation_date_utc = pytz.utc.localize(creation_date)
            return creation_date_utc
        except (IndexError, ValueError):
            print(f"Невозможно извлечь дату из вывода: {output}")
            return None
    except Exception as e:
        print(f"Ошибка при обработке файла {video_path}: {e}")
        return None



def copy_photos_by_date(source_directory, target_directory):
    """Копирует фото и видео из source_directory в target_directory, сортируя по дате создания."""
    extensions = ['.jpg', '.jpeg', '.png', '.mp4']
    
    all_files = [f for f in os.listdir(source_directory) if os.path.splitext(f)[1].lower() in extensions]
    total_files = len(all_files)

    dtt = datetime.datetime.now()
    name = dtt.strftime('%d_%m_%Y')
    log_file = f'g:/test/copy_log_{name}.txt'
    error_log = f'g:/test/error_log_{name}.txt'

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
        
        try:
            # Определяем дату создания в зависимости от типа файла
            if ext in ['.jpg', '.jpeg', '.png']:
                creation_date = get_creation_date(source_path)
            elif ext == '.mp4':
                creation_date = get_video_creation_date(source_path)
            else:
                raise ValueError("Неизвестный формат файла")
            
            if creation_date is None:
                raise ValueError("Дата создания не найдена")
            
            date_folder = creation_date.strftime('%Y_%m')
        except Exception as e:
            # Если не удалось определить дату, отправляем файл в "unknown_date"
            date_folder = "unknown_date"
            with open(error_log, 'a') as elog:
                elog.write(f"Ошибка для файла: {source_path}\n")
                elog.write(f"Причина: {str(e)}\n\n")
        
        target_path = os.path.join(target_directory, date_folder, filename)
        
        # Создание целевой папки, если она не существует
        if not os.path.exists(os.path.dirname(target_path)):
            os.makedirs(os.path.dirname(target_path))
        
        # Копирование файла
        shutil.copy2(source_path, target_path)
        
        # Обновление счетчиков
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
            log.write(f"Дата создания: {date_folder}\n\n")
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Итоговая запись в лог-файл
    with open(log_file, 'a') as log:
        log.write(f"Всего переданных фото: {photo_count}\n")
        log.write(f"Всего переданных видео: {video_count}\n")
        log.write(f"Осталось необработанных файлов: {total_files - processed_files}\n")
        log.write(f"Время обработки: {processing_time:.2f} секунд\n")
    
    # Итоговая информация
    print(f"\nВсего переданных фото: {photo_count}")
    print(f"Всего переданных видео: {video_count}")
    print(f"Осталось необработанных файлов: {total_files - processed_files}")
    print(f"Время обработки: {processing_time:.2f} секунд")

def copy_and_delete_photos_by_date(source_directory, target_directory):
    """Копирует фото и видео из source_directory в target_directory, сортируя по дате создания,
    а затем удаляет их из исходного каталога."""
    extensions = ['.jpg', '.jpeg', '.png', '.mp4']
    
    all_files = [f for f in os.listdir(source_directory) if os.path.splitext(f)[1].lower() in extensions]
    total_files = len(all_files)

    dtt = datetime.datetime.now()
    name = dtt.strftime('%d_%m_%Y')
    log_file = f'g:/test/copy_log_{name}.txt'
    error_log = f'g:/test/error_log_{name}.txt'

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
        
        try:
            # Определяем дату создания в зависимости от типа файла
            if ext in ['.jpg', '.jpeg', '.png']:
                creation_date = get_creation_date(source_path)
            elif ext == '.mp4':
                creation_date = get_video_creation_date(source_path)
            else:
                raise ValueError("Неизвестный формат файла")
            
            if creation_date is None:
                raise ValueError("Дата создания не найдена")
            
            date_folder = creation_date.strftime('%Y_%m')
        except Exception as e:
            # Если не удалось определить дату, отправляем файл в "unknown_date"
            date_folder = "unknown_date"
            with open(error_log, 'a') as elog:
                elog.write(f"Ошибка для файла: {source_path}\n")
                elog.write(f"Причина: {str(e)}\n\n")
        
        target_path = os.path.join(target_directory, date_folder, filename)
        
        # Создание целевой папки, если она не существует
        if not os.path.exists(os.path.dirname(target_path)):
            os.makedirs(os.path.dirname(target_path))
        
        # Копирование файла
        shutil.copy2(source_path, target_path)
        
        # Удаление файла из исходного каталога
        try:
            os.remove(source_path)
        except Exception as e:
            with open(error_log, 'a') as elog:
                elog.write(f"Не удалось удалить файл: {source_path}\n")
                elog.write(f"Причина: {str(e)}\n\n")
        
        # Обновление счетчиков
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
            log.write(f"Дата создания: {date_folder}\n\n")
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Итоговая запись в лог-файл
    with open(log_file, 'a') as log:
        log.write(f"Всего переданных фото: {photo_count}\n")
        log.write(f"Всего переданных видео: {video_count}\n")
        log.write(f"Осталось необработанных файлов: {total_files - processed_files}\n")
        log.write(f"Время обработки: {processing_time:.2f} секунд\n")
    
    # Итоговая информация
    print(f"\nВсего переданных фото: {photo_count}")
    print(f"Всего переданных видео: {video_count}")
    print(f"Осталось необработанных файлов: {total_files - processed_files}")
    print(f"Время обработки: {processing_time:.2f} секунд")
