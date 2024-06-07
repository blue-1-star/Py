from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import os

# Загрузка изображения
im_path ="G:/Programming/Py/Image/data/"
# filename = "id_cod_e.bmp"
filename = "id_cod.bmp"
image_path = im_path + filename 
image = Image.open(image_path)

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

# Используем предоставленные координаты
# x, y, w, h = 770, 330, 250, 20
x, y, w, h = 760, 334, 145, 20
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
nfile, ext = os.path.splitext(filename)[0].lower(), os.path.splitext(filename)[1].lower()  
# processed_image_path = os.path.join( im_path,  nfile , '.png')
processed_image_path =  im_path +  nfile + '.png'
# target_path = os.path.join(target_directory, date_folder, filename)
processed_image.save(processed_image_path)

# Отображаем результат
processed_image.show()

processed_image_path

