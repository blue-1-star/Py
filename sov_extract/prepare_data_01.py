import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    def find_header_row(file_path, sheet_name):
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        for i, row in df.iterrows():
            if all(isinstance(x, str) for x in row):  # Все значения строки текстовые
                return i
        return 0  # Если не нашли, используем 0 строку по умолчанию

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
    header_row = find_header_row(file_path, sheet_name)
    # print(f"Header row detected: {header_row}")
    data = pd.read_excel(xls, sheet_name=sheet_name, header=header_row)
    # print(data.head())
    # print(f"data is {type(data)}")
    # if isinstance(data, pd.DataFrame):
    #     print("Это DataFrame")
    # else:
    #     print("Это не DataFrame")
    header_row = 0 if header else None


    # data = pd.read_excel(xls, sheet_name=sheet_name, header=header_row) 
    # print(f"header : {header}, header_row : {header_row} ")
    # print(f"Columns in data: {len(data.columns)}, col_numbers: {col_numbers}")

 # Если столбцы указаны буквами, преобразуем их в реальные имена
    # if col_numbers and isinstance(col_numbers[0], str):
    #     col_numbers = excel_columns_to_names(data, col_numbers)
     # Проверка и удаление столбцов
    if col_numbers:
        print('col_numbers ------>')
        # Если col_numbers - индексы, преобразуем в имена
        if isinstance(col_numbers[0], int):
            print('col_numbers ------>')
            col_numbers = [data.columns[i] for i in col_numbers if i < len(data.columns)]
            print(col_numbers)
        # Удаляем столбцы
        # df = drop_columns(df, col_numbers)
            return drop_columns(data, col_numbers)
    df = drop_columns(data, col_numbers)
    return df
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
def select_columns_by_index(df: pd.DataFrame, column_indices: list) -> pd.DataFrame:
    """
    Выбирает столбцы DataFrame по номерам индексов.

    :param df: Входной DataFrame
    :param column_indices: Список номеров столбцов для выбора
    :return: Новый DataFrame с указанными столбцами
    """
    try:
        # Проверка, что индексы в пределах допустимого диапазона
        max_index = df.shape[1] - 1
        if any(i > max_index or i < 0 for i in column_indices):
            raise ValueError("Один или несколько индексов выходят за пределы допустимого диапазона.")
        
        # Выбираем столбцы по индексам
        selected_df = df.iloc[:, column_indices]
        return selected_df
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return pd.DataFrame()  # Возвращает пустой DataFrame в случае ошибки
    
def fill_nan_with_previous(df: pd.DataFrame, column_index: int) -> pd.DataFrame:
    """
    Заполняет значения NaN в указанном столбце значением из предыдущей строки.

    :param df: Входной DataFrame
    :param column_index: Номер столбца для обработки
    :return: DataFrame с заменёнными NaN
    """
    try:
        max_index = df.shape[1] - 1
        if column_index > max_index or column_index < 0:
            raise ValueError("Номер столбца выходит за пределы допустимого диапазона.")
        
        df.iloc[:, column_index] = df.iloc[:, column_index].ffill()
        return df
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return df

def plot_all_ingredients(stats):
    stats_sorted = stats.sort_values(by='All_ingredients')
    plt.figure(figsize=(8, 6))
    plt.bar(stats_sorted['Treat_N'], stats_sorted['All_ingredients'], color='skyblue')
    plt.xlabel('Treat_N')
    plt.ylabel('All_ingredients')
    plt.title('All_ingredients by Treat_N')
    plt.xticks(stats_sorted['Treat_N'], rotation=45)
    plt.show()

# Функция для построения сложенной столбчатой диаграммы
# def plot_all_ingredien_stack(stats, df):

def plot_all_ingredien_stack(stats):
    stats_sorted = stats.sort_values(by='All_ingredients')
    
    # Построение сложенной диаграммы
    plt.figure(figsize=(10, 7))
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#c2c2f0']  # цвета для компонентов
    bright_colors = ['#ff4d4d', '#3385ff']  # яркие цвета для Fuc_Lam и Alg

    plt.bar(stats_sorted['Treat_N'], stats_sorted['Residue_mean'], color=colors[2], label='Residue')
    # plt.bar(stats_sorted['Treat_N'], stats_sorted['Solids_mean'], bottom=stats_sorted['Residue_mean'], color=colors[3], label='Solids')
    # plt.bar(stats_sorted['Treat_N'], stats_sorted['Alg_mean'], bottom=stats_sorted['Residue_mean'] + stats_sorted['Solids_mean'], color=bright_colors[1], label='Alg')
    plt.bar(stats_sorted['Treat_N'], stats_sorted['Alg_mean'], bottom=stats_sorted['Residue_mean'], color=bright_colors[1], label='Alg')
    plt.bar(stats_sorted['Treat_N'], stats_sorted['Fuc_Lam_mean'], bottom=stats_sorted['Residue_mean'] +  stats_sorted['Alg_mean'], color=bright_colors[0], label='Fuc_Lam')

    plt.xlabel('Treat_N')
    plt.ylabel('All_ingredients')
    plt.title('All_ingredients by Treat_N (Stacked)')
    plt.xticks(stats_sorted['Treat_N'], rotation=45)
    plt.legend()
    # plt.savefig('./Data/stacked_bar_chart.pdf')
    plt.savefig(Path(__file__).parent /'Data'/'stacked_bar_chart.pdf')
    plt.show()
    
    # Построение тетрад
    plt.figure(figsize=(10, 7))
    bar_width = 0.3
    index = range(len(stats_sorted['Treat_N']))

    plt.bar([i - 1.5 * bar_width for i in index], stats_sorted['Fuc_Lam_mean'], bar_width, color=bright_colors[0], label='Fuc_Lam')
    plt.bar([i - 0.5 * bar_width for i in index], stats_sorted['Alg_mean'], bar_width, color=bright_colors[1], label='Alg')
    plt.bar([i + 0.5 * bar_width for i in index], stats_sorted['Residue_mean'], bar_width, color=colors[2], label='Residue')
    # plt.bar([i - 2.5 * bar_width for i in index], stats_sorted['Fuc_Lam_mean'], bar_width, color=bright_colors[0], label='Fuc_Lam')
    # plt.bar([i - 0.5 * bar_width for i in index], stats_sorted['Alg_mean'], bar_width, color=bright_colors[1], label='Alg')
    # plt.bar([i + 1.5 * bar_width for i in index], stats_sorted['Residue_mean'], bar_width, color=colors[2], label='Residue')
    # plt.bar([i + 1.5 * bar_width for i in index], stats_sorted['Solids_mean'], bar_width, color=colors[3], label='Solids')

    plt.xlabel('Treat_N')
    plt.ylabel('Ingredient Levels')
    plt.title('Ingredient Levels by Treat_N (Grouped)')
    plt.xticks(index, stats_sorted['Treat_N'], rotation=45)
    plt.legend()
    # plt.savefig('./Data/grouped_bar_chart.pdf')
    plt.savefig(Path(__file__).parent /'Data'/'grouped_bar_chart.pdf')
    plt.show()



file_path = r"G:\My\sov\extract\weights_1.xlsx"
sheet_name = "Sheet8"
col_numbers = [0,1,4,7,10]
# columns_rename = ['Treat_N','Fuc_Lam', 'Alg', 'Residue','Solids']
columns_rename = ['Treat_N','Fuc_Lam', 'Alg', 'Residue']
columns_to_remove = [2,3,5,6,8,9,11,12]
# col_numbers = [0,3,6,9]
# col_numbers = ['0','3','6','9']
# col_numbers = ['B','E','H','K']
# col_numbers = ['F and L average','F and L st dev','alg average','alg st dev']

# df = read_excel_custom(file_path,sheet_name,col_numbers, header=False)
# df = read_excel_custom(file_path,sheet_name, col_numbers)
df = read_excel_custom(file_path,sheet_name, col_numbers)
# print(df.columns)
# df = df.drop(df.columns[columns_to_remove], axis=1)
# df = drop_columns(df, col_numbers)
# print(df)
# sdf = select_columns_by_index(df, col_numbers)
# print(sdf)
filled_df = fill_nan_with_previous(df, 0)
filled_df.columns = columns_rename
df = filled_df
# print(df)

# df = pd.DataFrame(data)

# Группировка по Treat_N и вычисление статистик
stats = df.groupby('Treat_N').agg(['mean', 'std'])

# Удаление мультииндекса для удобства
stats.columns = ['_'.join(col) for col in stats.columns]

# Суммирование средних значений по столбцам
stats['All_ingredients'] = stats.filter(like='_mean').sum(axis=1)
stats.reset_index(inplace=True)  # Сброс индекса и превращение Treat_N в столбец
# df = df.merge(stats[['Treat_N', 'All_ingredients']], on='Treat_N', how='left')

# df['All_ingredients'] = stats['All_ingredients']
print(stats)  # Вывод результата
plot_all_ingredients(stats)
plot_all_ingredien_stack(stats)
# print(df)


