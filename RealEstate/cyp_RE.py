import matplotlib.pyplot as plt
import numpy as np

# Данные для графиков
years = np.arange(2003, 2025)
general_index = [70, 80, 95, 115, 140, 155, 100, 95, 85, 75, 70, 72, 
                75, 78, 82, 88, 95, 98, 115, 130, 145, 155]

villa_prices = [350, 420, 520, 650, 820, 950, 650, 600, 520, 450, 400, 
               420, 440, 460, 480, 520, 570, 590, 680, 780, 880, 950]

# Создаем фигуру с двумя субплогами
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# График 1: Обобщенный индекс цен
ax1.plot(years, general_index, marker='o', linewidth=2, markersize=6, color='#2E86AB')
ax1.fill_between(years, general_index, alpha=0.3, color='#2E86AB')
ax1.set_title('Динамика цен на недвижимость на Кипре (2003-2024)\nИндекс (2009 = 100)', 
              fontsize=14, fontweight='bold', pad=20)
ax1.set_xlabel('Год', fontsize=12)
ax1.set_ylabel('Индекс цен (2009=100)', fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.set_xticks(years[::2])  # Отображаем каждый второй год для читаемости

# Добавляем аннотации ключевых событий
ax1.annotate('Финансовый кризис', xy=(2009, 100), xytext=(2007, 120),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=10, color='red')
ax1.annotate('Новый рост', xy=(2021, 115), xytext=(2019, 130),
            arrowprops=dict(arrowstyle='->', color='green'),
            fontsize=10, color='green')

# График 2: Цены на виллы с 3 спальнями
ax2.plot(years, villa_prices, marker='s', linewidth=2, markersize=6, color='#A23B72')
ax2.fill_between(years, villa_prices, alpha=0.3, color='#A23B72')
ax2.set_title('Ориентировочная динамика цен на виллы с 3 спальнями (2003-2024)', 
              fontsize=14, fontweight='bold', pad=20)
ax2.set_xlabel('Год', fontsize=12)
ax2.set_ylabel('Средняя цена, тыс. €', fontsize=12)
ax2.grid(True, alpha=0.3)
ax2.set_xticks(years[::2])

# Добавляем аннотации для вилл
ax2.annotate('Пик рынка', xy=(2008, 950), xytext=(2006, 1000),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=10, color='red')
ax2.annotate('Дно рынка', xy=(2013, 400), xytext=(2011, 300),
            arrowprops=dict(arrowstyle='->', color='blue'),
            fontsize=10, color='blue')
ax2.annotate('Восстановление', xy=(2024, 950), xytext=(2020, 800),
            arrowprops=dict(arrowstyle='->', color='green'),
            fontsize=10, color='green')

# Настраиваем внешний вид
plt.tight_layout(pad=3.0)

# Добавляем общий заголовок
fig.suptitle('Цены на недвижимость на Кипре: 22-летняя динамика', 
             fontsize=16, fontweight='bold', y=0.98)

plt.show()

# Дополнительный график: оба тренда вместе для сравнения
plt.figure(figsize=(14, 8))

# Нормализуем данные для сравнения на одном графике
general_normalized = np.array(general_index) / max(general_index) * 100
villas_normalized = np.array(villa_prices) / max(villa_prices) * 100

plt.plot(years, general_normalized, marker='o', linewidth=2, label='Общий индекс цен', color='#2E86AB')
plt.plot(years, villas_normalized, marker='s', linewidth=2, label='Виллы (3 спальни)', color='#A23B72')

plt.title('Сравнение динамики: Общий индекс vs Виллы с 3 спальнями\n(нормализованные значения)', 
          fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Год', fontsize=12)
plt.ylabel('Нормализованный индекс (%)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.xticks(years[::2])

# Добавляем вертикальные линии для ключевых периодов
plt.axvline(x=2008, color='red', linestyle='--', alpha=0.7, label='Начало кризиса')
plt.axvline(x=2013, color='blue', linestyle='--', alpha=0.7, label='Дно рынка')
plt.axvline(x=2020, color='green', linestyle='--', alpha=0.7, label='Новый рост')

plt.legend()
plt.tight_layout()
plt.show()

# Вывод статистики
print("СТАТИСТИКА ПО ЦЕНАМ НА ВИЛЛЫ (3 спальни)")
print(f"Начальная цена (2003): {villa_prices[0]:,} тыс. €")
print(f"Пиковая цена (2008): {villa_prices[5]:,} тыс. €")
print(f"Минимальная цена (2013): {villa_prices[10]:,} тыс. €")
print(f"Текущая цена (2024): {villa_prices[-1]:,} тыс. €")
print(f"Рост за весь период: {((villa_prices[-1] - villa_prices[0]) / villa_prices[0] * 100):.1f}%")