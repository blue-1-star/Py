#  Generalisation of encryption problems with alphabet shifting
#  notes and preparatory material
#  1040 - 1103 - regular Russian sequential alphabet  (1040-1071 Capital, 1072 - 1103 small)
#  Ё - 1025 ё - 1105
#  Є - 1028 є - 1108  (укр)
#  І - 1030 і - 1110   
#  Ї - 1031 ї - 1111   
#  delta = 32  for russian  
#  65 - 90  - English alphabet (Capital) 97 - 122  - small   ( delta = 32 but 6 symbols (91-96) not alphabet )

# identifiers
#  
txt = " самый надежный шифр на белом свете с черной магией"
first_ch_code = 1040
second_ch_code = 1041
last_ch_code = 1071   # code last russian  char  
penultimate_ch_code = 1070
def encr_m2(txt):
    tx="" 
    for c in txt:
        ch=chr(ord(c)-2)
        if ord(c) == second_ch_code:
            ch=chr(last_ch_code)
        elif ord(c) == first_ch_code:
            ch=chr(penultimate_ch_code)
        tx+=ch
    return tx
def dcr_m2(txt):
    tx="" 
    for c in txt:
        ch=chr(ord(c)+2)
        if ord(c) == last_ch_code:
            ch=chr(second_ch_code)
        elif ord(c) == penultimate_ch_code:
            ch=chr(first_ch_code)
        tx+=ch
    return tx
etxt = encr_m2(txt)
print(etxt.lower())
detxt = dcr_m2(etxt)
print(detxt.lower())
