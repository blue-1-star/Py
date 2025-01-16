import pandas as pd

# Пример данных
data = {
    'Column': ['Treatment 1.ORF', 'Treatment 10.ORF', 'Treatment 11.ORF','Treatment 2.ORF', 'Treatment 3.ORF']
}
data1 = {
    'Column': ['Treatment 1.ORF', 'Treatment 10.ORF', 'Treatment 2.ORF']
}


# Создаем DataFrame
df = pd.DataFrame(data)

# Сортировка с учетом числовой части
# df = df.sort_values(by='Column', key=lambda x: x.str.extract(r'(\d+)').astype(int))
df = df.sort_values(by='Column', key=lambda x: x.str.extract(r'(\d+)')[0].astype(int))
# Вывод результата
print(df)
