
# p 30
print([2, 2, 4, 2].index(2))
print([2, 2, 4, 2].index(2,1))
print([2, 2, 4, 2].index(2,2))

# p 44  Listing 2.1 
employees = {'Alice' : 100000,
'Bob' : 99817,
'Carol' : 122908,
'Frank' : 88123,
'Eve' : 93121}
top_earners = [(k, v) for k, v in employees.items() if v >= 100000]
print(top_earners)
# Листинг 2.2. Однострочное решение для поиска информативных слов
text = '''
Call me Ishmael. Some years ago - never mind how long precisely - having
little or no money in my purse, and nothing particular to interest me
on shore, I thought I would sail about a little and see the watery part
of the world. It is a way I have of driving off the spleen, and regulating
the circulation. - Moby Dick'''
## Однострочник
w = [[x for x in line.split() if len(x)>3] for line in text.split('\n')]
## Результат
print(w)
# Листинг 2.4. Однострочное решение, помечающее строковые значения, содержащие строку символов 'anonymous'
txt = ['lambda functions are anonymous functions.',
'anonymous functions dont have a name.',
'functions are objects in Python.']
# mark = map(lambda s: (True, s) if 'anonymous' in s else (False, s), txt)   # GPT version
mark = [(True, s) if 'anonymous' in s else (False, s) for s in txt]
# mark = [(a,s)  for s in txt if 'anonymous' in txt else False  ]
# mark = [(i, s) for i, s in enumerate(txt) if 'anonymous' in s]
mark = [(bool('anonymous' in s), s) for s in txt]
print(list(mark))
my_list = ['apple', 'banana', 'orange']
for index, value in enumerate(my_list):
    print(f"Index: {index}, Value: {value}")

"""Листинг 2.5. Однострочное решение для поиска в тексте последовательностей
символов и их непосредственного окружения"""
letters_amazon = '''
We spent several years building our own database engine,
Amazon Aurora, a fully-managed MySQL and PostgreSQL-compatible
service with the same or better durability and availability as
the commercial engines, but at one-tenth of the cost. We were
not surprised when this worked.
'''
find = lambda x, q: x[x.find(q)-18:x.find(q)+18] if q in x else -1
print(find(letters_amazon, 'SQL'))
# Листинг 2.6. Однострочное решение для выборки данных
## Данные (ежедневные котировки акций ($))
price = [[9.9, 9.8, 9.8, 9.4, 9.5, 9.7],
[9.5, 9.4, 9.4, 9.3, 9.2, 9.1],
[8.4, 7.9, 7.9, 8.1, 8.0, 8.0],
[7.1, 5.9, 4.8, 4.8, 4.7, 3.9]]
## Однострочник
sample = [line[::2] for line in price]
## Результат
print(sample)
# Листинг 2.7. Однострочное решение для замены всех испорченных строк
## Данные
visitors = ['Firefox', 'corrupted', 'Chrome', 'corrupted',
'Safari', 'corrupted', 'Safari', 'corrupted',
'Chrome', 'corrupted', 'Firefox', 'corrupted']
## Однострочник
visitors[1::2] = visitors[::2]
## Результат
print(visitors)
# Листинг 2.8. Однострочное решение для предсказания частоты сердечных
# сокращений в различные моменты времени 

import matplotlib.pyplot as plt
## Данные
cardiac_cycle = [62, 60, 62, 64, 68, 77, 80, 76, 71, 66, 61, 60, 62]
expected_cycles = cardiac_cycle[1:-2] * 10
# plt.plot(expected_cycles)
# plt.show()
# Листинг 2.9. Однострочное решение для поиска компаний, платящих меньше
# установленной законом минимальной почасовой ставки
## Данные
companies = {
'CoolCompany' : {'Alice' : 33, 'Bob' : 28, 'Frank' : 29},
'CheapCompany' : {'Ann' : 4, 'Lee' : 9, 'Chrisi' : 7},
'SosoCompany' : {'Esther' : 38, 'Cole' : 8, 'Paris' : 18}}
## Однострочник
illegal = [x for x in companies if any(y<9 for y in companies[x].values())]
print(illegal)
# Листинг 2.10. Однострочное решение для приведения списка кортежей в формат базы данных
column_names = ['name', 'salary', 'job']
db_rows = [('Alice', 180000, 'data scientist'),
('Bob', 99000, 'mid-level manager'),
('Frank', 87000, 'CEO')]
## Однострочник
db = [dict(zip(column_names, row)) for row in db_rows]
## Результат
print(db)
# Листинг 3.1. Создание одномерного, двумерного и трехмерного массивов в NumPy
import numpy as np
# Создание одномерного массива из списка
a = np.array([1, 2, 3])
print(a)
"""
[1 2 3]
"""
# Создание двумерного массива из списка списков
b = np.array([[1, 2],
[3, 4]])
print(b)
# Создание трехмерного массива из списка списков списков
c = np.array([[[1, 2], [3, 4]],
[[5, 6], [7, 8]]])
print(c)
# p 76 
import numpy as np
## Данные: годовые зарплаты в тысячах долларов (за 2017, 2018 и 2019 гг.)
alice = [99, 101, 103]
bob = [110, 108, 105]
tim = [90, 88, 85]
salaries = np.array([alice, bob, tim])
taxation = np.array([[0.2, 0.25, 0.22],
[0.4, 0.5, 0.5],
[0.1, 0.2, 0.1]])
## Однострочник
max_income = np.max(salaries - salaries * taxation)
## Результат
print(max_income)
print(salaries - salaries * taxation)
# Листинг 3.7. Примеры многомерных срезов
# p 79
import numpy as np
a = np.array([[0, 1, 2, 3],
[4, 5, 6, 7],
[8, 9, 10, 11],
[12, 13, 14, 15]])
# # Третий столбец: [ 2 6 10 14]
print(a[:, 2])
print(a[1, :])
# Вторая строка: [4 5 6 7]
print(a[1, ::2])
# Вторая строка, каждый второй элемент: [4 6]
print(a[:, :-1])
# Все столбцы, за исключением последнего:  но и все строки
print(a[:-2])       # Аналогично a[:-2, :]      -  all except 2 last
"""Двумерный срез можно производить
с помощью синтаксиса a[срез1, срез2]. Для дополнительных измерений
необходимо добавить через запятую дополнительные операции срезов 
(с помощью операторов срезов начало:конец или начало:конец:шаг). """
#
# p 84
#Листинг 3.11. Однострочное решение, использующее срезы и присваивания срезам
## Зависимости
import numpy as np
## Данные: годовые зарплаты в тысячах долларов (за 2025, 2026 и 2027 гг.)
dataScientist = [130, 132, 137]
productManager = [127, 140, 145]
designer = [118, 118, 127]
softwareEngineer = [129, 131, 137]
employees = np.array([dataScientist,
productManager,
designer,
softwareEngineer])
## Однострочник
employees[0,::2] = employees[0,::2] * 1.1
## Результат
print(employees)
# ---
# p 88
# Листинг 3.14. Однострочное решение, использующее транслирование, булевы
# операторы и выборочный доступ по индексу
## Зависимости
import numpy as np
## Данные: измерения индекса качества воздуха, AQI (строка = город)
X = np.array(
[[ 42, 40, 41, 43, 44, 43 ], # Гонконг
[ 30, 31, 29, 29, 29, 30 ], # Нью-Йорк
[ 8, 13, 31, 11, 11, 9 ], # Берлин
[ 11, 11, 12, 13, 11, 12 ]]) # Монреаль
cities = np.array(["Hong Kong", "New York", "Berlin", "Montreal"])
## Однострочник
polluted = set(cities[np.nonzero(X > np.average(X))[0]])
## Результат
print(polluted)
# ------------------------------------
# p 92 
# Листинг 3.17. Однострочное решение, использующее срезы, типы массивов и булевы операторы
## Зависимости
import numpy as np
## Данные: популярные учетные записи Instagram (миллионы подписчиков)
inst = np.array([[232, "@instagram"],
[133, "@selenagomez"],
[59, "@victoriassecret"],
[120, "@cristiano"],
[111, "@beyonce"],
[76, "@nike"]])
## Однострочник
superstars = inst[inst[:,0].astype(float) > 100, 1]
## Результат
print(superstars)
# p 102
# Листинг 3.23. Однострочное решение, включающее функцию argsort() и срез с отрицательным значением шага
## Зависимости
import numpy as np
## Данные: оценки за экзамен SAT для различных абитуриентов
sat_scores = np.array([1100, 1256, 1543, 1043, 989, 1412, 1343])
students = np.array(["John", "Bob", "Alice", "Joe", "Jane", "Frank", "Carl"])
# a = np.sort( sat_scores)
a = np.sort( sat_scores)
b = np.argsort(sat_scores)
print("SAT=")
# print(b)
print(b[::-1])
print(b[:-4:-1])
print(students[b[:3:-1]])
## Однострочник
top_3 = students[np.argsort(sat_scores)][:-4:-1]
print(top_3)
#  -----------------------------------------
# p 104
# Листинг 3.24. Однострочное решение, использующее лямбда-функции, преобразование типов и булевы операторы
## Зависимости
import numpy as np
## Данные (строка = [название, рейтинг])
books = np.array([['Coffee Break NumPy', 4.6],
['Lord of the Rings', 5.0],
['Harry Potter', 4.3],
['Winnie-the-Pooh', 3.9],
['The Clown of God', 2.2],
['Coffee Break Python', 4.7]])
## Однострочник
predict_bestseller = lambda x, y : x[x[:,1].astype(float) > y]
## Результат
print(predict_bestseller(books, 3.9))


