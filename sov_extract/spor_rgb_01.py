import cv2
import numpy as np

import pandas as pd

def read_imagej_csv_pandas(filepath):
    """
    Считывает CSV-файл, экспортированный из ImageJ, и возвращает
    DataFrame pandas со всеми столбцами.
    """
    # pandas сам попробует определить, какие столбцы можно интерпретировать как числа
    df = pd.read_csv(filepath)
    return df

# Пример использования:

def subtract_background_and_count_spores(image, bg_values, expected_diameter, tolerance=0.2):
    """
    Вычитает фон из изображения и подсчитывает споры, фильтруя контуры по ожидаемому диаметру.
    
    Параметры:
      image: исходное цветное изображение (например, в формате BGR).
      bg_values: кортеж или список из 3 значений фона по каналам (например, (bg_blue, bg_green, bg_red)).
      expected_diameter: ожидаемый диаметр спор в пикселях.
      tolerance: допустимое отклонение (относительное) от ожидаемого периметра.
      
    Возвращает:
      count: количество найденных спор.
      diameters: список измеренных диаметров (в пикселях).
      result_img: изображение с нарисованными контурами обнаруженных спор.
    """
    # Преобразуем изображение в тип float32 для точных вычислений
    img_float = image.astype(np.float32)
    
    # Вычитаем фон по каналам.
    # Создаём массив фона с размерностью (1,1,3) для трансляции по всему изображению.
    bg_array = np.array(bg_values, dtype=np.float32).reshape((1, 1, 3))
    diff = img_float - bg_array
    # Обнуляем отрицательные значения и приводим обратно к uint8
    diff = np.clip(diff, 0, 255).astype(np.uint8)
    
    # Для дальнейшей обработки переводим изображение в оттенки серого.
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # Пороговая обработка с использованием метода Отсу
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Морфологические операции для устранения мелких шумов
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # Поиск контуров
    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Фильтрация контуров по периметру, основанному на ожидаемом диаметре
    filtered_contours = []
    diameters = []
    
    # Ожидаемая длина окружности при известном диаметре: L = π * D
    expected_perimeter = np.pi * expected_diameter
    min_perimeter = expected_perimeter * (1 - tolerance)
    max_perimeter = expected_perimeter * (1 + tolerance)
    
    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        if min_perimeter <= perimeter <= max_perimeter:
            # Получаем минимальную описывающую окружность для контура
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            diameter = 2 * radius
            filtered_contours.append(cnt)
            diameters.append(diameter)
    
    # Копируем исходное изображение для визуализации результата
    result_img = image.copy()
    cv2.drawContours(result_img, filtered_contours, -1, (0, 255, 0), 2)
    
    count = len(filtered_contours)
    return count, diameters, result_img

# Пример использования:
# if __name__ == "__main__":
#     # Загрузка изображения (например, в формате BGR)
#     image = cv2.imread("path_to_image.jpg")
    
#     # Задаём значения фона, полученные из ROI (примерные значения для каждого канала)
#     background_values = (100, 105, 110)  # (B, G, R) – пример, подберите свои значения
    
    # Ожидаемый диаметр спор (в пикселях)
    # expected_diameter = 50  # примерное значение
    
    # count, diameters, result = subtract_background_and_count_spores(image, background_values, expected_diameter)
    # print("Найдено спор:", count)
    # print("Измеренные диаметры:", diameters)
    
    # cv2.imshow("Результат", result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    csv_file = r"G:\My\sov\extract\Spores\original_img\best\4x\Results_best_4x_1_scale.csv"
    df = read_imagej_csv_pandas(csv_file)
    print(df.head())
