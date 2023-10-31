"""  ch 6 p 303
создается функция с двумя аргументами, являющимися числовыми списками. Результатом является число,
равное сумме попарных произведений элементов списков. Если в одном
из списков элементов меньше, чем в другом, то недостающие элементы
получают путем циклического повторения содержимого списка.
"""
#lambda X,Y : 
def f(X:"список",Y:"список"):
# def f(X,Y):
    " создается функция с двумя аргументами"
    s=0
    m = len(X) - len(Y)
    mx = max(len(X),len(Y))
    if len(X) - len(Y) < 0:
        # X[len(X)+i]= X[i] for i in range(abs(m))
        for i in range(abs(m)):
            # X[len(X)+i]= X[i] 
            X.append(X[i])
    elif len(Y) < len(X):
        for i in range(abs(m)):
            # Y[len(Y)+i]= Y[i] 
            Y.append(Y[i])
    for i in range(mx):
        s += X[i]*Y[i] 
    return s    
        
X=[1,2,3]
Y=[2,4,6,1]
print("f=",f(X,Y))
print(f.__doc__,"\n",f.__annotations__)

