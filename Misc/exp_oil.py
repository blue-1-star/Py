import matplotlib.pyplot as plt

# Дані
years = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
oil_export = [1.1, 2.0, 2.9, 3.2, 3.0, 3.6, 4.1]  # млн барелів/день
lng_export = [1.9, 3.0, 4.9, 6.5, 9.7, 10.6, 12.1]  # млрд куб. футів/день

# Створення графіка
plt.figure(figsize=(10, 5))
plt.plot(years, oil_export, marker='o', label='Експорт нафти,млн барелів/день ')
plt.plot(years, lng_export, marker='s', label='Експорт ЗПГ,млрд куб. футів/день')
plt.title('Експорт нафти та газу з США (2017–2023)')
plt.xlabel('Рік')
plt.ylabel('Обсяг експорту')
plt.grid(True)
plt.legend()
plt.show()