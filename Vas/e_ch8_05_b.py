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
        self.b=3.14
A = Acl()
def cr_subclass(class_name, A):
    nf ={name:value for name, value in vars(A).items() if isinstance(value,(int, float))}
    # create new class on base class A
    class B(A):
        def __init__(self):
            super().__init__()
            self.__dict__.update(nf)
    B.__name__=class_name
    return B()        
b=cr_subclass("BonA",A)
print("version 1",vars(b))
# not working    2023-11-06 12:14:50





