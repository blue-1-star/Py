from fractions import Fraction
from decimal import Decimal
import os
A=Fraction(2,5)
print("A =", A)
B=Fraction(3,7)
print("B =", B)
C=A+B
print("A+B =", C)
X=2/5
print("X =", X)
D=X+B
print("X+B =", D)
A=Decimal('1.01')
print("A =", A)
B=Decimal('2.02')
print("B =", B)
C=A+B
print("A+B =", C)
print("1.01+2.02 =",1.01+2.02)
# --------------
# mf = open("g:\Programming\Py\Vas\fd.txt")
# mf = open("g:/Programming/Py/Vas/fd.txt",encoding="utf-8" )
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "fd.txt")
with  open(file_path,encoding="utf-8" ) as mf:
# mf = open("g:/Programming/Py/Vas/test.txt", encoding="utf-8" )
    txt = mf.read()
print(txt)
mf.close()


