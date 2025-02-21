import os
from PIL import Image

def reduce_images_in_dir(dir_path):
    """
    Проходит по всем файлам в каталоге dir_path (включая вложенные папки) и для каждого файла с расширением .png,
    в имени которого присутствует суффикс '_comt_sel', уменьшает его размер, масштабируя изображение так, чтобы
    его площадь стала примерно в 10 раз меньше (коэффициент масштабирования ≈ 0.316).
    
    Функция сохраняет изменённое изображение, перезаписывая исходный файл.
    """
    # Коэффициент масштабирования по каждой оси для уменьшения площади в 10 раз
    scale_factor = 0.316

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.lower().endswith('.png') and '_cont_sel' in file:
                file_path = os.path.join(root, file)
                try:
                    with Image.open(file_path) as img:
                        original_width, original_height = img.size
                        new_width = max(1, int(original_width * scale_factor))
                        new_height = max(1, int(original_height * scale_factor))
                        
                        # Изменение размера с использованием качественной интерполяции
                        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
                        
                        # Сохраняем изображение с оптимизацией
                        resized_img.save(file_path, optimize=True)
                        
                        print(f"Файл '{file}' изменён: {original_width}x{original_height} -> {new_width}x{new_height}")
                except Exception as e:
                    print(f"Ошибка обработки файла {file_path}: {e}")

# Пример вызова функции:
import os
import glob
from PIL import Image

def reduce_images_com(input_dir, output_dir, pattern="*", zoom=0.1):
    # Создаем директорию для вывода, если она не существует
    os.makedirs(output_dir, exist_ok=True)
    
    # Формируем полный путь для поиска файлов
    search_pattern = os.path.join(input_dir, pattern)
    files = glob.glob(search_pattern)
    
    if not files:
        print("Нет файлов, соответствующих шаблону.")
        return
    
    for file in files:
        try:
            with Image.open(file) as img:
                # Вычисляем новые размеры изображения
                new_width = int(img.width * zoom)
                new_height = int(img.height * zoom)
                
                # Создаем уменьшенную копию изображения с учетом сглаживания
                reduced_img = img.resize((new_width, new_height), Image.ANTIALIAS)
                
                # Формируем путь для сохранения обработанного файла
                output_file = os.path.join(output_dir, os.path.basename(file))
                reduced_img.save(output_file)
                
                print(f"Обработан файл: {file} -> {output_file}")
        except Exception as e:
            print(f"Ошибка при обработке файла {file}: {e}")



dir = r"G:\My\sov\extract\Spores\original_img\test\test_reduce"
reduce_images_in_dir(dir)

