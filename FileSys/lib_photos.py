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
    