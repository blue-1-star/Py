import os
from psd_tools import PSDImage

def convert_psd_folder(input_dir, output_dir, output_format="png"):
    # Создаём выходную папку
    os.makedirs(output_dir, exist_ok=True)

    # Перебираем все файлы в папке
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".psd"):
                psd_path = os.path.join(root, file)
                output_name = os.path.splitext(file)[0] + "." + output_format.lower()
                output_path = os.path.join(output_dir, output_name)

                try:
                    psd = PSDImage.open(psd_path)
                    img = psd.composite()  # собираем все слои
                    img.save(output_path)
                    print(f"✔ {file} → {output_name}")
                except Exception as e:
                    print(f"Ошибка с {file}: {e}")


# Пример использования:
# convert_psd_folder("C:/Users/User/Pictures/psd_folder", "C:/Users/User/Pictures/converted", "jpg")
# input_dir = r"E:\Photo\Scan_Family\1\u1"
input_dir = r"E:\Photo\Scan_Family\3\U3"
subfolder = "jpg"
output_dir = os.path.join(input_dir,subfolder)

convert_psd_folder(input_dir,output_dir ,subfolder)

