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



# file = r"G:\My\sov\extract\FL for permuations.xlsx"    # FL - data for FL 
file = r"G:\My\sov\extract\Al for permuations.xlsx" # A - alginate data


output_dir = os.path.join(os.path.dirname(__file__), 'Data')


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
    # предусмотреть выдачу в заголовке (Fucoidan or Alginate в зависимлости от обрабатываемого файла)
    output_path = os.path.join(output_dir, f'Differences in carbs_mg between Methods_Alginate.svg')
    # plt.savefig(output_path,  format="pdf", dpi=300, bbox_inches='tight') 
    plt.savefig(output_path,  format="svg", dpi=300, bbox_inches='tight') 

    plt.show()
    plt.close()

    """
    1) необходимо структурировать  данный модуль - выделить функцию, которая примает имя файла 
    и осуществляет обработку данных  по такому же алгоритму
    для другого субстрата ( был фукоидан, нужен альгинат)
    отличие будет только в другом входном файле такой же структуры - полая идентичность 
    структуры  кроме других чисел в столюцах Measurement 1, carbs in 1 mg   ( 2,3)
    2) полученные результаты для разных субстратов необходимо визуализировать 
    путем модернизации функции def plot_gr(dataTall,output_dir):
    теперь каждый боксплот для фукоидана  будет иметь рядом соседний для альгината
    также нужно провести тонкую вертикальную отметку для каждого значения по оси X
    и левее от нее ставить боксплот для фукоидана, правее боксплот для альгината
    3) предусмотреть передачу внутрь plot_gr(dataTall,output_dir):
    параметра с наименованием обрабатываемого субтрата ( можно извлечь из имени файла Al or FL ) чтобы на графиках 
    отобразить подписи для фукоидана и альгината 

    """






