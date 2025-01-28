import cv2
import numpy as np
from PIL import Image

# Загрузка изображения
# image_path = "path_to_your_orf_file.jpg"  # Сначала конвертируйте ORF в JPEG или PNG
image_path = r"G:\My\sov\extract\ORF\F\F1.png"  # Сначала конвертируйте ORF в JPEG или PNG
output_folder = r"G:\My\sov\extract\ORF\Work"  # Папка для сохранения
image = cv2.imread(image_path)

# Преобразование в HSV для выделения по цвету
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_bound = np.array([30, 50, 50])  # Настройте диапазон цвета
upper_bound = np.array([90, 255, 255])

# Маска для выделения объекта
mask = cv2.inRange(hsv, lower_bound, upper_bound)

# Поиск контуров
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Обработка каждого контура
for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)  # Прямоугольник вокруг контура
    cropped = image[y:y+h, x:x+w]  # Вырезание объекта

    # Сохранение как PNG
    output_path = f"{output_folder}/sample_{i+1}.png"
    cv2.imwrite(output_path, cropped)

print("Все образцы сохранены в отдельные файлы!")
