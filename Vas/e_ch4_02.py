# определяются цифры, которые есть в представлении обоих чисел. 
N1 = 3457322
N2 = 5938577
def digits_n(number):
    digits = set()
    while number != 0:
        digits.add(number%10)
        number//=10        
    return digits
Nm1 = digits_n(N1)
Nm2 = digits_n(N2)
NN = Nm1 | Nm2
print(NN)
