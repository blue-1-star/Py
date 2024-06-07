from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

# Загрузка изображения
# image_path = 'data/Flat_Sv_TMP1.jpg'
# image_path =r"G:\Programming\Py\Image\data\Flat_Sv_TMP1.jpg"
# image_path =r"G:\Programming\Py\Image\data\id_cod_e.bmp"
im_path ="G:/Programming/Py/Image/data/"
filename = "id_cod_e.bmp"
image_path = im_path + filename 
image = Image.open(image_path)
# image.show()
# Предобработка изображения
# Применим фильтр для увеличения резкости
sharpened_image = image.filter(ImageFilter.SHARPEN)

# Увеличим контрастность изображения
enhancer = ImageEnhance.Contrast(sharpened_image)
contrast_image = enhancer.enhance(2)  # Параметр 2 можно изменить для регулировки контраста

# Преобразуем изображение в оттенки серого
gray_image = contrast_image.convert('L')

# Преобразование изображения в массив numpy для дальнейшей обработки
image_array = np.array(gray_image)

# Предположим, что у нас есть координаты области, где находится ID номер
# Эти координаты можно определить вручную или автоматически с использованием OCR инструментов
x, y, w, h = 100, 50, 200, 30  # Примерные координаты (x, y, ширина, высота)

# Извлекаем область с ID номером
id_region = image_array[y:y+h, x:x+w]

# Применяем дополнительную обработку к этой области (например, увеличение яркости)
id_region = Image.fromarray(id_region)
enhancer = ImageEnhance.Brightness(id_region)
id_region = enhancer.enhance(1.5)  # Параметр 1.5 можно изменить для регулировки яркости

# Вставляем обработанную область обратно в изображение
image_array[y:y+h, x:x+w] = np.array(id_region)

# Преобразуем массив обратно в изображение
processed_image = Image.fromarray(image_array)

# Сохраняем обработанное изображение
processed_image.save('G:/Programming/Py/Image/data/id_cod_e.png')

# Отображаем результат
processed_image.show()
