file = open("Numbers.txt", "w")
file.write("1,3,5,7,9,11")
file.close()
file = open("Numbers.txt", "r")
print(file.read())

