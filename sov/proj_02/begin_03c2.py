import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from bg_03 import transform, analyze_string

# Ваш существующий код для создания stats_df
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

# Группируем данные по столбцу 'code'
grouped = df2.groupby('code')

# Словарь для хранения статистик
statistics = {'Source': [], 'Factor': [], 'Day': [], 'Mean': [], 'Max': [], 'Min': [], 'Std': []}

# Рассчитываем статистики для каждой группы
for code, group in grouped:
    mean_tf = group['TF'].mean()
    max_tf = group['TF'].max()
    min_tf = group['TF'].min()
    std_tf = group['TF'].std()
    
    statistics['Source'].append(group['Source'].iloc[0])
    statistics['Factor'].append(group['Factor'].iloc[0])
    statistics['Day'].append(group['Day'].iloc[0])
    statistics['Mean'].append(mean_tf)
    statistics['Max'].append(max_tf)
    statistics['Min'].append(min_tf)
    statistics['Std'].append(std_tf)

# Преобразуем статистики в DataFrame
stats_df = pd.DataFrame(statistics)

# Проверка на дублирующиеся комбинации Source и Factor без учета Day
print(stats_df.duplicated(subset=['Source', 'Factor']).sum())

# Уникальные значения для Day
unique_days = stats_df['Day'].unique()

for day in unique_days:
    # Фильтруем данные по текущему значению Day
    day_df = stats_df[stats_df['Day'] == day]

    # Создаем сводную таблицу
    pivot_df = day_df.pivot(index='Factor', columns='Source', values='Mean')

    # Получаем уникальные факторы и источники
    factors = pivot_df.index
    sources = pivot_df.columns

    # Определяем положение на оси X для каждой группы
    x = np.arange(len(factors))
    width = 0.2  # Ширина каждого столбца

    fig, ax = plt.subplots()

    # Создаем столбцы для каждого Source
    for i, source in enumerate(sources):
        means = pivot_df[source]
        ax.bar(x + i * width, means, width, label=source)

    # Настройки осей и меток
    ax.set_title(f'Влияние факторов на источники для Day {day}')
    ax.set_xticks(x + width / 2 * (len(sources) - 1))
    ax.set_xticklabels(factors)
    ax.set_xlabel('Factor')
    ax.set_ylabel('Mean')
    ax.legend(title='Source')

    plt.tight_layout()
    plt.show()

# Аналогичный подход для другого взгляда: как факторы влияют на каждый источник
for day in unique_days:
    # Фильтруем данные по текущему значению Day
    day_df = stats_df[stats_df['Day'] == day]

    # Создаем сводную таблицу
    pivot_df_factor = day_df.pivot(index='Source', columns='Factor', values='Mean')

    # Получаем уникальные источники и факторы
    sources = pivot_df_factor.index
    factors = pivot_df_factor.columns

    # Определяем положение на оси X для каждой группы
    x = np.arange(len(sources))

    fig, ax = plt.subplots()

    # Создаем столбцы для каждого фактора
    for i, factor in enumerate(factors):
        means = pivot_df_factor[factor]
        ax.bar(x + i * width, means, width, label=factor)

    # Настройки осей и меток
    ax.set_title(f'Влияние источников на факторы для Day {day}')
    ax.set_xticks(x + width / 2 * (len(factors) - 1))
    ax.set_xticklabels(sources)
    ax.set_xlabel('Source')
    ax.set_ylabel('Mean')
    ax.legend(title='Factor')

    plt.tight_layout()
    plt.show()
