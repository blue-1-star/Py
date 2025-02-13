import cv2
import numpy as np
import os
import glob
import pandas as pd
import math
import re

def get_square_coordinates(R=5, n=3, m=5, Delta=0.5, shift=(0,0)):
    """
    Вычисляет координаты нижнего левого угла каждой ячейки решётки (в см)
    для чашки Петри с радиусом R (см), где решётка имеет размер n x m.
    
    Параметр Delta отвечает за сжатие/растяжение (изменение размеров ячеек),
    а shift=(dx,dy) (в см) просто смещает всю решётку.
    
    Система координат: нижний левый угол чашки – (0,0), верхний правый – (10,10),
    так как диаметр чашки = 10 см.
    
    Возвращает:
      coords - словарь, где ключ (i, j) (i: 0..n-1 снизу вверх, j: 0..m-1 слева направо),
               а значение – кортеж (x_cm, y_cm, s_cm), где s_cm – длина стороны ячейки.
    """
    s = 2 * (R - Delta) / math.sqrt(m**2 + n**2)
    # Определяем нижний левый угол решётки
    x0 = R - (m * s) / 2
    y0 = R - (n * s) / 2
    # Применяем сдвиг
    dx, dy = shift
    x0 += dx
    y0 += dy

    coords = {}
    for i in range(n):       # строки: 0 (нижняя) до n-1 (верхняя)
        for j in range(m):   # столбцы: 0 (самый левый) до m-1 (самый правый)
            x_cm = x0 + j * s
            y_cm = y0 + i * s
            coords[(i, j)] = (x_cm, y_cm, s)
    return coords

def extract_sample_info(file_name):
    """
    Извлекает информацию о типе образца и концентрации из имени файла.
    
    Ожидается, что имя файла начинается с 'A' или 'F':
      - 'A' означает альгинат,
      - 'F' означает фукоидан.
    
    Далее в имени файла ожидается число, обозначающее концентрацию,
    например, 0.25, 0.5, 0.75, 1.
    
    Возвращает кортеж (sample_type, concentration). Если данные не обнаружены,
    возвращает ('unknown', 'unknown').
    """
    sample_type = 'unknown'
    if file_name.upper().startswith('A'):
        sample_type = 'Alginate'
    elif file_name.upper().startswith('F'):
        sample_type = 'Fucoidan'
    
    match = re.search(r'(\d+\.?\d*)', file_name)
    concentration = match.group(1) + '%' if match else 'unknown'
    
    return sample_type, concentration

def process_file(file_path, output_root, R=5, n=3, m=5, Delta=0.5, shift=(0,0), pixel_per_cm=None):
    """
    Обрабатывает изображение чашки Петри:
      - Делит изображение на ячейки согласно решётке,
      - Для каждой ячейки выполняет сегментацию (Otsu) и вычисляет процент площади грибка (и Count).
      
      Сохраняет:
         • Аннотированное изображение вырезанной ячейки (например, FL_1_0.jpg),
         • Дополнительное аннотированное изображение, где на исходном изображении отмечена область этой ячейки (например, FL_1_0_onOriginal.jpg).
      
      Параметр pixel_per_cm (если задан) определяет масштаб изображения (пикселей на см).
      Если не задан, масштаб рассчитывается как dish_pixels / 10, где dish_pixels – меньшая сторона изображения.
      
      Возвращает результаты анализа в виде словаря.
    """
    image = cv2.imread(file_path)
    if image is None:
        print(f"Ошибка загрузки файла: {file_path}")
        return None
    height, width = image.shape[:2]
    if pixel_per_cm is None:
        dish_pixels = min(width, height)
        scale = dish_pixels / 10.0  # пикселей на см
    else:
        scale = pixel_per_cm

    coords_cm = get_square_coordinates(R=R, n=n, m=m, Delta=Delta, shift=shift)
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    out_dir = os.path.join(output_root, base_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    cell_results = {}  # ключ: номер ячейки (0..14) -> процент площади грибка
    cell_counts = {}   # ключ: номер ячейки -> число грибковых пикселей
    
    # Нумерация ячеек: cell_number = j * n + i (ячейки нумеруются по столбцам)
    for (i, j), (x_cm, y_cm, s_cm) in coords_cm.items():
        cell_number = j * n + i  # номера от 0 до 14
        x_px = int(round(x_cm * scale))
        s_px = int(round(s_cm * scale))
        y_bottom_px = int(round(y_cm * scale))
        top_y = height - (y_bottom_px + s_px)
        
        if x_px < 0 or top_y < 0 or (x_px + s_px) > width or (top_y + s_px) > height:
            print(f"Ячейка {(i,j)} (cell {cell_number}) выходит за границы изображения {file_path}. Пропуск.")
            continue
        
        # Извлекаем ROI ячейки и переводим в grayscale
        cell_roi = image[top_y:top_y+s_px, x_px:x_px+s_px]
        gray_roi = cv2.cvtColor(cell_roi, cv2.COLOR_BGR2GRAY)
        # Вычисляем Otsu-порог без инверсии
        ret, _ = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        delta = 15  # корректировка порога
        adjusted_threshold = ret - delta
        # Применяем пороговую операцию с новым порогом
        _, thresh_roi = cv2.threshold(gray_roi, adjusted_threshold, 255, cv2.THRESH_BINARY)
        
        # Поскольку грибок темный (пиксели с низкой яркостью), фон – светлый.
        # Считаем число грибковых пикселей как (общие пиксели - число светлых пикселей).
        total_pixels = s_px * s_px
        background_pixels = cv2.countNonZero(thresh_roi)
        fungus_pixels = total_pixels - background_pixels
        fungus_percentage = (fungus_pixels / total_pixels) * 100
        
        cell_results[cell_number] = fungus_percentage
        cell_counts[cell_number] = fungus_pixels
        
        # Получаем контуры для ячейки
        contours, _ = cv2.findContours(thresh_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Сохраняем аннотированное изображение ячейки
        annotated_roi = cell_roi.copy()
        cv2.drawContours(annotated_roi, contours, -1, (0, 0, 0), 2)
        cv2.rectangle(annotated_roi, (0, 0), (s_px-1, s_px-1), (255, 0, 0), 2)
        out_cell_path = os.path.join(out_dir, f"{base_name}_{cell_number}.jpg")
        cv2.imwrite(out_cell_path, annotated_roi)
        
        # Сохраняем изображение ячейки, отмеченной на исходном изображении
        annotated_on_original = image.copy()
        cv2.rectangle(annotated_on_original, (x_px, top_y), (x_px+s_px, top_y+s_px), (0, 255, 0), 3)
        cv2.putText(annotated_on_original, f"Cell_{cell_number}", (x_px, max(top_y-10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
        out_cell_original_path = os.path.join(out_dir, f"{base_name}_{cell_number}_onOriginal.jpg")
        cv2.imwrite(out_cell_original_path, annotated_on_original)
    
    # Возвращаем результаты анализа в виде словаря
    sample_type, concentration = extract_sample_info(base_name)
    return {
        "File": base_name,
        "SampleType": sample_type,
        "Concentration": concentration,
        **{f"Cell_{cell}": cell_results.get(cell, np.nan) for cell in range(n*m)},
        **{f"Count_Cell_{cell}": cell_counts.get(cell, np.nan) for cell in range(n*m)}
    }

def main():
    input_folder = r"G:\My\sov\extract\ORF\fungus"
    output_root = input_folder
    # Изменён шаблон для поиска всех jpg-файлов
    file_pattern = os.path.join(input_folder, "*.jpg")
    files = glob.glob(file_pattern)
    if not files:
        print("Не найдено файлов для обработки.")
        return

    wide_results = []
    for file_path in files:
        print(f"Обрабатывается файл: {file_path} ...")
        res = process_file(file_path, output_root, R=5, n=3, m=5, Delta=0.5, shift=(0,0))
        if res is not None:
            wide_results.append(res)
    
    if not wide_results:
        print("Нет данных для записи в Excel.")
        return
    
    # Преобразуем результаты из широкого формата в длинный формат:
    long_records = []
    for res in wide_results:
        file_name = res["File"]
        sample_type = res["SampleType"]
        concentration = res["Concentration"]
        for cell in range(15):
            long_records.append({
                "CellID": f"{file_name}_{cell}",
                "File": file_name,
                "SampleType": sample_type,
                "Concentration": concentration,
                "Region": f"Cell_{cell}",
                "FungusPercentage": res.get(f"Cell_{cell}", np.nan),
                "Count": res.get(f"Count_Cell_{cell}", np.nan)
            })
    
    df_long = pd.DataFrame(long_records)
    df_long = df_long.round(1)
    excel_path = os.path.join(output_root, "fungus_analysis_results_long.xlsx")
    df_long.to_excel(excel_path, index=False)
    print(f"Итоговый Excel-файл (длинный формат) сохранён: {excel_path}")

if __name__ == "__main__":
    main()
