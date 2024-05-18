import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from bg_03 import transform, analyze_string

# Предполагаем, что stats_df уже загружен и подготовлен
#  Ваш существующий код для создания stats_df
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

# One-Hot Encoding для фактора Factor
encoder = OneHotEncoder(drop= None)  # drop='first' to avoid multicollinearity
encoded_factors = encoder.fit_transform(stats_df[['Factor']]).toarray()
encoded_factor_df = pd.DataFrame(encoded_factors, columns=encoder.get_feature_names_out(['Factor']))

# Объединяем с исходными данными
data = pd.concat([stats_df[['Day', 'Source']], encoded_factor_df, stats_df['Mean']], axis=1)

# One-Hot Encoding для фактора Source
data = pd.get_dummies(data, columns=['Source'], drop_first=True)

# Обучение модели Random Forest
X = data.drop('Mean', axis=1)
y = data['Mean']
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Получение важности признаков
feature_importances = model.feature_importances_
feature_names = X.columns

# Создание DataFrame с важностью признаков
importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': feature_importances})

# Фильтрация только dummy-переменных для факторов
factor_importance_df = importance_df[importance_df['Feature'].str.contains('Factor_')]

# Визуализация важности факторов
plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=factor_importance_df.sort_values(by='Importance', ascending=False))
plt.title('Важность отдельных значений фактора (N, F, H)')
plt.xlabel('Важность')
plt.ylabel('Фактор')
plt.show()

