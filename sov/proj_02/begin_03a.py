import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bg_03 import analyze_string

# Загружаем данные
dir_dat = "G:/Programming/Py/sov/proj_02/"
file = "data_02.xlsx"
df = pd.read_excel(dir_dat + file)

# Переименовываем столбцы
df1 = df.rename(columns={'Treatment': 'TR', 'Treatment_code': 'code', 'Day': 'D', 'Fv/Fm': 'TF'})

# Применяем функцию analyze_string
df1[['Source', 'Factor', 'Day']] = pd.DataFrame(df1.apply(lambda row: analyze_string(row['TR']), axis=1).tolist(), index=df1.index)

# Группируем данные по 'code'
grouped = df1.groupby('code')

# Создаем новый DataFrame с сгруппированными данными по 'code'
dfgcode = pd.DataFrame()

# Добавляем столбец 'mean_group_code' средних значений для каждой группы 'code'
dfgcode['mean_group_code'] = grouped['TF'].mean()

# Создаем графики для каждой группы 'code'
for code, data in grouped:
    # fig, ax = plt.subplots(figsize=(8, 6))
    
    # Создаем столбчатую диаграмму для каждой группы
    # ax.bar(data['Source'] + '_' + data['Factor'] + '_' + data['Day'], data['TF'], label=f"Code: {code}", color='skyblue')
    print(data['Source'] + '_' + data['Factor'] + '_' + data['Day'], data['TF'])
    
    # ax.set_xlabel('Source_Factor_Day')
    # ax.set_ylabel('TF')
    # ax.set_title(f'Statistics for Code: {code}')
    # ax.legend()
    
    # plt.tight_layout()
    # plt.show()
