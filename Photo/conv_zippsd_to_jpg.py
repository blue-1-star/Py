import os
import zipfile
from psd_tools import PSDImage
from PIL import Image

def convert_psd_archive(archive_path, output_dir, output_format="png"):
    # Создаём выходную папку
    os.makedirs(output_dir, exist_ok=True)

    # Временная папка для распаковки
    temp_dir = os.path.join(output_dir, "_temp")
    os.makedirs(temp_dir, exist_ok=True)

    # Распаковываем архив
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Перебираем все .psd файлы
    for root, _, files in os.walk(temp_dir):
        for file in files:
            if file.lower().endswith(".psd"):
                psd_path = os.path.join(root, file)
                output_name = os.path.splitext(file)[0] + "." + output_format.lower()
                output_path = os.path.join(output_dir, output_name)

                try:
                    psd = PSDImage.open(psd_path)
                    img = psd.composite()  # собираем слои в итоговое изображение
                    img.save(output_path)
                    print(f"✔ {file} → {output_name}")
                except Exception as e:
                    print(f"Ошибка с {file}: {e}")

    # Чистим временные файлы
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)


# Пример вызова:
# convert_psd_archive("photos.zip", "converted", output_format="jpg")
