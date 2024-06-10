import pytesseract
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Загрузка изображения
im_path = "G:/Programming/Py/Image/data/"
# filename = "id_cod.bmp"
filename ="processed_image.png"
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

# Выводим распознанные цифры с их координатами
for digit_info in recognized_digits:
    print(f"Цифра: {digit_info['digit']}, Координаты: (x={digit_info['x']}, y={digit_info['y']}), Ширина: {digit_info['w']}, Высота: {digit_info['h']}")

# Создаем копию исходного изображения для рисования
image_with_boxes = cv2.cvtColor(image_array, cv2.COLOR_GRAY2BGR)

# Рисуем прямоугольники вокруг распознанных цифр и добавляем текстовые аннотации
for digit_info in recognized_digits:
    x, y, w, h = digit_info['x'], digit_info['y'], digit_info['w'], digit_info['h']
    cv2.rectangle(image_with_boxes, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.putText(image_with_boxes, digit_info['digit'], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

# Преобразуем обратно в изображение PIL для отображения
image_with_boxes = Image.fromarray(image_with_boxes)

# Отображаем исходное изображение
plt.figure(figsize=(10, 10))
plt.imshow(gray_image, cmap='gray')
plt.title('Исходное изображение')
plt.show()

# Отображаем изображение с выделенными цифрами и аннотациями
plt.figure(figsize=(10, 10))
plt.imshow(image_with_boxes)
plt.title('Распознанные цифры с координатами')
plt.show()
