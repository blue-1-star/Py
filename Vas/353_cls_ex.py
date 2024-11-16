
"""
если мы описываем в классе метод, который планируем вызывать из объекта (а на самом деле есть и другие варианты),
то в таком методе первый аргумент будет называться self и обозначает
он объект, из которого метод вызывается. 
GPT 
1. Статические методы (@staticmethod)
Статический метод — это метод, который не зависит от экземпляра класса (объекта)
и самого класса. Он не имеет аргумента self или cls. Это обычная функция, помещённая внутрь класса для удобства.
class MyClass:
    @staticmethod
    def static_method():
        print("Это статический метод.")

MyClass.static_method()
----
2. Методы класса (@classmethod)
Метод класса получает в качестве первого аргумента сам класс, а не объект. Для этого используется аргумент cls.
Такие методы часто применяются для работы с атрибутами или данными класса, а не конкретного экземпляра.

3. Модулирование методов через внешние функции
Иногда вместо метода используют обычную функцию, которая определяется вне класса,
но работает с его объектом. Например:

class MyClass:
    def __init__(self, name):
        self.name = name

def external_function(instance):
    print(f"Внешняя функция работает с объектом: {instance.name}")

obj = MyClass("Пример")
external_function(obj)

------------------
4. Методы-объекты (functools.partial или staticmethod в конструкторе)
Иногда методы могут быть добавлены к объекту или классу динамически (например, в момент выполнения программы):
from functools import partial

class MyClass:
    def __init__(self, name):
        self.name = name

    def greet(self, greeting):
        print(f"{greeting}, {self.name}!")

obj = MyClass("Иван")
custom_greet = partial(obj.greet, "Привет")
custom_greet()  # Привет, Иван!


"""
class MyClass:
    class_attribute = "Атрибут класса"

    @classmethod
    def class_method(cls):
        print(f"Это метод класса, атрибут: {cls.class_attribute}")

class MyClass1:
    class_attribute = "Атрибут класса"

    # @classmethod
    def class_method(cls):
        print(f"Это метод класса без декоратора @, атрибут: {cls.class_attribute}")

MyClass.class_method()
# MyClass1.class_method()

class MyClass2:

    def __init__(self, name):
        self.name = name

# def external_function(instance):
def external_function(inst):
    print(f"Внешняя функция работает с объектом: {inst.name}")

obj = MyClass2("Пример")
external_function(obj)
"""
3. Модулирование методов через внешние функции
Иногда вместо метода используют обычную функцию, которая определяется вне класса,
но работает с его объектом.

4. Методы-объекты (functools.partial или staticmethod в конструкторе)
Иногда методы могут быть добавлены к объекту или классу динамически (например, в момент выполнения программы):

from functools import partial

class MyClass:
    def __init__(self, name):
        self.name = name

    def greet(self, greeting):
        print(f"{greeting}, {self.name}!")

obj = MyClass("Иван")
custom_greet = partial(obj.greet, "Привет")
custom_greet()  # Привет, Иван!

--------------
5. Методы, переданные в качестве аргументов или замыкания
Методы могут быть определены как функции вне класса,
а затем переданы в качестве аргумента или функции обратного вызова.

6. Методы через метаклассы
Если вы используете метаклассы, методы могут определяться не через self или cls,
а с дополнительной кастомной логикой.


"""
from functools import partial

class MyClass3:
    def __init__(self, name):
        self.name = name

    def greet(self, greeting):
        print(f"{greeting}, {self.name}!")

obj = MyClass3("Иван")
custom_greet = partial(obj.greet, "Привет")
custom_greet()  # Привет, Иван!
"""
functools.partial — это встроенная функция в Python из модуля functools,
которая позволяет создавать частично применённые функции.

Это значит, что вы можете зафиксировать некоторые аргументы функции и создать новую функцию, 
которая будет автоматически использовать эти аргументы при вызове. Это полезно,
если вам нужно повторно использовать функцию с одними и теми же аргументами,
но не хотите каждый раз их передавать.

Как это работает?
Когда вы вызываете partial(func, *args, **kwargs), создаётся новая функция,
которая ведёт себя как func, но автоматически подставляет заданные аргументы *args и **kwargs.


"""

