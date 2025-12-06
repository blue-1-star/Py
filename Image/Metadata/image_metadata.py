import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from datetime import datetime
import piexif
import base64
from io import BytesIO
from typing import Dict, Any, Optional, Tuple
import json

class ImageMetadataExtractor:
    def __init__(self, preview_size: Tuple[int, int] = (100, 100)):
        """
        Инициализация экстрактора метаданных
        
        Args:
            preview_size: размер превью (ширина, высота)
        """
        self.preview_size = preview_size
        
    def extract_metadata(self, image_path: str) -> Dict[str, Any]:
        """
        Извлечение метаданных из изображения
        
        Args:
            image_path: путь к файлу изображения
            
        Returns:
            Словарь с метаданными
        """
        metadata = {
            'filename': os.path.basename(image_path),
            'filepath': os.path.abspath(image_path),
            'filesize': os.path.getsize(image_path),
            'creation_time': None,
            'modification_time': None,
            'exif_data': {},
            'location': None,
            'camera_info': {},
            'preview_base64': None
        }
        
        try:
            # Получаем время создания и модификации файла
            metadata['creation_time'] = datetime.fromtimestamp(
                os.path.getctime(image_path)
            ).isoformat()
            metadata['modification_time'] = datetime.fromtimestamp(
                os.path.getmtime(image_path)
            ).isoformat()
            
            # Открываем изображение
            with Image.open(image_path) as img:
                # Извлекаем EXIF данные
                metadata['exif_data'] = self._extract_exif_data(img)
                
                # Извлекаем GPS данные
                if 'GPSInfo' in metadata['exif_data']:
                    metadata['location'] = self._extract_gps_coordinates(
                        metadata['exif_data']['GPSInfo']
                    )
                
                # Извлекаем информацию о камере
                metadata['camera_info'] = self._extract_camera_info(
                    metadata['exif_data']
                )
                
                # Создаем превью
                metadata['preview_base64'] = self._create_preview(img)
                
                # Основная информация об изображении
                metadata.update({
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height
                })
                
        except Exception as e:
            metadata['error'] = str(e)
            
        return metadata
    
    def _extract_exif_data(self, image: Image.Image) -> Dict[str, Any]:
        """Извлечение EXIF данных из изображения"""
        exif_data = {}
        
        try:
            # Пробуем получить EXIF через PIL
            exif = image._getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    exif_data[tag_name] = value
            
            # Дополнительно пробуем через piexif для более полных данных
            if hasattr(image, 'info') and 'exif' in image.info:
                exif_dict = piexif.load(image.info['exif'])
                for ifd in exif_dict:
                    if ifd != "thumbnail":
                        for tag_id, value in exif_dict[ifd].items():
                            tag_name = TAGS.get(tag_id, tag_id)
                            if isinstance(value, bytes):
                                try:
                                    value = value.decode('utf-8').strip('\x00')
                                except:
                                    pass
                            exif_data[tag_name] = value
        except Exception:
            pass
            
        return exif_data
    
    def _extract_gps_coordinates(self, gps_info: Dict) -> Optional[Dict[str, float]]:
        """Извлечение GPS координат из EXIF данных"""
        try:
            def convert_to_degrees(value):
                """Конвертирует GPS координаты в градусы"""
                if isinstance(value, tuple):
                    d, m, s = value
                    return d + (m / 60.0) + (s / 3600.0)
                return float(value)
            
            gps_data = {}
            for key in gps_info.keys():
                decode = GPSTAGS.get(key, key)
                gps_data[decode] = gps_info[key]
            
            lat = convert_to_degrees(gps_data.get('GPSLatitude', (0, 0, 0)))
            lon = convert_to_degrees(gps_data.get('GPSLongitude', (0, 0, 0)))
            
            # Учитываем направление
            if gps_data.get('GPSLatitudeRef') == 'S':
                lat = -lat
            if gps_data.get('GPSLongitudeRef') == 'W':
                lon = -lon
            
            return {
                'latitude': lat,
                'longitude': lon,
                'altitude': gps_data.get('GPSAltitude', 0)
            }
        except Exception:
            return None
    
    def _extract_camera_info(self, exif_data: Dict) -> Dict[str, str]:
        """Извлечение информации о камере"""
        camera_info = {}
        
        # Маппинг тегов EXIF к читаемым названиям
        camera_tags = {
            'Make': 'manufacturer',
            'Model': 'model',
            'DateTimeOriginal': 'date_time',
            'ExposureTime': 'exposure_time',
            'FNumber': 'f_number',
            'ISOSpeedRatings': 'iso',
            'FocalLength': 'focal_length',
            'LensMake': 'lens_manufacturer',
            'LensModel': 'lens_model'
        }
        
        for exif_tag, readable_name in camera_tags.items():
            if exif_tag in exif_data:
                camera_info[readable_name] = str(exif_data[exif_tag])
        
        return camera_info
    
    def _create_preview(self, image: Image.Image) -> Optional[str]:
        """Создание превью в формате base64"""
        try:
            # Создаем копию изображения для превью
            preview = image.copy()
            
            # Конвертируем в RGB если нужно
            if preview.mode in ('RGBA', 'LA', 'P'):
                preview = preview.convert('RGB')
            
            # Масштабируем
            preview.thumbnail(self.preview_size)
            
            # Конвертируем в base64
            buffered = BytesIO()
            preview.save(buffered, format="JPEG", quality=50)
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            return f"data:image/jpeg;base64,{img_str}"
        except Exception:
            return None
    
    def get_formatted_metadata(self, image_path: str) -> str:
        """Получение форматированных метаданных в виде строки"""
        metadata = self.extract_metadata(image_path)
        
        result = []
        result.append(f"Файл: {metadata['filename']}")
        result.append(f"Путь: {metadata['filepath']}")
        result.append(f"Размер: {metadata['filesize']} байт")
        result.append(f"Разрешение: {metadata.get('width', 'N/A')}x{metadata.get('height', 'N/A')}")
        
        if metadata['creation_time']:
            result.append(f"Дата создания: {metadata['creation_time']}")
        
        if metadata['location']:
            loc = metadata['location']
            result.append(f"Координаты: {loc.get('latitude', 'N/A')}, {loc.get('longitude', 'N/A')}")
        
        if metadata['camera_info']:
            result.append("Информация о камере:")
            for key, value in metadata['camera_info'].items():
                result.append(f"  {key}: {value}")
        
        return "\n".join(result)