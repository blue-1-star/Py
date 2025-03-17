import cv2 as cv
import sys
import xlsxwriter
from PIL import Image
import easyocr
import os
import pandas as pd
from glob import glob
import time
import numpy as np
from pathlib import Path


def load_scale_data(excel_path):
    """
    Загружает данные о масштабе из Excel-файла.
    
    :param excel_path: Путь к Excel-файлу.
    :return: Словарь, где ключ — имя файла с расширением .jpg, значение — масштаб (pix/mm).
    """
    df = pd.read_excel(excel_path)
    # Добавляем .jpg к каждому имени файла
    scale_dict = {f"{file_name}.jpg": scale for file_name, scale in zip(df["File Name"], df["Scale pix/mm"])}
    return scale_dict


def getting_pixel_counts(img_path, show_images=False):
    """
    Вычисляет количество зелёных пикселей на изображении.
    
    :param img_path: Путь к изображению.
    :param show_images: Показывать ли изображения (для отладки).
    :return: Количество зелёных пикселей и общее количество пикселей.
    """
    img = cv.imread(img_path)
    if img is None:
        sys.exit("Could not read image")
    
    resized_img = cv.resize(img, (500, 500), interpolation=cv.INTER_LINEAR)
    
    # Преобразуем изображение в HSV
    hsv_img = cv.cvtColor(resized_img, cv.COLOR_BGR2HSV)
    
    # Создаем маску для зелёных цветов
    mask = cv.inRange(hsv_img, (40, 100, 20), (80, 255, 255))
    
    if show_images:
        cv.imshow("Original Image", img)
        cv.imshow("Resized Image", resized_img)
        cv.imshow("Green Mask", mask)
        
        k = cv.waitKey(0)
        cv.destroyAllWindows()
    
    white_pixel_count = cv.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    
    return white_pixel_count, total_pixels


def get_date_taken(image_path):
    """
    Получает дату создания изображения из EXIF-данных.
    
    :param image_path: Путь к изображению.
    :return: Дата и время создания или None, если EXIF-данные отсутствуют.
    """
    try:
        exif = Image.open(image_path)._getexif()
        if exif and 36867 in exif:  # 36867 — это код для даты создания
            return exif[36867]
        else:
            return None
    except Exception as e:
        print(f"Ошибка при получении EXIF-данных для {image_path}: {e}")
        return None


def get_sample_name(image_path):
    """
    Извлекает имя образца из изображения с помощью OCR.
    
    :param image_path: Путь к изображению.
    :return: Имя образца.
    """
    # reader = easyocr.Reader(['en'])
    reader = easyocr.Reader(['en'], verbose=False)
    output_array = reader.readtext(image_path, detail=0)
    return output_array[-1]


def visualize_green_contours(img_path, output_folder):
    """
    Визуализирует контуры зелёных листьев и сохраняет результат.
    
    :param img_path: Путь к исходному изображению.
    :param output_folder: Каталог для сохранения результата.
    """
    # Загружаем изображение
    img = cv.imread(img_path)
    if img is None:
        print(f"Не удалось загрузить изображение: {img_path}")
        return
    
    # Преобразуем изображение в HSV
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
    # Создаем маску для зелёных цветов
    mask = cv.inRange(hsv_img, (40, 100, 20), (80, 255, 255))
    
    # Находим контуры
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    # Рисуем контуры на исходном изображении
    output_img = img.copy()
    # cv.drawContours(output_img, contours, -1, (0, 255, 0), 2)  # Зелёный цвет, толщина 2
    cv.drawContours(output_img, contours, -1, (0, 0, 255), 2)  # Красный цвет, толщина 2
    # Сохраняем результат
    output_path = os.path.join(output_folder, f"contour_{os.path.basename(img_path)}")
    cv.imwrite(output_path, output_img)


def generate_excel_file(folder_path, excel_file_name, scale_data):
    """
    Генерирует Excel-файл с данными о площади зелёных листьев.
    
    :param folder_path: Путь к каталогу с изображениями.
    :param excel_file_name: Имя выходного Excel-файла.
    :param scale_data: Словарь с данными о масштабе (pix/mm).
    """
    # Создаем Excel-файл в каталоге с изображениями
    excel_file_path = os.path.join(folder_path, excel_file_name)
    workbook = xlsxwriter.Workbook(excel_file_path)
    worksheet = workbook.add_worksheet()
    
    # Заголовки таблицы
    header_data = [
        "FILE NAME", "SAMPLE NAME", "DATE", "TIME", 
        "SCALE (pix/mm)", "WHITE PIXEL COUNT", "TOTAL PIXELS", 
        "WHITE PIXEL PERCENTAGE", "WHITE PIXELS MM^2"
    ]
    header_format = workbook.add_format({'bold': True, 'bottom': 2})
    
    # Записываем заголовки
    for col_num, data in enumerate(header_data):
        worksheet.write(0, col_num, data, header_format)
    
    # Создаем подкаталог для контуров
    contours_folder = os.path.join(folder_path, "contours")
    if not os.path.exists(contours_folder):
        os.makedirs(contours_folder)
    
    # Обрабатываем изображения
    image_files = glob(os.path.join(folder_path, "*.jpg"))
    row = 1
    for cur_img_path in image_files:
        file_name = os.path.basename(cur_img_path)
        print(f"Обрабатывается файл: {file_name}")
        
        # Визуализируем контуры
        visualize_green_contours(cur_img_path, contours_folder)
        
        # Получаем данные из файла
        sample_name = get_sample_name(cur_img_path)
        
        # Получаем дату и время
        img_date_time = get_date_taken(cur_img_path)
        if img_date_time:
            img_date, img_time = img_date_time.split(" ")
        else:
            img_date, img_time = "N/A", "N/A"
        
        # Получаем масштаб из словаря
        scale_pix_per_mm = scale_data.get(file_name)
        if scale_pix_per_mm is None:
            print(f"Масштаб для файла {file_name} не найден. Доступные ключи: {list(scale_data.keys())}")
            continue
        
        # Получаем данные о зелёных пикселях
        # white_pixels, total_pixels = getting_pixel_counts(cur_img_path, show_images=False)
        white_pixels, total_pixels = getting_pixel_counts(cur_img_path, show_images=True)
        white_percent = (white_pixels / total_pixels) * 100
        white_percent_rounded = round(white_percent, 2)
        
        # Вычисляем площадь зелёных листьев в мм^2
        white_pixels_area_mm = round((white_pixels / (scale_pix_per_mm ** 2)), 2)
        
        # Записываем данные в строку
        row_data = [
            file_name, sample_name, img_date, img_time, scale_pix_per_mm,
            white_pixels, total_pixels, f"{white_percent_rounded}%", white_pixels_area_mm
        ]
        
        # Записываем строку в Excel
        worksheet.write_row(row, 0, tuple(row_data))
        row += 1
    
    # Автоматически подгоняем ширину столбцов
    worksheet.autofit()
    
    # Закрываем Excel-файл
    workbook.close()
    print(f"Excel-файл создан: {excel_file_path}")


if __name__ == "__main__":
    # Путь к каталогу с изображениями
    # img_folder = r"G:\My\sov\extract\plant1"
    img_folder = r"G:\My\sov\extract\plant2"
    
    # Путь к Excel-файлу с масштабами
    # scale_excel_path = r"G:\My\sov\extract\plant1\file_list.xlsx"
    scale_excel_path = r"G:\My\sov\extract\plant2\file_list.xlsx"
    
    # Загружаем данные о масштабе
    scale_data = load_scale_data(scale_excel_path)
    
    # Генерируем Excel-файл
    start_time = time.time()
    generate_excel_file(img_folder, "Green_area_analysis.xlsx", scale_data)
    print(f"Время выполнения: {int(time.time() - start_time)} секунд")