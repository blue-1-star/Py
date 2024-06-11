# Import PIL (Note: the package name is Pillow, yet we import from PIL).
# Yes, the import here is confusing. More context here: https://pypi.org/project/Pillow/
from PIL import Image

# Import pytesseract (a Python wrapper for Tesseract)
# Note: You will need to have Tesseract installed on your machine for pytesseract to work.
import pytesseract

# Extract text from the image
im_path ="G:/Programming/Py/Image/data/"
# filename = "id_cod_e.bmp"
# filename = "test.jpg"
filename = "p0002.png"
image_path = im_path + filename 
image = Image.open(image_path)
# image.show()
extracted_text = pytesseract.image_to_string(image, lang='ukr+eng')
# Write the extracted text to a file
# filename.replace()
txt_path = im_path + filename[:-3]+'txt' 
with open(txt_path, 'w') as f:
    f.write(extracted_text)
print(extracted_text)

"""
ROI for OCR
import cv2
from PIL import Image
import pytesseract

# Загрузка изображения с использованием OpenCV
image_path = "path_to_your_image.jpg"
image = cv2.imread(image_path)

# Указание координат области интереса (ROI)
# Формат: [y_start:y_end, x_start:x_end]
x_start, y_start, x_end, y_end = 100, 100, 400, 400
roi = image[y_start:y_end, x_start:x_end]

# Преобразование области интереса в формат PIL Image
roi_pil = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))

# Извлечение текста из области интереса с помощью Tesseract
extracted_text = pytesseract.image_to_string(roi_pil, lang='eng')

# Вывод извлеченного текста
print(extracted_text)

# Отображение оригинального изображения и области интереса (ROI)
cv2.imshow('Original Image', image)
cv2.imshow('Region of Interest', roi)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
#  
"""
import cv2
from PIL import Image
import pytesseract

# Загрузка изображения с использованием OpenCV
image_path = "path_to_your_image.jpg"
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
extracted_text = pytesseract.image_to_string(roi_pil, lang='eng')

# Вывод извлеченного текста
print(extracted_text)

# Отображение оригинального изображения и области интереса (ROI)
cv2.imshow('Original Image', image)
cv2.imshow('Region of Interest', roi_cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
