"""
методом рекурсии символы из текста, переданного аргументом функции, отображаются «через один»:
то есть отображается первый, третий, пятый и так далее, символы
"""
# GPT Author
def display_alternate_chars(text, index=0, res =""):
    # Базовый случай: если индекс вышел за пределы длины текста, завершаем рекурсию
    # res = ""
    if index >= len(text):
        return
    # Выводим символ с текущим индексом
    #print(text[index])
    res+=text[index]
    # Рекурсивно вызываем функцию для следующего символа через один
    display_alternate_chars(text, index + 2, res)
    return(res)

# Пример использования функции:
text = "Пример текста для проверки"
res =display_alternate_chars(text)
print(res)


