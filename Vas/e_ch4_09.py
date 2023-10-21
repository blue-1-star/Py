txt = "ИНСУМИНИН"
S = set(txt)
D=dict()
Tl = list(txt) 
print(S)
for s in S:
    Tl=list(txt)
    Tl.remove(s)
    D[s]=''.join(Tl) # операция слияния списка в текст '' - без разделителя 
print(D)
