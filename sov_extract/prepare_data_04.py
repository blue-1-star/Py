import pandas as pd
import numpy as np

def calculate_weights(df, total_biomass_mg=4000):
    """
    Рассчитывает веса субстратов в мг на основе процентных данных.

    Параметры:
        df (pd.DataFrame): Исходный датафрейм с колонками FL, A, R.
        total_biomass_mg (float): Общая биомасса в мг (по умолчанию 4000 мг).

    Возвращает:
        pd.DataFrame: Новый датафрейм с колонками FLw, Aw, Rw.
    """
    # Функция для преобразования строки "число ± погрешность" в два числа
    def parse_value_error(s):
        value, error = s.split('±')
        return float(value.strip()), float(error.strip())

    # Применяем функцию к каждой колонке
    df['FL_value'], df['FL_error'] = zip(*df['FL'].apply(parse_value_error))
    df['A_value'], df['A_error'] = zip(*df['A'].apply(parse_value_error))
    df['R_value'], df['R_error'] = zip(*df['R'].apply(parse_value_error))

    # Рассчитываем веса в мг
    df['FLw'] = df['FL_value'] / 100 * total_biomass_mg
    df['FLw_error'] = df['FL_error'] / 100 * total_biomass_mg

    df['Aw'] = df['A_value'] / 100 * total_biomass_mg
    df['Aw_error'] = df['A_error'] / 100 * total_biomass_mg

    df['Rw'] = df['R_value'] / 100 * total_biomass_mg
    df['Rw_error'] = df['R_error'] / 100 * total_biomass_mg

    # Создаём новый датафрейм с результатами
    result_df = df[['FLw', 'FLw_error', 'Aw', 'Aw_error', 'Rw', 'Rw_error']]
    result_df.columns = ['FLw', 'FLw_error', 'Aw', 'Aw_error', 'Rw', 'Rw_error']

    return result_df

# Пример использования
data = {
    'FL': ['5.52 ± 0.57', '8.60 ± 0.53'],
    'A': ['24.024 ± 0.478', '23.713 ± 0.154'],
    'R': ['31.96 ± 0.80', '15.80 ± 0.32']
}

# df = pd.DataFrame(data)
file_path = r"G:\My\sov\extract\Weight tables_my.xlsx"
xls = pd.ExcelFile(file_path)
df = xls.parse(sheet_name="Sheet1")
columns_to_delete = [0, 1, 2]
df.drop(df.columns[columns_to_delete], axis=1, inplace=True)
# print(df)

new_col = ['EM','PHS','Solv_1','Solv_2','FL','A','R','Total']
# df.columns = new_col

result_df = calculate_weights(df)
df['A'], df['FL'], df['R'] = result_df['Aw'], result_df['FLw'], result_df['Rw']
print(df)
# print(result_df)
