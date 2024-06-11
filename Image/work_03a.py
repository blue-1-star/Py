import cv2
from PIL import Image
import pytesseract

# Загрузка изображения с использованием OpenCV
im_path ="G:/Programming/Py/Image/data/"

filename = "p0002.png"
image_path = im_path + filename 
image = cv2.imread(image_path)

# Интерактивный выбор области интереса (ROI)
# Появится окно с изображением, в котором можно выделить область интереса мышью
roi = cv2.selectROI("Select ROI", image, showCrosshair=True, fromCenter=False)

# Координаты области интереса
x_start, y_start, width, height = roi
x_end = x_start + width
y_end = y_start + height

# Обрезка изображения до области интереса
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
