import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from openpyxl import load_workbook
import tempfile
import os
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.regression.mixed_linear_model import MixedLM

def create_phase_col(df):
    df['Phase'] = 1 
import pandas as pd

def add_phase_column(df):
    """
    Добавляет столбец 'Phase' в датафрейм и заполняет его:
    - Значение 1 для всех строк.
    - Значение 0 для строк, где Method равен '15' или '16'.
    
    Args:
        df (pd.DataFrame): Исходный датафрейм, в котором есть столбец 'Method'.

    Returns:
        pd.DataFrame: Датафрейм с добавленным столбцом 'Phase'.
    """
    # Добавляем столбец Phase со значением 1 по умолчанию
    df['Phase'] = 1
    
    # Присваиваем значение 0 для Method == 15 или Method == 16
    df.loc[df['Method'].isin(['method_15', 'method_16']), 'Phase'] = 0
    
    return df

# file = r"G:\My\sov\extract\FL for permuations.xlsx"    # FL - data for LR 
file_path1 = r"G:\My\sov\extract\Weight tables_my.xlsx" # column PHS 
file = r"G:\My\sov\extract\Al for permuations.xlsx" # A - alginate data
# file_path2 = r"G:\My\sov\extract\Carb Al mg per g.xlsx" # A - alginate data

#
# df_phs = pd.read_excel(file_path1)
# columns_to_delete = [0, 1, 2]
# df_phs.drop(df_phs.columns[columns_to_delete], axis=1, inplace=True)
# new_col = ['EM','PHS','Solv_1','Solv_2','FL','A','R','Total']
# df_phs.columns = new_col
# file = r"G:\My\sov\extract\FL for permuations.xlsx"    # FL - data for LR 
# file = r"G:\My\sov\extract\FL for mixed effect regression.xlsx"
output_dir = os.path.join(os.path.dirname(__file__), 'Data')

# def prepare_fucoidan(input_file):
sheet_name = 0          #"Sheet1"
xls = pd.ExcelFile(file)
# Проверка на существование листа
if isinstance(sheet_name, int):
    if sheet_name >= len(xls.sheet_names):
        raise ValueError("Лист с указанным индексом не существует.")
    sheet_name = xls.sheet_names[sheet_name]
else:
    if sheet_name not in xls.sheet_names:
        raise ValueError(f"Лист с именем '{sheet_name}' не найден. Доступные листы: {xls.sheet_names}")

df = xls.parse(sheet_name="Sheet1")
df = df.drop(columns='Combined Yield')

# Пример DataFrame
# df = pd.DataFrame({'Extraction techniique 1,2,3…16': [1, 2, 3, 4]})

# Переписываем в Python
df = (
    df.rename(columns={df.columns.values[0]: 'Method'})  # Переименование столбца
    .assign(Method=lambda x: 'method_' + x['Method'].astype(str))  # Добавляем префикс method_
)
# df = add_phase_column(df)
df['Extraction Technique'] = df['Extraction Technique'].str[0]  # first letter W or P or M
# Преобразование столбцов в категориальный тип
df = df.assign(
    Method=df['Method'].astype('category'),
    Solvent_Type=df['Solvent'].astype('category'),
    Extraction_Technique=df['Extraction Technique'].astype('category')
)

# Реализация эквивалента
df1 = (
    df.drop(columns=['Replicate Number'])  # Удаляем старый столбец
        .groupby('Method', group_keys=False)  # Группировка по 'Method'
        .apply(lambda group: group.assign(Replicate=pd.Categorical(group.reset_index().index + 1)))  # Создаем новый столбец 'Replicate'
)
# print(df)
# print(df1)
# Определяем столбцы, которые нужно оставить без изменений
# print(df1.columns)
id_vars = ['Method', 'Solvent_Type', 'Extraction_Technique', 'Replicate']
# Определяем только те столбцы, которые нужно трансформировать
value_vars = [col for col in df1.columns if col.startswith('Measurement')]

dataTall = pd.melt(
    df1,
    id_vars=id_vars,  # Оставляем эти столбцы как есть
    value_vars=value_vars,  # Преобразуем только Measurement 1, 2, 3
    var_name='Measurement',  # Название столбца для имен измерений
    value_name='carbs/mg'    # Название столбца для значений
)
# return df1

import os

def determine_substance(file_path):
  """
  Определяет тип вещества по имени файла, игнорируя регистр.

  Args:
    file_path: Путь к файлу.

  Returns:
    str: Строка "Alginate" или "Fucoidan" в зависимости от наличия подстроки в имени файла,
         иначе возвращает None.
  """

  filename = os.path.basename(file_path).lower()  # Приводим имя файла к нижнему регистру
  if "al" in filename:
    return "Alginate"
  elif "fl" in filename:
    return "Fucoidan"
  else:
    return None

def prepare_alginate(input_file, df_fuc):
    data_cleaned = pd.read_excel(input_file).rename(columns={
    'Extraction method': 'Method',
    'mg of carbohydrates in 1 g of extract': 'Rep1',
    'Unnamed: 2': 'Rep2',
    'Unnamed: 3': 'Rep3',
    'Average mg of carbohydrates in 1 g of extract': 'Average'
    })


# Пример DataFrame
# df = pd.DataFrame({'Extraction techniique 1,2,3…16': [1, 2, 3, 4]})

# Переписываем в Python
    df = (
        df.rename(columns={df.columns.values[0]: 'Method'})  # Переименование столбца
        .assign(Method=lambda x: 'method_' + x['Method'].astype(str))  # Добавляем префикс method_
    )
# df = add_phase_column(df)
    df['Extraction Technique'] = df['Extraction Technique'].str[0]  # first letter W or P or M
    # Преобразование столбцов в категориальный тип
    df = df.assign(
        Method=df['Method'].astype('category'),
        Solvent_Type=df['Solvent'].astype('category'),
        Extraction_Technique=df['Extraction Technique'].astype('category')
    )

# Реализация эквивалента
    df1 = (
        df.drop(columns=['Replicate Number'])  # Удаляем старый столбец
            .groupby('Method', group_keys=False)  # Группировка по 'Method'
            .apply(lambda group: group.assign(Replicate=pd.Categorical(group.reset_index().index + 1)))  # Создаем новый столбец 'Replicate'
    )
# print(df)
# print(df1)
# Определяем столбцы, которые нужно оставить без изменений
# print(df1.columns)
    id_vars = ['Method', 'Solvent_Type', 'Extraction_Technique', 'Replicate']
    # Определяем только те столбцы, которые нужно трансформировать
    value_vars = [col for col in df1.columns if col.startswith('Measurement')]

    dataTall = pd.melt(
        df1,
        id_vars=id_vars,  # Оставляем эти столбцы как есть
        value_vars=value_vars,  # Преобразуем только Measurement 1, 2, 3
        var_name='Measurement',  # Название столбца для имен измерений
        value_name='carbs/mg'    # Название столбца для значений
    )
    return df1



# print(dataTall)
agent = determine_substance(file)
output_file = os.path.join(output_dir, f"test_{agent[0].upper()}.xlsx")
# dataTall = prepare_fucoidan(file)
dataTall.to_excel(output_file)



def plot_gr(dataTall,output_dir):
        # Шаг 1: Обработка данных (эквивалент R кода)
    dataTall['Method'] = dataTall['Method'].str.replace('method_', '').astype(int)  # Убираем префикс и преобразуем в числа
    dataTall = dataTall.sort_values('Method')  # Сортируем по 'Method'
    method_order = sorted(dataTall['Method'].unique())  
    dataTall['Method'] = dataTall['Method'].astype('category')  # Преобразуем обратно в категориальный тип
    # Добавляем 2 категории для более детальной визуализации
    # Extraction_Technique  = [W, P, M]; цвет тела боксплота  W - голубой, P - бирюзовый, M - что то желтоватое
    dataTall['Extraction_Technique'] = dataTall['Extraction_Technique'].astype('category')  # Преобразуем обратно в категориальный тип
    # Solvent_Type  = [Water, Acid];  цвет обрамления тела боксплота ( ободок) Water - темно синий, Acid - оранжевый
    dataTall['Solvent_Type'] = dataTall['Solvent_Type'].astype('category')  # Преобразуем обратно в категориальный тип
    # 
    # Когда мы развернули данные в длинный формат из короткого у нас появилось по 9 точек для каждого боксплота
    # Для отрисовки необходимо вернуться в исходное состояние ( широкого формата) и показать по 3 точки в 
    # каждом боксплоте ( а не 9 как сейчас) условием сворачивания может быть например такое
    #  Avarage ( Replicate = r AND Method = m  ) 
    #  или словами - среднее по трем репликейтам для каждого метода заменяет три точки длинного формата на одно 
    # среднее значение для каждого метода. 
    # dataTall = dataTall.groupby(['Method', 'Extraction_Technique', 'Solvent_Type'], as_index=False)['carbs/mg'].mean()
    # Агрегирование данных: среднее значение по трем репликейтам
    dataTall = dataTall.groupby(['Method', 'Extraction_Technique', 'Solvent_Type', 'Replicate'], as_index=False)['carbs/mg'].mean()
    # dataTall = dataTall.groupby(['Method', 'Extraction_Technique', 'Solvent_Type'], as_index=False)['carbs/mg'].mean()
    # Цветовые схемы
    extraction_palette = {'W': 'deepskyblue', 'P': 'turquoise', 'M': 'gold'}
    solvent_palette = {'Water': 'darkblue', 'Acid': 'orange'}
    
    def get_border_color(method):
        return 'darkblue' if method % 2 == 0 else 'orange'
    # Шаг 2: Построение графика
    plt.figure(figsize=(12, 10))
    ax = sns.boxplot(
        data=dataTall,
        x='Method',
        y='carbs/mg',
        hue='Extraction_Technique',
        # palette='Dark2',  # Цветовая палитра для категорий
        palette= extraction_palette,  # Цветовая палитра для категорий
        dodge=True  # Раздвигаем боксплоты для разных групп
    )

    for i, artist in enumerate(ax.patches):
        # Определение цвета обрамления
        method = method_order[i % len(method_order)]
        edge_color = get_border_color(method)
        # solvent = dataTall['Solvent_Type'].iloc[i % len(dataTall)]
        edge_color = get_border_color(method)
        # edge_color = solvent_palette[solvent]
        artist.set_edgecolor(edge_color)
        artist.set_linewidth(2)
   
    sns.stripplot(
        data=dataTall,
        x='Method',
        y='carbs/mg',
        # hue='Solvent_Type',  # Используем тот же hue
        hue='Extraction_Technique',  # Должно совпадать с boxplot для сохранения порядка
        order=method_order,  # Совпадение порядка категорий
        # palette= solvent_palette,
        palette= extraction_palette,        
        dodge=True,  # Должно совпадать с боксплотом
        # jitter=0.2,  # Умеренный джиттер, чтобы не улетали далеко
        jitter=False,   # Отключаем случайное рассеивание
        marker='o',
        linewidth=1.5,
        edgecolor='black', 
        alpha=0.9
    )

    # Шаг 3: Настройка оформления
    font = {'family': 'Times New Roman','size': 14}
    plt.title('Differences in carbs/mg between Methods (Alginate)',fontdict=font)
    # plt.xlabel('Extraction method', fontsize=12)
    # plt.ylabel('Carbohydrates/mg', fontsize=12)
    font['size'] = 12
    plt.xlabel('Extraction Method', fontdict=font)
    plt.ylabel('Carbohydrate Content, mg/g of extract', fontdict=font)
    plt.legend(title='Legend', bbox_to_anchor=(1.05, 1), loc='upper left', prop=font)
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Шаг 4: Отображение графика
    # output_path = os.path.join(output_dir, f'Differences in carbs_mg between Methods.pdf')
    output_path = os.path.join(output_dir, f'Differences in carbs_mg between Methods_Alginate.svg')
    # plt.savefig(output_path,  format="pdf", dpi=300, bbox_inches='tight') 
    plt.savefig(output_path,  format="svg", dpi=300, bbox_inches='tight') 

    plt.show()
    plt.close()

# import statsmodels.graphics.interaction_plot as ip
# def f_out(outfile):
#     current_date = datetime.now().strftime("%d_%m")
#     output_dir = os.path.join(os.path.dirname(__file__), 'Data')
#     output_file = os.path.join(output_dir, f"{outfile}_{current_date}.txt")
#     return output_file
def f_out(outfile):
    """
    Формирует путь для файла в подкаталоге 'Data' текущего каталога,
    добавляя текущую дату к имени файла перед расширением.
    
    Parameters:
        outfile (str): Имя исходного файла (например, "output.pdf").
    
    Returns:
        str: Полный путь к файлу в формате "Data/<имя>_<дата>.<расширение>".
    """
    # Получаем текущую дату
    current_date = datetime.now().strftime("%d_%m")
    
    # Создаем директорию Data, если ее нет
    # Определяем рабочую директорию (используем os.getcwd() вместо __file__)
    # output_dir = os.path.join(os.getcwd(), 'Data')
    output_dir = os.path.join(os.path.dirname(__file__), 'Data')
    os.makedirs(output_dir, exist_ok=True)
    
    # Разделяем имя файла и расширение
    base_name, ext = os.path.splitext(outfile)
    
    # Формируем новое имя файла с добавлением даты
    output_file = os.path.join(output_dir, f"{base_name}_{current_date}{ext}")
    
    return output_file
# ip.interaction_plot(
#     dataTall['Method'],
#     dataTall['Solvent_Type'],
#     dataTall['carbs/mg'],
#     colors=['red', 'blue']
# )
def lin_r(dataTall):
    import statsmodels.api as sm
    from statsmodels.formula.api import ols

    # Регрессионная модель
    formula = 'Q("carbs/mg") ~ C(Method) + C(Solvent_Type) + C(Extraction_Technique)'
    model = ols(formula, data=dataTall).fit()
    # print(model.summary())
    return(model.summary())
res_lin_r = lin_r(dataTall)

# print( res_lin_r)
with open(f_out("res_lin_r.txt"), "w") as file:
    # Перенаправляем вывод в файл
    print(res_lin_r, file=file)
plot_gr(dataTall,output_dir)
formula = 'Q("carbs/mg") ~ C(Solvent_Type) + C(Extraction_Technique)'

# Подготовка данных (аналог rename и mutate)
# dataReg = dataTall.rename(
#     columns={'Solvent_Type': 'Solvent', 
#              'Extraction_Technique': 'Extraction', 
#              'carbs/mg': 'Concentration'}
# )
# dataReg['Measurement'] = dataReg['Measurement'].astype('category')
dataTall['Measurement'] = dataTall['Measurement'].astype('category')

# Создание смешанной модели
# formula = 'Concentration ~ C(Solvent) + C(Extraction) + C(Method)'
mixed_model = MixedLM.from_formula(
    formula,
    groups=dataTall['Replicate'],  # Случайный эффект для Replicate
    data=dataTall
)
# Подгонка модели
result = mixed_model.fit()

# Подгоняем модель с случайным эффектом по Replicate
# mixed_model = MixedLM.from_formula(formula, groups=dataTall['Replicate'], data=dataTall)
# mixed_result = mixed_model.fit()

# Вывод результатов
print(result.summary())
with open(f_out("mix_lin_r.txt"), "w") as file:
    # Перенаправляем вывод в файл
    print(result.summary(), file=file)
