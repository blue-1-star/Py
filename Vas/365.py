class MyClass:
    color="Red"
    def set(txt):
        MyClass.color=txt
    def show():
        print(MyClass.color)
MyClass.show()        
MyClass.set("Green")
print(MyClass.color)
MyClass.color ="Blue"
MyClass.show()
A=MyClass()
B=MyClass()
print("Class:",MyClass.color)
print("A:",A.color)
print("B:",B.color)
A.color ="White"
print("Class:",MyClass.color)
print("A:",A.color)
print("B:",B.color)
MyClass.color = "Yellow"
print("Class:",MyClass.color)
print("A:",A.color)
print("B:",B.color)
del A.color
print("Class:",MyClass.color)
print("A:",A.color)
print("B:",B.color)