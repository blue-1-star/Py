import os
import pandas as pd
from pathlib import Path

def extract_number_from_filename(filename):
    """
    Извлекает первое число из имени файла.
    Например, UGAN_02_03_d0.jpg -> 2.
    """
    # Разделяем имя файла по символам "_" и "."
    parts = filename.replace(".", "_").split("_")
    # Ищем первое число в частях имени файла
    for part in parts:
        if part.isdigit():
            return int(part)
    return None

def collect_data_from_excel_files(folder_path, output_file, list_names, list_columns):
    """
    Собирает данные из всех файлов Excel в каталоге и сохраняет их в один файл.
    
    :param folder_path: Путь к каталогу с файлами Excel.
    :param output_file: Имя выходного файла.
    :param list_names: Список чисел для фильтрации.
    :param list_columns: Список столбцов для выбора.
    """
    # Проверяем, существует ли каталог
    if not os.path.exists(folder_path):
        print(f"Каталог {folder_path} не существует.")
        return
    
    # Создаем пустой DataFrame для сбора данных
    combined_data = pd.DataFrame()
    
    # Получаем список всех файлов Excel в каталоге
    excel_files = list(Path(folder_path).glob("*.xlsx"))
    
    # Обрабатываем каждый файл
    for file_path in excel_files:
        print(f"Обрабатывается файл: {file_path.name}")
        
        # Читаем файл Excel
        df = pd.read_excel(file_path)
        
        # Фильтруем строки по первому числу в столбце "File Name"
        df_filtered = df[df["FILE NAME"].apply(lambda x: extract_number_from_filename(x) in list_names)]
        
        # Выбираем только нужные столбцы
        df_filtered = df_filtered[list_columns]
        
        # Добавляем отфильтрованные данные в общий DataFrame
        combined_data = pd.concat([combined_data, df_filtered], ignore_index=True)
    
    # Сохраняем собранные данные в один файл Excel
    output_path = os.path.join(folder_path, output_file)
    combined_data.to_excel(output_path, index=False)
    print(f"Данные сохранены в файл: {output_path}")

# Пример использования
folder_path = r"G:\My\sov\extract\plant\Data"
output_file = "Data_Plant.xlsx"
list_names = [1, 2, 10, 12, 14, 15, 16]
list_columns = ["FILE NAME", "SCALE (pix/mm)", "WHITE PIXEL COUNT", "TOTAL PIXELS", "WHITE PIXEL PERCENTAGE", "WHITE PIXELS MM^2"]

collect_data_from_excel_files(folder_path, output_file, list_names, list_columns)