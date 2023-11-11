# Листинг 8.8. Атрибуты классов и объектов
class Alpha:
    pass
class Bravo:
    name="Bravo"
    def display():
        print("Field name:",Bravo.name)
    def show(self):
        print("Field value:",self.value)
    def __init__(self):
        self.value=123    
A=Alpha()
B=Bravo()
print("Class Alpha:")        
n=1
for s in Alpha.__dict__:
    print("["+str(n)+"] "+s+":", Alpha.__dict__[s])
    n+=1
print("Class Bravo:")        
n=1
for s in Bravo.__dict__:
    print("["+str(n)+"] "+s+":", Bravo.__dict__[s])
    n+=1
print("Object A:",A.__dict__)    
print("Object B:",B.__dict__)    
Bravo.display()
Alpha.display=Bravo.display
del Bravo.display
B.show()
A.color="Red"
B.show=lambda: print("Object B:", B.value)
print("Class Alpha:")        
n=1
for s in Alpha.__dict__:
    print("["+str(n)+"] "+s+":", Alpha.__dict__[s])
    n+=1
print("Class Bravo:")        
n=1
for s in Bravo.__dict__:
    print("["+str(n)+"] "+s+":", Bravo.__dict__[s])
    n+=1
print("Object A:",A.__dict__)    
print("Object B:",B.__dict__) 
Alpha.display()
Bravo.show(B)
B.show()
    

