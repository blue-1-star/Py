"""
для объектов класса предусмотрены
операции сравнения. У каждого объекта есть поле-список с числовыми
значениями. Операции сравнения выполняются так: объекты на предмет 
равенства проверяются по первому элементу в списках, на предмет
«не равно» — по второму элементу в списках, «меньше» — по третьему 
элементу в списках, и так далее. Если соответствующего элемента
в списке нет, используется нулевое значение
"""
class e_ch9_05:
    def __init__(self, li):
        self.li= li
        Nmax=3                       # количество (вшитое) определенных операций   
        while  len(self.li) < Nmax:  # добавляем нулями до Nmax 
            self.li.append(0)

    def __str__(self):
        return str(self.li)
    def __eq__(self, other):
        if self.li[0]== other.li[0]:
            return True
        else:
            return False
    def __ne__(self, other):
        if self.li[1]== other.li[1]:
            return True
        else:
            return False    
    def __lt__(self, other):
        if self.li[2] < other.li[2]:
            return True
        else:
            return False        
        
A1 = e_ch9_05([1,2])
A2 = e_ch9_05([1,4,3])
A3 = e_ch9_05([3,4])
A4 = e_ch9_05([3,7,8,11])
A5 = e_ch9_05([3,2])
A6 = e_ch9_05([1,5,-1])
print("A1=",A1)
print("A2=",A2)
print("A6=",A6)
print("A4=",A4)

if A1 == A2:
    print("A1==A2") 
if A2 == A6:
    print("A2==A6")   
if A1 == A3:
    print("A1==A3")         
if A1 == A6:
    print("A1==A6")       
if A2 != A3:
    print("A2!=A3")
if A1 < A4:
    print("A1 < A4")    
if A6 < A3:
    print("A6 < A3")    
# else:
#     print("A1~=A2")    
# print("A1.li=",A1.li[0]," ", A1.li[1])
# print("A3.li=",A3.li[0]," ", A3.li[1])
# print("A6.li=",A6.li[0]," ", A6.li[1])




       