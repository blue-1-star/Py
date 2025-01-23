import numpy as np
from scipy.stats import friedmanchisquare, wilcoxon
from itertools import combinations

# Данные (16 групп по 3 измерения в каждой)
data = [
    [8, 7, 6], [7, 6, 5], [9, 8, 7], [6, 5, 4], 
    [5, 5, 5], [7, 6, 7], [8, 9, 7], [6, 7, 6], 
    [5, 6, 7], [8, 6, 9], [6, 6, 6], [5, 4, 5],
    [9, 9, 8], [7, 7, 7], [6, 6, 5], [8, 8, 8]
]

# Тест Фридмана
stat, p = friedmanchisquare(*data)
print(f"Тест Фридмана: статистика = {stat}, p-значение = {p}")

# Пост-хок тесты (парные сравнения)
alpha = 0.05 / len(data)  # Поправка Бонферрони
pairwise_results = {}
for (i, j) in combinations(range(len(data)), 2):
    stat, p_value = wilcoxon(data[i], data[j])
    pairwise_results[(i+1, j+1)] = p_value

# Вывод результатов
print("Парные сравнения (с учетом поправки Бонферрони):")
for (pair, p_value) in pairwise_results.items():
    result = "неотличимы" if p_value > alpha else "отличимы"
    print(f"Группы {pair[0]} и {pair[1]}: p = {p_value:.4f}, результат = {result}")
