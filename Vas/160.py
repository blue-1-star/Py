# Листинг 3.10
n=10
A = [1,1]
for k in range(n-2):
    A.append(A[-1]+A[-2])
print("A:",A)
# Changing the order of elements in an array
for k in range(len(A)-1):
    #A.append(A.pop(–k-2))
    A.append(A.pop(-k-2))
print("A:", A)
A.remove(max(A))
print("A:",A)
A.remove(min(A))
print("A:",A)
A.insert(0, A[0]+A[1])
print("A:",A)
B=[]
for k in range(len(A)//2):
    B.insert(0,A.pop(-1))
print("A:", A)
print("B:", B)
A.append(B)
print("A:", A)
A.pop(-1)
A.extend(B)
print("A:", A)





