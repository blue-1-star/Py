"""
описана функция, предназначенная для создания объектов. Функции при вызове передается список
и текстовый аргумент. Текстовый аргумент определяет название класса, на основе которого создается объект. 
Текстовые элементы из списка определяют названия полей объекта (нетекстовые аргументы игнорируются).
 Значениями полей объекта являются натуральные числа.
"""
def create_obj(a_list, name):
    if type(name)!=str:
        name="XXX"
    class MyClass:
        def __init__(self):
            self.__class__.__name__ = name 
            for k in a_list:
                if isinstance(k, (str)):
                    self.__dict__[k] = 0
        


        def show(self):
            print("Class:", self.__class__.__name__)
            for s in dir(self):
                if not s.startswith("_") and s!="show":
                    print(s,"=", self.__dict__[s])


    return MyClass()
A = create_obj(["a","b",1,(1,),"next"],"Mr")
A.show()


