import pandas as pd
import matplotlib.pyplot as plt

def analyze_hsv_data(csv_file, background_keyword="background"):
    """
    Считывает CSV-файл, полученный из ImageJ (где для каждой ROI есть измерения
    в каналах Hue, Saturation, Value), выделяет данные фона, строит гистограммы
    по HSV и геометрическим параметрам для спор.
    
    Параметры:
      csv_file : str
          Путь к CSV-файлу, экспортированному из ImageJ.
      background_keyword : str
          Часть текста или слово, по которому можно определить,
          что данная строка относится к фону (например, 'background').
    
    Возвращает:
      df : pandas.DataFrame
          Исходная таблица, прочитанная из CSV.
      pivot_df : pandas.DataFrame
          Сведённая таблица (pivot) по ROI и каналам (Hue/Sat/Val).
      background_hsv : dict
          Словарь со средними значениями HSV фона (если удалось найти).
    """
    # Считываем CSV-файл
    df = pd.read_csv(csv_file)
    
    # Часто в колонке Label хранится информация вида:
    #   "имя_изображения_или_ROI:Hue" 
    #   "имя_изображения_или_ROI:Sat"
    #   "имя_изображения_или_ROI:Val"
    # Разделим Label на две части: имя ROI и название канала
    def parse_label(label):
        # Предположим, что всегда есть двоеточие перед Hue/Sat/Val
        # Например: "myROI:Hue" => ("myROI", "Hue")
        parts = label.rsplit(':', 1)
        if len(parts) == 2:
            region_name, channel = parts
        else:
            # Если почему-то нет двоеточия, считаем весь label именем региона
            region_name = label
            channel = "Unknown"
        return region_name.strip(), channel.strip()
    
    df["region_name"], df["channel"] = zip(*df["Label"].apply(parse_label))
    
    # Предположим, что фон можно найти по некой метке, где в region_name
    # или channel встречается background_keyword. Пример:
    #   "background:Hue"
    #   "my_background_ROI:Val"
    # Либо вы точно знаете имя ROI фона (например, "ROI_Fon").
    
    # Найдём все строки, где region_name или channel содержит background_keyword
    background_mask = df["region_name"].str.contains(background_keyword, case=False, na=False) \
                     | df["channel"].str.contains(background_keyword, case=False, na=False)
    
    background_rows = df[background_mask]
    
    # Словарь для хранения среднего HSV фона (если удалось найти)
    background_hsv = {}
    
    if not background_rows.empty:
        # Часто измерения для фона тоже идут в трёх строчках: Hue, Sat, Val.
        # Вычислим средние значения Mean для каждого канала:
        for ch in ["Hue", "Sat", "Val", "Value"]:  # иногда канал пишется "Value" вместо "Val"
            # Фильтруем строки фона по каналу
            ch_mask = background_rows["channel"].str.lower() == ch.lower()
            if ch_mask.any():
                # Берём среднее из столбца "Mean"
                mean_val = background_rows[ch_mask]["Mean"].mean()
                background_hsv[ch] = mean_val
    
    # Построим сводную таблицу (pivot), чтобы на одной строке
    # для каждого region_name собрать значения Mean, Area и т.д. по каналам
    # (Hue, Sat, Val). Для простоты возьмём только столбцы, которые точно есть.
    columns_of_interest = ["Mean", "Area", "Feret", "Perim.", "MinFeret", "Major", "Minor"]
    
    # pivot_table с агрегацией 'first' (предполагается, что в одной ROI
    # одна строка на каждый канал)
    pivot_df = df.pivot_table(
        index="region_name",
        columns="channel",
        values=columns_of_interest,
        aggfunc="first"
    )
    
    # Пример того, как получить доступ к данным:
    # pivot_df["Mean", "Hue"] => все средние Hue по ROI
    # pivot_df["Area", "Hue"] => площадь для той же ROI (но иногда площадь не зависит от канала,
    #                           поэтому в CSV дублируется, и мы берём "first")
    
    # Допустим, что споры — это все ROI, кроме фона. Отфильтруем их:
    spore_mask = ~pivot_df.index.str.contains(background_keyword, case=False, na=False)
    spore_df = pivot_df[spore_mask].copy()
    
    # Построим гистограммы по Hue, Sat, Val (средние значения в столбце "Mean")
    # Проверим, какие каналы реально есть (Hue, Sat, Val или Value)
    channels_in_data = [c for c in ["Hue", "Sat", "Val", "Value"] if (("Mean", c) in spore_df.columns)]
    
    for ch in channels_in_data:
        plt.figure(figsize=(5, 3))
        plt.hist(spore_df[("Mean", ch)].dropna(), bins=30, color='skyblue', edgecolor='black')
        plt.title(f"Распределение Mean({ch}) среди спор")
        plt.xlabel(f"Mean({ch})")
        plt.ylabel("Частота")
        plt.tight_layout()
        plt.show()
    
    # Построим гистограммы по площади и диаметру (Feret) для спор.
    # Area (у некоторых это может быть одинаковое значение в каждой из трёх строк ROI,
    # поэтому мы берём, например, Area в строке Hue, или просто 'first', как выше).
    if ("Area", "Hue") in spore_df.columns:
        plt.figure(figsize=(5, 3))
        plt.hist(spore_df[("Area", "Hue")].dropna(), bins=30, color='lightgreen', edgecolor='black')
        plt.title("Распределение площади (Area) среди спор")
        plt.xlabel("Area (пиксели)")
        plt.ylabel("Частота")
        plt.tight_layout()
        plt.show()
    
    # Аналогично для Feret (примерный диаметр)
    if ("Feret", "Hue") in spore_df.columns:
        plt.figure(figsize=(5, 3))
        plt.hist(spore_df[("Feret", "Hue")].dropna(), bins=30, color='lightcoral', edgecolor='black')
        plt.title("Распределение диаметра (Feret) среди спор")
        plt.xlabel("Feret (пиксели)")
        plt.ylabel("Частота")
        plt.tight_layout()
        plt.show()
    
    # Число спор — это число ROI, оставшихся после фильтрации фона
    spore_count = spore_df.shape[0]
    print(f"Обнаружено (по таблице) спор (ROI): {spore_count}")
    
    # Пример, как можно вывести средний диаметр (Feret) по всем спорам
    if ("Feret", "Hue") in spore_df.columns:
        mean_diameter = spore_df[("Feret", "Hue")].mean()
        print(f"Средний диаметр (Feret) спор: {mean_diameter:.3f} пикселей")
    
    # Вернём исходные и сводные данные, а также усреднённый фон
    return df, pivot_df, background_hsv


if __name__ == "__main__":
    # Пример использования
    csv_path = "results.csv"  # Путь к вашему CSV-файлу
    df_full, df_pivot, bg_hsv = analyze_hsv_data(csv_path, background_keyword="background")
    
    print("Усреднённые значения HSV фона:", bg_hsv)
