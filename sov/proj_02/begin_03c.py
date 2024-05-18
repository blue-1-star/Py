import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from bg_03 import transform, analyze_string

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


# Пример данных stats_df
data = {
    'Source': ['A', 'A', 'B', 'B'],
    'Factor': ['X', 'Y', 'X', 'Y'],
    'Mean': [1.2, 2.3, 1.8, 2.1]
}

# stats_df = pd.DataFrame(data)


# Агрегируем данные по среднему значению для каждой комбинации Source и Factor
stats_df_agg = stats_df.groupby(['Source', 'Factor']).agg({'Mean': 'mean'}).reset_index()



# Создаем сводную таблицу
pivot_df = stats_df.pivot(index='Factor', columns='Source', values='Mean')

# Получаем уникальные факторы и источники
factors = pivot_df.index
sources = pivot_df.columns

# Определяем положение на оси X для каждой группы
x = np.arange(len(factors))
width = 0.3  # Ширина каждого столбца

fig, ax = plt.subplots()

# Создаем столбцы для каждого Source
for i, source in enumerate(sources):
    means = pivot_df[source]
    ax.bar(x + i * width, means, width, label=source)

# Настройки осей и меток
ax.set_title('Пример групповой столбчатой диаграммы')
ax.set_xticks(x + width / 2 * (len(sources) - 1))
ax.set_xticklabels(factors)
ax.set_xlabel('Factor')
ax.set_ylabel('Mean')
ax.legend(title='Source')

plt.tight_layout()
plt.show()


"""
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

# Агрегируем данные по среднему значению для каждой комбинации Source и Factor
stats_df_agg = stats_df.groupby(['Source', 'Factor']).agg({'Mean': 'mean'}).reset_index()

# Создаем сводную таблицу
pivot_df = stats_df_agg.pivot(index='Factor', columns='Source', values='Mean')

# Получаем уникальные факторы и источники
factors = pivot_df.index
sources = pivot_df.columns

# Определяем положение на оси X для каждой группы
x = np.arange(len(factors))
width = 0.3  # Ширина каждого столбца

fig, ax = plt.subplots()

# Создаем столбцы для каждого Source
for i, source in enumerate(sources):
    means = pivot_df[source]
    ax.bar(x + i * width, means, width, label=source)

# Настройки осей и меток
ax.set_title('Пример групповой столбчатой диаграммы')
ax.set_xticks(x + width / 2 * (len(sources) - 1))
ax.set_xticklabels(factors)
ax.set_xlabel('Factor')
ax.set_ylabel('Mean')
ax.legend(title='Source')

plt.tight_layout()
plt.show()

"""

"""
Это совсем не та задача - ты предлагаешь агрегировать данные, которые уже агрегированы на предыдущем шаге - мы рассматриваем сгруппы с вычисленным средним - 

задача состоит в том чтобы имея некую неизвестную функцию (целевую) F
F(Source, Factor, Day)  - где каждая из переменных независима и путем их вариаций подобрать наиболее оптимальную комбинацию этих независимых параметров максимизирующих функцию F

каждая строка - набор параметров в датафрейме является уникальной, отличаясь различными вариациями параметров 
Source - [ U0, U1, U2, C0]
Factor - [ N, F, H] 
Day - [7,10,14] 

Это достигнуто группированием всего набора данных по ' code'

Теперь хотелось выделить как влияет на имеющийся набор Source каждый из факторов - Factor
и другой взгляд - 
как всякий фактор влияет на выбранные поочередно Source



ChatGPT
Понял, ваша задача состоит в том, чтобы проанализировать влияние различных факторов на целевую функцию для различных источников и факторов.
 Давайте создадим групповую столбчатую диаграмму, чтобы визуализировать, как разные факторы влияют на каждый источник, и наоборот.

Шаги:
Подготовить данные: Убедиться, что данные организованы правильно.
Создать сводную таблицу: Создать сводную таблицу для группировки данных по Source и Factor.
Построить групповую столбчатую диаграмму: Использовать matplotlib для построения диаграммы.
Давайте сделаем это:

python
Copy code
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

# Создаем сводную таблицу
pivot_df = stats_df.pivot(index='Factor', columns='Source', values='Mean')

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
ax.set_title('Влияние факторов на источники')
ax.set_xticks(x + width / 2 * (len(sources) - 1))
ax.set_xticklabels(factors)
ax.set_xlabel('Factor')
ax.set_ylabel('Mean')
ax.legend(title='Source')

plt.tight_layout()
plt.show()

# Теперь другой взгляд: как факторы влияют на каждый источник
pivot_df_factor = stats_df.pivot(index='Source', columns='Factor', values='Mean')

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
ax.set_title('Влияние источников на факторы')
ax.set_xticks(x + width / 2 * (len(factors) - 1))
ax.set_xticklabels(sources)
ax.set_xlabel('Source')
ax.set_ylabel('Mean')
ax.legend(title='Factor')

plt.tight_layout()
plt.show()
Объяснение:
Подготовка данных:

Мы используем данные из вашего DataFrame и применяем analyze_string для получения значений Source, Factor и Day.
Расчет статистик:

Мы группируем данные по code и вычисляем среднее значение TF для каждой группы, затем сохраняем результаты в stats_df.
Создание сводной таблицы:

Первая сводная таблица (pivot_df) группирует данные по Factor и Source, чтобы посмотреть, как каждый фактор влияет на источник.
Вторая сводная таблица (pivot_df_factor) группирует данные по Source и Factor, чтобы посмотреть, как каждый источник влияет на фактор.
Построение диаграмм:

Первая диаграмма показывает влияние факторов на источники.
Вторая диаграмма показывает влияние источников на факторы.
Таким образом, вы сможете визуально оценить влияние каждого фактора на различные источники и наоборот.








Message ChatGPT

"""