from PIL import Image
from PIL.ExifTags import TAGS
import os
import datetime

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

source_path = r"G:\test\imvers\2024-06-02\IMG_20240529_120918.jpg"
creation_date = get_creation_date(source_path)
if creation_date:
    # date_folder = creation_date.strftime('%Y-%m-%d')
    date_folder = creation_date.strftime('%Y_%m')
    # print(f"{date.year}_{date.month:02d}")
    print(f'Date folder: {date_folder}')
else:
    print('Creation date not found in EXIF data')
