import pandas as pd
import numpy as np
def read_excel_custom(
    file_path,
    sheet_name=0,
    row_numbers=None,
    col_numbers=None,
    header=True
):
    """
    Читает Excel файл и возвращает датафрейм по указанным номерам строк и столбцов.

    :param file_path: str - путь к Excel файлу
    :param sheet_name: str/int - имя или индекс листа (по умолчанию 0)
    :param row_numbers: list - список строк для чтения (по умолчанию все строки)
    :param col_numbers: list - список столбцов для чтения (по умолчанию все столбцы)
    :param header: bool - использовать первую строку как заголовок (по умолчанию True)
    :return: pd.DataFrame - датафрейм с данными из Excel
    """
    # Читаем Excel файл
    xls = pd.ExcelFile(file_path)
    
    # Проверка на существование листа
    if isinstance(sheet_name, int):
        if sheet_name >= len(xls.sheet_names):
            raise ValueError("Лист с указанным индексом не существует.")
        sheet_name = xls.sheet_names[sheet_name]
    else:
        if sheet_name not in xls.sheet_names:
            raise ValueError(f"Лист с именем '{sheet_name}' не найден. Доступные листы: {xls.sheet_names}")
      
    # Загружаем данные с листа
    header_row = 0 if header else None
    data = pd.read_excel(xls, sheet_name=sheet_name, header=header_row) 

 # Если столбцы указаны буквами, преобразуем их в реальные имена
    # if col_numbers and isinstance(col_numbers[0], str):
    #     col_numbers = excel_columns_to_names(data, col_numbers)
     # Проверка и удаление столбцов
    if col_numbers:
        # Если col_numbers - индексы, преобразуем в имена
        if isinstance(col_numbers[0], int):
            col_numbers = [data.columns[i] for i in col_numbers if i < len(data.columns)]
            print(col_numbers)
        # Удаляем столбцы
        # df = drop_columns(df, col_numbers)
            return drop_columns(data, col_numbers)
    # df = drop_columns(data, col_numbers)
        # return df
def drop_columns(df, col_numbers):
    """
    Удаляет указанные столбцы из датафрейма.

    :param df: pd.DataFrame - исходный датафрейм
    :param columns_to_drop: list - список столбцов для удаления
    :return: pd.DataFrame - датафрейм без указанных столбцов
    """
    if col_numbers is None:
        return df  # Если список столбцов пуст, возвращаем исходный датафрейм
    # Удаляем по именам, если переданы строки
    if isinstance(col_numbers[0], str):
        return df.drop(columns=col_numbers, errors='ignore')
    # Удаляем по индексам, если переданы числа
    elif isinstance(col_numbers[0], int):
        return df.drop(df.columns[col_numbers], axis=1, errors='ignore')
    else:
        raise ValueError("col_numbers должен содержать либо имена столбцов, либо их индексы.")



    # return df.drop(df.columns[col_numbers], axis=1, errors='ignore')
   
    # return df.drop(columns=col_numbers, errors='ignore')

def print_dataframe(df):
    """
    Печатает датафрейм в удобном формате.

    :param df: pd.DataFrame - датафрейм для печати
    """
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)

import string

def excel_columns_to_names(df, col_letters):
    """
    Преобразует буквы столбцов Excel (A, B, C...) в имена столбцов датафрейма.

    :param df: pd.DataFrame - датафрейм с данными
    :param col_letters: list - список буквенных обозначений столбцов (например, ['A', 'D'])
    :return: list - список реальных имен столбцов
    """
    # Создаём маппинг: A -> 0, B -> 1, ...
    letter_to_index = {letter: idx for idx, letter in enumerate(string.ascii_uppercase)}
    
    col_names = []
    for letter in col_letters:
        index = letter_to_index.get(letter)
        if index is not None and index < len(df.columns):
            col_names.append(df.columns[index])
    
    return col_names



file_path = r"G:\My\sov\extract\NEW weights.xlsx"
sheet_name = "Sheet8"
col_numbers = [1,4,7,10]
# col_numbers = [0,3,6,9]
# col_numbers = ['0','3','6','9']
# col_numbers = ['B','E','H','K']
# col_numbers = ['F and L average','F and L st dev','alg average','alg st dev']

# df = read_excel_custom(file_path,sheet_name,col_numbers, header=False)
df = read_excel_custom(file_path,sheet_name, col_numbers)
# print(df.columns)
# df = drop_columns(df, col_numbers)
print(df)
# df0 = pd.DataFrame(np.arange(12).reshape(3, 4),
                #   columns=['A', 'B', 'C', 'D'])
# print(df0)
# df0_d = drop_columns(df0, ['B','C'])
# df0_d = drop_columns(df0, [1,2])
# print(df0_d)

