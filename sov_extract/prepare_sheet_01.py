import sys
from pathlib import Path
import pandas as pd
import numpy as np
# Добавляем общий каталог в sys.path
common_lib_path = Path(__file__).resolve().parents[1] / 'common_lib'
sys.path.append(str(common_lib_path))
from utils import fill_nan_with_previous
# from data_helpers import data_cleaner

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

import pandas as pd

def merge_rows_by_fraction(df):
    # Создаем копию датафрейма, чтобы избежать изменений в оригинале
    df = df.copy()
    
    # Разделяем столбец Num_in на целую и дробную часть
    df[['n', 'i']] = df['Num_in'].astype(str).str.split('.', expand=True)
    
    # Преобразуем столбец n в целочисленный тип
    df['n'] = df['n'].astype(int)
    
    # Если дробная часть отсутствует, присваиваем ей значение 1
    df['i'] = df['i'].replace({None: '1', '0': '1'}).astype(int)
    # Группируем по целой части и суммируем значения w_part
    # summed = df.groupby('n', as_index=False)['w_part'].sum().rename(columns={'w_part': 'w_sum'})
    # # Группируем по целой части и суммируем значения w_part, записываем в w_sum
    # df['w_sum'] = df.groupby('n')['w_part'].transform('sum')
    # Группируем по n и Treat_N и суммируем значения w_part, записываем в w_sum
    # df['w_sum'] = df.groupby(['n', 'Treat_N'])['w_part'].transform('sum')
    # Оставляем только строки с минимальной дробной частью для каждой группы
    # df['i'] = df['i'].fillna(0).astype(int)  # обрабатываем NaN как i1

     # Функция для суммирования с учетом прекращения при невозрастании i
    def cumulative_sum_with_stop(group):
        sum_part = 0
        w_sum = []
        for idx in range(len(group)):
            if idx == 0 or group['i'].iloc[idx] > group['i'].iloc[idx - 1]:
                sum_part += group['w_part'].iloc[idx]
            else:
                sum_part = group['w_part'].iloc[idx]
            w_sum.append(sum_part)
        return w_sum
    
    # Применяем группировку и кумулятивное суммирование
    df['w_sum'] = df.groupby(['n', 'Treat_N'], group_keys=False).apply(
        lambda x: x.assign(w_sum=cumulative_sum_with_stop(x)))['w_sum']

    # Оставляем только строки с минимальной дробной частью для каждой группы
    df = df.loc[df.groupby(['n', 'Treat_N'])['i'].idxmin()]
    
    # Добавляем суммарное значение обратно в датафрейм
    # df = df.merge(summed, on='n', how='left')
    
    # Удаляем вспомогательные столбцы
    df.drop(columns=['n', 'i'], inplace=True)
    
    return df

def replace_text_in_column(df, col_num, strf, strr):
    # Получаем имя столбца по его номеру
    col_name = df.columns[col_num]
    
    # Заменяем strf на strr в указанном столбце
    df[col_name] = df[col_name].str.replace(strf, strr, regex=False)
    
    return df
# ------------------
def replace_text_in_columns(df, col_nums, replace_pairs):
    # Проходим по каждому столбцу и выполняем соответствующие замены
    for col_num, (strf, strr) in zip(col_nums, replace_pairs):
        col_name = df.columns[col_num]
        df[col_name] = df[col_name].str.replace(strf, strr, regex=False)
    
    return df

def replace_text_in_columns_m(df, col_nums, replace_dicts):
    # Проходим по каждому столбцу и выполняем соответствующие замены
    for col_num, replace_dict in zip(col_nums, replace_dicts):
        col_name = df.columns[col_num]
        # replace_dict - это словарь вида {"strf1": "strr1", "strf2": "strr2"}
        for strf, strr in replace_dict.items():
            df[col_name] = df[col_name].str.replace(strf, strr, regex=False)
    
    return df




pd.set_option('display.max_rows', None)  # Показать все строки
pd.set_option('display.max_columns', 5)  # Показать все столбцы (4)


file_path = r"G:\My\sov\extract\weights.xlsx"
sheet_name = "Sheet1"
columns_rename = ['Treat_N', 'Num_in', 'Ex_ph_1','Ex_ph_2','w_part','w_sum','w_av', 'std']
df = read_sheet01(file_path)
ind_fill = [1,2,3]
df = fill_nan_with_previous(df, ind_fill)

df1 = count_transitions_with_tracking(df, 1, 0)

print(f"data = {df1}")
df1.columns = columns_rename
strf, strr  = 'ethanol 80%', 'et_80'
replace_list = [('ethanol 80%', 'et_80'), ('HCl 0.1 M', 'HCl')]
df1 = replace_text_in_columns(df1, [2,3], replace_list)
print(f"data = {df1.iloc[:, [0,2,3,5]]}")
df2 = merge_rows_by_fraction(df1)
print(f"df2 = {df2.iloc[:, [0,2,3,5]]}")

#
#
"""
алгоритм слияния строк ( результаты опыта собраны в нескольких пробирках от 1 до 3 - номера пробирок 
отображены вторым числом (можно считать дробная часть) после точки в столбце 1  (Num_in)  n.i1, n.i2,... )
1. для дробных частей одного и того же целого n столбца 1 (w_part) суммируются значения    n.i1, n.i2, ... 
    сумма заносится в столбец 5 ( w_sum)
    строки со значениями n.i2, ... в столбце 1 (Num_in) удаляются. Из группы n остается только одна строка n.i1  
Проход по всем строкам столбца 1  (w_part)


"""