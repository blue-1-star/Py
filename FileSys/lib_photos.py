from PIL import Image
from PIL.ExifTags import TAGS
import os
import datetime
import subprocess


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

def get_video_creation_date(video_path):
    try:
        result = subprocess.run(
            ['G:/Soft/PORTABLE/exiftool', '-CreateDate', '-d', '%Y-%m-%d %H:%M:%S', video_path],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output:
            creation_date_str = output.split(':', 1)[1].strip()
            creation_date = datetime.datetime.strptime(creation_date_str, '%Y-%m-%d %H:%M:%S')
            return creation_date
        else:
            return None
    except Exception as e:
        print(f"Ошибка при получении даты создания для {video_path}: {e}")
        return None
    