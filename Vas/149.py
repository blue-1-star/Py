#
from  random import *
# function to show  sublist 
def show(A):
    for a in A:
        for s in a:
            print(s, end=" ")
        print()
# function for creating a nested list of random digits
def rands(m, n):
    res=[[randint(0,9) for i in range(n)] for j in range(m)]
    return res
# function for creating a nested list of letters
def symbs(m, n):
    #val='A'
    val='А'
    res=[['' for i in range(n)] for j in range(m)]
    for i in range(m):
        for j in range(n):
            res[i][j]=val
            val=chr(ord(val)+1)
    return res
#  nested list creation
A=[[(j+1)*10+i+1 for i in range(5)] for j in range(3)]
print("List A")
show(A)
#print(A)
seed(2019)
B=rands(3,4)
print("List B")
show(B)
C=symbs(3,5)
print("List C")
show(C)
# List defines the number of rows in a nested list
size=[3,5,4,6]
D=[['*' for k in range(s)] for s in size]
print("List D")
show(D)
