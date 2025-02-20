import os
import json
import pandas as pd
import numpy as np
import re
from PIL import Image

def set_size(df_scale, dir_image, width=3072, height=2048):
    """
    Заполняет столбцы 'width' и 'height' в DataFrame df_scale.
    
    Если значения отсутствуют и width/height заданы (не None), используется указанное умолчание.
    Если же width (или height) равен None, для каждой записи функция пытается прочитать размеры 
    из соответствующего файла (имя из столбца 'File', при отсутствии расширения добавляется '.png').
    
    Аргументы:
      df_scale: DataFrame, содержащий хотя бы столбец 'File' (имя изображения без расширения)
      dir_image: путь к директории с изображениями
      width, height: значения по умолчанию, если размеры не заданы.
      
    Возвращает DataFrame с заполненными столбцами 'width' и 'height'.
    """
    for col, default_val in [('width', width), ('height', height)]:
        if col not in df_scale.columns:
            df_scale[col] = None

    def fill_size(row):
        if pd.isna(row['width']) or pd.isna(row['height']):
            if width is not None and height is not None:
                return pd.Series({'width': width, 'height': height})
            else:
                file_name = row['File']
                if '.' not in file_name:
                    file_name = file_name + '.png'
                file_path = os.path.join(dir_image, file_name)
                try:
                    with Image.open(file_path) as img:
                        w, h = img.size
                    return pd.Series({'width': w, 'height': h})
                except Exception as e:
                    # Если не удалось прочитать файл, используем умолчательные значения
                    return pd.Series({'width': 3072, 'height': 2048})
        else:
            return pd.Series({'width': row['width'], 'height': row['height']})
    
    df_scale[['width', 'height']] = df_scale.apply(fill_size, axis=1)
    return df_scale

def process_fungus_stats(data_xy_path, data_scale_path, dir_image, width_param=3072, height_param=2048):
    """
    Объединяет исходные данные из data_XY и data_Scale, вычисляет геометрические характеристики спор,
    проводит группировку для получения статистических параметров по каждому изображению (в единицах мкм),
    заполняет размеры изображения (с использованием функции set_size) и вычисляет % площади, занятой грибком.
    
    Аргументы:
      data_xy_path: путь к файлу result.xlsx (исходный data_XY)
      data_scale_path: путь к файлу spores_main.xlsx (исходный data_Scale)
      dir_image: путь к директории с изображениями (для чтения размеров, если они отсутствуют)
      width_param, height_param: умолчательные значения размеров изображения (в пикселях), если они не заданы.
         Если задать width_param=None, то размеры будут прочитаны из файлов.
    
    Итоговый DataFrame сохраняется как data_Scale_calc.xlsx в той же директории, что и data_scale_path.
    Возвращает итоговый DataFrame.
    """
    # Чтение исходных файлов
    data_XY = pd.read_excel(data_xy_path)
    data_Scale = pd.read_excel(data_scale_path)
    
    # Извлечение базового имени из столбца Image (удаляем расширение)
    data_XY['BaseName'] = data_XY['Image'].str.replace(r'\.[^.]+$', '', regex=True)
    
    # Объединение: left join по BaseName (data_XY) и File (data_Scale)
    merged_data = pd.merge(data_XY, data_Scale, left_on='BaseName', right_on='File', how='left')
    merged_data.rename(columns={'pix/mm': 'Scale'}, inplace=True)
    
    # Вычисление геометрических характеристик для каждой споры (в пикселях)
    merged_data['Length_X'] = abs(merged_data['X2'] - merged_data['X1'])
    merged_data['Length_Y'] = abs(merged_data['Y2'] - merged_data['Y1'])
    merged_data['Diameter'] = np.sqrt(merged_data['Length_X'] * merged_data['Length_Y'])
    merged_data['Area'] = np.pi * merged_data['Length_X'] * merged_data['Length_Y'] / 4

    # Перевод размеров спор в микрометры (учитывая, что Scale имеет размерность pix/mm)
    # Диаметр в мкм: (пиксели / (pix/mm)) * 1000
    # Площадь в мкм²: (пиксели² / (pix/mm)²) * 1e6
    merged_data['Diameter_um'] = merged_data['Diameter'] / merged_data['Scale'] * 1000
    merged_data['Area_um2'] = merged_data['Area'] / (merged_data['Scale']**2) * 1e6

    # Группировка по изображению (используем BaseName) для вычисления статистик
    grouped = merged_data.groupby('BaseName')
    stats_list = []
    for base_name, group in grouped:
        mean_diam = group['Diameter_um'].mean()
        std_diam = group['Diameter_um'].std()
        mean_area = group['Area_um2'].mean()
        std_area = group['Area_um2'].std()
        spore_total_area = group['Area_um2'].sum()  # суммарная площадь спор
        count = len(group)  # количество спор в группе
        # Гистограмма диаметров с автоматическим подбором бинов
        hist_counts, bin_edges = np.histogram(group['Diameter_um'], bins='auto')
        hist_data = {"bin_edges": bin_edges.tolist(), "counts": hist_counts.tolist()}
        hist_str = json.dumps(hist_data)
        
        stats_list.append({
            "File": base_name,
            "Count": count,  # добавлено поле количества
            "Mean_Diameter_um": mean_diam,
            "Std_Diameter_um": std_diam,
            "Mean_Area_um2": mean_area,
            "Std_Area_um2": std_area,
            "Diameter_Histogram": hist_str,
            "Spore_Total_Area_um2": spore_total_area
        })
    stats_df = pd.DataFrame(stats_list)
    
    # Объединение статистик с данными data_Scale по ключу File
    df_scale_calc = pd.merge(data_Scale, stats_df, on='File', how='left')
    
    # Переименование, если необходимо (например, переименовываем столбец 'pix/mm' в 'Scale')
    if 'pix/mm' in df_scale_calc.columns:
        df_scale_calc.rename(columns={'pix/mm': 'Scale'}, inplace=True)
    
    # Заполнение размеров изображения с помощью функции set_size
    df_scale_calc = set_size(df_scale_calc, dir_image, width=width_param, height=height_param)
    
    # Вычисление размеров изображения в мкм (переводим из пикселей)
    df_scale_calc['Image_Width_um'] = df_scale_calc['width'] / df_scale_calc['Scale'] * 1000
    df_scale_calc['Image_Height_um'] = df_scale_calc['height'] / df_scale_calc['Scale'] * 1000
    df_scale_calc['Image_Area_um2'] = df_scale_calc['Image_Width_um'] * df_scale_calc['Image_Height_um']
    
    # Вычисление % площади, занятой грибком (спорами)
    df_scale_calc['Fungus_Area_Percentage'] = (df_scale_calc['Spore_Total_Area_um2'] / df_scale_calc['Image_Area_um2']) * 100
    
    # Сохранение итогового файла data_Scale_calc.xlsx (в той же папке, что и data_scale_path)
    output_scale_calc_path = os.path.join(os.path.dirname(data_scale_path), "data_Scale_calc.xlsx")
    df_scale_calc = df_scale_calc.round(1)
    df_scale_calc.to_excel(output_scale_calc_path, index=False)
    print(f"data_Scale_calc сохранён в {output_scale_calc_path}")
    
    return df_scale_calc, merged_data
# 
#  VISUALISATION
# 
import os
import re
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def Short_Name_X(file_name):
    """
    Формирует краткое наименование для оси X по правилу:
    - Если в имени содержится "best" – префикс "B",
      если "worst" – префикс "W".
    - Далее через знак подчеркивания добавляется второе найденное число в имени.
    
    Примеры:
      "A best_4x_2_scale" -> "B_2"
      "A_worst_4x_7" -> "W_7"
    """
    lower_name = file_name.lower()
    if 'best' in lower_name:
        prefix = 'B'
    elif 'worst' in lower_name:
        prefix = 'W'
    else:
        prefix = ''
    numbers = re.findall(r'\d+', file_name)
    if len(numbers) >= 2:
        second_number = numbers[1]
    elif len(numbers) == 1:
        second_number = numbers[0]
    else:
        second_number = ''
    return f"{prefix}_{second_number}" if prefix else f"{second_number}"

def get_color(file_name):
    """
    Возвращает цвет для изображения в зависимости от подстроки в имени файла.
    "best" -> blue, "worst" -> red, иначе grey.
    """
    lower_name = file_name.lower()
    if 'best' in lower_name:
        return 'blue'
    elif 'worst' in lower_name:
        return 'red'
    else:
        return 'grey'

def visualize_spores_results(df_scale_calc, merged_data, data_scale_path):
    """
    Визуализация результатов по спорам.
    
    Для каждого изображения (с Count > 1) строится:
      1) Гистограмма распределения диаметров споры (в отдельном графике для каждого изображения).
      2) Общая столбиковая диаграмма, состоящая из трех подплотов:
           - Count
           - Mean_Diameter_um (с усиками, отражающими Std_Diameter_um)
           - Fungus_Area_Percentage
         Для каждого из этих показателей данные сортируются по возрастанию.
         
    Подписи по оси X формируются с помощью функции Short_Name_X и поворачиваются на 45°.
    
    Графики сохраняются в подкаталоге "graph", который создается в папке data_scale_path.
    """
    # Определяем директорию для сохранения графиков
    graph_dir = os.path.join(os.path.dirname(data_scale_path), "graph")
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    
    # Фильтруем изображения, оставляем только те, где Count > 1
    df_filtered = df_scale_calc[df_scale_calc['Count'] > 1].copy()
    if df_filtered.empty:
        print("Нет изображений с Count > 1 для визуализации.")
        return
    
    # Визуализация гистограмм по диаметрам для каждого изображения
    for idx, row in df_filtered.iterrows():
        file_base = row['File']
        short_label = Short_Name_X(file_base)
        # Извлекаем данные по спорам из merged_data по совпадению BaseName
        spores = merged_data[merged_data['BaseName'] == file_base]['Diameter_um'].dropna()
        if spores.empty:
            continue
        plt.figure()
        plt.hist(spores, bins='auto', edgecolor='black')
        plt.title(f"Гистограмма диаметров {short_label}")
        plt.xlabel("Диаметр (µm)")
        plt.ylabel("Количество")
        plt.xticks(rotation=45)
        # Сохраняем график гистограммы
        hist_path = os.path.join(graph_dir, f"hist_{short_label}.png")
        plt.savefig(hist_path, bbox_inches='tight')
        plt.close()
        print(f"Сохранена гистограмма для {short_label} в {hist_path}")
    
    # Подготовка данных для столбиковой диаграммы.
    # Для каждого показателя выполняем сортировку по возрастанию.
    df_temp = df_filtered.copy()
    df_temp['short'] = df_temp['File'].apply(Short_Name_X)
    df_temp['color'] = df_temp['File'].apply(get_color)
    
    # Сортировка по каждому показателю
    df_count = df_temp.sort_values(by='Count', ascending=True)
    df_mean_diam = df_temp.sort_values(by='Mean_Diameter_um', ascending=True)
    df_fungus = df_temp.sort_values(by='Fungus_Area_Percentage', ascending=True)
    
    # Создаем столбиковые диаграммы с отдельной сортировкой
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    
    # Диаграмма 1: Count
    x1 = np.arange(len(df_count))
    axs[0].bar(x1, df_count['Count'], color=df_count['color'])
    axs[0].set_title("Count")
    axs[0].set_xticks(x1)
    axs[0].set_xticklabels(df_count['short'], rotation=45)
    axs[0].set_ylabel("Количество спор")
    
    # Диаграмма 2: Mean Diameter (с усиками Std_Diameter_um)
    x2 = np.arange(len(df_mean_diam))
    axs[1].bar(x2, df_mean_diam['Mean_Diameter_um'], yerr=df_mean_diam['Std_Diameter_um'], capsize=5, color=df_mean_diam['color'])
    axs[1].set_title("Mean Diameter (µm)")
    axs[1].set_xticks(x2)
    axs[1].set_xticklabels(df_mean_diam['short'], rotation=45)
    axs[1].set_ylabel("Диаметр (µm)")
    
    # Диаграмма 3: Fungus Area Percentage
    x3 = np.arange(len(df_fungus))
    axs[2].bar(x3, df_fungus['Fungus_Area_Percentage'], color=df_fungus['color'])
    axs[2].set_title("Fungus Area Percentage")
    axs[2].set_xticks(x3)
    axs[2].set_xticklabels(df_fungus['short'], rotation=45)
    axs[2].set_ylabel("% площади грибка")
    
    plt.suptitle("Статистика по изображениям (Count > 1)")
    bar_chart_path = os.path.join(graph_dir, "bar_chart.png")
    plt.savefig(bar_chart_path, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"Сохранена столбиковая диаграмма в {bar_chart_path}")




# Пример использования функции:
if __name__ == '__main__':
    # Пути к исходным файлам
    data_xy_path = r"G:\My\sov\extract\Spores\original_img\test\best\4x\result.xlsx"
    data_scale_path = r"G:\My\sov\extract\Spores\original_img\test\best\4x\spores_main.xlsx"
    # Директория с изображениями
    dir_image = r"G:\My\sov\extract\Spores\original_img\test\best\4x"
    
    # Если размеры заданы по умолчанию (3072, 2048), передаем их;
    # Если необходимо брать размеры из файла, можно передать width_param=None, height_param=None.
    df_scale_calc = process_fungus_stats(data_xy_path, data_scale_path, dir_image, width_param=3072, height_param=2048)
    df_scale_calc, merged_data = process_fungus_stats(data_xy_path, data_scale_path, dir_image, width_param=3072, height_param=2048)
    visualize_spores_results(df_scale_calc, merged_data, data_scale_path)


