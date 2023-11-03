# Функция для создания объектов:
def create(fields,vals,name=None):
    # Если последний аргумент не текстовый:
    if type(name)!=str:
        name="MisterX"
    # Если первые два аргумента - не списки:
    if type(fields)!=list or type(vals)!=list:
        # Внутренний класс:
        class MyClass:
            # Метод:
            def show(self):
                print("Объект без полей")
                print("Класс",self.__class__.__name__)
    # Если первые два аргумента - списки:
    else:
        # Внутренний класс:
        class MyClass:
            # Конструктор:
            def __init__(self):
                k=0
                for f in fields:
                    self.__dict__[f]=vals[k]
                    k+=1
            # Метод:
            def show(self):
                print("Объект с полями:")
                for s in dir(self):
                    if not s.startswith("_") and s!="show":
                        print(s,"=",self.__dict__[s])
                print("Класс",self.__class__.__name__)
    # Название класса:
    MyClass.__name__=name
    # Результат функции:
    return MyClass()
# Создание объекта и проверка полей:
A=create(["red","green","blue"],[1,2,3],"MyColors")
A.show()
# Создание объекта и проверка полей:
B=create(["alpha","bravo"],["Alpha","Bravo"])
B.show()
# Создание объекта и проверка полей:
C=create(1,2,3)
C.show()
# Изменение значений полей объекта:
A.red=100
A.green=200
A.blue=300
A.show()
# Создание объекта и проверка полей:
D=A.__class__()
D.show()