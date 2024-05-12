import pandas as pd

# Предположим, что у вас уже есть DataFrame df1 с данными

# Группируем данные по столбцам 'D', 'TR' и 'code', а затем агрегируем их в строку
grouped_data = df1.groupby(['D', 'TR', 'code'])['TF'].agg(', '.join).reset_index()

# Подготовим список уникальных значений для каждой группы
unique_d = sorted(grouped_data['D'].unique())
unique_tr = sorted(grouped_data['TR'].unique())
unique_code = sorted(grouped_data['code'].unique())

# Создаем строки для каждой комбинации значений
result = []
for d in unique_d:
    for tr in unique_tr:
        for code in unique_code:
            tf_list = grouped_data[(grouped_data['D'] == d) & 
                                   (grouped_data['TR'] == tr) & 
                                   (grouped_data['code'] == code)]['TF'].tolist()
            result.append(f"Day {d} {tr} {code} {', '.join(tf_list)}")

# Выводим результат
for line in result:
    print(line)
