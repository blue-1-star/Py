
msg1 = input("Enter text:")

if msg1.islower():
    print("Lowercase")
else:
    print("This is not in lowercase")

for letter in msg1:
    print(letter,end="*")
    