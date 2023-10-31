"""  ch 6 p 303
создается функция с двумя аргументами, являющимися числовыми списками. Результатом является число,
равное сумме попарных произведений элементов списков. Если в одном
из списков элементов меньше, чем в другом, то недостающие элементы
получают путем циклического повторения содержимого списка.
"""
# lambda X,Y : 
def f(X:"список",Y:"список"):
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

g = lambda X, Y: sum(x * y for x, y in zip(X + X[:abs(len(X) - len(Y))], Y + Y[:abs(len(Y) - len(X))]))
# g = lambda X, Y: sum(x * y for x, y in zip(X + [X[i] for i in range(abs(len(X) - len(Y)))], Y))
#  GPT  отжигает - лает третий вариант - но при этом все три рабоатают? 
# f = lambda X, Y: sum(x * y for x, y in zip(X + [X[i] for i in range(abs(len(X) - len(Y)))]  if len(X) < len(Y)
#                            else X, Y + [Y[i] for i in range(abs(len(Y) - len(X)))] if len(Y) < len(X) else Y))



X=[1,2,3]
Y=[2,4,6,1,0,2]
print("f=",f(X,Y))
print(f.__doc__,"\n",f.__annotations__)
print("--- Lambda")
print("X =", X)
print("Y = ", Y)
print(g(X,Y))

