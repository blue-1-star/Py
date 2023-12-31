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
    def show(self):  
        fields_origin=[]      
        for f in dir(self):
            if not f.startswith("_") and f!="show":
                print(f,"=",self.__dict__[f]) 
        print("Class:",self.__class__.__name__)

A = Acl()
# A.show()
def get_numeric_fields(obj):
    numeric_fields = {}
    for key, value in obj.items():  # Предполагается, что obj - это словарь.
        if isinstance(value, (int, float)):
            numeric_fields[key] = value
    return numeric_fields;

#get dict from object :   vars()  or .__dict__  
# d = vars(A)
# print("method vars:",d)
# print("numeric_fields:",get_numeric_fields(vars(A)))





#  GPT suggested 3 ways of constructing class B  1.  A - class 2. A - object    3. use function  setattr(self, name, value)

def corr_obj(A):
    nf=get_numeric_fields(vars(A))

    class Bcl:
        def __init__(self):
            for name, value in nf.items():
                setattr(self,name,value)
                        
    Bcl.__name__= "new_class_on_Acl"
    return Bcl
B = corr_obj(A)
print(vars(B))


