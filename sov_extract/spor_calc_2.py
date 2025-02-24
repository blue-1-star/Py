import os
import json
import pandas as pd
import numpy as np
import re
from PIL import Image
# from spor_bootstrap_01 import bootstrap_statistic, mean_statistic, kde_mode_statistic
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
    # сохранение файла data_XY_calc.xlsx с пиксельными размерами ( merged_data)
    output_scale_calc_path = os.path.join(os.path.dirname(data_scale_path), "data_Scale_calc.xlsx")
    output_data_XY_calc_path = os.path.join(os.path.dirname(data_scale_path), "data_XY_calc.xlsx")
    df_scale_calc = df_scale_calc.round(1)
    # df_data_XY_calc = df_scale_calc.round(1)
    merged_data.to_excel(output_data_XY_calc_path, index=False)
    df_scale_calc.to_excel(output_scale_calc_path, index=False)
    print(f"data_Scale_calc сохранён в {output_scale_calc_path}")
    print(f"data_XY_calc сохранён в {output_scale_calc_path}")
    
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



import os
import re
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def Short_Name_X(file_name):
    """
    Generates a short label for the x-axis:
    - If the name contains "best", prefix "B"; if "worst", prefix "W".
    - Then an underscore and the second number found in the name.
    
    Examples:
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
    Returns a color depending on the filename:
    - "best" -> blue, "worst" -> red, otherwise grey.
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
    Visualizes spores results.
    
    1) For each image (with Count > 1), plots a histogram of diameters (in µm).
    2) Creates a combined bar chart with three subplots for:
         - Count,
         - Mean Diameter (µm) with error bars (Std_Diameter_um),
         - Fungus Area Percentage.
    
    For both visualizations:
      - X-axis labels are generated using Short_Name_X and rotated 45°.
      - All texts (titles, labels, ticks) are in English, using Times New Roman, bold, size 16.
    
    The resulting plots are saved in a subdirectory "graph" under the folder of data_scale_path.
    """
    # Set global font properties
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['font.size'] = 16
    
    # Define directory for saving graphs
    graph_dir = os.path.join(os.path.dirname(data_scale_path), "graph")
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    
    # Filter images with Count > 1
    df_filtered = df_scale_calc[df_scale_calc['Count'] > 1].copy()
    if df_filtered.empty:
        print("No images with Count > 1 for visualization.")
        return
    
    # Visualization of histograms for each image
    for idx, row in df_filtered.iterrows():
        file_base = row['File']
        short_label = Short_Name_X(file_base)
        # Extract diameter data for the image from merged_data
        spores = merged_data[merged_data['BaseName'] == file_base]['Diameter_um'].dropna()
        if spores.empty:
            continue
        plt.figure()
        plt.hist(spores, bins='auto', edgecolor='black')
        plt.title(f"Histogram of Diameters: {short_label}")
        plt.xlabel("Diameter of sporangium (µm)", fontweight='bold', fontsize=16)
        plt.xticks(rotation=45, fontsize=16)  # чтобы цифры по оси X имели такой же размер
        # plt.xlabel("Diameter (µm)")
        plt.ylabel("Frequency of spores / interval", fontweight='bold', fontsize=16)
        plt.xticks(rotation=0)
        hist_path = os.path.join(graph_dir, f"hist_{short_label}.png")
        # hist_path = os.path.join(graph_dir, f"hist_{short_label}.svg")
        plt.savefig(hist_path, bbox_inches='tight')
        plt.close()
        print(f"Histogram for {short_label} saved in {hist_path}")
    
    # Prepare data for bar charts: add short labels and colors
    df_temp = df_filtered.copy()
    df_temp['short'] = df_temp['File'].apply(Short_Name_X)
    df_temp['color'] = df_temp['File'].apply(get_color)
    
    # Sort data for each metric
    df_count = df_temp.sort_values(by='Count', ascending=True)
    df_mean_diam = df_temp.sort_values(by='Mean_Diameter_um', ascending=True)
    df_fungus = df_temp.sort_values(by='Fungus_Area_Percentage', ascending=True)
    
    # Create a figure with 3 subplots
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    
    # Bar chart for Count
    x1 = np.arange(len(df_count))
    axs[0].bar(x1, df_count['Count'], color=df_count['color'])
    axs[0].set_title("Count")
    axs[0].set_xticks(x1)
    axs[0].set_xticklabels(df_count['short'],fontsize=10, rotation=45)
    axs[0].set_ylabel("Spore Count")
    
    # Bar chart for Mean Diameter with error bars
    x2 = np.arange(len(df_mean_diam))
    axs[1].bar(x2, df_mean_diam['Mean_Diameter_um'], yerr=df_mean_diam['Std_Diameter_um'], capsize=5, color=df_mean_diam['color'])
    axs[1].set_title("Mean Diameter (µm)")
    axs[1].set_xticks(x2)
    axs[1].set_xticklabels(df_mean_diam['short'],fontsize=10, rotation=45)
    axs[1].set_ylabel("Diameter of sporangium (µm)")
    
    # Bar chart for Fungus Area Percentage
    x3 = np.arange(len(df_fungus))
    axs[2].bar(x3, df_fungus['Fungus_Area_Percentage'], color=df_fungus['color'])
    axs[2].set_title("Fungus Area Percentage")
    axs[2].set_xticks(x3)
    axs[2].set_xticklabels(df_fungus['short'],fontsize=10, rotation=45)
    axs[2].set_ylabel("Percentage (%)")
    
    plt.suptitle("Image Statistics (Count > 1)")
    bar_chart_path = os.path.join(graph_dir, "bar_chart.png")
    # bar_chart_path = os.path.join(graph_dir, "bar_chart.svg")
    plt.savefig(bar_chart_path, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"Bar chart saved in {bar_chart_path}")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde

def visualize_grouped_density(data, data_scale_path, group_column='BaseName', value_column='Diameter',
                              title='Density curves of spore diameter (FL12 vs FL9)'):
    """
    Visualizes density curves for two groups (FL12 and FL9) on a single plot.

    Parameters:
    - data: DataFrame containing the analysis results. It should have columns for grouping (e.g., 'BaseName')
            and measurements (e.g., 'Diameter').
    - data_scale_path: Path used to determine the output folder for graphs.
    - group_column: Name of the column with grouping information. Default is 'BaseName'.
    - value_column: Name of the column with the measured value (e.g., spore diameter). Default is 'Diameter'.
    - title: Title of the plot.
    """
    # Create graph output directory based on data_scale_path
    graph_dir = os.path.join(os.path.dirname(data_scale_path), "graph")
    os.makedirs(graph_dir, exist_ok=True)
    
    # Filter data for groups "worst" and "best" (case insensitive)
    worst_data = data[data[group_column].str.contains("worst", case=False, na=False)]
    best_data = data[data[group_column].str.contains("best", case=False, na=False)]
    
    plt.figure(figsize=(10, 6))
    
    # Set color palette so that colors for groups are consistent
    colors = sns.color_palette("deep")
    worst_color = colors[0]
    best_color = colors[1]

    # Plot density curves with fill for each group using the new labels
    sns.kdeplot(worst_data[value_column], label="FL12", fill=True, alpha=0.5, color=worst_color)
    sns.kdeplot(best_data[value_column], label="FL9", fill=True, alpha=0.5, color=best_color)
    
    xgrid = np.linspace(0, 200, 1000)  # grid for KDE evaluation

    # Add vertical dashed lines for the maximum density points
    if not worst_data.empty:
        kde_worst = gaussian_kde(worst_data[value_column])
        y_worst = kde_worst(xgrid)
        x_max_worst = xgrid[np.argmax(y_worst)]
        plt.axvline(x=x_max_worst, color=worst_color, linestyle="--",
                    label=f"Max FL12: {x_max_worst:.1f}")
    
    if not best_data.empty:
        kde_best = gaussian_kde(best_data[value_column])
        y_best = kde_best(xgrid)
        x_max_best = xgrid[np.argmax(y_best)]
        plt.axvline(x=x_max_best, color=best_color, linestyle="--",
                    label=f"Max FL9: {x_max_best:.1f}")

    # Set title and labels in English
    plt.title(title, fontsize=16, fontweight='bold')
    # plt.xlabel("Spore diameter (um)", fontsize=14, fontweight='bold')
    plt.xlabel("Diameter of sporangium (μm)", fontsize=14, fontweight='bold')
    plt.ylabel("Density", fontsize=14, fontweight='bold')
    
    # Set x-axis ticks and limits
    plt.xticks(np.arange(0, 210, 10), fontsize=12, rotation=45)
    plt.xlim(0, 200)
    plt.yticks(fontsize=12)
    
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    
    dens_chart_path = os.path.join(graph_dir, "dens_chart.png")
    plt.savefig(dens_chart_path, bbox_inches='tight')
    plt.show()



# Пример использования функции:
if __name__ == '__main__':
    # Пути к исходным файлам
    data_xy_path = r"G:\My\sov\extract\Spores\original_img\test\best\4x\result.xlsx"
    data_scale_path = r"G:\My\sov\extract\Spores\original_img\test\best\4x\spores_main.xlsx"
    # Директория с изображениями
    dir_image = r"G:\My\sov\extract\Spores\original_img\test\best\4x"
    
    # Если размеры заданы по умолчанию (3072, 2048), передаем их;
    # Если необходимо брать размеры из файла, можно передать width_param=None, height_param=None.
    # df_scale_calc = process_fungus_stats(data_xy_path, data_scale_path, dir_image, width_param=3072, height_param=2048)
    df_scale_calc, merged_data = process_fungus_stats(data_xy_path, data_scale_path, dir_image, width_param=3072, height_param=2048)
    visualize_spores_results(df_scale_calc, merged_data, data_scale_path)
    visualize_grouped_density(merged_data, data_scale_path, group_column='BaseName', value_column='Diameter',
                              title='Density curves for two groups (FL12 vs FL9)')
    

