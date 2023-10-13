wrd = input("Enter word:")
ln = len(wrd)
if wrd[0] == "a" or wrd[0] == "e" or wrd[0] == "i":
    nw = wrd +"way"
    #wrd[ln+1] = a
    #wrd[ln+2] = y
#elif wrd[0] == "e":
#    nw = wrd +"way" 
#elif wrd[0] == "i":
#     nw = wrd[1:ln]+ wrd[0]+ "ay"
else:
     nw = wrd[1:ln]+ wrd[0]+ "ay" 
     #print("Ok")
print(nw)
      


