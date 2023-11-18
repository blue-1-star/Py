"""
для объектов класса определена операция сложения. У каждого объекта
есть поле-список, и при сложении объектов получается новый объект
того же класса. Его поле-список  получается объединением 
полей-списков исходных объектов.
"""
class e_ch9_03:
    def __init__(self, li):
        self.code=li
    def __str__(self):
        return str(self.code)
    def __add__(self, li):
        if type(li)==list:  
            val=self.code          # union two list arguments 
        else:
            val=0
        return e_ch9_03(val)
# GPT Version 
class MyClass:
    def __init__(self, my_list):
        self.my_list = my_list

    def __add__(self, other):
        # Проверка наличия атрибута и его типа
        if hasattr(other, 'my_list') and isinstance(other.my_list, list):
            # Возвращаем новый объект с объединенным списком
            return MyClass(self.my_list + other.my_list)
        else:
            # Если other не является экземпляром MyClass или не содержит my_list, выбрасываем исключение
            raise ValueError("Невозможно выполнить сложение")

# Пример использования
obj1 = MyClass([1, 2, 3])
obj2 = MyClass([4, 5, 6])
result_obj = obj1 + obj2
print(result_obj.my_list)    