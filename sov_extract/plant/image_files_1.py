import os
import xlsxwriter
import fnmatch
from PIL import Image  # Импортируем Pillow для работы с изображениями


def list_files_to_excel(folder_path, file_pattern="*", excel_file_name="file_list.xlsx"):
    """
    Функция создает Excel-файл со списком имен файлов (без расширения), их размерами и размерами изображений.
    
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
    headers = ["File Name", "File Size (MB)", "Width (px)", "Height (px)", "Scale pix/mm"]
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)
    
    # Получаем список файлов в каталоге, соответствующих шаблону
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and fnmatch.fnmatch(f, file_pattern)]
    
    # Записываем имена файлов (без расширения), их размеры и размеры изображений в Excel
    for row_num, file_name in enumerate(files, start=1):
        # Полный путь к файлу
        file_path = os.path.join(folder_path, file_name)
        
        # Убираем расширение файла
        file_name_without_ext = os.path.splitext(file_name)[0]
        
        # Получаем размер файла в байтах и конвертируем в мегабайты
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)  # Конвертация в MB
        
        # Получаем размеры изображения (ширину и высоту)
        try:
            with Image.open(file_path) as img:
                width, height = img.size  # Получаем ширину и высоту
        except Exception as e:
            print(f"Ошибка при обработке файла {file_name}: {e}")
            width, height = "N/A", "N/A"  # Если файл не является изображением
        
        # Записываем данные в Excel
        worksheet.write(row_num, 0, file_name_without_ext)  # Имя файла
        worksheet.write(row_num, 1, round(file_size_mb, 2)) # Размер файла в MB с округлением до 2 знаков
        worksheet.write(row_num, 2, width)                 # Ширина изображения
        worksheet.write(row_num, 3, height)                # Высота изображения
    
    # Автоматически подгоняем ширину столбцов
    worksheet.autofit()
    
    # Закрываем Excel-файл
    workbook.close()
    
    print(f"Excel-файл создан: {excel_file_path}")

if __name__ == "__main__":
# Укажите путь к каталогу с файлами
    folder_path = r"G:\My\sov\extract\plant_d7"


# Укажите шаблон для выбора файлов (например, "*.jpg")  
    file_pattern = "*.jpg"

# Вызов функции
    list_files_to_excel(folder_path, file_pattern=file_pattern)