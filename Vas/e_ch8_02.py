class MyClass:
    def __init__(self, a1, a2):
        if type(a1)==int and type(a2) == int:
            self.number= a1 + a2
        elif type(a1)==str and type(a2) == str:
            self.txt= a1+a2
        elif type(a1)==int and type(a2) == str: 
            self.num = a1
            self.txt = a2
        elif type(a2)==int and type(a1) == str: 
            self.num = a2
            self.txt = a1    
    def show(self):
            # print("Class", self.__class__.__name__)        
        for s in dir(self):
            if not s.startswith("_") and s!="show":
                print(s,"=", self.__dict__[s])
A = MyClass(1,2)
B = MyClass("text1", "text2")
C = MyClass("text1", 2)
D = MyClass(1, "text2")

A.show()
B.show()
C.show()
D.show()

# GPT  
class MyClass_g:
    def __init__(self, *args, **kwargs):
        if all(isinstance(arg, int) for arg in args):
            self.number = sum(args)
        if all(isinstance(arg, str) for arg in args):
            self.txt = "".join(args)
        if 'num' in kwargs and 'txt' in kwargs:
            self.num = kwargs['num']
            self.txt = kwargs['txt']

    def show(self):
        for s in dir(self):
            if not s.startswith("_") and s != "show":
                print(s, "=", getattr(self, s))

A = MyClass_g(3, 2)
B = MyClass_g("text3g", "text4g")
C = MyClass_g(txt="text1", num=2)
D = MyClass_g(1, txt="text2")

A.show()
B.show()
C.show()
D.show()
