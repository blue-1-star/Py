import pandas as pd
import numpy as np

def read_excel_column(file_path, sheet_name, column_name_or_index, return_as="numpy"):
    """
    Читает указанный столбец из Excel-файла, преобразуя проценты в числа.

    Параметры:
    ----------
    file_path : str
        Путь к Excel-файлу.
    sheet_name : str
        Название листа в файле.
    column_name_or_index : str or int
        Имя столбца (например, "A" или "Revenue") или его индекс (начиная с 0).
    return_as : str, optional (default="numpy")
        Формат возвращаемых данных: "numpy" (массив) или "list" (список).

    Возвращает:
    -----------
    np.ndarray или list
        Числовые значения из столбца (проценты преобразованы в дроби).
    """
    # Загрузка данных из Excel
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Выбор столбца по имени или индексу
    if isinstance(column_name_or_index, int):
        column_data = df.iloc[:, column_name_or_index]
    else:
        column_data = df[column_name_or_index]
    
    # Преобразование процентов в числа (если данные в строковом формате)
    def convert_percentage(x):
        if isinstance(x, str) and x.endswith('%'):
            return float(x.strip('%')) / 100
        return x
    
    column_data = column_data.apply(convert_percentage)
    
    # Конвертация в выбранный формат
    if return_as == "numpy":
        return column_data.to_numpy(dtype=float)
    elif return_as == "list":
        return column_data.tolist()
    else:
        raise ValueError('Недопустимый формат. Используйте "numpy" или "list".')

# Пример вызова функции
# file_path = "data.xlsx"
file_path =r"G:\My\sov\extract\plant_tmp\Green_area_compare_an_Ug01.xlsx"
sheet_name = "Sheet1"
# column_data = read_excel_column(file_path, sheet_name, "B", return_as="numpy")
column_data = read_excel_column(file_path, sheet_name,4, return_as="numpy")
# print(column_data)  WPP_Fiji
c5 = read_excel_column(file_path, sheet_name,5, return_as="numpy")
c5n = read_excel_column(file_path, sheet_name,"WPP_Fiji", return_as="numpy")
c6 = read_excel_column(file_path, sheet_name,6, return_as="numpy")
c7 = read_excel_column(file_path, sheet_name,7, return_as="numpy")
print(column_data)
print(c5)
print(c5n)
# print(c6)
# print(c7)

# Вывод: [0.1  0.2  0.5  0.75] (numpy-массив)
