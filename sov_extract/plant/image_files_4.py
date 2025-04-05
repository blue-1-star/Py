import os
import xlsxwriter
import fnmatch
from PIL import Image  # Импортируем Pillow для работы с изображениями
from PIL.ExifTags import TAGS  # Импортируем TAGS для работы с EXIF

# Словарь с шириной сенсора для популярных камер
sensor_widths = {
    "Galaxy S23": 9.8,  # Ширина сенсора в мм
    "Canon EOS 5D Mark IV": 36.0,  # Полнокадровая камера
    "Nikon D850": 35.9,  # Полнокадровая камера
    # Добавьте другие модели по мере необходимости
}

def get_camera_model(image_path):
    """Извлекает модель камеры из EXIF-данных изображения."""
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "Model":
                        return value.strip() if value else "Неизвестно"
    except (AttributeError, KeyError, IndexError, Exception):
        pass
    return "Неизвестно"

def get_focal_length(image_path):
    """Извлекает фокусное расстояние из EXIF-данных."""
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "FocalLength":
                        return value
    except (AttributeError, KeyError, IndexError, Exception):
        pass
    return "Неизвестно"

def get_sensor_width(camera_model):
    """Возвращает ширину сенсора по модели камеры."""
    return sensor_widths.get(camera_model, "Неизвестно")

def list_files_to_excel(folder_path, file_pattern="*", excel_file_name="file_list.xlsx"):
    """
    Функция создает Excel-файл со списком имен файлов (без расширения), их размерами, размерами изображений,
    моделью камеры, фокусным расстоянием и шириной сенсора.
    
    :param folder_path: Путь к каталогу с файлами.
    :param file_pattern: Шаблон для выбора файлов (например, "*.jpg").
    :param excel_file_name: Имя Excel-файла (по умолчанию "file_list.xlsx").
    """
    # Полный путь к Excel-файлу
    excel_file_path = os.path.join(folder_path, excel_file_name)
    
    # Создаем Excel-файл
    workbook = xlsxwriter.Workbook(excel_file_path)
    worksheet = workbook.add_worksheet()
    
    # Заголовки таблицы
    headers = ["File Name", "File Size (MB)", "Width (px)", "Height (px)", "Scale pix/mm", "Cam", "Focal Length (mm)", "Sensor Width (mm)"]
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)
    
    # Получаем список файлов в каталоге, соответствующих шаблону
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and fnmatch.fnmatch(f, file_pattern)]
    
    # Записываем имена файлов (без расширения), их размеры, размеры изображений, модель камеры, фокусное расстояние и ширину сенсора в Excel
    for row_num, file_name in enumerate(files, start=1):
        # Полный путь к файлу
        file_path = os.path.join(folder_path, file_name)
        
        # Убираем расширение файла
        file_name_without_ext = os.path.splitext(file_name)[0]
        
        # Получаем размер файла в байтах и конвертируем в мегабайты
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)  # Конвертация в MB
        
        # Получаем размеры изображения (ширину и высоту), модель камеры, фокусное расстояние и ширину сенсора
        try:
            with Image.open(file_path) as img:
                width, height = img.size  # Получаем ширину и высоту
                camera_model = get_camera_model(file_path)  # Получаем модель камеры
                focal_length = get_focal_length(file_path)  # Получаем фокусное расстояние
                sensor_width = get_sensor_width(camera_model)  # Получаем ширину сенсора
        except Exception as e:
            print(f"Ошибка при обработке файла {file_name}: {e}")
            width, height = "N/A", "N/A"  # Если файл не является изображением
            camera_model = "N/A"  # Если не удалось извлечь модель камеры
            focal_length = "N/A"  # Если не удалось извлечь фокусное расстояние
            sensor_width = "N/A"  # Если не удалось определить ширину сенсора
        
        # Записываем данные в Excel
        worksheet.write(row_num, 0, file_name_without_ext)  # Имя файла
        worksheet.write(row_num, 1, round(file_size_mb, 2)) # Размер файла в MB с округлением до 2 знаков
        worksheet.write(row_num, 2, width)                 # Ширина изображения
        worksheet.write(row_num, 3, height)                # Высота изображения
        worksheet.write(row_num, 4, "")                    # Пустой столбец для Scale (ручное заполнение)
        worksheet.write(row_num, 5, camera_model)         # Модель камеры
        worksheet.write(row_num, 6, focal_length)         # Фокусное расстояние
        worksheet.write(row_num, 7, sensor_width)         # Ширина сенсора
    
    # Автоматически подгоняем ширину столбцов
    worksheet.autofit()
    
    # Закрываем Excel-файл
    workbook.close()
    
    print(f"Excel-файл создан: {excel_file_path}")

if __name__ == "__main__":
    # Укажите путь к каталогу с файлами
    # folder_path = r"G:\My\sov\extract\plant_d14"
    # folder_path = r"G:\My\sov\extract\plant2"
    # folder_path = r"G:\My\sov\extract\plant_d0"
    # folder_path = r"G:\My\sov\extract\plant_d3"
    # folder_path = r"G:\My\sov\extract\plant_d7"
    # folder_path = r"G:\My\sov\extract\plant_d10"
    # folder_path = r"G:\My\sov\extract\plant_d14"
    # folder_path = r"G:\My\sov\extract\plant_d0a"
    folder_path = r"G:\My\sov\extract\plant_tmp"
        
    # Укажите шаблон для выбора файлов (например, "*.jpg")
    file_pattern = "*.jpg"

    # Вызов функции
    list_files_to_excel(folder_path, file_pattern=file_pattern)
    