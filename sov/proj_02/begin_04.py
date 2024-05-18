"""
давай посмотрим на решаемую задачу более обобщенно, не привязываясь к столбчатым диаграммам. 
А как бы ты определил наиболее весомый фактор роста для целевой функции F(S,F,D)  имея 36 строк данных 
( у нас они в датафрейме stats_df ) и какими соттветственно графиками мог бы проиллюстрировать полученный вывод? 
-----------------------------------
Для определения наиболее весомого фактора роста для целевой функции F(Source, Factor, Day) можно воспользоваться статистическими методами
 и методами машинного обучения. Одним из подходов является использование анализа дисперсии (ANOVA) для оценки значимости каждого фактора.
 Также можно использовать регрессионный анализ или методы машинного обучения, такие как случайный лес (Random Forest) для оценки важности 
 признаков.

Вот пример, как можно провести анализ важности факторов и визуализировать результаты:

ANOVA для определения значимости факторов:

Проведем ANOVA для каждого фактора (Source, Factor, Day), чтобы оценить их влияние на целевую переменную (Mean).
Random Forest для оценки важности признаков:

Используем Random Forest для оценки важности каждого фактора.
Визуализация результатов:

Создадим box plot для каждого фактора, чтобы увидеть распределение значений.
Визуализируем важность факторов, полученных с помощью Random Forest.
-----------------------------------------------
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from statsmodels.formula.api import ols
import statsmodels.api as sm
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

# Преобразуем категориальные переменные в числовые
le = LabelEncoder()
stats_df['Source_enc'] = le.fit_transform(stats_df['Source'])
stats_df['Factor_enc'] = le.fit_transform(stats_df['Factor'])
stats_df['Day_enc'] = le.fit_transform(stats_df['Day'])

# Random Forest для оценки важности признаков
X = stats_df[['Source_enc', 'Factor_enc', 'Day_enc']]
y = stats_df['Mean']
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X, y)
feature_importances = rf.feature_importances_

# Важность факторов
feature_names = ['Source', 'Factor', 'Day']
importances_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})

# ANOVA для оценки значимости факторов
model = ols('Mean ~ C(Source) + C(Factor) + C(Day)', data=stats_df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)

# Визуализация результатов
plt.figure(figsize=(12, 6))

# Важность факторов (Random Forest)
plt.subplot(1, 2, 1)
sns.barplot(x='Importance', y='Feature', data=importances_df.sort_values(by='Importance', ascending=False))
plt.title('Importance of factors (Random Forest)')
plt.xlabel('Importance')
plt.ylabel('Factors')

# Box plot для каждого фактора
plt.subplot(1, 2, 2)
sns.boxplot(x='Mean', y='Source', data=stats_df, palette='Set3')
plt.title('Box plot by Source')
plt.xlabel('Fm/Fv')
plt.ylabel('Source')

plt.tight_layout()
plt.show()

# Печать таблицы ANOVA
print(anova_table)

"""
Для определения наиболее весомого фактора роста для целевой функции F(Source, Factor, Day)  использовались статистические методы
 и методы машинного обучения. Одним из подходов является использование анализа дисперсии (ANOVA) для оценки значимости каждого фактора.
 Также можно использовать регрессионный анализ или методы машинного обучения,
 такие как случайный лес (Random Forest) для оценки важности признаков.

"""