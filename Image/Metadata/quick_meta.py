#!/usr/bin/env python3
"""
ПРОСТЕЙШИЙ скрипт для метаданных изображения
Сохраните как: quick_meta.py
"""

from PIL import Image, ExifTags
import os

def quick_metadata(image_path):
    """Быстрая проверка метаданных одного файла"""
    print(f"\n📷 Файл: {os.path.basename(image_path)}")
    print(f"📁 Путь: {image_path}")
    
    try:
        img = Image.open(image_path)
        print(f"📐 Размер: {img.size[0]}x{img.size[1]}")
        print(f"🎨 Формат: {img.format}")
        
        # Базовые EXIF данные
        exif = img._getexif()
        if exif:
            print("\n📊 Основные метаданные:")
            for tag_id, value in exif.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                if tag in ['DateTime', 'Model', 'Make', 'GPSInfo']:
                    print(f"  {tag}: {value}")
        
        # Проверяем GPS
        if exif and 34853 in exif:  # 34853 = GPSInfo
            print("\n📍 Найдены GPS координаты!")
            gps_info = exif[34853]
            for key in gps_info:
                gps_tag = ExifTags.GPSTAGS.get(key, key)
                print(f"  {gps_tag}: {gps_info[key]}")
                
    except Exception as e:
        print(f"❌ Ошибка: {e}")

# Использование
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        quick_metadata(sys.argv[1])
    else:
        print("Использование: python quick_meta.py <путь_к_фото>")