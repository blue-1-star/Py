import os
import xlsxwriter
import fnmatch 
def list_files_to_excel(folder_path, file_pattern="*", excel_file_name="file_list.xlsx"):
    """
    Функция создает Excel-файл со списком имен файлов (без расширения) и их размерами из указанного каталога.
    
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
    headers = ["File Name (without extension)", "File Size (MB)"]
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)
    
    # Получаем список файлов в каталоге, соответствующих шаблону
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and fnmatch.fnmatch(f, file_pattern)]
    
    # Записываем имена файлов (без расширения) и их размеры в Excel
    for row_num, file_name in enumerate(files, start=1):
        # Полный путь к файлу
        file_path = os.path.join(folder_path, file_name)
        
        # Убираем расширение файла
        file_name_without_ext = os.path.splitext(file_name)[0]
        
        # Получаем размер файла в байтах и конвертируем в мегабайты
        file_size_bytes = os.path.getsize(file_path)
        file_size_mb = file_size_bytes / (1024 * 1024)  # Конвертация в MB
        
        # Записываем данные в Excel
        worksheet.write(row_num, 0, file_name_without_ext)  # Имя файла
        worksheet.write(row_num, 1, round(file_size_mb, 2)) # Размер файла в MB с округлением до 2 знаков
    
    # Автоматически подгоняем ширину столбцов
    worksheet.autofit()
    
    # Закрываем Excel-файл
    workbook.close()
    
    print(f"Excel-файл создан: {excel_file_path}")

# Пример использования
if __name__ == "__main__":
    # Укажите путь к каталогу с файлами
    folder_path = r"G:\My\sov\extract\plant1"
    
    # Укажите шаблон для выбора файлов (например, "*.jpg")
    file_pattern = "*.jpg"
    
    # Вызов функции
    list_files_to_excel(folder_path, file_pattern=file_pattern)