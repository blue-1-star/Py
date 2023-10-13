# Листинг 3.2. Операции со списками
A=[10,20,30]
print("A:", A)
B=["Python",[1,2]]
print("B:", B)
C=A+B
print("C:", C)
# Add element to end list
C+=[100]
print("C:", C)
C[1:2] = []
print("C:", C)
# Add element to begin list
C=[200]+C
print("C:", C)
C[:3]=["A","B"]
print("C:", C)
C[2:2]=[8,9]
print("C:", C)
C[2:3] = ["New","Insert"]
print("C:", C)

