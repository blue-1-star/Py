import pytesseract
from PIL import Image
import cv2
import numpy as np

# Загрузка изображения
im_path ="G:/Programming/Py/Image/data/"
# filename = "id_cod_e.bmp"
filename = "id_cod.bmp"
image_path = im_path + filename 
image = Image.open(image_path)

# Преобразуем изображение в оттенки серого
gray_image = image.convert('L')

# Преобразуем изображение в массив numpy
image_array = np.array(gray_image)

# Применим пороговое значение для улучшения контраста
_, thresh_image = cv2.threshold(image_array, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Используем pytesseract для распознавания текста
custom_config = r'--oem 3 --psm 6 outputbase digits'
detection_data = pytesseract.image_to_data(thresh_image, config=custom_config, output_type=pytesseract.Output.DICT)

# Извлекаем координаты и текст
num_boxes = len(detection_data['level'])
recognized_digits = []
for i in range(num_boxes):
    if detection_data['text'][i].strip().isdigit():
        (x, y, w, h) = (detection_data['left'][i], detection_data['top'][i], detection_data['width'][i], detection_data['height'][i])
        recognized_digits.append({
            'digit': detection_data['text'][i],
            'x': x,
            'y': y,
            'w': w,
            'h': h
        })

recognized_digits
