import sys
from pathlib import Path
import pandas as pd
import numpy as np
# Добавляем общий каталог в sys.path
common_lib_path = Path(__file__).resolve().parents[1] / 'common_lib'
sys.path.append(str(common_lib_path))
from utils import fill_nan_with_previous
# from data_helpers import data_cleaner

columns_rename = ['Treat_N', 'Num_in', 'Ex_ph_1','Ex_ph_1','w_in','w_sum','w_av']
def read_sheet01(
    file_path,
    sheet_name=0,
    header=True
):
    """
    Читает Excel файл sheet1 и возвращает датафрейм 

    :param file_path: str - путь к Excel файлу
    :param sheet_name: str/int - имя или индекс листа (по умолчанию 0)
    
    :param header: bool - использовать первую строку как заголовок (по умолчанию True)
    :return: pd.DataFrame - датафрейм с данными из Excel sheet1

    """
    xls = pd.ExcelFile(file_path)
    # print(f"Доступные листы: {xls.sheet_names}")
    # data = pd.DataFrame()
    data = pd.read_excel(xls, sheet_name=sheet_name)
    # print(data.head())
    print(f"data is {type(data)}")
    print(data.columns)
    return data

def count_transitions_with_tracking(df: pd.DataFrame, column_index: int, output_column: int) -> pd.DataFrame:
    """
    Подсчитывает переходы на основе разности целых частей значений столбца.
    Инкрементирует счётчик, если предыдущее значение минус текущее меньше 0,
    и записывает результат в другой столбец. Начинает с 1 для первой строки.

    :param df: Входной DataFrame
    :param column: Название столбца с данными
    :param output_column: Название столбца для записи счетчика
    :return: DataFrame с дополнительным столбцом счётчика
    """
    counter = 1
    previous_value = None
    result = []
    df.iloc[:, output_column] = [0] * len(df)
    
    for i, value in enumerate(df.iloc[:, column_index]):
        try:
            # int_value = int(float(value))  # Преобразуем строку в число, отбрасываем дробную часть
            value1 = float(value)
        except ValueError:
            int_value = 0  # Если преобразование невозможно, устанавливаем 0
        if i == 0:
            result.append(counter)
        else:
            if (value1 - previous_value) < 0:
                counter += 1
            result.append(counter)
        previous_value = value1
    
    df.iloc[:, output_column] = result
    return df
    # return result

pd.set_option('display.max_rows', None)  # Показать все строки
pd.set_option('display.max_columns', 5)  # Показать все столбцы (4)


file_path = r"G:\My\sov\extract\weights.xlsx"
sheet_name = "Sheet1"
df = read_sheet01(file_path)
ind_fill = [1,2,3]
df = fill_nan_with_previous(df, ind_fill)

df1 = count_transitions_with_tracking(df, 1, 0)
# print(f"data = {df1}")
print(f"data = {df.iloc[:, [2,3]]}")
