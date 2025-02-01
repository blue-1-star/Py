import os
import cv2
import numpy as np
from PIL import Image, ImageStat, ImageDraw, PngImagePlugin
from datetime import datetime
import tempfile
import rawpy
# from brightness_analysys_2a import process_image
# def draw_brightness_area(image, shape='square', size=100):
#     """
#     Накладывает контур выделенной области на изображение.
#     Возвращает обработанное изображение.
#     """
#     image = np.array(image)
#     height, width, _ = image.shape
#     center_x, center_y = width // 2, height // 2
    
#     if shape == 'square':
#         top_left = (center_x - size // 2, center_y - size // 2)
#         bottom_right = (center_x + size // 2, center_y + size // 2)
#         cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
#     elif shape == 'circle':
#         cv2.circle(image, (center_x, center_y), size // 2, (0, 255, 0), 2)
    
#     return Image.fromarray(image)

def save_image_with_contour(image, image_path, output_folder='output'):
    """Сохраняет изображение с контуром."""
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.splitext(os.path.basename(image_path))[0]
    output_path = os.path.join(output_folder, f"{filename}_.png")
    image.save(output_path)
    return output_path



def images_to_pdf(image_paths, pdf_path):
    """Объединяет список изображений в PDF."""
    images = [Image.open(img).convert('RGB') for img in image_paths]
    images[0].save(pdf_path, save_all=True, append_images=images[1:])

def process_images_to_pdf(image_paths, pdf_output='output/processed_images.pdf'):
    """
    Обрабатывает список изображений, создавая контуры и PDF.
    """
    processed_images = [draw_brightness_area(img) for img in image_paths]
    images_to_pdf(processed_images, pdf_output)
    print(f'PDF сохранен: {pdf_output}')


def reduce_image_size(input_file, output_file, quality=90):
    """
    Уменьшает размер изображения.

    Args:
        input_file (str): Путь к исходному файлу.
        output_file (str): Путь к выходному файлу.
        quality (int, optional): Качество сжатия (от 1 до 95). По умолчанию 90.
    """

    try:
        img = Image.open(input_file)
        img.save(output_file, optimize=True, quality=quality)
        print(f"Размер изображения успешно уменьшен: {input_file} -> {output_file}")
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")


# def crop_image_x(image_path, image, shape='rectangle', size=(100, 100) ):
def crop_image_x(image, image_path, shape='rectangle', size=(100, 100) ):
    """
    Вырезает заданную область (прямоугольник или эллипс) из изображения,
    накладывает контур и сохраняет изображение с контурами.
    """
    width, height = image.size
    center_x, center_y = width // 2, height // 2
    size_x, size_y = size
    
    # Создание копии изображения для наложения контура
    image_with_contour = image.copy()
    # начертание контура  в файле  image_with_contour
    draw_brightness_area(image_with_contour, shape, (center_x, center_y), size)
    
    # Сохранение изображения с контуром
    image_dir = os.path.dirname(image_path)
    contour_dir = os.path.join(image_dir, "contour")
    os.makedirs(contour_dir, exist_ok=True)
    # Извлекаем имя файла без расширения
    filename = os.path.splitext(os.path.basename(image_path))[0]
    contour_path = os.path.join(contour_dir, f"{filename}_{shape[0]}.png")

    # image.save(output_path)

    # Добавление метаданных
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("shape", shape)
    metadata.add_text("center", f"{center_x},{center_y}")
    metadata.add_text("size", f"{size_x},{size_y}")
    
    # image_with_contour.save(contour_path, "PNG", pnginfo=metadata, optimize=True, quality=10)
    image_with_contour.save(contour_path, "JPEG", quality=50)
    # img.save(output_file, optimize=True, quality=quality)
    
    # Обрезка изображения
    if shape == 'rectangle':
        left = max(center_x - size_x // 2, 0)
        upper = max(center_y - size_y // 2, 0)
        right = min(center_x + size_x // 2, width)
        lower = min(center_y + size_y // 2, height)
        return image.crop((left, upper, right, lower))
    
    elif shape == 'ellipse':
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse(
            (center_x - size_x // 2, center_y - size_y // 2,
             center_x + size_x // 2, center_y + size_y // 2),
            fill=255
        )
        result = Image.composite(image, Image.new("RGB", image.size, (0, 0, 0)), mask)
        bbox = mask.getbbox()
        return result.crop(bbox)

# 
# 
# def crop_image_x(image, image_path, shape='rectangle', size=(100, 100)):
#     """
#     Вырезает заданную область (прямоугольник или эллипс) из изображения и сохраняет контур в подкаталог.
#     """
#     width, height = image.size
#     center_x, center_y = width // 2, height // 2

#     # Обработка аргумента size
#     if isinstance(size, int):
#         size_x, size_y = size, size
#     else:
#         size_x, size_y = size

#     # Создаём путь для сохранения изображения с контуром
#     image_dir = os.path.dirname(image_path)
#     contour_dir = os.path.join(image_dir, "contour")
#     os.makedirs(contour_dir, exist_ok=True)

#     filename = os.path.splitext(os.path.basename(image_path))[0]
#     contour_path = os.path.join(contour_dir, f"{filename}_contour.png")

#     if shape == 'rectangle':
#         left = max(center_x - size_x // 2, 0)
#         upper = max(center_y - size_y // 2, 0)
#         right = min(center_x + size_x // 2, width)
#         lower = min(center_y + size_y // 2, height)
#         cropped_img = image.crop((left, upper, right, lower))

#     elif shape == 'ellipse':
#         mask = Image.new("L", image.size, 0)
#         draw = ImageDraw.Draw(mask)
#         draw.ellipse(
#             (center_x - size_x // 2, center_y - size_y // 2,
#              center_x + size_x // 2, center_y + size_y // 2),
#             fill=255
#         )
#         result = Image.composite(image, Image.new("RGB", image.size, (0, 0, 0)), mask)
#         bbox = mask.getbbox()
#         cropped_img = result.crop(bbox)

#     else:
#         print(f"Warning: Unknown shape '{shape}', returning original image.")
#         return image

#     # Сохраняем вырезанный контур в каталог "contour"
#     cropped_img.save(contour_path)
#     print(f"Контур сохранён: {contour_path}")

#     return cropped_img



def draw_brightness_area(image, shape, center, size):
    """
    Накладывает контур выделенной области на изображение.
    """
    draw = ImageDraw.Draw(image)
    center_x, center_y = center
    size_x, size_y = size
    
    if shape == 'rectangle':
        left = center_x - size_x // 2
        upper = center_y - size_y // 2
        right = center_x + size_x // 2
        lower = center_y + size_y // 2
        draw.rectangle([left, upper, right, lower], outline="red", width=3)
    
    elif shape == 'ellipse':
        draw.ellipse(
            (center_x - size_x // 2, center_y - size_y // 2,
             center_x + size_x // 2, center_y + size_y // 2),
            outline="red", width=3
        )


# Пример использования:
# input_image = "image.jpg"
# output_image = "image_compressed.jpg"
# reduce_image_size(input_image, output_image, quality=85)


# image_dir = r"G:\My\sov\extract\ORF\AF"  # Ваш путь к папке с изображениями
# current_date = datetime.now().strftime("%d_%m")
# output_dir = os.path.join(os.path.dirname(__file__), 'Data')
# output_file = os.path.join(output_dir, f"brightness_analys_6_{current_date}.xlsx")
# output_pdf = os.path.join(output_dir, f"bright_analys_6_{current_date}.pdf")
# lower_threshold = 0
# size = 500
# cont_folder = f"{image_dir}_contour"


# img =  draw_brightness_area(img, shape='square', size=size)
# contour_path = save_image_with_contour(img, img_path, output_folder=cont_folder)
# contour_paths.append(contour_path) 

