import os
from PIL import Image
import rawpy  # Для обробки RAW-зображень
import numpy as np
import pandas as pd

def calculate_brightness(img_path):
    """ Обчислює середню яскравість зображення для JPEG/RAW """
    if img_path.lower().endswith('.orf'):
        # Обробка RAW-зображення через rawpy
        with rawpy.imread(img_path) as raw:
            rgb = raw.postprocess()
        img = Image.fromarray(rgb).convert("L")  # Конвертуємо у ч/б
    else:
        # Обробка стандартних форматів (JPEG, PNG тощо)
        img = Image.open(img_path).convert("L")
    
    # Обчислюємо середню яскравість
    return np.mean(img)

def analyze_images(image_dir):
    """ Аналізує яскравість зображень та створює порівняльні таблиці в Excel. """
    image_files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(('.orf', '.jpeg', '.jpg'))])
    results = []

    for file in image_files:
        file_path = os.path.join(image_dir, file)
        try:
            brightness = calculate_brightness(file_path)
            format_group = "ORF" if file.lower().endswith(".orf") else "JPEG"
            results.append({
                'Filename': file,
                'Format': format_group,
                'Brightness': brightness
            })
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    df = pd.DataFrame(results)
    df['Rank_in_Group'] = df.groupby('Format')['Brightness'].rank(ascending=False, method='min')
    df['Rank_Global'] = df['Brightness'].rank(ascending=False, method='min')

    output_file = os.path.join(image_dir, "image_brightness_analysis.xlsx")
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.sort_values(by=['Filename']).to_excel(writer, sheet_name='Initial Data', index=False)
        df.sort_values(by=['Format', 'Rank_in_Group']).to_excel(writer, sheet_name='Sorted by Group', index=False)
        df.sort_values(by=['Rank_Global']).to_excel(writer, sheet_name='Sorted Globally', index=False)
    
    print(f"Excel файл створено: {output_file}")

# Вказуємо директорію
image_dir = r"G:\My\sov\extract"
analyze_images(image_dir)


