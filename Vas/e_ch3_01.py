# exercises  Chapter 3, p 169, e - 01   
txt="Если в качестве аргумента функции передать текст, \
то результатом возвращается список из букв (символов) данного текста. \
Возможны и другие варианты использования этой функции для создания \
списков — некоторые мы рассмотрим далее."
A=(2,5,7,22,11,35,44,1) 
B=tuple(txt)
#B=list(txt)

n=-1
m=-7
#print(B)
print("size of text =", len(B))
C=B[-22:-1]
C1=B[:7]
#C=B(:6)
print("C:",C)
print("C1:",C1)
C2=B[-7:]
print("C2:",C2)
print("Last 7 B:",B[m:n])
#print("A last: ",A[-4:])
# step
s = 3
B1=B[::s]
print("--------------")
print("Result:",B1)
#print("Reverse:", tuple(reversed(B)))