import numpy as np
# import math 
import matplotlib.pyplot as plt

# Устанавливаем диапазон значений для x
x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)  # от -2π до 2π

# Вычисляем значения тригонометрических функций
y_sin = np.sin(x)
y_cos = np.cos(x)
y_tan = np.tan(x)
y_cot = 1 / np.tan(x)
y_asin = np.arcsin(x)
y_atan = np.arctan(x)
# y_atan= math.atan(x)
# Настройка графиков
plt.figure(figsize=(12, 8))

# Синус
plt.subplot(2, 2, 1)
plt.plot(x, y_sin, label='sin(x)', color='blue')
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
plt.title('График функции sin(x)')
plt.ylim(-1.5, 1.5)
plt.grid(True)
plt.legend()

# Косинус
# Arcsin
plt.subplot(2, 2, 2)
plt.plot(x, y_asin, label='arcsin(x)', color='green')
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
plt.title('График функции arcsin(x)')
plt.ylim(-np.pi / 2, np.pi / 2)
plt.grid(True)
plt.legend()

# Тангенс
# Арктангенс
plt.subplot(2, 2, 3)
plt.plot(x, y_atan, label='atan(x)', color='red')
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
plt.title('График функции atan(x)')
plt.ylim(-np.pi / 2, np.pi / 2)  # Ограничиваем по вертикали, чтобы избежать асимптот
plt.grid(True)
plt.legend()

# Котангенс
# plt.subplot(2, 2, 4)
# plt.plot(x, y_cot, label='cot(x)', color='purple')
# plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
# plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
# plt.title('График функции cot(x)')
# plt.ylim(-10, 10)  # Ограничиваем по вертикали
# plt.grid(True)
# plt.legend()

# Общая настройка и отображение
plt.tight_layout()
plt.show()
