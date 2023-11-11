# Листинг 8.5. Объект реализации класса
class Alpha:
    pass
class Bravo:
    pass
MyClass=Alpha
A=MyClass()
MyClass=Bravo
B=MyClass()
Alpha = Bravo
C=Alpha()
MyClass=A.__class__
D=MyClass()
print("digit 7", type(7).__name__)
print("str :", type("it's string").__name__)
print("Object A:", type(A).__name__)
print("Object B:", type(B).__name__)
print("Object C:", type(C).__name__)  # Bravo
print("Object D:", type(D).__name__)  # Alpha
MyClass.__name__="First"
Bravo.__name__="Second"
print("Object A:", type(A).__name__)
print("Object B:", type(B).__name__)
print("Object C:", type(C).__name__)  # Bravo
print("Object D:", type(D).__name__)  # Alpha
