import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def gen_data(file):
    df = pd.read_excel(file)
    df = df.rename(columns={'Treatment': 'TR', 'Treatment_code': 'code', 'Day': 'D', 'Fv/Fm': 'TF'})
    df['code'] = df['code'].astype(int)
    df['D'] = df['D'].astype(int) 
    df[['Source', 'Factor', 'Day']] = pd.DataFrame(df.apply(lambda row: analyze_string(row['TR']), axis=1).tolist(), index=df.index)
    return df

def stats_group(df, col):
    # Проверяем тип переданного параметра col
    if isinstance(col, int):
        # Если это номер столбца, получаем имя столбца по номеру
        col = df.columns[col]
    elif isinstance(col, str):
        # Если это имя столбца, проверяем, что такое имя существует в датафрейме
        if col not in df.columns:
            raise ValueError(f"Column '{col}' does not exist in the DataFrame")
    else:
        raise TypeError("Parameter 'col' must be either an integer or a string")
    
    # Группируем по указанному столбцу
    grouped = df.groupby(col)
    # Словарь для хранения статистик
    statistics = {'Source': [], 'Factor': [], 'Day': [], 'Mean': [], 'Max': [], 'Min': [], 'Std': []}

# Рассчитываем статистики для каждой группы
    for code, group in grouped:
        mean_tf = group['TF'].mean()
        max_tf = group['TF'].max()
        min_tf = group['TF'].min()
        std_tf = group['TF'].std()
        
        statistics['Source'].append(group['Source'].iloc[0])
        statistics['Factor'].append(group['Factor'].iloc[0])
        statistics['Day'].append(group['Day'].iloc[0])
        statistics['Mean'].append(mean_tf)
        statistics['Max'].append(max_tf)
        statistics['Min'].append(min_tf)
        statistics['Std'].append(std_tf) 

    stats_df = pd.DataFrame(statistics)
    return stats_df

def transform(df1, cod):
        codex = {
        9 :['U0','N',7,0],
        10:['U0','F',7,0],
        11:['U0','H',7,0],
        12:['U1','N',7,0],
        13:['U1','F',7,0],
        14:['U1','H',7,0],
        15:['U2','N',7,0],
        16:['U2','F',7,0],
        17:['U2','H',7,0],
        18:['C0','N',7,0],
        19:['C0','F',7,0],
        20:['C0','H',7,0],
        21:['U0','N',10,0],
        22:['U1','N',10,0],
        23:['U2','N',10,0],
        24:['C0','N',10,0],
        25:['U0','F',10,0],
        26:['U1','F',10,0],
        27:['U2','F',10,0],
        28:['C0','F',10,0],
        29:['U0','H',10,0],
        30:['U1','H',10,0],
        31:['U2','H',10,0],
        32:['C0','H',10,0],
        33:['U0','N',14,0],
        34:['U1','N',14,0],
        35:['U2','N',14,0],
        36:['C0','N',14,0],
        37:['U0','F',14,0],
        38:['U1','F',14,0],
        39:['U2','F',14,0],
        40:['C0','F',14,0],
        41:['U0','H',14,0],
        42:['U1','H',14,0],
        43:['U2','H',14,0],
        44:['C0','H',14,0],        
    }
        cond_cod, k = False, 0

        for key, val in codex.items():
            if   key == cod:
                cond_cod  = True
                v1 = df1.loc[df1['code'] == cod, 'TF'].values[k]
                k += 1
                # print(v1)
                break            
        if cond_cod: 
            codex[key][3]=v1
            return codex[key]   # странно, но codex[key] + list(v1)- не работает, так же как и 
                                # codex[key].append(v1)
        else: 
            print('code not defined!')

# analyze string

def analyze_string(input_str):
    # Разбиваем строку на слова
    words = input_str.split()

    # Проверяем, что строка содержит ровно 5 слов
    if len(words) != 5:
        return "Некорректная строка"

    # Проверяем формат каждого слова
    if words[0] != "Day":
        return "Первое слово должно быть 'Day'"
    if not words[1].isdigit() or not words[3].isdigit():
        return "Второе и четвертое слово должны быть числами"
    if words[2] not in ["UGAN", "Control"]:
        return "Третье слово должно быть 'UGAN' или 'Control'"
    if words[4] not in ["N", "F", "H"]:
        return "Пятое слово должно быть 'N', 'F' или 'H'"

    # Определяем префикс в зависимости от третьего слова
    prefix = "U" if words[2] == "UGAN" else "C0"

    # Определяем символ
    symbol = words[4]

    # Определяем первое число
    num1 = int(words[1])
    num2 = int(words[3]) % 10 if prefix != "C0" else ""

    # Формируем результат
    # result = f"{prefix}{num2}_{symbol}_{num1:02d}"
    result = [f"{prefix}{num2}",f"{symbol}", f"{num1:02d}"]
    return result           

def create_bar_charts(stats_df):
    # Уникальные значения для Day
    unique_days = stats_df['Day'].unique()

    # Уникальные факторы и источники
    factors = stats_df['Factor'].unique()
    sources = stats_df['Source'].unique()

    # Создаем графики
    fig, axes = plt.subplots(2, 1, figsize=(16, 12))

    # Ширина столбцов
    width = 0.2

    # Определяем общую высоту для меток дней
    common_y = max(stats_df['Mean'])   # Уменьшаем высоту

    # График 1: Влияние факторов на источники
    colors = ['b', 'g', 'r', 'c']  # Задаем цвета для каждого источника
    for i, day in enumerate(unique_days):
        day_df = stats_df[stats_df['Day'] == day]
        pivot_df = day_df.pivot(index='Factor', columns='Source', values='Mean')
        x = np.arange(len(factors)) + i * (len(factors) + 1)  # добавляем промежуток между днями
        for j, source in enumerate(sources):
            means = pivot_df[source]
            bars = axes[0].bar(x + j * width, means, width, label=source if i == 0 else "", color=colors[j], alpha=0.7)
        # Добавляем метки для каждого дня на одинаковой высоте
        axes[0].text(np.mean(x) + (len(sources) - 1) * width / 2, common_y, f'Day {day}', ha='center', va='bottom')

    # Добавляем подписи для факторов на оси X
    xticks = []
    for i in range(len(unique_days)):
        xticks.extend(np.arange(len(factors)) + i * (len(factors) + 1))
    xticks = [tick + width * (len(sources) - 1) / 2 for tick in xticks]
    axes[0].set_xticks(xticks)
    axes[0].set_xticklabels(np.tile(factors, len(unique_days)))
    axes[0].set_title('Влияние факторов на источники')
    axes[0].set_xlabel('Factor')
    axes[0].set_ylabel('Mean')
    axes[0].legend(title='Source', bbox_to_anchor=(1.05, 1), loc='upper left')

    # График 2: Влияние источников на факторы
    for i, day in enumerate(unique_days):
        day_df = stats_df[stats_df['Day'] == day]
        pivot_df = day_df.pivot(index='Source', columns='Factor', values='Mean')
        x = np.arange(len(sources)) + i * (len(sources) + 1)  # добавляем промежуток между днями
        for j, factor in enumerate(factors):
            means = pivot_df[factor]
            bars = axes[1].bar(x + j * width, means, width, label=factor if i == 0 else "", color=colors[j], alpha=0.7)
        # Добавляем метки для каждого дня на одинаковой высоте
        axes[1].text(np.mean(x) + (len(factors) - 1) * width / 2, common_y, f'Day {day}', ha='center', va='bottom')

    # Добавляем подписи для источников на оси X
    xticks = []
    for i in range(len(unique_days)):
        xticks.extend(np.arange(len(sources)) + i * (len(sources) + 1))
    xticks = [tick + width * (len(factors) - 1) / 2 for tick in xticks]
    axes[1].set_xticks(xticks)
    axes[1].set_xticklabels(np.tile(sources, len(unique_days)))
    axes[1].set_title('Влияние источников на факторы')
    axes[1].set_xlabel('Source')
    axes[1].set_ylabel('Mean')
    axes[1].legend(title='Factor', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()
# 
def create_nested_pie_charts(stats_df):
    # Уникальные значения для Day
    unique_days = stats_df['Day'].unique()

    for day in unique_days:
        day_df = stats_df[stats_df['Day'] == day]

        # Подготовка данных для первого графика: внешние круги по источникам, внутренние по факторам
        outer_values_1 = day_df.groupby('Source')['Mean'].sum()
        inner_values_1 = day_df.groupby(['Source', 'Factor'])['Mean'].sum()
        outer_labels_1 = outer_values_1.index
        inner_labels_1 = [f'{source}-{factor}' for source, factor in inner_values_1.index]

        # Подготовка данных для второго графика: внешние круги по факторам, внутренние по источникам
        outer_values_2 = day_df.groupby('Factor')['Mean'].sum()
        inner_values_2 = day_df.groupby(['Factor', 'Source'])['Mean'].sum()
        outer_labels_2 = outer_values_2.index
        inner_labels_2 = [f'{factor}-{source}' for factor, source in inner_values_2.index]

        fig, axs = plt.subplots(1, 2, figsize=(20, 10), subplot_kw=dict(aspect="equal"))

        # Первый график
        axs[0].pie(outer_values_1, labels=outer_labels_1, radius=1, wedgeprops=dict(width=0.3, edgecolor='w'))
        axs[0].pie(inner_values_1, labels=inner_labels_1, radius=0.7, wedgeprops=dict(width=0.3, edgecolor='w'))
        axs[0].set_title(f'Day {day}: External area - Sources, Internal - Factors')

        # Второй график
        axs[1].pie(outer_values_2, labels=outer_labels_2, radius=1, wedgeprops=dict(width=0.3, edgecolor='w'))
        axs[1].pie(inner_values_2, labels=inner_labels_2, radius=0.7, wedgeprops=dict(width=0.3, edgecolor='w'))
        axs[1].set_title(f'Day {day}: External area - Factors, Internal - Sources')

        plt.show()
