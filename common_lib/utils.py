import pandas as pd
# def fill_nan_with_previous(df: pd.DataFrame, column_index: int) -> pd.DataFrame:
#     """
#     Заполняет значения NaN в указанном столбце значением из предыдущей строки.

#     :param df: Входной DataFrame
#     :param column_index: Номер столбца для обработки
#     :return: DataFrame с заменёнными NaN
#     """
#     try:
#         max_index = df.shape[1] - 1
#         if column_index > max_index or column_index < 0:
#             raise ValueError("Номер столбца выходит за пределы допустимого диапазона.")
        
#         df.iloc[:, column_index] = df.iloc[:, column_index].ffill()
#         return df
        
#     except Exception as e:
#         print(f"Ошибка: {e}")
#         return df
# import pandas as pd

def fill_nan_with_previous(df: pd.DataFrame, column_indices: list) -> pd.DataFrame:
    """
    Заполняет значения NaN в указанных столбцах значением из предыдущей строки (forward fill).
    
    :param df: Входной DataFrame
    :param column_indices: Список индексов столбцов для обработки
    :return: DataFrame с заполненными NaN
    """
    try:
        max_index = df.shape[1] - 1
        
        # Проверяем, чтобы индексы были в допустимом диапазоне
        invalid_indices = [i for i in column_indices if i > max_index or i < 0]
        if invalid_indices:
            raise ValueError(f"Некоторые индексы ({invalid_indices}) выходят за пределы диапазона.")
        
        # Заполняем NaN для каждого столбца из списка
        for column_index in column_indices:
            df.iloc[:, column_index] = df.iloc[:, column_index].ffill()
        
        return df

    except Exception as e:
        print(f"Ошибка: {e}")
        return df

def f_out(outfile):
    current_date = datetime.now().strftime("%d_%m")
    output_dir = os.path.join(os.path.dirname(__file__), 'Data')
    output_file = os.path.join(output_dir, f"outfile_{current_date}.txt")
    return output_file
