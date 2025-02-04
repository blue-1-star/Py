import matplotlib.pyplot as plt
import numpy as np

# Пример данных (канал Hue)
hue_channel = np.random.randint(0, 180, size=1000)  # Случайные значения от 0 до 179

# Построение гистограммы и получение численных значений
hist_values, bin_edges, _ = plt.hist(hue_channel, bins=180, range=(0, 180))

# Вывод численных значений
print("Значения гистограммы:", hist_values)
print("Границы бинов:", bin_edges)

# Закрываем график, если он не нужен
# plt.show()
plt.close()
