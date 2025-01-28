import rawpy
from PIL import Image
import os

import rawpy
from PIL import Image
import os

def process_raw(filename):
    with rawpy.imread(filename) as raw:
        rgb = raw.postprocess(use_camera_wb=True, half_size=False, output_bps=16)
        img = Image.fromarray(rgb)

        # Получаем путь к выходному файлу с новым расширением
        output_filename, _ = os.path.splitext(filename)
        output_filename += ".png"

        img.save(output_filename)

# Замените 'путь_к_файлу.ARW' на ваш файл

# Замените 'путь_к_файлу.ARW' на ваш файл
input_folder = r"G:\My\sov\extract\ORF\A" 
output_folder = r"G:\My\sov\extract\ORF\A" 
process_raw(input_folder)
