import cv2
import numpy as np
import os
import pandas as pd

# Путь к изображению
image_path = r"G:\My\sov\extract\ORF\spori\FL_1.jpg"
output_dir = r"G:\My\sov\extract\ORF\spori\results"
os.makedirs(output_dir, exist_ok=True)

# Загрузка изображения
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Размеры изображения и квадратов
height, width = image.shape
num_squares_x = 5
num_squares_y = 3
square_width = width // num_squares_x
square_height = height // num_squares_y

# Список для хранения результатов
results = []

# Функция для анализа квадрата
def analyze_square(square, square_index):
    # Пороговая обработка
    _, thresholded = cv2.threshold(square, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Подсчет пикселей, соответствующих грибку
    fungus_pixels = np.sum(thresholded == 255)
    total_pixels = square.size
    fungus_percentage = (fungus_pixels / total_pixels) * 100
    
    # Сохранение результата
    results.append({
        'Substance': get_substance(square_index),
        'Fungus Percentage': fungus_percentage,
        'Square Index': square_index
    })
    
    # Сохранение изображения
    output_path = os.path.join(output_dir, f"{os.path.basename(image_path)}_{square_index + 1}.jpg")
    cv2.imwrite(output_path, thresholded)

# Функция для определения вещества по индексу квадрата
def get_substance(square_index):
    if square_index % num_squares_x == 0:
        return 'Water'
    elif square_index % num_squares_x == 1:
        return '0.25%'
    elif square_index % num_squares_x == 2:
        return '0.5%'
    elif square_index % num_squares_x == 3:
        return '0.75%'
    elif square_index % num_squares_x == 4:
        return '1%'

# Обработка каждого квадрата
for i in range(num_squares_y):
    for j in range(num_squares_x):
        square_index = i * num_squares_x + j
        x_start = j * square_width
        y_start = i * square_height
        square = image[y_start:y_start + square_height, x_start:x_start + square_width]
        analyze_square(square, square_index)

# Сохранение результатов в Excel
df = pd.DataFrame(results)
excel_path = os.path.join(output_dir, 'results.xlsx')
df.to_excel(excel_path, index=False)

print(f"Анализ завершен. Результаты сохранены в {output_dir}")