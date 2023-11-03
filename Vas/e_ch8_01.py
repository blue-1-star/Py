# p 402
"""
 класс со следующими
характеристиками. У класса есть конструктор, которому (кроме ссылки
на объект вызова) передаются два значения. Эти значения присваиваются полям объекта класса.
 В классе должен быть описан метод, при вызове которого отображаются значения полей класса
 """
import inspect
class MyClass:
    def __init__(self, a,b):
        self.fa = a
        self.fb = b
    def show(self):
        print("Class", self.__class__.__name__)        
        for s in dir(self):
            if not s.startswith("_") and s!="show":
                print(s,"=", self.__dict__[s])
A = MyClass(12,9)           
A.show()
# print(dir(A))
# print(A.__dict__.keys())
#  ------    GPT  

class MyClass_gpt:
    def __init__(self, a, b):
        self.fa = a
        self.fb = b

    def show(self):
        print("Class", self.__class__.__name__)
        for name, value in inspect.getmembers(self):
            if not name.startswith("_"):
                print(name, "=", value)

Ag = MyClass_gpt(1, 5)
Ag.show()


