import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from bg_03 import transform, analyze_string

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

# Получаем уникальные факторы и источники
factors = stats_df['Factor'].unique()
sources = stats_df['Source'].unique()

# Определяем положение на оси X для каждой группы
x = np.arange(len(factors))
width = 0.2  # Ширина каждого столбца

fig, ax = plt.subplots(figsize=(14, 8))

# Создаем столбцы для каждого значения Day
for j, day in enumerate(unique_days):
    # Фильтруем данные по текущему значению Day
    day_df = stats_df[stats_df['Day'] == day]

    for i, source in enumerate(sources):
        source_day_df = day_df[day_df['Source'] == source]
        means = source_day_df.set_index('Factor').reindex(factors)['Mean']
        ax.bar(x + i * width + j * width * len(sources), means, width, label=f'{source} - Day {day}')

# Настройки осей и меток
ax.set_title('Влияние факторов на источники для всех значений Day')
ax.set_xticks(x + width * len(unique_days) * len(sources) / 2)
ax.set_xticklabels(factors)
ax.set_xlabel('Factor')
ax.set_ylabel('Mean')

# Удаляем дубликаты легенд
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), title='Source - Day')

plt.tight_layout()
plt.show()
