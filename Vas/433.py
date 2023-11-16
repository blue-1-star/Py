# Листинг 9.9. Приведение типов
class MyClass:
    def __init__(self, val):
        self.value=val
    def __str__(self):
        return "Field "+str(self.value)
    def __bool__(self):
        if type(self.value)==int:
            return True
        else:
            return False
    def __int__(self):
        if self:
            return self.value
        else:
            return 0
A=MyClass(100)
print(A)
print("Number ", int(A))
print("A — 1 =", int(A)-1)        
B=MyClass("B")
print(B)
print("Number ", int(B))
print("B + 1 =", int(B)+1)

