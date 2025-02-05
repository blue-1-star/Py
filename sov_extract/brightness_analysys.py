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
def process_image(img_path):
    if img_path.lower().endswith('.orf'):
        with rawpy.imread(img_path) as raw:
            rgb = raw.postprocess()
        img = Image.fromarray(rgb)
    else:
        img = Image.open(img_path)
    return img

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

def rgb_to_hsv(rgb_array):
    """
    Преобразует массив RGB в HSV.

    Параметры:
        rgb_array (numpy.ndarray): Массив RGB с формой (height, width, 3).

    Возвращает:
        hsv_array (numpy.ndarray): Массив HSV с формой (height, width, 3).
    """
    # Преобразуем RGB в HSV с помощью OpenCV
    hsv_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2HSV)
    return hsv_array


def get_hsv_histograms(hsv_array):
    """
    Вычисляет гистограммы для каналов HSV.

    Параметры:
        hsv_array (numpy.ndarray): Массив HSV с формой (height, width, 3).

    Возвращает:
        hist_hue (numpy.ndarray): Гистограмма для канала Hue.
        hist_saturation (numpy.ndarray): Гистограмма для канала Saturation.
        hist_value (numpy.ndarray): Гистограмма для канала Value.
        bin_edges (numpy.ndarray): Границы бинов для гистограмм.
    """
    # Извлекаем каналы HSV
    hue_channel = hsv_array[:, :, 0].flatten()  # Оттенок (0–179)
    saturation_channel = hsv_array[:, :, 1].flatten()  # Насыщенность (0–255)
    value_channel = hsv_array[:, :, 2].flatten()  # Яркость (0–255)
     # Вычисляем гистограммы
    hist_hue, bin_edges = np.histogram(hue_channel, bins=180, range=(0, 180))
    hist_saturation, _ = np.histogram(saturation_channel, bins=256, range=(0, 256))
    hist_value, _ = np.histogram(value_channel, bins=256, range=(0, 256))

    return hist_hue, hist_saturation, hist_value, bin_edges

def plot_hist1(hue_channel, output_dir):

    plt.hist(hue_channel.flatten(), bins=180, range=(0, 180), color='red', alpha=0.7)
    plt.title("Гистограмма оттенков (Hue)")
    plt.xlabel("Hue")
    plt.ylabel("Частота")
    plt.show()


    # Вычисляем гистограммы
    hist_hue, bin_edges = np.histogram(hue_channel, bins=180, range=(0, 180))
    hist_saturation, _ = np.histogram(saturation_channel, bins=256, range=(0, 256))
    hist_value, _ = np.histogram(value_channel, bins=256, range=(0, 256))
    
    return hist_hue, hist_saturation, hist_value, bin_edges

# 2025-02-05 06:31:45

import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def plot_hist(channel, image_path, shape='rectangle', size=(100, 100), channel_name='Hue'):
    """
    Строит и сохраняет гистограмму для указанного канала.

    Параметры:
        channel (numpy.ndarray): Канал изображения (Hue, Saturation, Value).
        image_path (str): Путь к исходному изображению.
        shape (str): Форма области (например, 'rectangle' или 'ellipse').
        size (tuple): Размер области (ширина, высота).
        channel_name (str): Название канала ('Hue', 'Saturation', 'Value').
    """
    # Определяем каталог для сохранения
    image_dir = os.path.dirname(image_path)
    contour_dir = os.path.join(image_dir, "contour")
    os.makedirs(contour_dir, exist_ok=True)

    # Извлекаем имя файла без расширения
    filename = os.path.splitext(os.path.basename(image_path))[0]

    # Определяем имя файла для гистограммы
    hist_name = f"h{channel_name[0]}"  # hH, hS, hV
    hist_path = os.path.join(contour_dir, f"{filename}_{shape[0]}_{hist_name}.png")
    hist_data_path = os.path.join(contour_dir, f"{filename}_{shape[0]}_hdig_{hist_name}.txt")

    # Строим гистограмму
    plt.figure()
    plt.hist(channel.flatten(), bins=180, range=(0, 180), color='red', alpha=0.7)
    plt.title(f"Гистограмма {channel_name} для изображения {filename}")
    plt.xlabel(channel_name)
    plt.ylabel("Частота")
    plt.savefig(hist_path)  # Сохраняем график
    plt.close()

    # Сохраняем числовые данные гистограммы
    hist_values, bin_edges = np.histogram(channel.flatten(), bins=180, range=(0, 180))
    np.savetxt(hist_data_path, hist_values, fmt='%d')  # Сохраняем данные в текстовый файл

    print(f"Гистограмма {channel_name} сохранена в {hist_path}")
    print(f"Числовые данные гистограммы сохранены в {hist_data_path}")

def plot_hist_with_image(channel, image_path, shape='rectangle', size=(100, 100), channel_name='Hue'):
    """
    Строит и сохраняет гистограмму вместе с исходным изображением.

    Параметры:
        channel (numpy.ndarray): Канал изображения (Hue, Saturation, Value).
        image_path (str): Путь к исходному изображению.
        shape (str): Форма области (например, 'rectangle' или 'ellipse').
        size (tuple): Размер области (ширина, высота).
        channel_name (str): Название канала ('Hue', 'Saturation', 'Value').
    """
    # Определяем каталог для сохранения
    image_dir = os.path.dirname(image_path)
    contour_dir = os.path.join(image_dir, "contour")
    os.makedirs(contour_dir, exist_ok=True)

    # Извлекаем имя файла без расширения
    filename = os.path.splitext(os.path.basename(image_path))[0]

    # Определяем имя файла для гистограммы
    hist_name = f"h{channel_name[0]}"  # hH, hS, hV
    hist_path = os.path.join(contour_dir, f"{filename}_{shape[0]}_{hist_name}_with_image.png")
    cont_path = os.path.join(contour_dir, f"{filename}_{shape[0]}.png")
    # Загружаем исходное изображение
    # img = Image.open(image_path)
    img = Image.open(cont_path)
    # img = process_image(image_path)  # Используем вашу функцию для обработки RAW-файлов
    # Создаём полотно с двумя графиками
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Отображаем исходное изображение
    ax1.imshow(img)
    ax1.set_title(f"Исходное изображение: {filename}")
    ax1.axis('off')

    # Строим гистограмму
    ax2.hist(channel.flatten(), bins=180, range=(0, 180), color='red', alpha=0.7)
    ax2.set_title(f"Гистограмма {channel_name} для изображения {filename}")
    ax2.set_xlabel(channel_name)
    ax2.set_ylabel("Частота")

    # Сохраняем полотно
    plt.tight_layout()
    plt.savefig(hist_path)
    plt.close()

    print(f"Гистограмма {channel_name} с изображением сохранена в {hist_path}")

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

