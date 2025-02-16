import cv2
import numpy as np
import matplotlib.pyplot as plt

# Загрузка изображения
file_image = r"G:\My\sov\extract\Spores\original_img\test\best\4x\A best_4x_1_scale.png"
img = cv2.imread(file_image)
# Преобразование в HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Определяем диапазон для чёрного цвета (настройте значения по необходимости)
lower_black = np.array([0, 0, 0])
upper_black = np.array([180, 255, 50])

# Создаем маску: все пиксели, попадающие в заданный диапазон, будут белыми
mask = cv2.inRange(hsv, lower_black, upper_black)

# (Опционально) Улучшаем маску с помощью морфологических операций
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)

# Наносим маску на исходное изображение для визуализации результата сегментации
result = cv2.bitwise_and(img, img, mask=mask)

# Отображаем результаты с помощью matplotlib
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Исходное изображение")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(mask, cmap="gray")
plt.title("Маска для чёрного цвета")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title("Изолированные споры")
plt.axis("off")

plt.tight_layout()
plt.show()
