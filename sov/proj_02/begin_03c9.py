import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# from scipy import stats
from lib_sov import gen_data, stats_group

# Ваш существующий код для создания stats_df
dir_dat = "G:/Programming/Py/sov/proj_02/"
file = "data_02.xlsx"
df = gen_data(dir_dat + file)
print(df.columns)
# Пполучаем статистики в сгруппированных по столбцу 'code' данных
stats_df = stats_group(df, 'code')
# print(stats_df.head())
# Уникальные значения для Day
unique_days = stats_df['Day'].unique()

# Уникальные факторы и источники
factors = stats_df['Factor'].unique()
sources = stats_df['Source'].unique()

# Создаем графики
fig, axes = plt.subplots(2, 1, figsize=(16, 12))

# Ширина столбцов
width = 0.5

# График 1: Влияние факторов на источники
colors = ['b', 'g', 'r', 'c']  # Задаем цвета для каждого источника
for i, day in enumerate(unique_days):
    day_df = stats_df[stats_df['Day'] == day]
    pivot_df = day_df.pivot(index='Factor', columns='Source', values='Mean')
    x = np.arange(len(factors)) + i * (len(factors) + 1) * len(sources)  # добавляем промежуток между днями
    for j, source in enumerate(sources):
        means = pivot_df[source]
        # bars = axes[0].bar(x + j * width, means, width, label=source if i == 0 else "", color=colors[j], alpha=0.7)
        bars = axes[0].bar(x + j * width *1.3, means, width, label=source if i == 0 else "", color=colors[j], alpha=0.7)
    # Добавляем метки для каждого дня
    # axes[0].text(np.mean(x) + (len(sources) - 1) * width / 2, max(means) + 0.1, f'Day {day}', ha='center', va='bottom')
    axes[0].text(np.mean(x) + (len(sources) - 1) * width / 2, max(means), f'Day {day}', ha='center', va='bottom')

# Добавляем подписи для факторов на оси X
xticks = []
for i in range(len(unique_days)):
    for j in range(len(factors)):
        xticks.append(i * (len(factors) + 1) * len(sources) + j * len(sources) + (len(sources) - 1) * width / 2)
axes[0].set_xticks(xticks)
axes[0].set_xticklabels(np.tile(factors, len(unique_days)))
axes[0].set_title('Влияние факторов на источники')
axes[0].set_xlabel('Factor')
axes[0].set_ylabel('Mean')
axes[0].legend(title='Source', bbox_to_anchor=(1.05, 1), loc='upper left')

# График 2: Влияние источников на факторы
for i, day in enumerate(unique_days):
    day_df = stats_df[stats_df['Day'] == day]
    pivot_df = day_df.pivot(index='Source', columns='Factor', values='Mean')
    x = np.arange(len(sources)) + i * (len(sources) + 1) * len(factors)  # добавляем промежуток между днями
    for j, factor in enumerate(factors):
        means = pivot_df[factor]
        bars = axes[1].bar(x + j * width, means, width, label=factor if i == 0 else "", color=colors[j], alpha=0.7)
    # Добавляем метки для каждого дня
    axes[1].text(np.mean(x) + (len(factors) - 1) * width / 2, max(means) + 0.1, f'Day {day}', ha='center', va='bottom')

# Добавляем подписи для источников на оси X
xticks = []
for i in range(len(unique_days)):
    for j in range(len(sources)):
        xticks.append(i * (len(sources) + 1) * len(factors) + j * len(factors) + (len(factors) - 1) * width / 2)
axes[1].set_xticks(xticks)
axes[1].set_xticklabels(np.tile(sources, len(unique_days)))
axes[1].set_title('Влияние источников на факторы')
axes[1].set_xlabel('Source')
axes[1].set_ylabel('Mean')
axes[1].legend(title='Factor', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()


"""
import pandas as pd

def stats_group(df, col):
    # Проверяем тип переданного параметра col
    if isinstance(col, int):
        # Если это номер столбца, получаем имя столбца по номеру
        col = df.columns[col]
    elif isinstance(col, str):
        # Если это имя столбца, проверяем, что такое имя существует в датафрейме
        if col not in df.columns:
            raise ValueError(f"Column '{col}' does not exist in the DataFrame")
    else:
        raise TypeError("Parameter 'col' must be either an integer or a string")
    
    # Группируем по указанному столбцу
    stats = df.groupby(col)
    
    return stats

# Пример использования
data = {
    'A': [1, 2, 1, 2],
    'B': [5, 6, 7, 8],
    'C': [9, 10, 11, 12]
}

df = pd.DataFrame(data)

# Группировка по столбцу 'A'
grouped_by_name = stats_group(df, 'A')
print(grouped_by_name.mean())

# Группировка по второму столбцу (столбец 'B')
grouped_by_index = stats_group(df, 1)
print(grouped_by_index.mean())

"""