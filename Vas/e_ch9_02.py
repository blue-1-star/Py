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
# GPT VERSION
class CustomObject:
    def __init__(self, integer_value, text_value, float_value):
        self.integer_value = integer_value
        self.text_value = text_value
        self.float_value = float_value

    def __int__(self):
        return int(self.integer_value)

    def __str__(self):
        return str(self.text_value)

    def __float__(self):
        return float(self.float_value)


# Пример использования класса
obj = CustomObject(42, "Hello, world!", 3.14)

# Приведение к целочисленному типу
integer_result = int(obj)
print(f"Integer representation: {integer_result}")

# Приведение к текстовому типу
text_result = str(obj)
print(f"Text representation: {text_result}")

# Приведение к действительному числовому типу
float_result = float(obj)
print(f"Float representation: {float_result}")
