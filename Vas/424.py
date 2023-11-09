# Листинг 9.7. Использование инструкции super()
class Alpha:
    def __init__(self, num):
        self.code=num
        print("assigned a value to a field:  code ")
    def show(self):
        print(" field code: ",self.code)
class Bravo(Alpha):
    def __init__(self, num, txt):
        super().__init__(num)
        self.name=txt
        print("assigned a value to a field  name")
    def show(self):
        super().show()
        print("name:", self.name)
class Charlie(Bravo):
    def __init__(self, num, txt, val):
        super().__init__(num, txt)
        self.value=val
        print("assigned a value to a field  value")
    def show(self):
        super().show()
        print("value:", self.value)
print("Object A")        
A=Alpha(100)
A.show()
print("Object B")        
B=Bravo(200, "B")
B.show()
print("Object C")        
C=Charlie(300,"C",[1,2,3])
C.show()
