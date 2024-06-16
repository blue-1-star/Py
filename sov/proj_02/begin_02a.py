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

# Группируем данные по 'code'
grouped = df2.groupby('code')

# Словарь для хранения статистик
statistics = {'Source': [], 'Factor': [], 'Mean': [], 'Max': [], 'Min': [], 'Std': []}

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

# Создаем графики
fig, ax = plt.subplots(figsize=(16,8 ))

# Бар график для среднего значения
bar_width = 0.25
index = np.arange(len(stats_df))

bar1 = ax.bar(index, stats_df['Mean'], bar_width, label='Mean')

# Добавляем ошибочные полосы
ax.errorbar(index, stats_df['Mean'], yerr=stats_df['Std'], fmt='o', color='r', label='Std Dev')

# Добавляем максимальные и минимальные значения
for i in range(len(stats_df)):
    ax.text(index[i], stats_df['Max'][i]+0.001, f'{stats_df["Max"][i]:.2f}',\
    ha='center', va='bottom', color='green')
    ax.text(index[i] - 0.2, stats_df['Min'][i], f'{stats_df["Min"][i]:.2f}',\
    ha='right', va='top', color='m', fontsize=8)
     # Добавляем текстовые метки для среднего значения
    # ax.text(index[i], stats_df['Mean'][i], f'{stats_df["Mean"][i]:.2f}',\
    # ha='center',va='bottom', color='blue', fontsize=8)

    ax.scatter(index[i], stats_df['Max'][i], color='green', s=50, zorder=5, marker='^', label='Max' if i == 0 else "")  # Треугольник
    ax.scatter(index[i], stats_df['Min'][i], color='m', s=50, zorder=5, marker='v', label='Min' if i == 0 else "")    # down


# Настраиваем оси и заголовки
ax.set_xlabel('Treatment_code')
ax.set_ylabel('Fv/Fm')
ax.set_title('Statistics by Code')
ax.set_xticks(index)
ax.set_xticklabels(stats_df['Source'] + '_' + stats_df['Factor'], rotation=45, ha='right')
ax.legend()
# Устанавливаем лимиты для оси Y, чтобы график был сжат по вертикали
# ax.set_ylim([stats_df['Mean'].min() - 2 * stats_df['Std'].max(), stats_df['Max'].max() + stats_df['Std'].max()])
ax.set_ylim([stats_df['Mean'].min() - 1.4 * stats_df['Std'].max(), stats_df['Max'].max() + 0.9 * stats_df['Std'].max()])
plt.tight_layout()
plt.show()

"""
теперь есть потребность в его модификации
в связи с тем что идет подготовка экспериментальных данных  для новых значений в  группе Source
( она будет  содержать ещё  три источника  U3, U4, U5 ) необходимо заполнить датафрейм df2
строками, с модельными данными по такому алгоритму  
Пока df2['code'].max() <= Max_Code  
10 строк с одинаковым кодом в столбце 
df2[['code']] = Max_Code 
и далее в цикле увеличиваем 
df2[['code']] =+  1
и с десятью случайных нормально - распределенных 
вещественных значений со средним как у столбца  df2[[Source]] == N0 для столбца df2[[Source]] == N3
df2[[Source]] == N1 для столбца df2[[Source]] == N4
df2[[Source]] == N2 для столбца df2[[Source]] == N5
- эти модельные данные имитирует имеющиеся данные для N0, N1, N2 только изменяя их случайностью генератора
Всего будет построено ( добавлено в df2 - 390 новых строк с повторяющися df2[[code]]  
 по 10 раз, а уникальных комбинаций по столбцам  df2[['Source', 'Factor', 'Day']] 
 будет 39 ( DAY  = 7, 10, 14)  (Source  = U3,U4,U5) ( Factor = N,H,F )  
 Если df2['code'].max() > Max_Code   - исходные данные уже заполнены в , функцию генератор не применять
"""