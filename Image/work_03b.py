import cv2
from PIL import Image
import pytesseract

# Загрузка изображения с использованием OpenCV
im_path ="G:/Programming/Py/Image/data/"

filename = "p0002.png"
image_path = im_path + filename 
image = cv2.imread(image_path)

# Уменьшение масштаба изображения (например, до 50% от оригинального размера)
scale_percent = 25  # Процент от оригинального размера
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

# Изменение размера изображения
resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Интерактивный выбор области интереса (ROI) на уменьшенном изображении
roi = cv2.selectROI("Select ROI", resized_image, showCrosshair=True, fromCenter=False)

# Преобразование координат ROI на оригинальное изображение
x_start, y_start, roi_width, roi_height = roi
x_start = int(x_start * 100 / scale_percent)
y_start = int(y_start * 100 / scale_percent)
roi_width = int(roi_width * 100 / scale_percent)
roi_height = int(roi_height * 100 / scale_percent)
x_end = x_start + roi_width
y_end = y_start + roi_height

# Обрезка изображения до области интереса на оригинальном изображении
roi_cropped = image[y_start:y_end, x_start:x_end]

# Преобразование области интереса в формат PIL Image
roi_pil = Image.fromarray(cv2.cvtColor(roi_cropped, cv2.COLOR_BGR2RGB))

# Извлечение текста из области интереса с помощью Tesseract
extracted_text = pytesseract.image_to_string(roi_pil, lang='ukr')

# Вывод извлеченного текста
print(extracted_text)

# Отображение оригинального изображения и области интереса (ROI)
cv2.imshow('Original Image', image)
cv2.imshow('Region of Interest', roi_cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
