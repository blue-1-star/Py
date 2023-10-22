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
