"""
создается итератор, генерирующий нечетные натуральные числа. 
Количество генерируемых чисел определяется аргументом конструктора
"""
class e_ch9_09:
    def __init__(self,n):
        li=[i for i in range(n) if i%2 != 0]
        self.vals=iter(li)
        return self.vals
# A=e_ch9_09(3)
# n = 3 
# li=[i for i in range(n) if i%2 != 0]       
# for i in A.vals:
    # print(i)
# GPT Version
class OddNumbersIterator:
    def __init__(self, count):
        self.count = count
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.count <= 0:
            raise StopIteration

        result = self.current
        self.current += 2
        self.count -= 1
        return result

# Пример использования
count = 5
odd_iterator = OddNumbersIterator(count)

for num in odd_iterator:
    print(num)

