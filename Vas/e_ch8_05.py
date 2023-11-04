"""
описывается функция, предназначенная для создания объекта. Объект создается на основе уже существующего объекта,
 который передается функции в качестве аргумента.
В создаваемый объект добавляются только те неслужебные поля из исходного объекта, которые имеют целочисленное значен
"""
class Acl:
    def __init__(self):
        self.a1=1
        self.a2=2
        self.a3="c"
    def show(self):        
        for f in dir(self):
            if not f.startswith("_") and f!="show":
                print(f,"=",self.__dict__[f]) 
        print("Class:",self.__class__.__name__)        
A = Acl()
A.show()
def corr_obj(A):

    return B

