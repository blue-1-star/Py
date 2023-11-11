"""
 класс с переопределенными методами для приведения к разным типам. В частности, у объекта должны
быть поля с целочисленным значением, текстом и действительным числовым значением. При приведении объекта к 
целочисленному, текстовому или действительному числовому типу возвращается значение соответствующего поля
"""
# GPT version
class MyClass:
    instances = []

    def __init__(self, value):
        self.value = value
        MyClass.instances.append(self)

# Создаем несколько объектов
obj1 = MyClass(10)
obj2 = MyClass(20)
obj3 = MyClass(30)

# Перебираем все объекты класса
for instance in MyClass.instances:
    print(instance.value)
# A = MyClass(11)

