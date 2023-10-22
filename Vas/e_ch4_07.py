S="Мой дядя самых честных правил, когда не в шутку занемог, он уважать себя заставил, и лучше выдумать не мог!"
Sl = list(S)
Sm = set(S.lower()) 
# Sm1 = set(S) 
# print(Sm)
# print(len(Sm),  len(S))
def count_ch(S, s):  
    # counting the number of occurrences of a character s in the list  S 
    count=0
    for i in range(len(S)):
        if s==S[i]: count+=1
    return count            
# V =[]
# D = dict()
D = {s:count_ch(Sl,s) for s in Sm}
Ds = dict(sorted(D.items(), key=lambda item: item[1], reverse=True))  # сортировка по убывающим значениям
# print(D)
print(Ds)


