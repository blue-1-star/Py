import pandas as pd
import numpy as np
import string

def read_excel_custom(
    file_path,
    sheet_name=0,
    row_numbers=None,
    col_numbers=None,
    header=True
):
    """
    Читает Excel файл и возвращает датафрейм по указанным номерам строк и столбцов.
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
    # if col_numbers:
    # Преобразуем все к нижнему регистру и удаляем пробелы
    #     data.columns = data.columns.str.strip().str.lower()
    #     col_numbers = [col.lower() for col in col_numbers]
    
    # print("Столбцы в исходном датафрейме:", data.columns.tolist())
    # print("Удаляемые столбцы:", col_numbers)
    # Удаляем столбцы по индексам или именам
    if col_numbers:
    # Преобразуем все к нижнему регистру и удаляем пробелы
        data.columns = data.columns.str.strip().str.lower()
        col_numbers = [col.lower() for col in col_numbers]
    
        print("Столбцы в исходном датафрейме:", data.columns.tolist())
        print("Удаляемые столбцы:", col_numbers)
        # Удаляем столбцы
        data = drop_columns(data, col_numbers)
    
    return data
    

def drop_columns(df, col_numbers):
    """
    Удаляет указанные столбцы из датафрейма.
    """
    if col_numbers is None:
        return df  # Если список столбцов пуст, возвращаем исходный датафрейм
    
    return df.drop(columns=col_numbers, errors='ignore')


def print_dataframe(df):
    """
    Печатает датафрейм в удобном формате.
    """
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)


file_path = r"G:\My\sov\extract\NEW weights.xlsx"
sheet_name = "Sheet8"
# col_numbers = [1, 4, 7, 10]  # Удаляем по индексам (преобразуются в имена)
col_numbers = ['F and L average', 'F and L st dev', 'alg average','alg st dev']  # Удаляем по индексам (преобразуются в имена)

df = read_excel_custom(file_path, sheet_name, col_numbers)

if df is not None:
    print_dataframe(df.shape)
else:
    print("Датафрейм пуст.")
