# Creation of a surface copy
A=[1,3,[10,20],"Python",[40,50]]
B=A[:]
C=A.copy()
print("Origin value")
print("A:", A)
print("B:", B)
print("C:", C)
A[0]=[100,200]
A[2][1]=300
A[3]="Java"
A[4]=90
C[4][1]="C++"
print("After changes")
print("A:", A)
print("B:", B)
print("C:", C)

