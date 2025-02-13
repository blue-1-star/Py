import cv2
import numpy as np
import os
import glob
import pandas as pd
import math

def get_square_coordinates(R=5, n=3, m=5, Delta=0.5):
    """
    Вычисляет координаты нижнего левго угла каждой ячейки решётки (в см)
    для чашки Петри с радиусом R (см), где решётка имеет размер n x m и
    её крайние точки сдвинуты от окружности на Delta (см).

    Система координат: нижний левый угол чашки – (0,0), верхний правый – (10,10),
    так как диаметр чашки = 10 см.

    Возвращает:
      coords - словарь, где ключ (i, j) (i: 0..n-1 снизу вверх, j: 0..m-1 слева направо),
               а значение – кортеж (x_cm, y_cm, s_cm), где s_cm – длина стороны ячейки.
    """
    s = 2 * (R - Delta) / math.sqrt(m**2 + n**2)
    x0 = R - (m * s) / 2
    y0 = R - (n * s) / 2

    coords = {}
    for i in range(n):       # строки: 0 (нижняя) до n-1 (верхняя)
        for j in range(m):   # столбцы: 0 (самый левый) до m-1 (самый правый)
            x_cm = x0 + j * s
            y_cm = y0 + i * s
            coords[(i, j)] = (x_cm, y_cm, s)
    return coords

def process_file(file_path, output_root, R=5, n=3, m=5, Delta=0.5):
    """
    Обрабатывает изображение чашки Петри:
      - Делит изображение на ячейки согласно решётке,
      - Для каждой ячейки выполняет сегментацию (Otsu) и вычисляет процент площади (и Count),
      - Область P1 формируется как объединяющий прямоугольник по ячейкам с веществом (исключая ячейки первого столбца, j==0),
      - Сохраняет:
          • Аннотированное изображение вырезанной ячейки (например, FL_1_0.jpg),
          • Дополнительное аннотированное изображение, где на исходном изображении отмечена область этой ячейки (например, FL_1_0_onOriginal.jpg),
          • Аннотированное изображение для объединённой области P1.
      - Возвращает результаты анализа.
    """
    import cv2, os, math, numpy as np  # Если функция вызывается отдельно
    image = cv2.imread(file_path)
    if image is None:
        print(f"Ошибка загрузки файла: {file_path}")
        return None
    height, width = image.shape[:2]
    # Предполагаем, что диаметр чашки (10 см) соответствует меньшей стороне изображения
    dish_pixels = min(width, height)
    scale = dish_pixels / 10.0  # пикселей на см

    coords_cm = get_square_coordinates(R=R, n=n, m=m, Delta=Delta)
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    out_dir = os.path.join(output_root, base_name)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    cell_results = {}  # ключ: номер ячейки (0..14) -> процент площади грибка
    cell_counts = {}   # ключ: номер ячейки -> число белых пикселей

    # Для объединённой области P1 (ячейки с веществом: все, где j != 0)
    substance_cells_rois = []

    # Нумерация ячеек: используем cell_number = j * n + i
    for (i, j), (x_cm, y_cm, s_cm) in coords_cm.items():
        cell_number = j * n + i  # cell_number от 0 до 14
        x_px = int(round(x_cm * scale))
        s_px = int(round(s_cm * scale))
        y_bottom_px = int(round(y_cm * scale))
        top_y = height - (y_bottom_px + s_px)
        
        if x_px < 0 or top_y < 0 or (x_px + s_px) > width or (top_y + s_px) > height:
            print(f"Ячейка {(i,j)} (cell {cell_number}) выходит за границы изображения {file_path}. Пропуск.")
            continue
        
        # Извлекаем ROI ячейки
        cell_roi = image[top_y:top_y+s_px, x_px:x_px+s_px]
        gray_roi = cv2.cvtColor(cell_roi, cv2.COLOR_BGR2GRAY)
        # ret, thresh_roi = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Вычисляем Otsu-порог без инверсии:
        ret, _ = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        delta = 15
        # Подбираем смещение: уменьшаем порог, чтобы считать грибковыми только ещё более тёмные пиксели
        adjusted_threshold = ret - delta  # например, если ret=149 и delta=20, то adjusted_threshold = 129
        # Применяем пороговую операцию с новым порогом
        _, thresh_roi = cv2.threshold(gray_roi, adjusted_threshold, 255, cv2.THRESH_BINARY)


        # Если грибок изображён как тёмная область, можно инвертировать:
        # thresh_roi = cv2.bitwise_not(thresh_roi)
        
        #  подсчет грибковых площадей для светлых грибков
        #  
        # fungus_pixels = cv2.countNonZero(thresh_roi)
        # total_pixels = s_px * s_px
        # fungus_percentage = (fungus_pixels / total_pixels) * 100
        #  подсчет грибковых площадей для темных грибков
        total_pixels = s_px * s_px
        background_pixels = cv2.countNonZero(thresh_roi)
        fungus_pixels = total_pixels - background_pixels
        fungus_percentage = (fungus_pixels / total_pixels) * 100
        
        cell_results[cell_number] = fungus_percentage
        cell_counts[cell_number] = fungus_pixels
        
        # Если ячейка относится к области с веществом (j != 0)
        if j != 0:
            substance_cells_rois.append((x_px, top_y, s_px, s_px))
        
        # Получаем контуры для ячейки
        contours, _ = cv2.findContours(thresh_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Аннотированное изображение ROI ячейки (как раньше)
        annotated_roi = cell_roi.copy()
        cv2.drawContours(annotated_roi, contours, -1, (0, 0, 0), 2)
        cv2.rectangle(annotated_roi, (0, 0), (s_px-1, s_px-1), (255, 0, 0), 2)
        out_cell_path = os.path.join(out_dir, f"{base_name}_{cell_number}.jpg")
        cv2.imwrite(out_cell_path, annotated_roi)
        
        # Дополнительная аннотация: рисуем область ячейки на исходном изображении
        annotated_on_original = image.copy()
        cv2.rectangle(annotated_on_original, (x_px, top_y), (x_px+s_px, top_y+s_px), (0, 255, 0), 3)
        cv2.putText(annotated_on_original, f"Cell_{cell_number}", (x_px, max(top_y-10, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        out_cell_original_path = os.path.join(out_dir, f"{base_name}_{cell_number}_onOriginal.jpg")
        cv2.imwrite(out_cell_original_path, annotated_on_original)
    
    # Обработка объединённой области P1 (ячейки с веществом: j != 0)
    if substance_cells_rois:
        xs = [x for (x, y, w, h) in substance_cells_rois]
        ys = [y for (x, y, w, h) in substance_cells_rois]
        rights = [x+w for (x, y, w, h) in substance_cells_rois]
        bottoms = [y+h for (x, y, w, h) in substance_cells_rois]
        roi_x = min(xs)
        roi_y = min(ys)
        roi_width = max(rights) - roi_x
        roi_height = max(bottoms) - roi_y
        
        roi_P1 = image[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
        gray_P1 = cv2.cvtColor(roi_P1, cv2.COLOR_BGR2GRAY)
        ret, thresh_P1 = cv2.threshold(gray_P1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # При необходимости: thresh_P1 = cv2.bitwise_not(thresh_P1)
        
        fungus_pixels_P1 = cv2.countNonZero(thresh_P1)
        total_pixels_P1 = roi_width * roi_height
        fungus_percentage_P1 = (fungus_pixels_P1 / total_pixels_P1) * 100
        
        contours_P1, _ = cv2.findContours(thresh_P1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # count_P1 = len(contours_P1)
        count_P1 = fungus_pixels_P1

        
        annotated_full = image.copy()
        cv2.rectangle(annotated_full, (roi_x, roi_y), (roi_x+roi_width, roi_y+roi_height), (0, 0, 0), 3)
        for cnt in contours_P1:
            cnt_shifted = cnt + [roi_x, roi_y]
            cv2.drawContours(annotated_full, [cnt_shifted], -1, (0, 0, 0), 2)
        out_P1_path = os.path.join(out_dir, f"{base_name}_P1.jpg")
        cv2.imwrite(out_P1_path, annotated_full)
    else:
        fungus_percentage_P1 = np.nan
        count_P1 = 0

    # Возвращаем результаты анализа в виде словаря
    return {
        "File": base_name,
        "Substance": extract_substance(base_name),
        "Mean(FL_i_P1)": fungus_percentage_P1,
        "Count(FL_i_P1)": count_P1,
        **{f"Cell_{cell}": cell_results.get(cell, np.nan) for cell in range(n*m)},
        **{f"Count_Cell_{cell}": cell_counts.get(cell, np.nan) for cell in range(n*m)}
    }


def extract_substance(file_name):
    """
    Извлекает информацию о веществе (Substance) из имени файла.
    Если имя содержит 'water' – возвращает 'water',
    иначе ищет числовые значения (например, '0.25', '0.5', '0.75', '1')
    и возвращает, например, '0.5%'. При отсутствии – 'unknown'.
    """
    lower_file = file_name.lower()
    if "water" in lower_file:
        return "water"
    for conc in ["0.25", "0.5", "0.75", "1"]:
        if conc in lower_file:
            return f"{conc}%"
    return "unknown"

def main():
    input_folder = r"G:\My\sov\extract\ORF\fungus"
    output_root = input_folder
    file_pattern = os.path.join(input_folder, "FL*.jpg")
    files = glob.glob(file_pattern)
    if not files:
        print("Не найдено файлов для обработки.")
        return

    wide_results = []
    for file_path in files:
        print(f"Обрабатывается файл: {file_path} ...")
        res = process_file(file_path, output_root, R=5, n=3, m=5, Delta=0.5)
        if res is not None:
            wide_results.append(res)
    
    if not wide_results:
        print("Нет данных для записи в Excel.")
        return
    
    # Преобразуем из широкого формата в длинный.
    # Для каждого файла будем создавать строки для каждой ячейки (Cell_0 ... Cell_14)
    # и одну строку для области P1.
    long_records = []
    for res in wide_results:
        file_name = res["File"]
        substance = res["Substance"]
        # Ячейки (Cell_0 ... Cell_14)
        for cell in range(15):
            long_records.append({
                "CellID": f"{file_name}_{cell}",
                "File": file_name,
                "Substance": substance,
                "Region": f"Cell_{cell}",
                "FungusPercentage": res.get(f"Cell_{cell}", np.nan),
                "Count": res.get(f"Count_Cell_{cell}", np.nan)
            })
        # Область P1
        long_records.append({
            "CellID": f"{file_name}_P1",
            "File": file_name,
            "Substance": substance,
            "Region": "P1",
            "FungusPercentage": res.get("Mean(FL_i_P1)", np.nan),
            "Count": res.get("Count(FL_i_P1)", np.nan)
        })
    
    df_long = pd.DataFrame(long_records)
    df_long = df_long.round(1)
    excel_path = os.path.join(output_root, "fungus_analysis_results_long.xlsx")
    df_long.to_excel(excel_path, index=False)
    print(f"Итоговый Excel-файл (длинный формат) сохранён: {excel_path}")

if __name__ == "__main__":
    main()
