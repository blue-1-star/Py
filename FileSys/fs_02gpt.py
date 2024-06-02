import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_data(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    if exif_data:
        exif = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
        return exif
    return None

def get_creation_date(exif_data):
    if 'DateTimeOriginal' in exif_data:
        return exif_data['DateTimeOriginal']
    elif 'DateTime' in exif_data:
        return exif_data['DateTime']
    return None

def copy_photos_by_date(source_directory, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    cnt =0
    for filename in os.listdir(source_directory):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            source_file = os.path.join(source_directory, filename)
            
            try:
                exif_data = get_exif_data(source_file)
                if exif_data:
                    date_str = get_creation_date(exif_data)
                    if date_str:
                        date = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                    else:
                        raise ValueError("Дата создания не найдена в EXIF данных.")
                else:
                    raise ValueError("EXIF данные отсутствуют.")
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
            cnt+=1
            # print(f"Файл {filename} скопирован в {destination_file}")
    print(f"copied {cnt} files" )
        
# Пример использования
source_directory = 'g:/test_meta_data/'
target_directory = 'g:/test_meta_data/Dest'
copy_photos_by_date(source_directory, target_directory)
"""
if exif_data:
    exif = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
    return exif

Пояснение
if exif_data::

Это условие проверяет, есть ли данные EXIF в изображении. Если данные EXIF присутствуют, условие выполняется.
exif_data.items():

exif_data — это словарь, содержащий данные EXIF. Метод items() возвращает все пары (ключ, значение) в этом словаре.
{TAGS.get(tag, tag): value for tag, value in exif_data.items()}:

Это генератор словаря (dict comprehension), который создает новый словарь. Вот как он работает:
Проходимся по всем парам (ключ, значение) в exif_data.
Для каждого tag (ключа) и value (значения) создаем новую пару в словаре.
Ключом в новом словаре становится TAGS.get(tag, tag), а значением остается value.
Подробнее о TAGS.get(tag, tag)
TAGS:

TAGS — это словарь из модуля PIL.ExifTags, который содержит человекочитаемые имена для тегов EXIF.
Например, тег 306 может быть преобразован в 'DateTime'.
TAGS.get(tag, tag):

TAGS.get(tag, tag) пытается получить человекочитаемое имя тега.
Первый аргумент tag — это ключ, который ищем в словаре TAGS.
Второй аргумент tag — это значение по умолчанию, которое будет использовано, если ключ tag не найден в TAGS.
Таким образом, если ключ tag найден в TAGS, возвращается его человекочитаемое имя. В противном случае, возвращается сам tag.
Пример
Допустим, exif_data содержит следующий словарь:

{
    306: '2020:06:17 15:17:36',  # DateTime
    271: 'Canon',                # Make
    272: 'Canon EOS 80D'         # Model
}


Конечно! Давайте разберем этот оператор подробнее:

python
Copy code
if exif_data:
    exif = {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
    return exif
Пояснение
if exif_data::

Это условие проверяет, есть ли данные EXIF в изображении. Если данные EXIF присутствуют, условие выполняется.
exif_data.items():

exif_data — это словарь, содержащий данные EXIF. Метод items() возвращает все пары (ключ, значение) в этом словаре.
{TAGS.get(tag, tag): value for tag, value in exif_data.items()}:

Это генератор словаря (dict comprehension), который создает новый словарь. Вот как он работает:
Проходимся по всем парам (ключ, значение) в exif_data.
Для каждого tag (ключа) и value (значения) создаем новую пару в словаре.
Ключом в новом словаре становится TAGS.get(tag, tag), а значением остается value.
Подробнее о TAGS.get(tag, tag)
TAGS:

TAGS — это словарь из модуля PIL.ExifTags, который содержит человекочитаемые имена для тегов EXIF.
Например, тег 306 может быть преобразован в 'DateTime'.
TAGS.get(tag, tag):

TAGS.get(tag, tag) пытается получить человекочитаемое имя тега.
Первый аргумент tag — это ключ, который ищем в словаре TAGS.
Второй аргумент tag — это значение по умолчанию, которое будет использовано, если ключ tag не найден в TAGS.
Таким образом, если ключ tag найден в TAGS, возвращается его человекочитаемое имя. В противном случае, возвращается сам tag.
Пример
Допустим, exif_data содержит следующий словарь:

python
Copy code
{
    306: '2020:06:17 15:17:36',  # DateTime
    271: 'Canon',                # Make
    272: 'Canon EOS 80D'         # Model
}
При проходе по exif_data.items(), пары (ключ, значение) будут:

(306, '2020:06:17 15:17:36')
(271, 'Canon')
(272, 'Canon EOS 80D')
TAGS.get(306, 306) вернет 'DateTime'

TAGS.get(271, 271) вернет 'Make'

TAGS.get(272, 272) вернет 'Model'

В результате генератор словаря создаст новый словарь:

{
    'DateTime': '2020:06:17 15:17:36',
    'Make': 'Canon',
    'Model': 'Canon EOS 80D'
}

Возвращение словаря
Новый словарь, в котором ключи заменены на человекочитаемые имена, возвращается:

return exif

"""