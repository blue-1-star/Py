"""
У объектов класса должно быть поле, представляющее собой числовой список. Этот список
формируется на основе списка, переданного конструктору в качестве аргумента. При этом из списка-аргумента в список-поле включаются только 
числовые элементы (элементы других типов игнорируются). 
Необходимо также описать метод, отображающий содержимое поля-списка,
а также метод, вычисляющий среднее значение элементов поля-списка
"""
class MyClass:
    def __init__(self, a_list):
        a1 = []
        for k in a_list:
            if type(k) == int or type(k) == float:
                a1.append(k)
        self.a = a1
    def show(self):
        print(self.a)
    def av(self):
        print("av:",sum(self.a)/len(self.a) )
A = MyClass([1,2,3,4,"q",(2.4,3.17),(6,)])        
A.show()
A.av()
# GPT Version
class MyClass_g:
    def __init__(self, a_list):
        a1 = []
        for k in a_list:
            if isinstance(k, (int, float)):
                a1.append(k)
        self.a = a1

    def show(self):
        print(self.a)

    def av(self):
        if not self.a:
            return None
        return sum(self.a) / len(self.a)
B = MyClass_g([1,2,3,4,"q",(2.4,3.17),(6,)])    
B.show()
print(B.av())



