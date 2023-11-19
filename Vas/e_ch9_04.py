"""
для объектов предусмотрены операции сложения с числом, вычитания числа
и вычитания из числа, а также умножения на число и деления на число. 
У объекта должно быть поле с числовым значением, и при выполнении указанных
операций они должны выполняться с полем объекта
"""
class e_ch9_04:
    def __init__(self, num):
        self.num=num
    def __str__(self):
        return str(self.num)
    def __add__(self, ad):
        return self.num + ad
    def __sub__(self, ad):
        return self.num - ad
    def __rsub__(self, sb):
        return sb - self.num 
    def __mul__(self, ml):
        return ml*self.num 
    def __truediv__(self, td):
        return self.num/td 
    
A = e_ch9_04(2)
print(A)
print("A+7=",A+7)
print("A-3=",A-3)
print("3-A=",3-A)
print("A*4=",A*4)
print("A/2=",A/2)



