import pandas as pd
import os
import xlsxwriter

def replace_substring_in_column(df, col_name, sub1, sub2):
    """
    Заменяет подстроку sub1 на sub2 в указанном столбце DataFrame.
    
    :param df: DataFrame, в котором нужно выполнить замену.
    :param col_name: Имя столбца, в котором выполняется замена.
    :param sub1: Подстрока, которую нужно заменить.
    :param sub2: Подстрока, на которую нужно заменить.
    :return: DataFrame с измененными значениями.
    """
    # Проверяем, существует ли столбец в DataFrame
    if col_name not in df.columns:
        print(f"Столбец {col_name} не найден в DataFrame.")
        return df
    
    # Выполняем замену подстроки
    df[col_name] = df[col_name].astype(str).str.replace(sub1, sub2, regex=False)
    
    return df

# Пример использования


# Заменяем "_d0" на "_new" в столбце "FILE NAME"
# df = replace_substring_in_column(df, "FILE NAME", "_d0", "_new")
folder_path = r"G:\My\sov\extract\plant\Data"
file_name = "Data_Plant.xlsx"
file_path = os.path.join(folder_path, file_name)
df = pd.read_excel(file_path)
df = replace_substring_in_column(df, "FILE NAME", "day", "d")
# worksheet.autofit()
df.to_excel(file_path, index=False)
print(f'File {file_path} created' )
