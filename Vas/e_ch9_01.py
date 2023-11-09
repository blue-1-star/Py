"""
создается цепочка наследования
из трех классов. У объекта исходного класса имеется поле, и у каждого
следующего класса добавляется по одному полю. Опишите методы, переопределяемые в производных классах, 
которые позволяют присваивать значения полям и отображать значения полей
"""
# p 475
class A:
    def __init__(self,f1):
        self.f1 = f1
    def show(self):
        print(self.f1)
    def __str__(self):
        return f'A object with f1={self.f1}'
class B(A):
    def __init__(self,f2):
        self.f2 = f2
    def show(self):
        print(self.f2)
    def __str__(self):
        return f'B object with f2={self.f2}'    
class C(B):
    def __init__(self,f3):
        self.f3 = f3
    def show(self):
        print(self.f3)
    def __str__(self):
        return f'C object with f3={self.f3}'            
a = A(22)
b = B(64) 
c= C(88)   
a.show()
print(a)
print(b)
print(c)



        