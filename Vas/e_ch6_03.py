"""
функция с произвольным количеством числовых аргументов, а результатом возвращается
список из трех элементов: среднее значение аргументов, максимальное
значение среди аргументов и минимальное значение среди аргументов.
"""
def suma(*x):
    def calc():
        s=0
        for i in range(len(x)):   # inside the function calc x will be a tuple
            s+=x[i]
        a = s/len(x)
        res = [s, s/len(x), min(x), max(x)]               
        return res
    return calc()
print(suma(2,4,6,7,10))
