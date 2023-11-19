"""
класс, объекты которого можно индексировать. В частности, у объекта
должно быть два поля-списка с числами. При индексировании объекта
возвращается сумма элементов из списков с соответствующим индексом.
Если в каком-то списке нет такого элемента, он заменяется нулевым значением.
"""
class e_ch9_07:
    def __init__(self, li1, li2):
        self.li1 = li1
        self.li2 = li2
    def __setitem__(self, k, value):
        # Присваивание значения элементу по индексу в соответствующем списке
        if 0 <= k < len(self.li1):
            self.li1[k] = value
        elif len(self.li1) <= k < len(self.li1) + len(self.li2):
            self.li2[k - len(self.li1)] = value
        else:
            raise IndexError("Индекс вне диапазона")
    # def __getitem_(k,li1, li2):
        # return li1[k]+li2[k]
    # def __getitem__(self, k):  # GPT version
    #     # Возвращает сумму элементов из списков с соответствующим индексом
    #     val1 = self.li1[k] if k < len(self.li1) else 0
    #     val2 = self.li2[k] if k < len(self.li2) else 0
    #     return val1 + val2       
    # 
    def __getitem__(self, k):
        # Возвращает сумму элементов из списков с соответствующим индексом
        val1 = self.li1[k] if 0 <= k < len(self.li1) else 0
        val2 = self.li2[k - len(self.li1)] if len(self.li1) <= k < len(self.li1) + len(self.li2) else 0
        return val1 + val2 
A1 = e_ch9_07([1,2,3],[4,5,6])    
print("Index 0:",A1[0]," Index 1:", A1[1] )
A1[3] = 20
print(A1[3])  # Выведет 20 (0 + 20)
A1[4] = 11
print(A1[4])  # Выведет 11 (0 + 11)

    

   