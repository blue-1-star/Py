import pandas as pd
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