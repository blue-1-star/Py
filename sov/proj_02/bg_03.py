# dict transform data
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
