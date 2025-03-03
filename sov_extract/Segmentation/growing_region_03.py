import pandas as pd
import numpy as np
import cv2

def region_growing(image, seed, threshold):
    """
    Алгоритм роста области (region growing) с фиксированным порогом.
    
    :param image: входное изображение (numpy array)
    :param seed: начальная точка (x, y)
    :param threshold: порог для включения пикселей в область
    :return: маска (numpy array), где 1 - выделенная область, 0 - фон
    """
    h, w = image.shape[:2]
    mask = np.zeros((h, w), np.uint8)
    seed_x, seed_y = seed
    seed_value = image[seed_y, seed_x]

    # Очередь точек для проверки
    points = [(seed_x, seed_y)]
    mask[seed_y, seed_x] = 1

    while points:
        x, y = points.pop(0)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and mask[ny, nx] == 0:
                if abs(int(image[ny, nx]) - int(seed_value)) <= threshold:
                    mask[ny, nx] = 1
                    points.append((nx, ny))

    return mask

def find_spore(image_path, data_file, x, y):
    """
    Определяет, к какой споре принадлежит точка (x, y).
    
    :param image_path: путь к изображению
    :param data_file: путь к файлу auto_select_region.xlsx
    :param x: координата X точки
    :param y: координата Y точки
    :return: номер споры или -1, если точка не принадлежит ни одной
    """
    # Загружаем данные из Excel
    df = pd.read_excel(data_file)
    
    # Находим ближайшую seed-точку
    df['distance'] = np.sqrt((df['Seed X'] - x)**2 + (df['Seed Y'] - y)**2)
    closest_spore = df.loc[df['distance'].idxmin()]

    # Загружаем изображение
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"Ошибка загрузки изображения: {image_path}")

    # Применяем алгоритм region growing
    mask = region_growing(image, (closest_spore['Seed X'], closest_spore['Seed Y']), closest_spore['Threshold'])

    # Проверяем, принадлежит ли точка (x, y) найденной области
    if mask[y, x] == 1:
        return closest_spore['Spore Number']
    return -1

import cv2
import numpy as np
import pandas as pd

def remove_spore(image_path, overlay_path, data_file, x, y):
    """
    Удаляет спору, восстанавливая фон исходного изображения.
    
    :param image_path: путь к оригинальному изображению
    :param overlay_path: путь к оверлею, где нанесены споры
    :param data_file: путь к файлу auto_select_region.xlsx
    :param x: координата X точки, где кликнул пользователь
    :param y: координата Y точки, где кликнул пользователь
    :return: обновленный оверлей
    """
    # Загружаем изображение и оверлей
    original = cv2.imread(image_path)  # Оригинальное изображение (цветное)
    overlay = cv2.imread(overlay_path)  # Оверлей с нанесёнными спорами

    if original is None or overlay is None:
        raise ValueError("Ошибка загрузки изображений")

    # Определяем номер споры
    spore_number = find_spore(image_path, data_file, x, y)
    if spore_number == -1:
        print("Спора не найдена, ничего не удаляем.")
        return overlay

    # Загружаем данные и находим параметры споры
    df = pd.read_excel(data_file)
    spore_data = df[df["Spore Number"] == spore_number].iloc[0]

    # Получаем маску споры
    mask = region_growing(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE),
                          (spore_data["Seed X"], spore_data["Seed Y"]),
                          spore_data["Threshold"])

    # Восстанавливаем фон
    overlay[mask == 1] = original[mask == 1]

    return overlay
