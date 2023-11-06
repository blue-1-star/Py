"""
Напишите программу, в которой описан класс и функция, предназначенная для создания списка из объектов. У объектов класса должно быть поле
(предназначенное для записи целочисленных значений). При вызове функции аргументом ей передается целое число, 
определяющее количество объектов в списке. Поля объектов заполняются целыми нечетными числами.
"""
#  I'm dumb, in a stupor before this task.
# However, the GPT solves such a thing in a second
class MyObject:
    def __init__(self, value):
        # Поле объекта, предназначенное для записи целочисленных нечетных значений
        self.value = value

def create_object_list(num_objects):
    object_list = []
    for i in range(num_objects):
        # Создаем объект MyObject с нечетным значением
        obj = MyObject(2 * i + 1)
        object_list.append(obj)
    return object_list

# Пример использования функции
num_objects = 5  # Задаем количество объектов в списке
objects = create_object_list(num_objects)

# Выводим значения полей объектов
for obj in objects:
    print(obj.value)
