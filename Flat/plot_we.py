import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Функция для построения парной столбчатой диаграммы
def plot_utility_bills(file_path, sheet_name, period_months=12):
    """
    Построение парной столбчатой диаграммы оплат за электроэнергию и воду.py
    
    :param file_path: Путь к файлу Excel.
    :param sheet_name: Название листа в Excel.
    :param period_months: Количество месяцев для отображения (по умолчанию 12).
    """
    # Чтение данных из Excel
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Преобразование столбца 'Date' в формат datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')
    
    # Фильтрация данных за указанный период
    end_date = df['Date'].max()  # Последняя дата в данных
    start_date = end_date - timedelta(days=30 * period_months)  # Начальная дата (период назад)
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    
    # Построение диаграммы
    plt.figure(figsize=(12, 6))
    
    # Ширина столбцов
    bar_width = 0.35
    
    # Позиции для столбцов
    positions = range(len(filtered_df))
    
    # Столбцы для оплаты за электроэнергию
    plt.bar(
        [p - bar_width / 2 for p in positions],  # Смещение влево
        filtered_df['El_bill'],
        width=bar_width,
        label='Оплата за электроэнергию (грн)',
        color='green'
    )
    
    # Столбцы для оплаты за воду
    plt.bar(
        [p + bar_width / 2 for p in positions],  # Смещение вправо
        filtered_df['water'],
        width=bar_width,
        label='Оплата за воду (грн)',
        color='blue'
    )
    
    # Настройка осей и заголовка
    plt.xlabel('Месяц')
    plt.ylabel('Сумма (грн)')
    plt.title(f'Оплата за электроэнергию и воду за последние {period_months} месяцев')
    plt.xticks(positions, filtered_df['Date'].dt.strftime('%Y-%m'), rotation=45)
    plt.legend()
    
    # Отображение диаграммы
    plt.tight_layout()
    plt.show()

# Пример использования
# inp_dir = r"D:\OneDrive\Документы"
inp_dir = r"G:\Flat"
excel_file = "Flat_Arn.xlsx"
sheet_name = "Push"
file_path = os.path.join(inp_dir, excel_file)

# Построение диаграммы за последние 12 месяцев
plot_utility_bills(file_path, sheet_name, period_months=4)