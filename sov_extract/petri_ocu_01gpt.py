import cv2
import numpy as np
import os
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt

# Параметры
input_path = r"G:\My\sov\extract\ORF\fungus\FL*.jpg"  # Путь к каталогу с изображениями
output_dir = r"G:\My\sov\extract\ORF\fungus\results"  # Путь к каталогу для результатов

# Функция для вычисления координат каждой ячейки
def get_cell_coordinates(center_x, center_y, radius):
    cell_width = (2 * radius) / 5  # Ширина ячейки (диаметр делим на 5 по X)
    cell_height = (2 * radius) / 3  # Высота ячейки (диаметр делим на 3 по Y)
    
    cells = []
    for i in range(3):
        for j in range(5):
            x1 = int(center_x - radius + j * cell_width)
            y1 = int(center_y - radius + i * cell_height)
            x2 = int(x1 + cell_width)
            y2 = int(y1 + cell_height)
            cells.append((x1, y1, x2, y2))
    return cells

# Создание каталога для результатов
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Список файлов для обработки
files = glob(input_path)
results = []

for file in files:
    # Читаем изображение
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Ищем круг чашки Петри
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100,
                               param1=50, param2=30, minRadius=100, maxRadius=300)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        center_x, center_y, radius = circles[0, 0]
        
        # Вычисляем координаты ячеек
        cells = get_cell_coordinates(center_x, center_y, radius)
        
        for idx, (x1, y1, x2, y2) in enumerate(cells):
            cell = gray[y1:y2, x1:x2]
            _, binary_cell = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            dark_pixel_ratio = np.sum(binary_cell == 0) / binary_cell.size  # Процент тёмных пикселей
            
            # Определяем тип ячейки (вода или вещество)
            substance = "Water" if idx % 5 == 0 else f"Substance {0.25 * (idx % 5):.2f}%"
            
            # Сохраняем данные
            results.append({
                "File": os.path.basename(file),
                "Cell_Number": idx + 1,
                "Substance": substance,
                "Dark_Pixel_Ratio": dark_pixel_ratio
            })
            
            # Сохраняем изображение с контуром ячейки
            outlined_image = image.copy()
            cv2.rectangle(outlined_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            output_image_path = os.path.join(output_dir, f"{os.path.basename(file).split('.')[0]}_cell_{idx + 1}.jpg")
            cv2.imwrite(output_image_path, outlined_image)

# Сохраняем результаты в Excel
df = pd.DataFrame(results)
output_excel_path = os.path.join(output_dir, "results.xlsx")
df.to_excel(output_excel_path, index=False)
print(f"Результаты сохранены в {output_excel_path}")
