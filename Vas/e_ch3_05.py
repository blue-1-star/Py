# ex 05 ch 03  p 170
from  random import *
seed(1777)
def rands(m, n):
    res=[[randint(0,55) for i in range(n)] for j in range(m)]
    return res
def show(A):
    for a in A:
        for s in a:
            print(s, end=" ")
        print()    
def del_row_col(A, dm, dn):
    #  Delete row = dm
    A.pop(dm-1)
    # row dimensionality of the matrix minus 1 -> m-1

    for i in range(m-1):
        A[i].pop(dn)
        # a column  dn  in each row is deleted
        A[i].pop(dn-1)


dm, dn = 2, 3   # номера удаляемых строки и столбца
m, n = 4,5
A=rands(m,n) 
show(A)
print("-------")
del_row_col(A,dm,dn)
show(A)    


