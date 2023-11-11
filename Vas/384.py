# Листинг 8.11. Класс как аргумент и результат функции
# Функция получает ссылку на класс в качестве аргумента
# The function receives a reference to a class as an argument and the result returns a reference to the class
def F(Alpha):
    class Bravo:
        value=Alpha()
    Bravo.__name__="My"+Alpha.__name__
    return Bravo
class Charlie:
    def __init__(self):
        self.number=123
    def show(self):
        print("Field number:", self.number)
obj = F(Charlie)()        
obj.value.show()
print("Class of object obj:", obj.__class__.__name__)
print("Class of field value:", obj.value.__class__.__name__)


