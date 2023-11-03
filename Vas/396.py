# Листинг 8.15. Цепочка объектов  
class MyClass:
    def __init__(self, name, n=1):
        self.name=name
        if n==1:
            self.next=None
        else:
            self.next=MyClass(self.name, n-1)
        self.set()
    def __del__(self):
        print("Delete:", self.code)
    def set(self, num=1):
        self.code=self.name+"["+str(num)+"]"
        if self.next!=None:
            self.next.set(num+1)
    def show(self):
        print(self.code)
        if self.next!=None:
            self.next.show()        
print("One object:")
A=MyClass("Alpha")
A.show()
print("Object chain:")
B=MyClass("Bravo",5)
B.show()
print("Starting with the third object")
B.next.next.show()
print("Delete object:")
del A
del B


