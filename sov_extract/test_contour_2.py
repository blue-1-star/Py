import cv2
import numpy as np

# Загружаем изображение
# Загружаем изображение
image_path = r"G:\My\sov\extract\ORF\F\F1.png"  # Сначала конвертируйте ORF в JPEG или PNG
output_folder = r"G:\My\sov\extract\ORF\Work"  # Папка для сохранения

image = cv2.imread(image_path)

if image is None:
    print("Ошибка: изображение не загружено!")
    exit()

# Переводим в HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Настраиваем диапазон цветов (измените под ваш объект)
lower_bound = np.array([10, 20, 20])
upper_bound = np.array([120, 255, 255])

# Создаём маску
mask = cv2.inRange(hsv, lower_bound, upper_bound)

# Проверяем, есть ли белые области
cv2.namedWindow("Contours", cv2.WINDOW_NORMAL)  # Разрешаем менять размер окна
cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)  # Разрешаем менять размер окна
cv2.imshow("Mask", mask)
cv2.waitKey(500)  # Пауза, чтобы увидеть маску

# Ищем контуры
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Найдено контуров: {len(contours)}")

# Выводим информацию о контурах
for i, cnt in enumerate(contours):
    print(f"Контур {i}: {cnt.shape}, длина: {len(cnt)}")

# Пробуем нарисовать контуры
image_copy = image.copy()
cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 3)

# Если контуры не рисуются, попробуем нарисовать прямоугольник
if contours:
    x, y, w, h = cv2.boundingRect(contours[0])
    cv2.rectangle(image_copy, (x, y), (x + w, y + h), (255, 0, 0), 3)
    print(f"Прямоугольник: x={x}, y={y}, w={w}, h={h}")

# Показываем результат
cv2.imshow("Contours", image_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
