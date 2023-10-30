A="\"Java\"\n\"Python\""
B=r"\"Java\"\n\"Python\""
print(A)
print(B)
name="Python"
C=f"Language {name} простой и понятный!"
print(C)
C=f"Language {name}!r простой и понятный!"
print(C)
num=12.34567
txt=f"Число: {num:9.3f}"
print(txt)
txt=f"Число: {num:09.3f}"
print(txt)
num=42
txt=f"Число: {num:*>9d}"
print(txt)
txt=f"Число: {num:#09x}"
print(txt)
txt=f"Число: {num:#9x}"
print(txt)
txt=f"Число: {num:*<9x}"
print(txt)
# p 223
txt="number {0} it's {0: b} or {0: x}".format(42)
print(txt)
txt="code: {0:05d}, symbol {0:*^5c}".format(65)
print(txt)
txt="number: {:_>+20.3E}".format(123.468)
print(txt)
B="{0:_{2}{1}s}"
num=6
# Explanation on page 225 
for k in range(1, num+1):
    print(B.format("*", k,">"), end="")
    print(" "*(2*(num-k)), end="")
    print(B.format("*", k,"<"))
    
