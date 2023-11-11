# Листинг 8.7. Методы класса и объекта  
class MyClass:
    def __init__(self):
        self.value=123
        print("Create object", self.value)
    def __del__(self):
        print("Delete object", self.value)
    def set(self, n):
        self.value=n    
    def show(self):
        print("Field object", self.value)
obj=MyClass()
obj.show()
obj.set(100)
MyClass.show(obj)
MyClass.set(obj,200)   
obj.show()
MyClass.__init__(obj)
MyClass.__del__(obj)
obj.show()
obj.value=321
obj.show()
# constructor call via object
obj.__init__()            
obj.__del__()
obj.show()
