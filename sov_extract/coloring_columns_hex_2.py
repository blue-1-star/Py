import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from datetime import datetime, timedelta
import os

def insert_empty_columns(df, columns_list):
    """
    Вставляет пустой столбец после каждого столбца из списка columns_list в датафрейм df.

    :param df: pd.DataFrame, исходный датафрейм
    :param columns_list: list, список имен столбцов, после которых нужно вставить пустые столбцы
    :return: pd.DataFrame, новый датафрейм с добавленными пустыми столбцами
    """
    df = df.copy()  # Создаем копию датафрейма, чтобы избежать изменений оригинала
    
    for col in columns_list:
        if col in df.columns:
            empty_col_name = f"{col}_empty"
            col_index = df.columns.get_loc(col) + 1  # Индекс столбца, после которого добавляем пустой
            df.insert(col_index, empty_col_name, None)  # Вставляем пустой столбец

    return df




columns_with_hex = ['avg_color_circle', 'avg_color_square']
current_date = datetime.now().strftime("%d_%m")
yesterday_date = datetime.now() - timedelta(days=1)
prev_d = yesterday_date.strftime("%d_%m")
output_dir = os.path.join(os.path.dirname(__file__), 'Data')
# input_file = os.path.join(output_dir, f"brightness_analysis_{current_date}.xlsx")
input_file = os.path.join(output_dir, f"brightness_analysis_{prev_d}.xlsx")
# input_file = os.path.join(output_dir, f"brightness_analysis_17_01.xlsx")
output_file = os.path.join(output_dir, f"bright_analysis_{current_date}_color.xlsx")
df = pd.read_excel(input_file)
df = insert_empty_columns(df,columns_with_hex)
df.to_excel(output_file, index = False)
print(f"Файл успешно сохранён: {output_file}")
# add_color_columns_to_excel(
#     input_file=input_file,
#     output_file=output_file,
#     columns_with_hex=columns_with_hex
# )