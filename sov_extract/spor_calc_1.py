import os
import json
import numpy as np
import pandas as pd
from PIL import Image

def set_size(df_scale, dir_image, width=3072, height=2048):
    """
    Функция заполнения столбцов width, height в DataFrame df_scale (результирующем data_Scale_calc).
    
    Параметры:
      - df_scale: DataFrame с исходными данными из data_Scale.
         Ожидается наличие столбца 'File' (имя изображения без расширения).
         Если в df_scale уже есть столбцы 'width' и 'height' и они заполнены – они используются как есть.
      - dir_image: директория с изображениями.
      - width, height:
            Если заданы (не None), то для строк с отсутствующими значениями будут использованы эти параметры.
            Если же width (или height) равен None, то для каждой строки функция попытается открыть соответствующий файл 
            (имя берётся из столбца 'File'; если расширение отсутствует – по умолчанию добавляется '.png')
            и взять из него реальные размеры.
      - По умолчанию, если столбцы отсутствуют, подставляются значения (3072, 2048).
    
    Функция возвращает изменённый DataFrame с заполненными столбцами 'width' и 'height'.
    """
    # Если столбцы существуют, заполним только отсутствующие значения
    for col, default_val in [('width', width), ('height', height)]:
        if col not in df_scale.columns:
            df_scale[col] = None

    def fill_size(row):
        # Если значение отсутствует, то:
        if pd.isna(row['width']) or pd.isna(row['height']):
            # Если width не None – сигнал "использовать умолчание"
            if width is not None and height is not None:
                return pd.Series({'width': width, 'height': height})
            else:
                # Если width равен None – читаем из файла
                file_name = row['File']
                if '.' not in file_name:
                    file_name = file_name + '.png'
                file_path = os.path.join(dir_image, file_name)
                try:
                    with Image.open(file_path) as img:
                        w, h = img.size
                    return pd.Series({'width': w, 'height': h})
                except Exception as e:
                    # Если по какой-то причине не удалось открыть файл, возвращаем умолчательные значения
                    return pd.Series({'width': 3072, 'height': 2048})
        else:
            # Если значения присутствуют – оставляем как есть
            return pd.Series({'width': row['width'], 'height': row['height']})
    
    df_scale[['width', 'height']] = df_scale.apply(fill_size, axis=1)
    return df_scale

def create_data_scale_calc(data_xy_calc_path, data_scale_path, dir_image, width_param=3072, height_param=2048):
    """
    Функция формирования файла data_Scale_calc с интегральными статистиками по изображению.
    
    Используются:
      - data_XY_calc: Excel-файл, в котором для каждой споры вычислены геометрические характеристики.
         Ожидаются столбцы: Image (с расширением), Scale (pix/mm), Diameter, Area, а также BaseName (без расширения);
         если столбца BaseName нет, он будет создан.
      - data_Scale: Excel-файл, содержащий столбец File (имя изображения без расширения) и, возможно, 
         столбцы 'width', 'height'. Если размеры отсутствуют, функция set_size выполнит их заполнение.
    
    Интегральные статистики, вычисляемые для каждого изображения (группировка по BaseName):
      - Средний диаметр и стандартное отклонение (в мкм);
      - Средняя площадь и стандартное отклонение (в мкм²);
      - Гистограмма распределения диаметров (как JSON-строка, содержащая биновые границы и частоты);
      - Суммарная площадь спор (для последующего расчёта % Area грибка).
    
    Далее функция вычисляет площадь изображения в мкм² по размерам (width, height), 
    преобразованным из пикселей с использованием параметра Scale (pix/mm):
      Image_Width_µm = (width / Scale) * 1000
      Image_Height_µm = (height / Scale) * 1000
    
    % Area грибка определяется как отношение суммарной площади спор к площади изображения.
    
    Результирующий DataFrame сохраняется в Excel-файл data_Scale_calc.xlsx.
    
    Параметры:
      - data_xy_calc_path: путь к файлу data_XY_calc.xlsx.
      - data_scale_path: путь к файлу data_Scale (исходный, до объединения).
      - dir_image: путь к директории с изображениями.
      - width_param, height_param: параметры для функции set_size;
           если заданы (не None), то используются как значения по умолчанию,
           если же width_param (или height_param) равен None, то для каждой записи будет выполнено чтение файла.
    """
    # Чтение данных
    df_xy = pd.read_excel(data_xy_calc_path)
    df_scale = pd.read_excel(data_scale_path)
    
    # Если нет столбца BaseName в df_xy – создаём его (удаляем расширение из Image)
    if 'BaseName' not in df_xy.columns:
        df_xy['BaseName'] = df_xy['Image'].str.replace(r'\.[^.]+$', '', regex=True)
    
    # Преобразование измерений спор из пикселей в мкм
    # Диаметр в мкм: (Diameter [пикс]) / (Scale [pix/mm]) * 1000 = мм * 1000
    # Площадь в мкм²: (Area [пикс²]) / (Scale²) * 1e6
    df_xy['Diameter_um'] = df_xy['Diameter'] / df_xy['Scale'] * 1000
    df_xy['Area_um2'] = df_xy['Area'] / (df_xy['Scale']**2) * 1e6
    
    # Группировка по изображению (используем BaseName, чтобы сопоставить с File из data_Scale)
    grouped = df_xy.groupby('BaseName')
    stats_list = []
    for base_name, group in grouped:
        mean_diam = group['Diameter_um'].mean()
        std_diam = group['Diameter_um'].std()
        mean_area = group['Area_um2'].mean()
        std_area = group['Area_um2'].std()
        spore_total_area = group['Area_um2'].sum()  # суммарная площадь спор
        
        # Гистограмма диаметров (используем автоматический подбор бинов)
        hist_counts, bin_edges = np.histogram(group['Diameter_um'], bins='auto')
        hist_data = {"bin_edges": bin_edges.tolist(), "counts": hist_counts.tolist()}
        hist_str = json.dumps(hist_data)
        
        stats_list.append({
            "File": base_name,
            "Mean_Diameter_um": mean_diam,
            "Std_Diameter_um": std_diam,
            "Mean_Area_um2": mean_area,
            "Std_Area_um2": std_area,
            "Diameter_Histogram": hist_str,
            "Spore_Total_Area_um2": spore_total_area
        })
    stats_df = pd.DataFrame(stats_list)
    
    # Объединяем статистики с данными из data_Scale по ключу File
    df_scale_calc = pd.merge(df_scale, stats_df, on='File', how='left')
    
    # Если в исходном data_Scale нет столбца 'pix/mm', но он есть как 'Scale', можно оставить его.
    # Если столбец 'pix/mm' присутствует – переименуем его в 'Scale' для удобства:
    if 'pix/mm' in df_scale_calc.columns:
        df_scale_calc.rename(columns={'pix/mm': 'Scale'}, inplace=True)
    
    # Заполнение размеров изображений с использованием функции set_size.
    # Если столбцы 'width', 'height' отсутствуют или не заполнены – set_size заполнит их согласно параметрам:
    df_scale_calc = set_size(df_scale_calc, dir_image, width=width_param, height=height_param)
    
    # Вычисление общей площади изображения в мкм²
    # Переводим размеры из пикселей в мкм: Image_Width_um = (width / Scale) * 1000, аналогично для height.
    df_scale_calc['Image_Width_um'] = df_scale_calc['width'] / df_scale_calc['Scale'] * 1000
    df_scale_calc['Image_Height_um'] = df_scale_calc['height'] / df_scale_calc['Scale'] * 1000
    df_scale_calc['Image_Area_um2'] = df_scale_calc['Image_Width_um'] * df_scale_calc['Image_Height_um']
    
    # Вычисление процента площади, занятой грибком (спорами)
    df_scale_calc['Fungus_Area_Percentage'] = (df_scale_calc['Spore_Total_Area_um2'] / df_scale_calc['Image_Area_um2']) * 100
    
    # Сохранение результирующего файла data_Scale_calc.xlsx
    output_scale_calc_path = os.path.join(os.path.dirname(data_scale_path), "data_Scale_calc.xlsx")
    df_scale_calc.to_excel(output_scale_calc_path, index=False)
    print(f"data_Scale_calc сохранён в {output_scale_calc_path}")
    
    return df_scale_calc

# Пример вызова функции:
if __name__ == '__main__':
    # Пути к файлам (как заданы ранее)
    data_xy_calc_path = r"G:\My\sov\extract\Spores\original_img\test\best\4x\data_XY_calc.xlsx"
    data_scale_path = r"G:\My\sov\extract\Spores\original_img\test\best\4x\spores_main.xlsx"
    # Директория, где лежат изображения
    dir_image = r"G:\My\sov\extract\Spores\original_img\test\best\4x"
    
    # Если хотите использовать умолчательные размеры (3072,2048), передайте их,
    # а если хотите получить реальные размеры из файлов, передайте width_param=None (и соответственно height_param=None)
    df_scale_calc = create_data_scale_calc(data_xy_calc_path, data_scale_path, dir_image, width_param=3072, height_param=2048)
