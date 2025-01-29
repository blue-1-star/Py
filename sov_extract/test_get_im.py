import os
import re
# from  brightness_analysys_1b import get_image_files_with_meta_se
from brightness_analysys_1b import get_image_files_with_metadata, get_elements_by_index, extract_number_from_filename,\
    get_image_files_with_meta_se
image_dir = r"G:\My\sov\extract\ORF\AF" # Ваш путь к папке с изображениями
files_with_meta = get_image_files_with_meta_se(image_dir)
for file_info in files_with_meta:
    print(file_info)