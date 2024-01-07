# Очистка и подготовка данных  Chapter 07
# Фильтрация отсутствующих данных
# p 214
import numpy as np 
import pandas as pd
data = pd.Series([1, np.nan, 3.5, np.nan, 7])
print(f'{data}\n{data.dropna()}\nnotna->\n{data[data.notna()]}')
"""
требуется оставить только строки, содержащие определенное ко-
личество отсутствующих наблюдений. Этот порог можно задать с помощью
аргумента thresh:
"""
df = pd.DataFrame(np.random.standard_normal((7, 3)))
df.iloc[:4, 1] = np.nan
df.iloc[:2, 2] = np.nan
print(f'{df}\ndropna->\n{df.dropna()}\ntresh=2->\n{df.dropna(thresh=2)}')
# Восполнение отсутствующих данных p 216
print(f'fillna->\n{df.fillna(0)}')
print(f'fillna dict->\n{df.fillna({1: 0.5,2: 0})}')
df = pd.DataFrame(np.random.standard_normal((6, 3)))
df.iloc[2:, 1] = np.nan
df.iloc[4:, 2] = np.nan
print(f'fillna method ffill->\n{df.fillna(method="ffill")}')
print(f'fillna method ffill->\n{df.fillna(method="ffill", limit = 2)}')
# fillna -> to fill in the data by substituting the mean or median.
data = pd.Series([1., np.nan, 3.5, np.nan, 7])
print(f'fillna mean->\n{data.fillna(data.mean())}')
# Устранение дубликатов  p 218
data = pd.DataFrame({"k1": ["one", "two"] * 3 + ["two"],
"k2": [1, 1, 2, 3, 3, 4, 4]})
print(f'{data}\n{data.duplicated()}\n{data.drop_duplicates()}')
data["v1"] = range(7)
print(f'{data}\n{data.drop_duplicates(subset=["k1"])}\n{data.drop_duplicates(subset=["k2"])}')
# Преобразование данных с помощью функции или отображения  p 220
data = pd.DataFrame({"food": ["bacon", "pulled pork", "bacon",
"pastrami", "corned beef", "bacon",
"pastrami", "honey ham", "nova lox"],
"ounces": [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})
print(f'{data}')
meat_to_animal = {
"bacon": "pig",
"pulled pork": "pig",
"pastrami": "cow",
"corned beef": "cow",
"honey ham": "pig",
"nova lox": "salmon"
}
data["animal"]=data["food"].map(meat_to_animal)
print(data)
# Можно было бы также передать функцию, выполняющую всю эту работу:
def get_animal(x):
    return meat_to_animal[x]
# Замена значений   p 221
data = pd.Series([1., -999., 2., -999., -1000., 3.])
print(f'{data}\n{data.replace(-999, np.nan)}')
# Переименование индексов осей  p 222
data = pd.DataFrame(np.arange(12).reshape((3, 4)),
index=["Ohio", "Colorado", "New York"],
columns=["one", "two", "three", "four"])
print(data)
def transform(x):
    return x[:4].upper()
print(f'{data.index.map(transform)}')
data.index = data.index.map(transform)
print(f'{data}')
# Если требуется создать преобразованный вариант набора данных, не меняя оригинал, то будет полезен метод rename:
print(data.rename(index=str.title, columns=str.upper))
d1 =data.rename(index={"OHIO": "INDIANA"},
columns={"three": "peekaboo"})
print(d1)
# Дискретизация и группировка по интервалам  p 223
ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
bins = [18, 25, 35, 60, 100]
age_categories = pd.cut(ages, bins)
print(age_categories)
print(pd.value_counts(age_categories))
"""
Если передать методу pandas.cut целое число интервалов, а не явно заданные
границы, то он разобьет данные на интервалы равной длины, исходя из мини-
мального и максимального значений. 
"""
data = np.random.uniform(size=20)
print(pd.cut(data, 4, precision=2))
# Обнаружение и фильтрация выбросов
data = pd.DataFrame(np.random.standard_normal((1000, 4)))
print(data.describe())
col = data[0]
print(col[col.abs()>3])
print(data[(data.abs() > 3).any(axis="columns")])
# Следующий код срезает значения, выходящие за границы интервала от –3 до 3
# Выражение np.sign(data) равно 1 или –1
data[data.abs() > 3] = np.sign(data) * 3
print(data.describe())
# Перестановки и случайная выборка  p 227
df = pd.DataFrame(np.arange(5 * 7).reshape((5, 7)))
sampler = np.random.permutation(5)
print(df)
print(sampler)
print(f'take->\n{df.take(sampler)}\niloc->\n{df.iloc[sampler]}')
column_sampler = np.random.permutation(7)
print(f'take for columns->\n{df.take(column_sampler, axis="columns")}')
print(f'sample->\n{df.sample(n=3)}')
choices = pd.Series([5, 7, -1, 6, 4])
print(f'choices->\n{choices.sample(n=10, replace=True)}')
print(f'choices->\n{choices.values}\n{pd.Series(choices.values).sample(n=10, replace=True).values}')
# Вычисление индикаторных переменных  p 229
df = pd.DataFrame({"key": ["b", "b", "a", "c", "a", "b"],
"data1": range(6)})
print(df)
print(f'dummies->\n{pd.get_dummies(df["key"])}')
print(f'dummies->\n{pd.get_dummies(df["key"],prefix="key")}')
dummies = pd.get_dummies(df["key"], prefix="key")
df_with_dummy = df[["data1"]].join(dummies)
print(df_with_dummy)
# p 230
ph_d = "McKinney/datasets/movielens/"
mnames = ["movie_id", "title", "genres"]
movies = pd.read_table(ph_d+"movies.dat", sep="::",
header=None, names=mnames, engine="python")
print(movies[:10])
dummies = movies["genres"].str.get_dummies("|")
print(dummies.iloc[:10, :6])
movies_windic = movies.join(dummies.add_prefix("Genre_"))
print(movies_windic.iloc[0])
# p 231
np.random.seed(12345)
values = np.random.uniform(size=10)
print(values)
bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
print(pd.get_dummies(pd.cut(values, bins)))
# 7.3. Расширение типов данных 
s = pd.Series([1, 2, 3, None])
print(s)
s = pd.Series([1, 2, 3, None], dtype=pd.Int64Dtype())
print(s)
s = pd.Series(['one', 'two', None, 'three'], dtype=pd.StringDtype())
print(s)
# 7.4. Манипуляции со строками   p 235
val = "a,b, guido"
vals = val.split(",")
print(vals)
pieces = [x.strip() for x in val.split(",")]
print(pieces)
first, second, third = pieces 
print(first + "::" + second + "::" + third)
print("::".join(pieces))
print(val.count(","))
print(val.replace(",", "::"))
# Регулярные выражения   p 238










