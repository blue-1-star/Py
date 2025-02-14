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

def get_square_coordinates_pix(R=5, n=3, m=5, Delta=0.5, shift=(0,0), pixel_per_cm=None):
    """
    Вычисляет координаты ячеек (например, для вырезания областей на изображении)
    R - базовый размер (например, диаметр чашки в см),
    n, m - число строк и столбцов,
    Delta - отступ между ячейками (в см),
    shift - сдвиг начала координат,
    pixel_per_cm - масштаб: пикселей на см.
    """
    # Если задан pixel_per_cm, переводим размеры в пиксели:
    if pixel_per_cm is not None:
        R_px = R * pixel_per_cm
        Delta_px = Delta * pixel_per_cm
    else:
        # Если масштаб не задан, можно задать значение по умолчанию или
        # попробовать вычислить его, например, по меньшей стороне изображения (как в pixel_per_cm=None выше)
        R_px = R  # или R_px = dish_pixels / 10, если dish_pixels известен
        Delta_px = Delta

    # Пример расчета размеров ячейки (это зависит от того, как именно устроена сетка):
    cell_width = R_px / m
    cell_height = R_px / n

    coordinates = []
    for i in range(n):
        for j in range(m):
            # Вычисляем координаты верхнего левого угла каждой ячейки с учетом сдвига и отступа
            x = shift[0] + j * (cell_width + Delta_px)
            y = shift[1] + i * (cell_height + Delta_px)
            coordinates.append((x, y, cell_width, cell_height))
    return coordinates



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

consent = [0, 0.25, 0.5, 0.75, 1]  # список концентраций, длина должна совпадать с m

def get_concentration(cell, m, consent):
    """
    По номеру ячейки (cell), вычисляем номер столбца как cell % m
    и возвращаем соответствующее значение концентрации в формате процентов.
    """
    col = cell % m
    conc_value = consent[col]
    # Если нужно вернуть значение в процентах:
    return f"{int(conc_value * 100)}%"
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
        # "Concentration": concentration,
        **{f"Concentration_Cell_{cell}": get_concentration(cell, m, consent) for cell in range(n * m)},
        **{f"Cell_{cell}": cell_results.get(cell, np.nan) for cell in range(n*m)},
        **{f"Count_Cell_{cell}": cell_counts.get(cell, np.nan) for cell in range(n*m)},
    }

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

# Пример DataFrame. Он должен содержать по крайней мере следующие столбцы:
# 'SampleType', 'File', 'FungusPercentage', 'Region'
# Например:
# df = pd.read_csv("your_data.csv")

# Функция для извлечения числа из имени файла
def extract_file_number(file_name):
    # Предположим, что число – последовательность цифр в имени файла
    match = re.search(r'(\d+)', file_name)
    return int(match.group(1)) if match else np.nan

def visualisation0(df):
    # Добавляем столбец с числовой меткой из 'File'
    df['FileNumber'] = df['File'].apply(extract_file_number)

    # Агрегируем данные по File: среднее, стандартное отклонение и SampleType
    agg_df = df.groupby('File').agg(
        mean_fungus=('FungusPercentage', 'mean'),
        std_fungus=('FungusPercentage', 'std'),
        file_number=('FileNumber', 'first'),
        sample_type=('SampleType', 'first')  # предполагаем, что для одного файла все записи одного типа
    ).reset_index()

    # Сортируем по среднему значению FungusPercentage по возрастанию
    agg_df = agg_df.sort_values(by='mean_fungus', ascending=True)

    # Определяем словарь с цветами для различных типов вещества
    color_map = {
        "Alginate": "blue",
        "Fucoidan": "green"
    }

    # 1) Столбиковая диаграмма для агрегированных данных (с усиками стандартного отклонения)
    plt.figure(figsize=(10, 6))

    # Чтобы легенда не повторялась, собираем уже добавленные типы
    added_types = set()
    for idx, row in agg_df.iterrows():
        # Определяем цвет по sample_type
        col = color_map.get(row['sample_type'], "gray")
        # Для легенды: добавляем метку только при первом появлении sample_type
        label = row['sample_type'] if row['sample_type'] not in added_types else ""
        added_types.add(row['sample_type'])
        plt.bar(str(row['file_number']), row['mean_fungus'],
                yerr=row['std_fungus'], capsize=5, color=col, label=label)

    plt.xlabel('Номер файла (из имени)')
    plt.ylabel('Среднее значение FungusPercentage')
    plt.title('Среднее значение FungusPercentage по файлам (с усиками стандартного отклонения)')
    plt.legend(title="SampleType")
    plt.tight_layout()
    plt.show()

    # 2) График неагрегированных данных: узкие столбики для каждого Region
    plt.figure(figsize=(10, 6))
    bar_width = 0.1  # ширина отдельного столбика (подберите по необходимости)

    # Упорядочим файлы согласно агрегированным данным
    ordered_files = agg_df['File'].tolist()

    for file in ordered_files:
        # Получаем числовую метку и тип образца для цветового разделения
        file_row = agg_df[agg_df['File'] == file].iloc[0]
        file_num = file_row['file_number']
        file_sample_type = file_row['sample_type']
        
        # Выбираем все строки исходного DataFrame для данного файла
        sub_df = df[df['File'] == file]
        n_regions = len(sub_df)
        # Распределяем небольшие смещения, чтобы столбики для одного файла не перекрывались
        offsets = np.linspace(-bar_width, bar_width, n_regions)
        
        for offset, (_, row) in zip(offsets, sub_df.iterrows()):
            plt.bar(file_num + offset, row['FungusPercentage'], width=bar_width/3,
                    color=color_map.get(file_sample_type, "gray"))

    plt.xlabel('Номер файла (из имени)')
    plt.ylabel('FungusPercentage')
    plt.title('Индивидуальные значения FungusPercentage по Region для каждого файла')
    plt.xticks(agg_df['file_number'], agg_df['file_number'].astype(str))
    plt.tight_layout()
    plt.show()

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.patches import Patch

def visualisation1(df, output_root):
    """
    Функция строит графики антигрибкового воздействия.
    
    Параметры:
      df: pandas.DataFrame с колонками:
          - 'SampleType' (например, 'Alginate' или 'Fucoidan')
          - 'File' (имя файла, из которого извлекается число)
          - 'FungusPercentage'
          - 'Region'
      output_root: путь к каталогу, в котором будет создан подкаталог graph для сохранения графика.
      
    График сохраняется в файл вида "fungal_<dd_mm>.jpg" в каталоге output_root/graph.
    """
    # Создаем выходной каталог, если его нет:
    graph_dir = os.path.join(output_root, "graph")
    os.makedirs(graph_dir, exist_ok=True)
    
    # Если в DataFrame еще нет столбца с числовой меткой из имени файла, добавляем его.
    if 'FileNumber' not in df.columns:
        def extract_file_number(file_name):
            m = re.search(r'(\d+)', file_name)
            return int(m.group(1)) if m else np.nan
        df['FileNumber'] = df['File'].apply(extract_file_number)
    
    # Агрегация по SampleType и File: рассчитываем среднее и стандартное отклонение
    agg_df = df.groupby(['SampleType', 'File']).agg(
        mean_fungus=('FungusPercentage', 'mean'),
        std_fungus=('FungusPercentage', 'std'),
        file_number=('FileNumber', 'first')
    ).reset_index()
    
    # Сортируем данные: сначала по SampleType, затем по среднему значению (возрастание)
    agg_df.sort_values(by=['SampleType', 'mean_fungus'], ascending=[True, True], inplace=True)
    agg_df = agg_df.reset_index(drop=True)
    
    # Задаем x-позиции для каждого файла (агрегированные данные)
    x_positions = np.arange(len(agg_df))
    
    # Словарь для цветового оформления SampleType
    color_map = {
        "Alginate": "blue",
        "Fucoidan": "green"
    }
    # Определяем цвета для каждого файла согласно его SampleType
    bar_colors = [color_map.get(st, "gray") for st in agg_df['SampleType']]
    
    # Создаем фигуру с двумя подграфиками (агрегированные и неагрегированные данные)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16), sharex=True)
    
    # ----- График 1: агрегированные данные с усиками (error bars) -----
    ax1.bar(x_positions, agg_df['mean_fungus'], yerr=agg_df['std_fungus'],
            capsize=5, color=bar_colors, edgecolor='black')
    
    # Добавляем вертикальные линии-разделители между группами (SampleType)
    for i in range(1, len(agg_df)):
        if agg_df['SampleType'].iloc[i] != agg_df['SampleType'].iloc[i-1]:
            ax1.axvline(x=i - 0.5, color='black', linestyle='--')
    
    ax1.set_ylabel("Mean FungusPercentage")
    ax1.set_title("Агрегированные данные: среднее значение с усиками")
    ax1.set_xticks(x_positions)
    # Используем извлеченное число из имени файла в качестве подписи
    ax1.set_xticklabels(agg_df['file_number'].astype(int).astype(str))
    
    # Формируем легенду по SampleType (чтобы не было повторений)
    unique_types = agg_df['SampleType'].unique()
    legend_handles = [Patch(color=color_map.get(t, "gray"), label=t) for t in unique_types]
    ax1.legend(handles=legend_handles, title="SampleType")
    
    # ----- График 2: неагрегированные данные (узкие столбики по Region) -----
    # Для каждого файла из agg_df находим соответствующие записи в исходном df
    for i, row in agg_df.iterrows():
        file_name = row['File']
        sample_type = row['SampleType']
        file_x = x_positions[i]
        sub_df = df[df['File'] == file_name]
        num_regions = len(sub_df)
        # Сдвиги, чтобы столбики не накладывались (узкие столбики, ширина ~0.05)
        offsets = np.linspace(-0.2, 0.2, num_regions)
        for offset, (_, sub_row) in zip(offsets, sub_df.iterrows()):
            ax2.bar(file_x + offset, sub_row['FungusPercentage'], width=0.05,
                    color=color_map.get(sample_type, "gray"), edgecolor='black')
    
    ax2.set_xlabel("Номер файла (из имени)")
    ax2.set_ylabel("FungusPercentage")
    ax2.set_title("Неагрегированные данные: значения по Region")
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels(agg_df['file_number'].astype(int).astype(str))
    
    plt.tight_layout()
    
    # Сохраняем график в файл
    current_date = datetime.now().strftime("%d_%m")
    output_file = os.path.join(graph_dir, f"fungal_{current_date}.jpg")
    plt.savefig(output_file, dpi=300)
    plt.close(fig)
    
    print(f"График сохранен в {output_file}")
import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.patches import Patch

def visualisation(df, output_root):
    """
    Строит два графика:
      - Верхний (агрегированные данные): для каждой группы (SampleType) по файлам строится столбчатая диаграмма
        со средним значением FungusPercentage и усиками (error bars). Между группами добавляются вертикальные линии.
      - Нижний (неагрегированные данные): для каждого файла строятся узкие столбики для каждого региона (Region).
    График сохраняется в файл вида "fungal_<dd_mm>.jpg" в подкаталоге output_root/graph.
    """
    # Создаем каталог для графиков, если его нет
    graph_dir = os.path.join(output_root, "graph")
    os.makedirs(graph_dir, exist_ok=True)
    
    # Если столбца с числовой меткой нет, добавляем его:
    if 'FileNumber' not in df.columns:
        def extract_file_number(file_name):
            m = re.search(r'(\d+)', file_name)
            return int(m.group(1)) if m else np.nan
        df['FileNumber'] = df['File'].apply(extract_file_number)
    
    # Агрегируем данные по SampleType и File
    agg_df = df.groupby(['SampleType', 'File']).agg(
        mean_fungus=('FungusPercentage', 'mean'),
        std_fungus=('FungusPercentage', 'std'),
        file_number=('FileNumber', 'first')
    ).reset_index()
    
    # Сортируем сначала по SampleType, затем по среднему значению FungusPercentage (по возрастанию)
    agg_df.sort_values(by=['SampleType', 'mean_fungus'], ascending=[True, True], inplace=True)
    agg_df = agg_df.reset_index(drop=True)
    
    # Задаем позиции для каждого файла
    x_positions = np.arange(len(agg_df))
    
    # Цветовое оформление для SampleType
    color_map = {
        "Alginate": "blue",
        "Fucoidan": "green"
    }
    bar_colors = [color_map.get(st, "gray") for st in agg_df['SampleType']]
    
    # Создаем фигуру с двумя подграфиками, разделенными по оси X
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # -------- График 1: агрегированные данные --------
    ax1.bar(x_positions, agg_df['mean_fungus'], yerr=agg_df['std_fungus'],
            capsize=5, color=bar_colors, edgecolor='black')
    
    # Добавляем вертикальные разделительные линии между группами SampleType
    for i in range(1, len(agg_df)):
        if agg_df['SampleType'].iloc[i] != agg_df['SampleType'].iloc[i-1]:
            ax1.axvline(x=i - 0.5, color='black', linestyle='--')
    
    ax1.set_ylabel("Mean FungusPercentage")
    ax1.set_title("Агрегированные данные: среднее значение с усиками")
    
    # Добавляем метки по оси X и на верхнем графике (метки сверху и снизу)
    ax1.set_xticks(x_positions)
    ax1.set_xticklabels(agg_df['file_number'].astype(int).astype(str), rotation=0)
    ax1.tick_params(axis='x', labelbottom=True, labeltop=True)
    
    # Формируем легенду по SampleType
    unique_types = agg_df['SampleType'].unique()
    legend_handles = [Patch(color=color_map.get(t, "gray"), label=t) for t in unique_types]
    ax1.legend(handles=legend_handles, title="SampleType")
    
    # -------- График 2: неагрегированные данные --------
    for i, row in agg_df.iterrows():
        file_name = row['File']
        sample_type = row['SampleType']
        file_x = x_positions[i]
        sub_df = df[df['File'] == file_name]
        num_regions = len(sub_df)
        # Распределяем столбики для разных Region внутри файла (сдвиг по оси X)
        offsets = np.linspace(-0.2, 0.2, num_regions)
        for offset, (_, sub_row) in zip(offsets, sub_df.iterrows()):
            ax2.bar(file_x + offset, sub_row['FungusPercentage'], width=0.05,
                    color=color_map.get(sample_type, "gray"), edgecolor='black')
    
    ax2.set_xlabel("Номер файла (из имени)")
    ax2.set_ylabel("FungusPercentage")
    ax2.set_title("Неагрегированные данные: значения по Region")
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels(agg_df['file_number'].astype(int).astype(str), rotation=0)
    
    plt.tight_layout()
    
    # Сохраняем график в файл
    current_date = datetime.now().strftime("%d_%m")
    output_file = os.path.join(graph_dir, f"fungal_{current_date}.jpg")
    plt.savefig(output_file, dpi=300)
    plt.show()
    plt.close(fig)
    
    print(f"График сохранен в {output_file}")

import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.patches import Patch

def visualisation_concentration_analysis(df, output_root):
    """
    Визуализация концентрационного анализа:
    
    1) Visualization A:
       Для каждого файла (группировка по SampleType) по каждому значению Concentration (0, 25, 50, 75, 100%)
       рассчитывается среднее значение FungusPercentage с error bars (усреднение по 3 репликам).
       Реплика определяется по столбцу 'Region' (ожидается формат "Cell_X"): 
         - Реплика 1: X % 3 == 0  (например, ячейки 0, 3, 6, 9, 12)
         - Реплика 2: X % 3 == 1  (например, ячейки 1, 4, 7, 10, 13)
         - Реплика 3: X % 3 == 2  (например, ячейки 2, 5, 8, 11, 14)
       На графике для каждого SampleType (например, Alginate, Fucoidan) для каждого файла строится линия
       (с маркерами и error bars) по концентрациям.
       
    2) Visualization B:
       Для каждого файла (с группировкой по SampleType) сравниваются две группы:
         - Контроль: Concentration == 0%
         - Тест: Concentration в {25, 50, 75, 100}%.
       Для каждой группы вычисляется среднее (с error bars по репликам), после чего строится группированная
       столбиковая диаграмма.
       
    Результаты сохраняются в каталог output_root/graph с именами, содержащими текущую дату.
    """
    # --- Подготовка данных ---
    df = df.copy()
    
    # Добавляем столбец Replicate на основе номера ячейки, извлекаемого из Region ("Cell_X")
    def get_replicate(region):
        m = re.search(r'Cell_(\d+)', region)
        if m:
            cell_num = int(m.group(1))
            return cell_num % 3  # реплики: 0,1,2
        return np.nan
    if 'Replicate' not in df.columns:
        df['Replicate'] = df['Region'].apply(get_replicate)
    
    # Обеспечим числовой формат для Concentration.
    # Ожидается, что столбец Concentration имеет формат "25%" и т.д.
    def parse_concentration(val):
        if isinstance(val, str):
            return float(val.replace('%',''))
        return float(val)
    if 'Concentration' in df.columns:
        df['Concentration_numeric'] = df['Concentration'].apply(parse_concentration)
    else:
        raise ValueError("DataFrame должен содержать столбец 'Concentration'")
    
    # --- Visualization A: FungusPercentage по Concentration для каждого файла ---
    # Сначала усредняем по репликам: группируем по File, SampleType, Concentration_numeric и Replicate
    rep_summary = df.groupby(['File', 'SampleType', 'Concentration_numeric', 'Replicate'])['FungusPercentage'].mean().reset_index()
    # Далее усредняем по репликам (3 значения) для каждого File, SampleType, Concentration_numeric
    summary = rep_summary.groupby(['File', 'SampleType', 'Concentration_numeric']).agg(
        mean_Fungus=('FungusPercentage', 'mean'),
        std_Fungus=('FungusPercentage', 'std')
    ).reset_index()
    
    # Определяем SampleType и соответствующие цвета
    sample_types = summary['SampleType'].unique()
    color_map = {"Alginate": "blue", "Fucoidan": "green"}
    
    # Для наглядности создадим subplot для каждого SampleType
    figA, axesA = plt.subplots(1, len(sample_types), figsize=(6*len(sample_types), 6), sharey=True)
    if len(sample_types) == 1:
        axesA = [axesA]
    for ax, st in zip(axesA, sample_types):
        subset = summary[summary['SampleType'] == st]
        files = subset['File'].unique()
        for file in files:
            file_data = subset[subset['File'] == file].sort_values(by='Concentration_numeric')
            ax.errorbar(file_data['Concentration_numeric'], file_data['mean_Fungus'],
                        yerr=file_data['std_Fungus'], marker='o', capsize=5,
                        label=file, color=color_map.get(st, "gray"))
        ax.set_title(f"{st}")
        ax.set_xlabel("Concentration (%)")
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xlim(-5, 105)
        ax.set_ylabel("Mean FungusPercentage")
        ax.legend(title="File", fontsize='small')
    figA.suptitle("FungusPercentage vs Concentration (среднее по 3 репликам)", fontsize=16)
    
    # --- Visualization B: Сравнение Control vs Treatment ---
    # Для каждой ячейки уже есть значение Concentration_numeric; выделим:
    # Контроль: Concentration == 0
    # Тест: Concentration > 0
    # Группируем сначала по File, SampleType и Replicate, чтобы получить усреднение по каждой реплике.
    def calc_group(x, group):
        if group == 'control':
            sel = x[x['Concentration_numeric'] == 0]
        else:
            sel = x[x['Concentration_numeric'] > 0]
        return sel['FungusPercentage'].mean() if not sel.empty else np.nan

    group_summary = df.groupby(['File', 'SampleType', 'Replicate']).apply(
        lambda x: pd.Series({
            'control': calc_group(x, 'control'),
            'treatment': calc_group(x, 'treatment')
        })
    ).reset_index()
    
    # Теперь усредняем по репликам для каждого File, SampleType
    group_final = group_summary.groupby(['File', 'SampleType']).agg(
        control_mean = ('control', 'mean'),
        control_std = ('control', 'std'),
        treatment_mean = ('treatment', 'mean'),
        treatment_std = ('treatment', 'std')
    ).reset_index()
    
    # Построим график: для каждого SampleType – отдельный subplot, в котором по оси X файлы,
    # а для каждого файла два столбца: Control (0%) и Treatment (25-100%)
    figB, axesB = plt.subplots(1, len(sample_types), figsize=(6*len(sample_types), 6), sharey=True)
    if len(sample_types) == 1:
        axesB = [axesB]
    bar_width = 0.35
    for ax, st in zip(axesB, sample_types):
        subset = group_final[group_final['SampleType'] == st]
        files = subset['File'].values
        x = np.arange(len(files))
        ax.bar(x - bar_width/2, subset['control_mean'], width=bar_width,
               yerr=subset['control_std'], capsize=5, label="Control (0%)",
               color="lightblue", edgecolor="black")
        ax.bar(x + bar_width/2, subset['treatment_mean'], width=bar_width,
               yerr=subset['treatment_std'], capsize=5, label="Treatment (25-100%)",
               color="salmon", edgecolor="black")
        ax.set_title(f"{st}")
        ax.set_xticks(x)
        ax.set_xticklabels(files, rotation=45)
        ax.set_xlabel("File")
        ax.set_ylabel("Mean FungusPercentage")
        ax.legend()
    figB.suptitle("Сравнение Control vs Treatment для каждого файла", fontsize=16)
    
    # --- Сохранение графиков ---
    graph_dir = os.path.join(output_root, "graph")
    os.makedirs(graph_dir, exist_ok=True)
    current_date = datetime.now().strftime("%d_%m")
    output_file_A = os.path.join(graph_dir, f"fungal_concentration_A_{current_date}.jpg")
    output_file_B = os.path.join(graph_dir, f"fungal_concentration_B_{current_date}.jpg")
    figA.tight_layout(rect=[0,0,1,0.95])
    figB.tight_layout(rect=[0,0,1,0.95])
    figA.savefig(output_file_A, dpi=300)
    figB.savefig(output_file_B, dpi=300)
    plt.show()
    plt.close(figA)
    plt.close(figB)
    
    print(f"Visualization A saved to {output_file_A}")
    print(f"Visualization B saved to {output_file_B}")




def main():
    # input_folder = r"G:\My\sov\extract\ORF\fungus"
    input_folder = r"G:\My\sov\extract\ORF\work_petri"
    
    output_root = input_folder
    os.makedirs(output_root, exist_ok=True)    
    csv_file = os.path.join(output_root, "fungus_csv.csv")
    if os.path.exists(csv_file):
        print(f"CSV файл {csv_file} найден. Загрузка данных из CSV...")
        df_long = pd.read_csv(csv_file)
    else:
        print("CSV файл не найден. Выполняются вычисления...")
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
            # concentration = res["Concentration"]
            for cell in range(15):
                long_records.append({
                    "CellID": f"{file_name}_{cell}",
                    "File": file_name,
                    "SampleType": sample_type,
                    "Region": f"Cell_{cell}",
                    "Concentration": res.get(f"Concentration_Cell_{cell}", np.nan), # "Concentration": concentration,
                    "FungusPercentage": res.get(f"Cell_{cell}", np.nan),
                    "Count": res.get(f"Count_Cell_{cell}", np.nan)
                })
        df_long = pd.DataFrame(long_records)
        df_long.to_csv(csv_file, index=False)
        print(f"Данные сохранены в CSV: {csv_file}")
    df_long = df_long.round(1)
    excel_path = os.path.join(output_root, "fungus_analysis.xlsx")
    df_long.to_excel(excel_path, index=False)
    print(f"Итоговый Excel-файл (длинный формат) сохранён: {excel_path}")
    visualisation(df_long, output_root)
    visualisation_concentration_analysis(df_long, output_root)

if __name__ == "__main__":
    main()
