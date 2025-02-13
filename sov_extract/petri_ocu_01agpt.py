import cv2
import numpy as np

# Путь к изображению
image_path = r"G:\My\sov\extract\ORF\fungus\FL_1.jpg"

# Загружаем изображение
image = cv2.imread(image_path)
if image is None:
    print("Не удалось загрузить изображение по пути:", image_path)
    exit()

# Получаем размеры исходного изображения
height, width = image.shape[:2]

# Если известно, что чашка Петри находится правее, можно обрабатывать правую половину изображения
roi = image[0:height, width//2:width].copy()

# Преобразуем ROI в оттенки серого
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# Гауссовское размытие для уменьшения шума
blurred = cv2.GaussianBlur(gray, (9, 9), 2)

# Применяем адаптивный порог.
# Используем THRESH_BINARY, но если фон белый и объект темнее, то после порогового преобразования объект может оказаться черным.
# Поэтому, если среднее значение порогового изображения высокое, инвертируем его.
thresh = cv2.adaptiveThreshold(
    blurred,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)

# Если среднее значение слишком высокое (изображение в основном белое), инвертируем пороговое изображение
if np.mean(thresh) > 127:
    thresh = cv2.bitwise_not(thresh)

# Применяем морфологическое закрытие для устранения разрывов в контуре
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Находим контуры в обработанном изображении
contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Ищем самый крупный контур по площади (так как чашка Петри должна быть значительно больше)
largest_contour = None
max_area = 0
for cnt in contours:
    area = cv2.contourArea(cnt)
    # Отбрасываем слишком маленькие объекты; порог можно настраивать
    if area < 5000:
        continue
    if area > max_area:
        max_area = area
        largest_contour = cnt

# Создаем копию ROI для вывода результата
roi_output = roi.copy()

if largest_contour is not None:
    # Определяем минимальный описывающий круг для найденного контура
    (x, y), radius = cv2.minEnclosingCircle(largest_contour)
    center = (int(x), int(y))
    radius = int(radius)
    cv2.circle(roi_output, center, radius, (0, 255, 0), thickness=3)
    
    # Выводим координаты в глобальной системе (учитывая, что ROI – это правая половина изображения)
    global_center = (center[0] + width//2, center[1])
    print("Найден круг чашки Петри:")
    print("  Центр (в глобальных координатах):", global_center)
    print("  Радиус:", radius)
else:
    print("Круг чашки Петри не найден.")

# Создаем окно с изменяемым размером и уменьшаем его в 5 раз
cv2.namedWindow("Результат", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Результат", width // 5, height // 5)
cv2.imshow("Результат", roi_output)
cv2.waitKey(0)
cv2.destroyAllWindows()
