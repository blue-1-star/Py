from PIL import Image
import os
import rawpy
# input_folder = r"G:\My\sov\extract\ORF\A" 
input_folder = r"G:\My\sov\extract\ORF\Work" 
output_folder = r"G:\My\sov\extract\ORF\A" 
import shutil

def process_files(input_dir, output_dir=None):
    """
    Преобразует файлы в указанном каталоге в формат PNG.
    Если файл является RAW, то обрабатывается функцией process_raw.

    Args:
        input_dir (str): Путь к входному каталогу.
        output_dir (str, optional): Путь к выходному каталогу. По умолчанию совпадает с входным.
    """

    if output_dir is None:
        output_dir = input_dir

    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.bmp']:  # Список поддерживаемых форматов
                # Если файл уже PNG, JPG, BMP, то просто копируем
                shutil.copy2(filepath, output_dir)
            elif ext in ['.orf', '.arw', '.cr2', '.nef', '.dng']:  # Список поддерживаемых RAW форматов
                process_raw(filepath, output_dir)
            else:
                print(f"Неподдерживаемый формат файла: {filename}")

def process_raw(filename, output_dir):
    print(f"Обрабатывается файл: {filename}")
    with rawpy.imread(filename) as raw:
        # rgb = raw.postprocess(use_camera_wb=True, half_size=False, output_bps=16)
        rgb = raw.postprocess()
        img = Image.fromarray(rgb)

        # Получаем имя файла без расширения и добавляем .png
        output_filename = os.path.splitext(filename)[0] + ".png"
        output_path = os.path.join(output_dir, output_filename)

        img.save(output_path)

# Пример использования:
# output_dir = "путь_к_выходному_каталогу"  # Если нужно другой каталог
process_files(input_folder)
