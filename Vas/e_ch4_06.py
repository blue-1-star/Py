N = 5
A = [i for i in range(N)]
B=A[-1::-1]
# dic={A[s]: B[s] for s in B}
dic={B[s]: A[s] for s in B}
print(dic)
