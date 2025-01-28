import cv2
import numpy as np

# Загружаем изображение
image_path = r"G:\My\sov\extract\ORF\F\F1.png"  # Сначала конвертируйте ORF в JPEG или PNG
output_folder = r"G:\My\sov\extract\ORF\Work"  # Папка для сохранения

image = cv2.imread(image_path)


hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# cv2.resizeWindow("Contours", 800, 600)
# Настраиваем диапазон цвета
lower_bound = np.array([10, 20, 20])
upper_bound = np.array([120, 255, 255])
mask = cv2.inRange(hsv, lower_bound, upper_bound)

# Ищем контуры
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(f"Всего контуров: {len(contours)}")

# Убираем мелкие контуры
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 90]
print(f"После фильтрации: {len(filtered_contours)}")

# Находим самый крупный контур (основной объект)
main_contour = max(filtered_contours, key=cv2.contourArea)

# Убираем подписи (если они есть)
filtered_contours = [cnt for cnt in filtered_contours if cnt is not main_contour]

# Приглаживаем контур
smoothed_contour = cv2.approxPolyDP(main_contour, epsilon=90, closed=True)

# Рисуем итоговый контур
result_image = image.copy()
cv2.drawContours(result_image, [smoothed_contour], -1, (0, 255, 0), 3)

# Показываем результат
# scale_percent = 10  # Уменьшаем до 50% от исходного размера
# width = int(result_image.shape[1] * scale_percent / 100)
# height = int(result_image.shape[0] * scale_percent / 100)
# resized_image = cv2.resize(result_image, (width, height), interpolation=cv2.INTER_AREA)
cv2.namedWindow("Result", cv2.WINDOW_NORMAL)  # Создаем окно
cv2.resizeWindow("Result", 800, 600)         # Устанавливаем размер
cv2.imshow("Result", result_image)           # Отображаем изображение
cv2.waitKey(0)                               # Ждем нажатия клавиши
cv2.destroyAllWindows()                      # Закрываем все окна

