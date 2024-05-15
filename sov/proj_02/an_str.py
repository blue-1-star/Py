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

# Примеры использования
print(analyze_string("Day 7 UGAN 11 N"))  # Вывод: U1_N_07
print(analyze_string("Day 10 Control 1 F"))  # Вывод: C0_F_10
print(analyze_string("Day 14 UGAN 12 H"))  # Вывод: U2_H_14


"""
можешь предложить функцию - анализатор текстовой строки 
Строка содержит 5 слов
Втрое и четвертое слово - числа
Первое слово Day
3-е слово - UGAN | Control
5- слово  -  N | F | H

На выходе должно быть
U либо C с числом  = (второе число ) Mod 10 
( если C то C0)
подчерк
символ F | N | H
подчерк
первое число

Например 
строка Day 7 UGAN 11 N -> U1_N_7   ( для красоты можно показывать 07)

Day 10 Control 1 F   ->    C0_F_10 

"""