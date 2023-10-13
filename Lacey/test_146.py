from errno import EMSGSIZE


alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
"k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
"u", "v", "w", "x", "y", "z", " "]
#print(alphabet[3])
lna = len(alphabet)
def inpmes():
    msg = input("Enter message: ").lower()
    #msg = msg.lower
    # value in range 0: lna-1
    shift = (int(input("Enter digit:")))%lna
    return([msg,shift]) 
def encrypt():
    msg = inpmes()

    #sh = inpmes()[1]
    print(msg)
    #print("find letter  - ", msg[0],"its number = ",  alphabet.index(msg[0]))
    ems = ""
    for l in msg[0]:
        # alphabetical rotation - nsh - new index for encrypt symbol
        nsh = (alphabet.index(l) + msg[1]) % lna 
        # character by character form the encrypted string
        ems += alphabet[nsh]
    return ems



def decrypt():
    msg = inpmes()
    dms =""
    for l in msg[0]:
        # alphabetical rotation - osh - old (decrypt) index for  symbol       

        osh = (alphabet.index(l) - msg[1]) 
        if osh < 0:
            osh += lna 
        # character by character form the encrypted string
        dms += alphabet[osh]
    return dms
    
again = "y"
while again == "y":
    print()
    print("1) Make a code")
    print("2) Decode message")
    print("3) Quit")
    selection = int(input("Enter your selectuion:"))
    if selection == 1:
        print(encrypt())
    elif selection == 2:
        print(decrypt())
    elif selection == 3:
        again = "n"
    else:
         print("Incorrect selection entered")
      
    