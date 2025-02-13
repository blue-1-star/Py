import cv2
import numpy as np

# Путь к изображению
# image_path = r"G:\My\sov\extract\ORF\fungus\FL_1.jpg"
image_path = r"G:\My\sov\extract\ImageJ\FL_1.jpg"


# Загружаем изображение
image = cv2.imread(image_path)
if image is None:
    print("Не удалось загрузить изображение по пути:", image_path)
    exit()

# Получаем размеры исходного изображения
height, width = image.shape[:2]

# Определяем ROI. Здесь используем нижнюю половину по вертикали и правую половину по горизонтали,
# так как, по вашему описанию, круг расположен ниже и правее.
roi = image[height // 2: height, width // 2: width].copy()
roi_height, roi_width = roi.shape[:2]

# Преобразуем ROI в оттенки серого и сглаживаем
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (9, 9), 2)

# Применяем адаптивный порог.
# Если фон белый и круг темнее, при THRESH_BINARY может получиться, что круг окажется черным.
# Поэтому, если среднее значение полученного порога высокое, происходит инвертирование.
thresh = cv2.adaptiveThreshold(
    blurred,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)
if np.mean(thresh) > 127:
    thresh = cv2.bitwise_not(thresh)

# Для отладки: выводим изображение после адаптивного порога
cv2.namedWindow("Threshold", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Threshold", roi_width // 5, roi_height // 5)
cv2.imshow("Threshold", thresh)

# Применяем морфологическое закрытие для устранения разрывов в контурах
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

# Для отладки: выводим изображение после морфологической обработки
cv2.namedWindow("Closed", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Closed", roi_width // 5, roi_height // 5)
cv2.imshow("Closed", closed)

# Находим контуры в обработанном изображении ROI
contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Выбираем самый крупный контур по площади (порог уменьшен, чтобы не отсеивать неполный круг)
largest_contour = None
max_area = 0
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 2000:  # если объект слишком маленький, пропускаем его
        continue
    if area > max_area:
        max_area = area
        largest_contour = cnt

# Копия ROI для вывода результата
roi_output = roi.copy()

if largest_contour is not None:
    # Определяем минимальный описывающий круг для найденного контура
    (x, y), radius = cv2.minEnclosingCircle(largest_contour)
    center = (int(x), int(y))
    radius = int(radius)
    cv2.circle(roi_output, center, radius, (0, 255, 0), thickness=3)
    
    print("Найден круг чашки Петри:")
    print("  Центр (в координатах ROI):", center)
    print("  Радиус:", radius)
else:
    print("Круг не найден.")

# Окно вывода: его размеры устанавливаются пропорционально ROI
cv2.namedWindow("Результат", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Результат", roi_width // 5, roi_height // 5)
cv2.imshow("Результат", roi_output)
cv2.waitKey(0)
cv2.destroyAllWindows()
