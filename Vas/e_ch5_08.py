# каждая буква заменяется на следующую (а последняя — на первую), но только эта операция
# отдельно выполняется для гласных букв и для согласных
# 1) решение в области Прописных букв
txt = "А роза упала на лапу Азора"

Rb = 1040     #  Beginning of the Russian uppercase area in the encoding UTF-8
Re = 1071     #   End of Russian uppercase area in encoding There are 32 letters in total
vowels_r = {"А", "Е", "Ё", "И", "О", "У", "Ы", "Э", "Ю", "Я"}
Alpha = list(chr(i) for i in range(Rb,Re+1))  # Capital russian
# subtask  - function to create list consonants letters
# consonants as a subtraction from all letters  vowels 
def consonants(vowels_r,Rb,Re):
    all = set(chr(i) for i in range(Rb,Re+1))
    cons = all - vowels_r
    return cons
def enc_on_base(A,shift,ch):
    # we obtain the set A and the shift for the cipher, the symbol ...   output shifted by shifter character
    
    ch=chr(ord(ch)+shift)
    return ch

# sorted_set = sorted(cons_l, key=lambda x: x.upper())
# print(cons_l)
# print(sorted_set)
def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else: 
        return 0
it=list()
def mir(N,shift):
    for i in range(N,-1,-1):
        it.append(2*N-(N-sign(shift)*(N-i) ))
    return(it)        
N=5
shift=1
it=mir(N,shift)    
# print(it)
ch=1
# A = [range(-2*N-1,3*N+1)]
A = [range(N)]

# Auxiliary program for debugging purposes in shifting characters on the shifter
def numb_pos(N):     
    bl=list()
    for i in range(-6,N +1):           
        b = i%N
        if i < 0:
            b= N+i
        if i==N:
            b=0        
        bl.append((i,b))    
    return bl
            
# print(i,"% :",b)
def norm_code_sym(Rb,s):   # character code reduced to the range 0-32
    return ord(s) - Rb 
def denorm_code_sym(Rb,s):   # character code back to the range 1040 -....
    return s + Rb 

def shift_n(S,sm,shift):
    #  S -  alphabet, sm -  incoming character, shift - specified shift
    # The function returns shifted by shift positions of the incoming symbol sm in the definition area S  
    sm_o= norm_code_sym(Rb,sm)                #  normalized code sm to interval 0-31)

    # taking modulo cuts off the exit beyond the boundary of the nomalised interval 
    # shift %=N      # to further consider shifting arbitrarily
    b = (sm_o + shift) % len(S)   
    if shift < 0:
        b=len(S)+shift
    if shift==N:
        b=0
    sym = chr(denorm_code_sym(Rb,b))
    return sym
# bl=numb_pos(A)
# print(bl)
# shift = -31
# print(norm_code_sym(Rb,Re,"А"))
# print(norm_code_sym(Rb,Re,"Я"))
# print( shift_n(Alpha,"А",shift ) )
# bl1 = numb_pos(N)
# print(numb_pos(A))
# print(bl1)
shift = 1
txu = txt.upper() 
cons_l = consonants(vowels_r,Rb, Re) 
def encrypt_mg(txu, cons_l,vowels_r):
    txe = str()
    tx=""
    for c in txu:
        if c in cons_l:
            A = cons_l
            tx+=shift_n(A,c,shift)
        elif c in vowels_r:
            A = vowels_r
            tx+=shift_n(A,c,shift)
        else: 
            tx+=c
    return tx

txe=encrypt_mg(txu,cons_l,vowels_r)
print(txe, " ", len(txe)," ",len(txt))
st=""
print(txu)

for c in txu:
    st+=str(ord(c))+" "
# print(st)
st1=""
# for c in tx:
    # st1+=str(ord(c))+" "
# print(st1)








