import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from bg_03 import transform, analyze_string

# Загружаем данные
dir_dat = "G:/Programming/Py/sov/proj_02/"
file = "data_02.xlsx"
df = pd.read_excel(dir_dat + file)

# Переименовываем столбцы
df1 = df.rename(columns={'Treatment': 'TR', 'Treatment_code': 'code', 'Day': 'D', 'Fv/Fm': 'TF'})
df1['code'] = df1['code'].astype(int)
df1['D'] = df1['D'].astype(int)
df2 = df1.copy()

# Применяем функцию analyze_string
df2[['Source', 'Factor', 'Day']] = pd.DataFrame(df2.apply(lambda row: analyze_string(row['TR']), axis=1).tolist(), index=df2.index)

# Сохраняем результаты
file = r"G:\Programming\R\sov\proj_02\df2_.xlsx"
# df2.to_excel(file)


# Группируем данные по столбцу 'code'
grouped = df2.groupby('code')

# Рассчитываем статистики для каждой группы
for code, group in grouped:
    mean_tf = group['TF'].mean()
    max_tf = group['TF'].max()
    min_tf = group['TF'].min()
    std_tf = group['TF'].std()
    
    statistics['Source'].append(group['Source'].iloc[0])
    statistics['Factor'].append(group['Factor'].iloc[0])
    statistics['Mean'].append(mean_tf)
    statistics['Max'].append(max_tf)
    statistics['Min'].append(min_tf)
    statistics['Std'].append(std_tf)

# Преобразуем статистики в DataFrame
stats_df = pd.DataFrame(statistics)
# Создаем графики для каждой группы 'code'
for code, data in grouped:
    fig, axes = plt.subplots(nrows=1, ncols=len(data['Source'].unique()), figsize=(16, 6), sharey=True)
    
    # Разбиваем данные по уникальным значениям 'Source'
    for i, source in enumerate(data['Source'].unique()):
        ax = axes[i] if len(data['Source'].unique()) > 1 else axes
        source_data = data[data['Source'] == source]
        
        # Создаем подграфик для каждого значения 'Source'
        for factor, factor_data in source_data.groupby('Factor'):
            for day, day_data in factor_data.groupby('Day'):
                ax.plot(day_data['D'], day_data['TF'], label=f"Factor: {factor}, Day: {day}")
        
        ax.set_title(f'Source: {source}')
        ax.set_xlabel('Day')
        ax.set_ylabel('TF')
        ax.legend()

    plt.tight_layout()
    plt.show()

