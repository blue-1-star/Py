# Листинг 9.10. Знакомство с перегрузкой операторов
class MyClass:
    def __init__(self, num):
        self.code=num
    def __str__(self):
        return str(self.code)
    def __add__(self, n):
        if type(n)==int:
            val=self.code+n
        else:
            val=0
        return MyClass(val)
    def __radd__(self, n):
        if type(n)==int:
            val=self.code-n
        else:
            val=0
        return MyClass(val)
A=MyClass(100)
print("Object of Class A:",A)
B=A+25
print("Object B:",B)
C=A+"Hello"
print("Object C:",C)
B1 = 11+A
print("radd operation B1:",B1)
