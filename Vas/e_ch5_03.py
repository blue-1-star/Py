txt = "А роза упала на лапу Азора! ё ма Ё ВынЬ да полож Ъ __ ::"
txt_eng = "It’s very handy to know that the ASCII code for 0 is 48 and that the digits codes are in order."
delta=ord("а")-ord("А")
# print(delta)
# print(ord('а'), ord('А'), ord('я'), ord('Я') )
# print("ь -", ord('ь'), "ъ -",ord('ъ'))
# dr = ord('а') - ord('А')
# print("dr =",dr)

# for c in range(1040,1107):
    # print(chr(c),'-', c, end=' ')
# print()    
# print("Ё -",ord('Ё'),"ё -",ord('ё'))
# -------------
def show_chars(A,B):
    for c in range(A,B+1):
        print(chr(c),'-', c, end=' ')    
    if A > 1000: 
        print("Ё -",ord('Ё'),"ё -",ord('ё'))


def between(A,Z,x):
    res = False
    if x >= A and x <= Z:
        res = True 
    return res
# print(between(2,15,18))
# show_chars(1040,1071)  # russian code
# show_chars(65,122)     # english code
def swapcase_m(txt):
    new_str =""
    for c in txt:
        if between(1040, 1071, ord(c)) or between(65,90,ord(c)):
            dlt = delta
        elif between(1072,1103,ord(c)) or between(97,122,ord(c)):
            dlt = -delta
        elif ord(c) == 1025: 
            dlt = 80 
        elif ord(c) == 1105: 
            dlt = -80         
        else:
            dlt = 0
        # dlt = m*delta
        ch = chr(ord(c)+dlt)
        new_str += ch
    return new_str
print(txt)    
print(swapcase_m(txt))
print(txt_eng)
print(swapcase_m(txt_eng))

