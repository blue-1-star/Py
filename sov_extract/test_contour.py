import cv2
import numpy as np

# Загружаем изображение
image_path = r"G:\My\sov\extract\ORF\F\F1.png"  # Сначала конвертируйте ORF в JPEG или PNG
output_folder = r"G:\My\sov\extract\ORF\Work"  # Папка для сохранения
image = cv2.imread(image_path)
# image = cv2.imread("image.jpg")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Определяем диапазон цвета (например, зелёный)
lower_bound = np.array([35, 50, 50])
upper_bound = np.array([85, 255, 255])
я 
# Создаём бинарную маску
mask = cv2.inRange(hsv, lower_bound, upper_bound)

# Ищем контуры
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Рисуем контуры на исходном изображении
cv2.namedWindow("Contours", cv2.WINDOW_NORMAL)  # Разрешаем менять размер окна

cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# Показываем результат
cv2.imshow("Contours", image)
cv2.waitKey(0)
cv2.destroyAllWindows()


