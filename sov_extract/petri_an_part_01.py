import cv2
import numpy as np
import os
import glob
import pandas as pd
import math

def get_square_coordinates(R=5, n=3, m=5, Delta=0.5):
    """
    Вычисляет координаты нижнего левого угла каждой ячейки решётки (в см)
    для чашки Петри с радиусом R (см), где решётка имеет размер n x m и
    её концевые точки сдвинуты от окружности на Delta (см).
    
    Система координат: нижний левый угол чашки – (0,0), верхний правый – (10,10),
    так как диаметр чашки = 10 см.
    
    Возвращает:
      coords - словарь, где ключ (i, j) (i: 0..n-1 снизу вверх, j: 0..m-1 слева направо),
               а значение – кортеж (x_cm, y_cm, s_cm), где s_cm – длина стороны ячейки.
    """
    # Вычисляем длину стороны ячейки по формуле:
    # Расстояние от центра чашки (5,5) до вершины решётки должно быть R - Delta.
    # Если решётка имеет размеры m*s и n*s, её нижний левый угол находится в точке:
    # (R - m*s/2, R - n*s/2).
    # При этом расстояние от центра до вершины (R - m*s/2 + m*s, R - n*s/2 + n*s) =
    # (R + m*s/2, R + n*s/2) равно R - Delta, что даёт:
    # sqrt((m*s/2)^2 + (n*s/2)^2) = R - Delta  =>  s = 2*(R - Delta)/sqrt(m^2 + n^2)
    s = 2 * (R - Delta) / math.sqrt(m**2 + n**2)
    
    # Нижний левый угол решётки (в см)
    x0 = R - (m * s) / 2
    y0 = R - (n * s) / 2

    coords = {}
    for i in range(n):       # i: строки снизу вверх
        for j in range(m):   # j: столбцы слева направо
            x_cm = x0 + j * s
            y_cm = y0 + i * s
            coords[(i, j)] = (x_cm, y_cm, s)
    return coords

def process_file(file_path, output_root, R=5, n=3, m=5, Delta=0.5):
    """
    Обрабатывает одно изображение чашки Петри:
      - Вычисляет координаты ячеек решётки,
      - Для каждой ячейки выполняет сегментацию (Otsu) и вычисляет процент площади, занятой грибком,
      - Сохраняет аннотированные изображения ячеек в подкаталог с именем обрабатываемого файла.
      
    Аргументы:
      file_path   - путь к изображению
      output_root - корневой каталог для сохранения результатов (подкаталог будет создан с именем файла)
      R, n, m, Delta - параметры чашки и решётки (см)
      
    Возвращает:
      (base_name, cell_results) - base_name: имя файла без расширения,
                                  cell_results: словарь, где ключ – номер ячейки (1..n*m),
                                  значение – процент площади с грибком.
    """
    image = cv2.imread(file_path)
    if image is None:
        print(f"Ошибка загрузки файла: {file_path}")
        return None
    height, width = image.shape[:2]
    # Определяем масштаб: считается, что диаметр чашки (10 см) соответствует меньшей стороне изображения
    dish_pixels = min(width, height)
    scale = dish_pixels / 10.0  # пикселей на см

    # Получаем координаты ячеек в см
    coords_cm = get_square_coordinates(R=R, n=n, m=m, Delta=Delta)
    
    # Создаём подкаталог для выходных файлов с именем файла (без расширения)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    out_dir = os.path.join(output_root, base_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    cell_results = {}  # номер ячейки -> процент площади с грибком

    # Обрабатываем каждую ячейку
    for (i, j), (x_cm, y_cm, s_cm) in coords_cm.items():
        cell_number = i * m + j + 1  # нумерация от 1 до n*m (например, 1..15)
        # Переводим координаты из см в пиксели.
        # В системе, где (0,0) – нижний левый угол чашки:
        x_px = int(round(x_cm * scale))
        s_px = int(round(s_cm * scale))
        y_bottom_px = int(round(y_cm * scale))
        # Для OpenCV (начало координат – верхний левый угол) вычисляем:
        top_y = height - (y_bottom_px + s_px)
        # Проверяем, что регион внутри изображения
        if x_px < 0 or top_y < 0 or (x_px + s_px) > width or (top_y + s_px) > height:
            print(f"Ячейка {(i,j)} выходит за границы изображения {file_path}. Пропуск.")
            continue
        # Вырезаем регион интереса (ROI) для ячейки
        cell_roi = image[top_y:top_y+s_px, x_px:x_px+s_px]
        
        # Сегментация:
        gray_roi = cv2.cvtColor(cell_roi, cv2.COLOR_BGR2GRAY)
        # Применяем пороговое значение с методом Отсу
        ret, thresh_roi = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Если грибок отображается тёмными областями (на светлом фоне),
        # возможно, потребуется инверсия (раскомментировать строку ниже):
        # thresh_roi = cv2.bitwise_not(thresh_roi)
        
        # Вычисляем площадь грибка как число «белых» пикселей
        fungus_pixels = cv2.countNonZero(thresh_roi)
        total_pixels = s_px * s_px
        fungus_percentage = (fungus_pixels / total_pixels) * 100
        
        cell_results[cell_number] = fungus_percentage
        
        # Для аннотации: находим контуры (аналог Analyze Particles)
        contours, hierarchy = cv2.findContours(thresh_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        annotated_roi = cell_roi.copy()
        cv2.drawContours(annotated_roi, contours, -1, (0, 0, 255), 2)
        # Рисуем границы ячейки (синяя рамка)
        cv2.rectangle(annotated_roi, (0, 0), (s_px-1, s_px-1), (255, 0, 0), 2)
        
        # Сохраняем аннотированное изображение ячейки
        out_cell_path = os.path.join(out_dir, f"{base_name}_{cell_number}.jpg")
        cv2.imwrite(out_cell_path, annotated_roi)
    
    return base_name, cell_results

def extract_substance(file_name):
    """
    Простейшая функция для извлечения информации о веществе (Substance)
    из имени файла. Если имя содержит 'water' – возвращает 'water',
    иначе ищет числовые значения, например, '0.25', '0.5', '0.75' или '1'
    и возвращает, например, '0.5%'. При отсутствии информации – 'unknown'.
    """
    lower_file = file_name.lower()
    if "water" in lower_file:
        return "water"
    for conc in ["0.25", "0.5", "0.75", "1"]:
        if conc in lower_file:
            return f"{conc}%"
    return "unknown"

def main():
    # Каталог с изображениями
    input_folder = r"G:\My\sov\extract\ORF\fungus"
    # Выходные файлы (аннотированные изображения и Excel) будем сохранять в этом же каталоге
    output_root = input_folder

    # Получаем список файлов, удовлетворяющих шаблону (например, FL_1.jpg, FL_2.jpg, ...)
    file_pattern = os.path.join(input_folder, "FL*.jpg")
    files = glob.glob(file_pattern)
    if not files:
        print("Не найдено файлов для обработки.")
        return

    results_list = []  # для накопления строк итогового DataFrame

    # Внешний цикл по файлам – показываем ход обработки
    for file_path in files:
        print(f"Обрабатывается файл: {file_path} ...")
        result = process_file(file_path, output_root, R=5, n=3, m=5, Delta=0.5)
        if result is None:
            continue
        base_name, cell_results = result
        substance = extract_substance(base_name)
        # Формируем строку с данными:
        row = {"File": base_name, "Substance": substance}
        # Для 15 ячеек (при n=3, m=5)
        for cell_num in range(1, 3*5 + 1):
            row[f"Cell_{cell_num}"] = cell_results.get(cell_num, np.nan)
        results_list.append(row)

    # Создаём DataFrame и записываем в Excel
    df = pd.DataFrame(results_list)
    excel_path = os.path.join(output_root, "fungus_analysis_results.xlsx")
    df.to_excel(excel_path, index=False)
    print(f"Итоговый Excel-файл сохранён: {excel_path}")

if __name__ == "__main__":
    main()
