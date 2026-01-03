import os
import glob
from pathlib import Path
import pandas as pd
import sqlite3
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
from image_metadata import ImageMetadataExtractor

class ImageCatalogProcessor:
    def __init__(self, 
                 preview_size: Tuple[int, int] = (100, 100),
                 supported_formats: List[str] = None):
        """
        Инициализация процессора каталогов изображений
        
        Args:
            preview_size: размер превью
            supported_formats: поддерживаемые форматы изображений
        """
        self.extractor = ImageMetadataExtractor(preview_size)
        self.supported_formats = supported_formats or [
            '*.jpg', '*.jpeg', '*.png', '*.gif', 
            '*.bmp', '*.tiff', '*.tif', '*.webp'
        ]
    
    def process_directories(self, 
                           directories: List[str], 
                           recursive: bool = True) -> List[Dict[str, Any]]:
        """
        Обработка списка каталогов
        
        Args:
            directories: список путей к каталогам
            recursive: рекурсивный поиск
            
        Returns:
            Список словарей с метаданными
        """
        all_metadata = []
        
        for directory in directories:
            if not os.path.exists(directory):
                print(f"Предупреждение: каталог '{directory}' не существует")
                continue
            
            print(f"Обработка каталога: {directory}")
            
            # Собираем все файлы изображений
            image_files = []
            for fmt in self.supported_formats:
                pattern = os.path.join(directory, '**', fmt) if recursive else os.path.join(directory, fmt)
                image_files.extend(glob.glob(pattern, recursive=recursive))
            
            print(f"Найдено {len(image_files)} изображений")
            
            # Обрабатываем каждый файл
            for i, image_file in enumerate(image_files, 1):
                print(f"Обработка {i}/{len(image_files)}: {os.path.basename(image_file)}")
                
                try:
                    metadata = self.extractor.extract_metadata(image_file)
                    all_metadata.append(metadata)
                except Exception as e:
                    print(f"Ошибка при обработке {image_file}: {e}")
        
        return all_metadata
    
    def save_to_excel(self, 
                     metadata_list: List[Dict[str, Any]], 
                     output_file: str = "image_metadata.xlsx"):
        """
        Сохранение метаданных в Excel файл
        
        Args:
            metadata_list: список метаданных
            output_file: путь к выходному файлу
        """
        if not metadata_list:
            print("Нет данных для сохранения")
            return
        
        # Подготовка данных для DataFrame
        data = []
        for metadata in metadata_list:
            row = {
                'filename': metadata.get('filename', ''),
                'filepath': metadata.get('filepath', ''),
                'filesize': metadata.get('filesize', 0),
                'width': metadata.get('width', 0),
                'height': metadata.get('height', 0),
                'format': metadata.get('format', ''),
                'creation_time': metadata.get('creation_time', ''),
                'modification_time': metadata.get('modification_time', ''),
            }
            
            # Добавляем координаты
            location = metadata.get('location')
            if location:
                row.update({
                    'latitude': location.get('latitude'),
                    'longitude': location.get('longitude'),
                    'altitude': location.get('altitude')
                })
            else:
                row.update({
                    'latitude': None,
                    'longitude': None,
                    'altitude': None
                })
            
            # Добавляем информацию о камере
            camera_info = metadata.get('camera_info', {})
            row.update({
                'camera_manufacturer': camera_info.get('manufacturer'),
                'camera_model': camera_info.get('model'),
                'date_time': camera_info.get('date_time'),
                'exposure_time': camera_info.get('exposure_time'),
                'f_number': camera_info.get('f_number'),
                'iso': camera_info.get('iso'),
                'focal_length': camera_info.get('focal_length')
            })
            
            # Добавляем превью (только ссылка на base64)
            row['has_preview'] = metadata.get('preview_base64') is not None
            
            # Сохраняем полные EXIF данные как JSON
            row['exif_json'] = json.dumps(metadata.get('exif_data', {}), default=str)
            
            data.append(row)
        
        # Создаем DataFrame
        df = pd.DataFrame(data)
        
        # Сохраняем в Excel
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Metadata', index=False)
            
            # Настраиваем ширину колонок
            worksheet = writer.sheets['Metadata']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"Данные сохранены в {output_file}")
    
    def save_to_sqlite(self, 
                      metadata_list: List[Dict[str, Any]], 
                      output_file: str = "image_metadata.db"):
        """
        Сохранение метаданных в SQLite базу данных
        
        Args:
            metadata_list: список метаданных
            output_file: путь к файлу БД
        """
        if not metadata_list:
            print("Нет данных для сохранения")
            return
        
        conn = sqlite3.connect(output_file)
        cursor = conn.cursor()
        
        # Создаем таблицы
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                filepath TEXT UNIQUE,
                filesize INTEGER,
                width INTEGER,
                height INTEGER,
                format TEXT,
                creation_time TEXT,
                modification_time TEXT,
                latitude REAL,
                longitude REAL,
                altitude REAL,
                camera_manufacturer TEXT,
                camera_model TEXT,
                date_time TEXT,
                exposure_time TEXT,
                f_number TEXT,
                iso INTEGER,
                focal_length TEXT,
                has_preview BOOLEAN,
                exif_json TEXT,
                processed_time TEXT
            )
        ''')
        
        # Вставляем данные
        for metadata in metadata_list:
            location = metadata.get('location', {})
            camera_info = metadata.get('camera_info', {})
            
            cursor.execute('''
                INSERT OR REPLACE INTO images (
                    filename, filepath, filesize, width, height, format,
                    creation_time, modification_time,
                    latitude, longitude, altitude,
                    camera_manufacturer, camera_model, date_time,
                    exposure_time, f_number, iso, focal_length,
                    has_preview, exif_json, processed_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                metadata.get('filename'),
                metadata.get('filepath'),
                metadata.get('filesize', 0),
                metadata.get('width', 0),
                metadata.get('height', 0),
                metadata.get('format'),
                metadata.get('creation_time'),
                metadata.get('modification_time'),
                location.get('latitude'),
                location.get('longitude'),
                location.get('altitude'),
                camera_info.get('manufacturer'),
                camera_info.get('model'),
                camera_info.get('date_time'),
                camera_info.get('exposure_time'),
                camera_info.get('f_number'),
                camera_info.get('iso'),
                camera_info.get('focal_length'),
                metadata.get('preview_base64') is not None,
                json.dumps(metadata.get('exif_data', {}), default=str),
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
        
        print(f"Данные сохранены в базу данных {output_file}")
    
    def process_and_save(self, 
                        directories: List[str], 
                        output_format: str = 'excel',
                        output_file: str = None,
                        recursive: bool = True):
        """
        Основной метод обработки и сохранения
        
        Args:
            directories: список каталогов
            output_format: формат вывода ('excel' или 'sqlite')
            output_file: путь к выходному файлу
            recursive: рекурсивный поиск
        """
        # Обрабатываем каталоги
        metadata_list = self.process_directories(directories, recursive)
        
        if not metadata_list:
            print("Не найдено изображений для обработки")
            return
        
        print(f"Обработано {len(metadata_list)} изображений")
        
        # Определяем имя выходного файла
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if output_format == 'excel':
                output_file = f"image_metadata_{timestamp}.xlsx"
            else:
                output_file = f"image_metadata_{timestamp}.db"
        
        # Сохраняем в выбранном формате
        if output_format.lower() == 'excel':
            self.save_to_excel(metadata_list, output_file)
        elif output_format.lower() in ['sqlite', 'db', 'database']:
            self.save_to_sqlite(metadata_list, output_file)
        else:
            raise ValueError(f"Неподдерживаемый формат: {output_format}")
        
        return metadata_list