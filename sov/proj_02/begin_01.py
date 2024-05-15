import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from scipy import stats
from bg_03 import transform, analyze_string
dir_dat = "G:/Programming/Py/sov/proj_02/"
file ="data_02.xlsx" 
df = pd.read_excel(dir_dat+file)
df1 = df.rename(columns={'Treatment':'TR','Treatment_code':'code','Day':'D','Fv/Fm':'TF'})
df1['code']= df1['code'].astype(int)
df1['D']= df1['D'].astype(int)
df2 = df1.copy()

df2[['Source', 'Factor', 'Day']] =\
pd.DataFrame(df2.apply(lambda row: analyze_string(row['TR']), axis=1).tolist(), index=df2.index)
file= r"G:\Programming\R\sov\proj_02\df2_.xlsx"
grouped = df2.groupby(['D','Source', 'Factor', ])
for (day, source, factor), group in grouped:
    print(f"Day: {day}, Source: {source}, Factor: {factor}")
    print(group)
gr_code = df2.groupby([code])
# df2.to_excel(file)
# plt.plot(df2['TF'])
# plt.title("bird's eye view")
# plt.ylabel('Fv/Fm')
# plt.xlabel('all experimental data')

# plt.show()
"""
Необходимо вычислив статистики группировки по столбцу df2[code]  построить столбчатые диаграммы
по столбцам Source и Factor, показав на графике средние значения величин для столбца df2[code] и отметив
максимальные и минимальные значения и среднеквадратичное отколонение
"""
# Answer GPT 4 

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from bg_03 import transform, analyze_string

# Загружаем данные
dir_dat = "G:/Programming/Py/sov/proj_02/"
file ="data_02.xlsx"
df = pd.read_excel(dir_dat + file)

# Переименовываем столбцы
df1 = df.rename(columns={'Treatment':'TR', 'Treatment_code':'code', 'Day':'D', 'Fv/Fm':'TF'})
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
fig, ax = plt.subplots(figsize=(10, 6))

# Бар график для среднего значения
bar_width = 0.35
index = np.arange(len(stats_df))

bar1 = plt.bar(index, stats_df['Mean'], bar_width, label='Mean')
error_config = {'ecolor': '0.3'}
plt.errorbar(index, stats_df['Mean'], yerr=stats_df['Std'], fmt='o', color='r', label='Std Dev', error_kw=error_config)

# Добавляем максимальные и минимальные значения
for i in range(len(stats_df)):
    plt.text(index[i], stats_df['Max'][i], f'{stats_df["Max"][i]:.2f}', ha='center', va='bottom', color='green')
    plt.text(index[i], stats_df['Min'][i], f'{stats_df["Min"][i]:.2f}', ha='center', va='top', color='blue')

# Настраиваем оси и заголовки
plt.xlabel('Code')
plt.ylabel('TF')
plt.title('Statistics by Code')
plt.xticks(index, stats_df['Source'] + '_' + stats_df['Factor'])
plt.legend()

plt.tight_layout()
plt.show()

"""