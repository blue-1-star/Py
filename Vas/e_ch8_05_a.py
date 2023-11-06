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
def get_numeric_fields(obj):
    numeric_fields = {}
    for key, value in obj.items():  # Предполагается, что obj - это словарь.
        # if isinstance(value, (int, float)):
        if isinstance(value, (int)):
            numeric_fields[key] = value
    return numeric_fields;
#  GPT suggested 3 ways of constructing class B  1.  A - class,  2. A - object    3. use function  setattr(self, name, value)

def corr_obj(A):
    nf=get_numeric_fields(vars(A))
    class Bcl:
        def __init__(self):
            for name, value in nf.items():
                setattr(self,name,value)                        
            Bcl.__name__= "new_class_on_Acl"
        def show(self):
            print("Class:", self.__class__.__name__)
            for s in dir(self):
                if not s.startswith("_") and s!="show":
                    print(s,"=", self.__dict__[s])
    return Bcl()
def cr_subclass(class_name, A):
    nf ={name:value for name, value in vars(A).items() if isinstance(value,(int, float))}
    # create new class on base class A
    class B(A):
        def __init__(self):
            super().__init__()
            self.__dict__.update(nf)
    B.__name__=class_name
    return B()        

B = corr_obj(A)
B.show()
print(vars(B))
# b=cr_subclass("BonA",A)
# print("version 1",vars(b))




